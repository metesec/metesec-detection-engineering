"""Fail-closed Sentinel rule execution and alert-outcome assessment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re


_DETECTION_ID = re.compile(r"^MSEC-DET-[0-9]{4}$")
_DURATION = re.compile(
    r"^P(?:(?P<days>[0-9]+)D)?(?:T(?=[0-9])(?:(?P<hours>[0-9]+)H)?"
    r"(?:(?P<minutes>[0-9]+)M)?(?:(?P<seconds>[0-9]+)S)?)?$"
)
_TIMESTAMP = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:"
    r"[0-9]{2}(?:\.[0-9]+)?Z$"
)
_EXECUTION_STATUSES = {"succeeded", "failed", "unknown"}
_HEALTH_STATUSES = {"healthy", "degraded", "failed", "unknown"}


class SentinelRuntimeHealthError(ValueError):
    """Raised when the runtime-health contract or observation fails closed."""


@dataclass(frozen=True)
class RuntimePolicy:
    expected_enabled: bool
    degraded_after_missed_runs: int
    failed_after_missed_runs: int


@dataclass(frozen=True)
class RuleExpectation:
    detection_id: str
    query_frequency: str
    frequency: timedelta


@dataclass(frozen=True)
class AlertOutcome:
    window_start: datetime
    window_end: datetime
    alerts_created: int
    incidents_created: int

    def to_dict(self) -> dict[str, object]:
        return {
            "window_start": _format_timestamp(self.window_start),
            "window_end": _format_timestamp(self.window_end),
            "alerts_created": self.alerts_created,
            "incidents_created": self.incidents_created,
        }


@dataclass(frozen=True)
class RuleObservation:
    detection_id: str
    rule_exists: bool
    enabled: bool | None
    last_execution_at: datetime | None
    last_execution_status: str
    alert_outcome: AlertOutcome | None


@dataclass(frozen=True)
class RuntimeAssessment:
    detection_id: str
    expected_frequency: str
    status: str
    age_seconds: int | None
    reasons: tuple[str, ...]
    alert_outcome: AlertOutcome | None

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.detection_id,
            "expected_frequency": self.expected_frequency,
            "status": self.status,
            "age_seconds": self.age_seconds,
            "reasons": list(self.reasons),
            "alert_outcome": (
                None if self.alert_outcome is None else self.alert_outcome.to_dict()
            ),
        }


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SentinelRuntimeHealthError(f"{label}: unable to read JSON: {error}") from error
    if not isinstance(value, dict):
        raise SentinelRuntimeHealthError(f"{label}: expected a JSON object")
    return value


def _exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise SentinelRuntimeHealthError(f"{label} must contain exactly {sorted(keys)}")
    return value


def _positive_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise SentinelRuntimeHealthError(f"{label} must be a positive integer")
    return value


def _duration(value: object, label: str) -> timedelta:
    if not isinstance(value, str):
        raise SentinelRuntimeHealthError(f"{label} must be an ISO 8601 duration")
    match = _DURATION.fullmatch(value)
    if match is None or not any(match.groupdict().values()):
        raise SentinelRuntimeHealthError(f"{label} must be a bounded ISO 8601 duration")
    duration = timedelta(
        days=int(match.group("days") or 0),
        hours=int(match.group("hours") or 0),
        minutes=int(match.group("minutes") or 0),
        seconds=int(match.group("seconds") or 0),
    )
    if duration <= timedelta(0):
        raise SentinelRuntimeHealthError(f"{label} must be greater than zero")
    return duration


def _timestamp(value: object, label: str) -> datetime:
    if not isinstance(value, str) or _TIMESTAMP.fullmatch(value) is None:
        raise SentinelRuntimeHealthError(f"{label} must be a UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise SentinelRuntimeHealthError(f"{label} is not a valid timestamp") from error
    return parsed.astimezone(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _resolve_inside(repo_root: Path, raw_path: object, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise SentinelRuntimeHealthError(f"{label} must be a non-empty path")
    root = repo_root.resolve()
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise SentinelRuntimeHealthError(f"{label} escapes the repository") from error
    if not candidate.is_file():
        raise SentinelRuntimeHealthError(f"{label} does not exist")
    return candidate


def load_expectations(
    repo_root: Path, policy_path: Path
) -> tuple[RuntimePolicy, tuple[RuleExpectation, ...]]:
    raw = _exact_keys(
        _load_json(policy_path, policy_path.as_posix()),
        {
            "schema_version",
            "target",
            "source_profile",
            "expected_enabled",
            "degraded_after_missed_runs",
            "failed_after_missed_runs",
        },
        policy_path.as_posix(),
    )
    if raw["schema_version"] != 1 or raw["target"] != "microsoft-sentinel":
        raise SentinelRuntimeHealthError("Sentinel runtime-health policy header is invalid")
    if raw["expected_enabled"] is not True:
        raise SentinelRuntimeHealthError("Sentinel runtime-health expected_enabled must be true")
    degraded_runs = _positive_int(
        raw["degraded_after_missed_runs"], "degraded_after_missed_runs"
    )
    failed_runs = _positive_int(
        raw["failed_after_missed_runs"], "failed_after_missed_runs"
    )
    if degraded_runs >= failed_runs:
        raise SentinelRuntimeHealthError(
            "degraded_after_missed_runs must be less than failed_after_missed_runs"
        )

    profile_path = _resolve_inside(repo_root, raw["source_profile"], "source_profile")
    profile = _load_json(profile_path, profile_path.as_posix())
    rules = profile.get("rules")
    if (
        profile.get("schema_version") != 1
        or profile.get("target") != "microsoft-sentinel"
        or not isinstance(rules, list)
        or not rules
    ):
        raise SentinelRuntimeHealthError("Sentinel analytics-rule source profile is invalid")

    expectations: list[RuleExpectation] = []
    seen: set[str] = set()
    for index, rule in enumerate(rules):
        label = f"analytics-rule profile rules[{index}]"
        if not isinstance(rule, dict):
            raise SentinelRuntimeHealthError(f"{label} must be an object")
        detection_id = rule.get("id")
        if (
            not isinstance(detection_id, str)
            or _DETECTION_ID.fullmatch(detection_id) is None
            or detection_id in seen
        ):
            raise SentinelRuntimeHealthError(f"{label}.id is invalid or duplicated")
        seen.add(detection_id)
        query_frequency = rule.get("query_frequency")
        frequency = _duration(query_frequency, f"{label}.query_frequency")
        expectations.append(
            RuleExpectation(
                detection_id=detection_id,
                query_frequency=str(query_frequency),
                frequency=frequency,
            )
        )
    return (
        RuntimePolicy(
            expected_enabled=True,
            degraded_after_missed_runs=degraded_runs,
            failed_after_missed_runs=failed_runs,
        ),
        tuple(expectations),
    )


def _outcome(value: object, observed_at: datetime, label: str) -> AlertOutcome | None:
    if value is None:
        return None
    raw = _exact_keys(
        value,
        {"window_start", "window_end", "alerts_created", "incidents_created"},
        label,
    )
    window_start = _timestamp(raw["window_start"], f"{label}.window_start")
    window_end = _timestamp(raw["window_end"], f"{label}.window_end")
    if window_start > window_end:
        raise SentinelRuntimeHealthError(f"{label}: window_start is after window_end")
    if window_end > observed_at:
        raise SentinelRuntimeHealthError(f"{label}: window_end is after observed_at")
    counts: dict[str, int] = {}
    for key in ("alerts_created", "incidents_created"):
        item = raw[key]
        if isinstance(item, bool) or not isinstance(item, int) or item < 0:
            raise SentinelRuntimeHealthError(f"{label}.{key} must be a non-negative integer")
        counts[key] = item
    return AlertOutcome(
        window_start=window_start,
        window_end=window_end,
        alerts_created=counts["alerts_created"],
        incidents_created=counts["incidents_created"],
    )


def load_observation(path: Path) -> tuple[datetime, tuple[RuleObservation, ...]]:
    raw = _exact_keys(
        _load_json(path, path.as_posix()),
        {"schema_version", "target", "observed_at", "rules"},
        path.as_posix(),
    )
    if raw["schema_version"] != 1 or raw["target"] != "microsoft-sentinel":
        raise SentinelRuntimeHealthError("Sentinel runtime observation header is invalid")
    observed_at = _timestamp(raw["observed_at"], "observation observed_at")
    raw_rules = raw["rules"]
    if not isinstance(raw_rules, list):
        raise SentinelRuntimeHealthError("observation rules must be an array")

    observations: list[RuleObservation] = []
    seen: set[str] = set()
    rule_keys = {
        "id",
        "rule_exists",
        "enabled",
        "last_execution_at",
        "last_execution_status",
        "alert_outcome",
    }
    for index, item in enumerate(raw_rules):
        label = f"observation rules[{index}]"
        rule = _exact_keys(item, rule_keys, label)
        detection_id = rule["id"]
        if (
            not isinstance(detection_id, str)
            or _DETECTION_ID.fullmatch(detection_id) is None
            or detection_id in seen
        ):
            raise SentinelRuntimeHealthError(f"{label}.id is invalid or duplicated")
        seen.add(detection_id)
        rule_exists = rule["rule_exists"]
        if not isinstance(rule_exists, bool):
            raise SentinelRuntimeHealthError(f"{label}.rule_exists must be boolean")
        enabled = rule["enabled"]
        if enabled is not None and not isinstance(enabled, bool):
            raise SentinelRuntimeHealthError(f"{label}.enabled must be boolean or null")
        latest_raw = rule["last_execution_at"]
        latest = (
            None
            if latest_raw is None
            else _timestamp(latest_raw, f"{label}.last_execution_at")
        )
        execution_status = rule["last_execution_status"]
        if execution_status not in _EXECUTION_STATUSES:
            raise SentinelRuntimeHealthError(f"{label}.last_execution_status is invalid")
        alert_outcome = _outcome(rule["alert_outcome"], observed_at, f"{label}.alert_outcome")

        if not rule_exists and (
            enabled is not None
            or latest is not None
            or execution_status != "unknown"
            or alert_outcome is not None
        ):
            raise SentinelRuntimeHealthError(
                f"{label}: absent rule cannot have runtime or outcome values"
            )
        if rule_exists and enabled is None:
            raise SentinelRuntimeHealthError(f"{label}: existing rule requires enabled state")
        if latest is not None and latest > observed_at:
            raise SentinelRuntimeHealthError(f"{label}.last_execution_at is in the future")
        if latest is None and execution_status != "unknown":
            raise SentinelRuntimeHealthError(
                f"{label}: execution status requires last_execution_at"
            )

        observations.append(
            RuleObservation(
                detection_id=detection_id,
                rule_exists=rule_exists,
                enabled=enabled,
                last_execution_at=latest,
                last_execution_status=str(execution_status),
                alert_outcome=alert_outcome,
            )
        )
    return observed_at, tuple(observations)


def assess_runtime_health(
    policy: RuntimePolicy,
    expectations: tuple[RuleExpectation, ...],
    observed_at: datetime,
    observations: tuple[RuleObservation, ...],
) -> tuple[RuntimeAssessment, ...]:
    expected_ids = {item.detection_id for item in expectations}
    unexpected = sorted({item.detection_id for item in observations}.difference(expected_ids))
    if unexpected:
        raise SentinelRuntimeHealthError(f"observation contains unknown rules: {unexpected}")
    observed = {item.detection_id: item for item in observations}
    assessments: list[RuntimeAssessment] = []

    for expectation in expectations:
        observation = observed.get(expectation.detection_id)
        if observation is None:
            assessments.append(
                RuntimeAssessment(
                    detection_id=expectation.detection_id,
                    expected_frequency=expectation.query_frequency,
                    status="unknown",
                    age_seconds=None,
                    reasons=("observation_missing",),
                    alert_outcome=None,
                )
            )
            continue

        status = "healthy"
        reasons: list[str] = []
        age_seconds: int | None = None
        if not observation.rule_exists:
            status = "failed"
            reasons.append("rule_missing")
        else:
            if policy.expected_enabled and observation.enabled is False:
                status = "degraded"
                reasons.append("rule_disabled")
            if observation.last_execution_at is None:
                if status == "healthy":
                    status = "unknown"
                reasons.append("execution_missing")
            else:
                age = observed_at - observation.last_execution_at
                age_seconds = int(age.total_seconds())
                failed_after = expectation.frequency * policy.failed_after_missed_runs
                degraded_after = expectation.frequency * policy.degraded_after_missed_runs
                if age > failed_after:
                    status = "failed"
                    reasons.append("execution_stale")
                elif age > degraded_after and status != "failed":
                    status = "degraded"
                    reasons.append("execution_late")

            if observation.last_execution_status == "failed":
                status = "failed"
                reasons.append("execution_failed")
            elif observation.last_execution_status == "unknown":
                if status == "healthy":
                    status = "unknown"
                reasons.append("execution_status_unknown")

        if status == "healthy":
            reasons.append("execution_healthy")
        if status not in _HEALTH_STATUSES:
            raise AssertionError(f"unsupported runtime status {status}")
        assessments.append(
            RuntimeAssessment(
                detection_id=expectation.detection_id,
                expected_frequency=expectation.query_frequency,
                status=status,
                age_seconds=age_seconds,
                reasons=tuple(reasons),
                alert_outcome=observation.alert_outcome,
            )
        )
    return tuple(assessments)


def assessment_document(
    observed_at: datetime, assessments: tuple[RuntimeAssessment, ...]
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "target": "microsoft-sentinel",
        "observed_at": _format_timestamp(observed_at),
        "summary": {
            "rules": len(assessments),
            **{
                status: sum(item.status == status for item in assessments)
                for status in ("healthy", "degraded", "failed", "unknown")
            },
        },
        "rules": [item.to_dict() for item in assessments],
    }


__all__ = [
    "AlertOutcome",
    "RuleExpectation",
    "RuleObservation",
    "RuntimeAssessment",
    "RuntimePolicy",
    "SentinelRuntimeHealthError",
    "assess_runtime_health",
    "assessment_document",
    "load_expectations",
    "load_observation",
]
