"""Fail-closed evaluation of environment-local Sentinel data-source observations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SOURCE_ID = re.compile(r"^MSEC-SDS-[0-9]{4}$")
_DETECTION_ID = re.compile(r"^MSEC-DET-[0-9]{4}$")
_DURATION = re.compile(
    r"^P(?:(?P<days>[0-9]+)D)?(?:T(?=[0-9])(?:(?P<hours>[0-9]+)H)?"
    r"(?:(?P<minutes>[0-9]+)M)?(?:(?P<seconds>[0-9]+)S)?)?$"
)
_TIMESTAMP = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:"
    r"[0-9]{2}(?:\.[0-9]+)?Z$"
)
_COLUMN_TYPES = {
    "bool",
    "datetime",
    "dynamic",
    "guid",
    "int",
    "long",
    "real",
    "string",
    "timespan",
}
_STATUSES = {"ready", "degraded", "unavailable", "unknown"}


class SentinelDataSourceError(ValueError):
    """Raised when a data-source contract or observation fails closed."""


@dataclass(frozen=True)
class RequiredColumn:
    name: str
    data_type: str


@dataclass(frozen=True)
class DataSourceContract:
    source_id: str
    table: str
    display_name: str
    consumers: tuple[str, ...]
    event_time_column: str
    required_columns: tuple[RequiredColumn, ...]
    degraded_after: timedelta
    unavailable_after: timedelta


@dataclass(frozen=True)
class SourceObservation:
    source_id: str
    table: str
    table_exists: bool
    latest_event_at: datetime | None
    columns: tuple[RequiredColumn, ...]


@dataclass(frozen=True)
class DataSourceAssessment:
    source_id: str
    table: str
    status: str
    age_seconds: int | None
    missing_columns: tuple[str, ...]
    type_mismatches: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "table": self.table,
            "status": self.status,
            "age_seconds": self.age_seconds,
            "missing_columns": list(self.missing_columns),
            "type_mismatches": list(self.type_mismatches),
            "reasons": list(self.reasons),
        }


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SentinelDataSourceError(f"{label}: unable to read JSON: {error}") from error
    if not isinstance(value, dict):
        raise SentinelDataSourceError(f"{label}: expected a JSON object")
    return value


def _exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise SentinelDataSourceError(f"{label} must contain exactly {sorted(keys)}")
    return value


def _identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise SentinelDataSourceError(f"{label} is not a safe identifier")
    return value


def _duration(value: object, label: str) -> timedelta:
    if not isinstance(value, str):
        raise SentinelDataSourceError(f"{label} must be an ISO 8601 duration")
    match = _DURATION.fullmatch(value)
    if match is None or not any(match.groupdict().values()):
        raise SentinelDataSourceError(f"{label} must be a bounded ISO 8601 duration")
    duration = timedelta(
        days=int(match.group("days") or 0),
        hours=int(match.group("hours") or 0),
        minutes=int(match.group("minutes") or 0),
        seconds=int(match.group("seconds") or 0),
    )
    if duration <= timedelta(0):
        raise SentinelDataSourceError(f"{label} must be greater than zero")
    return duration


def _timestamp(value: object, label: str) -> datetime:
    if not isinstance(value, str) or _TIMESTAMP.fullmatch(value) is None:
        raise SentinelDataSourceError(f"{label} must be a UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise SentinelDataSourceError(f"{label} is not a valid timestamp") from error
    return parsed.astimezone(timezone.utc)


def _columns(raw: object, label: str) -> tuple[RequiredColumn, ...]:
    if not isinstance(raw, list):
        raise SentinelDataSourceError(f"{label} must be an array")
    columns: list[RequiredColumn] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        item_label = f"{label}[{index}]"
        value = _exact_keys(item, {"name", "type"}, item_label)
        name = _identifier(value["name"], f"{item_label}.name")
        data_type = value["type"]
        if data_type not in _COLUMN_TYPES:
            raise SentinelDataSourceError(f"{item_label}.type is unsupported")
        if name in seen:
            raise SentinelDataSourceError(f"{item_label}.name is duplicated")
        seen.add(name)
        columns.append(RequiredColumn(name=name, data_type=str(data_type)))
    return tuple(columns)


def load_contract(contract_path: Path, preview_path: Path) -> tuple[DataSourceContract, ...]:
    raw = _exact_keys(
        _load_json(contract_path, contract_path.as_posix()),
        {"schema_version", "target", "sources"},
        contract_path.as_posix(),
    )
    if raw["schema_version"] != 1 or raw["target"] != "microsoft-sentinel":
        raise SentinelDataSourceError("data-source contract header is invalid")
    raw_sources = raw["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise SentinelDataSourceError("data-source contract sources must be non-empty")

    preview = _load_json(preview_path, preview_path.as_posix())
    preview_bindings = preview.get("detections")
    if preview.get("schema_version") != 2 or not isinstance(preview_bindings, list):
        raise SentinelDataSourceError("Sentinel preview profile version 2 is required")
    expected_by_table: dict[str, list[str]] = {}
    for index, binding in enumerate(preview_bindings):
        if not isinstance(binding, dict):
            raise SentinelDataSourceError(f"preview detections[{index}] must be an object")
        table = _identifier(binding.get("query_table"), f"preview detections[{index}].query_table")
        detection_id = binding.get("id")
        if not isinstance(detection_id, str) or _DETECTION_ID.fullmatch(detection_id) is None:
            raise SentinelDataSourceError(f"preview detections[{index}].id is invalid")
        expected_by_table.setdefault(table, []).append(detection_id)

    contracts: list[DataSourceContract] = []
    seen_ids: set[str] = set()
    seen_tables: set[str] = set()
    source_keys = {
        "id",
        "table",
        "display_name",
        "consumers",
        "event_time_column",
        "required_columns",
        "freshness",
    }
    for index, item in enumerate(raw_sources):
        label = f"data-source contract sources[{index}]"
        source = _exact_keys(item, source_keys, label)
        source_id = source["id"]
        if not isinstance(source_id, str) or _SOURCE_ID.fullmatch(source_id) is None:
            raise SentinelDataSourceError(f"{label}.id is invalid")
        table = _identifier(source["table"], f"{label}.table")
        display_name = source["display_name"]
        if not isinstance(display_name, str) or not display_name.strip():
            raise SentinelDataSourceError(f"{label}.display_name must be non-empty")
        consumers = source["consumers"]
        if (
            not isinstance(consumers, list)
            or not consumers
            or any(
                not isinstance(item, str) or _DETECTION_ID.fullmatch(item) is None
                for item in consumers
            )
            or len(consumers) != len(set(consumers))
        ):
            raise SentinelDataSourceError(f"{label}.consumers is invalid")
        if source_id in seen_ids or table in seen_tables:
            raise SentinelDataSourceError(f"{label} duplicates an ID or table")
        seen_ids.add(source_id)
        seen_tables.add(table)

        required_columns = _columns(source["required_columns"], f"{label}.required_columns")
        if not required_columns:
            raise SentinelDataSourceError(f"{label}.required_columns must be non-empty")
        event_time_column = _identifier(
            source["event_time_column"], f"{label}.event_time_column"
        )
        required_types = {column.name: column.data_type for column in required_columns}
        if required_types.get(event_time_column) != "datetime":
            raise SentinelDataSourceError(
                f"{label}.event_time_column must be a required datetime column"
            )

        freshness = _exact_keys(
            source["freshness"],
            {"degraded_after", "unavailable_after"},
            f"{label}.freshness",
        )
        degraded_after = _duration(
            freshness["degraded_after"], f"{label}.freshness.degraded_after"
        )
        unavailable_after = _duration(
            freshness["unavailable_after"], f"{label}.freshness.unavailable_after"
        )
        if degraded_after >= unavailable_after:
            raise SentinelDataSourceError(
                f"{label}.freshness degraded_after must be less than unavailable_after"
            )
        if expected_by_table.get(table) != consumers:
            raise SentinelDataSourceError(
                f"{label}.consumers must exactly match the Sentinel preview bindings"
            )

        contracts.append(
            DataSourceContract(
                source_id=source_id,
                table=table,
                display_name=display_name,
                consumers=tuple(str(item) for item in consumers),
                event_time_column=event_time_column,
                required_columns=required_columns,
                degraded_after=degraded_after,
                unavailable_after=unavailable_after,
            )
        )

    missing_tables = set(expected_by_table).difference(seen_tables)
    if missing_tables:
        raise SentinelDataSourceError(
            f"Sentinel preview tables lack contracts: {sorted(missing_tables)}"
        )
    return tuple(contracts)


def load_observation(path: Path) -> tuple[datetime, tuple[SourceObservation, ...]]:
    raw = _exact_keys(
        _load_json(path, path.as_posix()),
        {"schema_version", "target", "observed_at", "sources"},
        path.as_posix(),
    )
    if raw["schema_version"] != 1 or raw["target"] != "microsoft-sentinel":
        raise SentinelDataSourceError("data-source observation header is invalid")
    observed_at = _timestamp(raw["observed_at"], "observation observed_at")
    raw_sources = raw["sources"]
    if not isinstance(raw_sources, list):
        raise SentinelDataSourceError("observation sources must be an array")

    observations: list[SourceObservation] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(raw_sources):
        label = f"observation sources[{index}]"
        source = _exact_keys(
            item,
            {"id", "table", "table_exists", "latest_event_at", "columns"},
            label,
        )
        source_id = source["id"]
        if not isinstance(source_id, str) or _SOURCE_ID.fullmatch(source_id) is None:
            raise SentinelDataSourceError(f"{label}.id is invalid")
        if source_id in seen_ids:
            raise SentinelDataSourceError(f"{label}.id is duplicated")
        seen_ids.add(source_id)
        table = _identifier(source["table"], f"{label}.table")
        table_exists = source["table_exists"]
        if not isinstance(table_exists, bool):
            raise SentinelDataSourceError(f"{label}.table_exists must be boolean")
        columns = _columns(source["columns"], f"{label}.columns")
        latest_raw = source["latest_event_at"]
        latest_event_at = (
            None
            if latest_raw is None
            else _timestamp(latest_raw, f"{label}.latest_event_at")
        )
        if not table_exists and (latest_event_at is not None or columns):
            raise SentinelDataSourceError(
                f"{label} cannot report columns or events when the table is absent"
            )
        if latest_event_at is not None and latest_event_at > observed_at:
            raise SentinelDataSourceError(f"{label}.latest_event_at is in the future")
        observations.append(
            SourceObservation(
                source_id=source_id,
                table=table,
                table_exists=table_exists,
                latest_event_at=latest_event_at,
                columns=columns,
            )
        )
    return observed_at, tuple(observations)


def assess_data_sources(
    contracts: tuple[DataSourceContract, ...],
    observed_at: datetime,
    observations: tuple[SourceObservation, ...],
) -> tuple[DataSourceAssessment, ...]:
    contract_ids = {contract.source_id for contract in contracts}
    unknown_ids = {item.source_id for item in observations}.difference(contract_ids)
    if unknown_ids:
        raise SentinelDataSourceError(f"observation contains unknown sources: {sorted(unknown_ids)}")
    observed = {item.source_id: item for item in observations}
    assessments: list[DataSourceAssessment] = []

    for contract in contracts:
        observation = observed.get(contract.source_id)
        if observation is None:
            assessments.append(
                DataSourceAssessment(
                    source_id=contract.source_id,
                    table=contract.table,
                    status="unknown",
                    age_seconds=None,
                    missing_columns=(),
                    type_mismatches=(),
                    reasons=("observation_missing",),
                )
            )
            continue
        if observation.table != contract.table:
            raise SentinelDataSourceError(
                f"{contract.source_id}: observed table does not match the contract"
            )

        required = {column.name: column.data_type for column in contract.required_columns}
        actual = {column.name: column.data_type for column in observation.columns}
        missing_columns = tuple(name for name in required if name not in actual)
        type_mismatches = tuple(
            f"{name}: expected {required[name]}, got {actual[name]}"
            for name in required
            if name in actual and required[name] != actual[name]
        )
        reasons: list[str] = []
        age_seconds: int | None = None

        if not observation.table_exists:
            status = "unavailable"
            reasons.append("table_missing")
        elif observation.latest_event_at is None:
            status = "unavailable"
            reasons.append("no_observed_events")
        else:
            age = observed_at - observation.latest_event_at
            age_seconds = int(age.total_seconds())
            if age > contract.unavailable_after:
                status = "unavailable"
                reasons.append("freshness_unavailable")
            elif age > contract.degraded_after:
                status = "degraded"
                reasons.append("freshness_degraded")
            else:
                status = "ready"

        if observation.table_exists and missing_columns:
            reasons.append("required_columns_missing")
            if status == "ready":
                status = "degraded"
        if observation.table_exists and type_mismatches:
            reasons.append("required_column_type_mismatch")
            if status == "ready":
                status = "degraded"
        if status == "ready":
            reasons.append("contract_satisfied")
        if status not in _STATUSES:
            raise AssertionError(f"unsupported assessment status: {status}")

        assessments.append(
            DataSourceAssessment(
                source_id=contract.source_id,
                table=contract.table,
                status=status,
                age_seconds=age_seconds,
                missing_columns=missing_columns,
                type_mismatches=type_mismatches,
                reasons=tuple(reasons),
            )
        )

    return tuple(assessments)


__all__ = [
    "DataSourceAssessment",
    "DataSourceContract",
    "SentinelDataSourceError",
    "SourceObservation",
    "assess_data_sources",
    "load_contract",
    "load_observation",
]
