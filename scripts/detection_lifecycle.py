"""Lifecycle and review-cadence evaluation for logical detections."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import json
from pathlib import Path
import re


_DETECTION_ID = re.compile(r"^MSEC-DET-[0-9]{4}$")
_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
_STATUSES = {"draft", "experimental", "stable", "deprecated"}
_REVIEW_STATES = {"current", "due", "overdue"}


class DetectionLifecycleError(ValueError):
    """Raised when lifecycle data or a transition fails closed."""


@dataclass(frozen=True)
class LifecycleRecord:
    detection_id: str
    title: str
    status: str
    created: date
    modified: date
    review_interval_days: int


@dataclass(frozen=True)
class LifecycleAssessment:
    detection_id: str
    title: str
    status: str
    modified: date
    review_interval_days: int
    review_due: date
    review_state: str
    days_until_due: int

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.detection_id,
            "title": self.title,
            "status": self.status,
            "modified": self.modified.isoformat(),
            "review_interval_days": self.review_interval_days,
            "review_due": self.review_due.isoformat(),
            "review_state": self.review_state,
            "days_until_due": self.days_until_due,
        }


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise DetectionLifecycleError(f"{label}: unable to read JSON: {error}") from error
    if not isinstance(value, dict):
        raise DetectionLifecycleError(f"{label}: expected a JSON object")
    return value


def _exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise DetectionLifecycleError(f"{label} must contain exactly {sorted(keys)}")
    return value


def parse_date(value: object, label: str) -> date:
    if not isinstance(value, str) or _DATE.fullmatch(value) is None:
        raise DetectionLifecycleError(f"{label} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise DetectionLifecycleError(f"{label} is not a valid date") from error


def load_policy(path: Path) -> dict[str, tuple[str, ...]]:
    raw = _exact_keys(
        _load_json(path, path.as_posix()),
        {"schema_version", "review_states", "transitions"},
        path.as_posix(),
    )
    if raw["schema_version"] != 1:
        raise DetectionLifecycleError("lifecycle policy schema_version must be 1")
    review_states = raw["review_states"]
    if review_states != ["current", "due", "overdue"]:
        raise DetectionLifecycleError("lifecycle policy review_states are invalid")
    raw_transitions = raw["transitions"]
    if not isinstance(raw_transitions, list):
        raise DetectionLifecycleError("lifecycle policy transitions must be an array")

    transitions: dict[str, tuple[str, ...]] = {}
    for index, item in enumerate(raw_transitions):
        label = f"lifecycle policy transitions[{index}]"
        entry = _exact_keys(item, {"from", "to"}, label)
        source = entry["from"]
        destinations = entry["to"]
        if source not in _STATUSES or source in transitions:
            raise DetectionLifecycleError(f"{label}.from is invalid or duplicated")
        if (
            not isinstance(destinations, list)
            or not destinations
            or len(destinations) != len(set(destinations))
            or any(destination not in _STATUSES for destination in destinations)
            or source not in destinations
        ):
            raise DetectionLifecycleError(f"{label}.to is invalid")
        transitions[str(source)] = tuple(str(item) for item in destinations)
    if set(transitions) != _STATUSES:
        raise DetectionLifecycleError("lifecycle policy must define every status exactly once")
    return transitions


def _record_from_values(
    detection_id: object,
    title: object,
    lifecycle: object,
    label: str,
) -> LifecycleRecord:
    if not isinstance(detection_id, str) or _DETECTION_ID.fullmatch(detection_id) is None:
        raise DetectionLifecycleError(f"{label}.id is invalid")
    if not isinstance(title, str) or not title.strip():
        raise DetectionLifecycleError(f"{label}.title must be non-empty")
    entry = _exact_keys(
        lifecycle,
        {"status", "created", "modified", "review_interval_days"},
        f"{label}.lifecycle",
    )
    status = entry["status"]
    if status not in _STATUSES:
        raise DetectionLifecycleError(f"{label}.lifecycle.status is invalid")
    created = parse_date(entry["created"], f"{label}.lifecycle.created")
    modified = parse_date(entry["modified"], f"{label}.lifecycle.modified")
    interval = entry["review_interval_days"]
    if isinstance(interval, bool) or not isinstance(interval, int) or not 30 <= interval <= 730:
        raise DetectionLifecycleError(
            f"{label}.lifecycle.review_interval_days must be between 30 and 730"
        )
    if created > modified:
        raise DetectionLifecycleError(f"{label}: created date is after modified date")
    return LifecycleRecord(
        detection_id=detection_id,
        title=title,
        status=str(status),
        created=created,
        modified=modified,
        review_interval_days=interval,
    )


def load_manifest_records(catalog_root: Path) -> tuple[LifecycleRecord, ...]:
    paths = sorted(catalog_root.glob("*/manifest.json"), key=lambda item: item.as_posix())
    if not paths:
        raise DetectionLifecycleError(f"{catalog_root.as_posix()}: no manifests found")
    records: list[LifecycleRecord] = []
    seen: set[str] = set()
    for path in paths:
        raw = _load_json(path, path.as_posix())
        record = _record_from_values(raw.get("id"), raw.get("title"), raw.get("lifecycle"), path.as_posix())
        if record.detection_id in seen:
            raise DetectionLifecycleError(f"duplicate detection ID {record.detection_id}")
        seen.add(record.detection_id)
        records.append(record)
    return tuple(records)


def load_baseline_catalogue(path: Path) -> tuple[LifecycleRecord, ...]:
    raw = _load_json(path, path.as_posix())
    detections = raw.get("detections")
    if raw.get("schema_version") != 1 or not isinstance(detections, list):
        raise DetectionLifecycleError("baseline must be a detection catalogue version 1")
    records: list[LifecycleRecord] = []
    seen: set[str] = set()
    for index, detection in enumerate(detections):
        if not isinstance(detection, dict):
            raise DetectionLifecycleError(f"baseline detections[{index}] must be an object")
        record = _record_from_values(
            detection.get("id"),
            detection.get("title"),
            detection.get("lifecycle"),
            f"baseline detections[{index}]",
        )
        if record.detection_id in seen:
            raise DetectionLifecycleError(f"baseline duplicates {record.detection_id}")
        seen.add(record.detection_id)
        records.append(record)
    return tuple(records)


def validate_transitions(
    current: tuple[LifecycleRecord, ...],
    previous: tuple[LifecycleRecord, ...],
    transitions: dict[str, tuple[str, ...]],
) -> None:
    current_by_id = {record.detection_id: record for record in current}
    previous_by_id = {record.detection_id: record for record in previous}
    removed = sorted(set(previous_by_id).difference(current_by_id))
    if removed:
        raise DetectionLifecycleError(
            f"baseline detections were removed instead of deprecated: {removed}"
        )

    for detection_id in sorted(set(current_by_id).intersection(previous_by_id)):
        latest = current_by_id[detection_id]
        baseline = previous_by_id[detection_id]
        if latest.created != baseline.created:
            raise DetectionLifecycleError(f"{detection_id}: created date is immutable")
        if latest.modified < baseline.modified:
            raise DetectionLifecycleError(f"{detection_id}: modified date moved backwards")
        if latest.status not in transitions.get(baseline.status, ()):
            raise DetectionLifecycleError(
                f"{detection_id}: transition {baseline.status} -> {latest.status} is not allowed"
            )
        lifecycle_changed = (
            latest.status != baseline.status
            or latest.review_interval_days != baseline.review_interval_days
        )
        if lifecycle_changed and latest.modified <= baseline.modified:
            raise DetectionLifecycleError(
                f"{detection_id}: lifecycle change requires a later modified date"
            )


def assess_lifecycle(
    records: tuple[LifecycleRecord, ...], as_of: date
) -> tuple[LifecycleAssessment, ...]:
    assessments: list[LifecycleAssessment] = []
    for record in records:
        if record.modified > as_of:
            raise DetectionLifecycleError(
                f"{record.detection_id}: modified date is after assessment date"
            )
        review_due = record.modified + timedelta(days=record.review_interval_days)
        days_until_due = (review_due - as_of).days
        if days_until_due > 0:
            review_state = "current"
        elif days_until_due == 0:
            review_state = "due"
        else:
            review_state = "overdue"
        if review_state not in _REVIEW_STATES:
            raise AssertionError(f"unsupported review state {review_state}")
        assessments.append(
            LifecycleAssessment(
                detection_id=record.detection_id,
                title=record.title,
                status=record.status,
                modified=record.modified,
                review_interval_days=record.review_interval_days,
                review_due=review_due,
                review_state=review_state,
                days_until_due=days_until_due,
            )
        )
    return tuple(assessments)


def assessment_document(
    assessments: tuple[LifecycleAssessment, ...], as_of: date, baseline_checked: bool
) -> dict[str, object]:
    counts = {
        state: sum(item.review_state == state for item in assessments)
        for state in ("current", "due", "overdue")
    }
    return {
        "schema_version": 1,
        "as_of": as_of.isoformat(),
        "baseline_checked": baseline_checked,
        "summary": {
            "detections": len(assessments),
            **counts,
            "next_review_due": min(item.review_due for item in assessments).isoformat(),
        },
        "detections": [item.to_dict() for item in assessments],
    }


__all__ = [
    "DetectionLifecycleError",
    "LifecycleAssessment",
    "LifecycleRecord",
    "assess_lifecycle",
    "assessment_document",
    "load_baseline_catalogue",
    "load_manifest_records",
    "load_policy",
    "parse_date",
    "validate_transitions",
]
