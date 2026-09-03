"""Deterministic Sigma-to-KQL compilation for the bounded Sentinel preview target."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import version
import json
from pathlib import Path
import re

from sigma.backends.kusto import KustoBackend
from sigma.pipelines.azuremonitor import azure_monitor_pipeline

try:
    from .sigma_validation import parse_sigma_collection
except ImportError:  # Support direct execution from the scripts directory.
    from sigma_validation import parse_sigma_collection


EXPECTED_KUSTO_BACKEND_VERSION = "1.0.1"
_TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class SentinelCompilationError(ValueError):
    """Raised when a target profile or compilation result fails closed."""


@dataclass(frozen=True)
class SentinelTarget:
    detection_id: str
    implementation: Path
    query_table: str
    golden: Path


@dataclass(frozen=True)
class CompiledSentinelQuery:
    detection_id: str
    query: str
    golden: Path


def _resolve_inside(repo_root: Path, raw_path: str, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise SentinelCompilationError(f"{label} must be a non-empty path")

    root = repo_root.resolve()
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise SentinelCompilationError(f"{label} escapes the repository") from error
    return candidate


def verify_backend_version() -> None:
    actual = version("pySigma-backend-kusto")
    if actual != EXPECTED_KUSTO_BACKEND_VERSION:
        raise SentinelCompilationError(
            "pySigma Kusto backend version mismatch: "
            f"expected {EXPECTED_KUSTO_BACKEND_VERSION}, got {actual}"
        )


def load_target_profile(repo_root: Path, profile_path: Path) -> list[SentinelTarget]:
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SentinelCompilationError(
            f"{profile_path.as_posix()}: unable to read target profile: {error}"
        ) from error

    if not isinstance(profile, dict):
        raise SentinelCompilationError(
            f"{profile_path.as_posix()}: target profile must be a JSON object"
        )

    expected_header = {
        "schema_version": 1,
        "target": "microsoft-sentinel",
        "backend": "kusto",
        "pipeline": "azure_monitor",
    }
    if set(profile) != {*expected_header, "detections"}:
        raise SentinelCompilationError(
            f"{profile_path.as_posix()}: profile keys do not match version 1"
        )
    for key, expected in expected_header.items():
        if profile.get(key) != expected:
            raise SentinelCompilationError(
                f"{profile_path.as_posix()}: {key} must equal {expected!r}"
            )

    detections = profile.get("detections")
    if not isinstance(detections, list) or not detections:
        raise SentinelCompilationError(
            f"{profile_path.as_posix()}: detections must be a non-empty array"
        )

    allowed_keys = {"id", "implementation", "query_table", "golden"}
    targets: list[SentinelTarget] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(detections):
        label = f"{profile_path.as_posix()}: detections[{index}]"
        if not isinstance(entry, dict) or set(entry) != allowed_keys:
            raise SentinelCompilationError(
                f"{label} must contain exactly {sorted(allowed_keys)}"
            )

        detection_id = entry["id"]
        if not isinstance(detection_id, str) or not re.fullmatch(
            r"MSEC-DET-[0-9]{4}", detection_id
        ):
            raise SentinelCompilationError(f"{label}.id is invalid")
        if detection_id in seen_ids:
            raise SentinelCompilationError(f"{label}.id is duplicated")
        seen_ids.add(detection_id)

        query_table = entry["query_table"]
        if not isinstance(query_table, str) or not _TABLE_NAME.fullmatch(query_table):
            raise SentinelCompilationError(f"{label}.query_table is invalid")

        implementation_path = entry["implementation"]
        implementation = _resolve_inside(
            repo_root, implementation_path, f"{label}.implementation"
        )
        golden = _resolve_inside(repo_root, entry["golden"], f"{label}.golden")

        if detection_id not in implementation.parts:
            raise SentinelCompilationError(
                f"{label}.implementation does not contain {detection_id}"
            )
        if not implementation.is_file():
            raise SentinelCompilationError(f"{label}.implementation does not exist")
        if not golden.is_file():
            raise SentinelCompilationError(f"{label}.golden does not exist")

        manifest_path = (
            repo_root / "catalog" / "detections" / detection_id / "manifest.json"
        )
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise SentinelCompilationError(
                f"{label}: unable to read matching catalogue manifest: {error}"
            ) from error

        declared = any(
            candidate.get("type") == "sigma"
            and candidate.get("path") == implementation_path
            and candidate.get("status") == "active"
            and "sentinel" in candidate.get("targets", [])
            for candidate in manifest.get("implementations", [])
            if isinstance(candidate, dict)
        )
        if manifest.get("id") != detection_id or not declared:
            raise SentinelCompilationError(
                f"{label}.implementation is not an active Sentinel Sigma source "
                "in the matching catalogue manifest"
            )

        targets.append(
            SentinelTarget(
                detection_id=detection_id,
                implementation=implementation,
                query_table=query_table,
                golden=golden,
            )
        )

    return targets


def compile_target(target: SentinelTarget) -> CompiledSentinelQuery:
    yaml_text = target.implementation.read_text(encoding="utf-8")
    collection = parse_sigma_collection(yaml_text, target.implementation.as_posix())
    if len(collection.rules) != 1:
        raise SentinelCompilationError(
            f"{target.implementation.as_posix()}: expected exactly one Sigma rule"
        )

    backend = KustoBackend(
        processing_pipeline=azure_monitor_pipeline(query_table=target.query_table)
    )
    queries = backend.convert(collection)
    if len(queries) != 1 or not isinstance(queries[0], str) or not queries[0].strip():
        raise SentinelCompilationError(
            f"{target.detection_id}: compiler did not produce exactly one KQL query"
        )

    query = queries[0].replace("\r\n", "\n").rstrip() + "\n"
    return CompiledSentinelQuery(
        detection_id=target.detection_id,
        query=query,
        golden=target.golden,
    )


def compile_profile(repo_root: Path, profile_path: Path) -> list[CompiledSentinelQuery]:
    verify_backend_version()
    return [
        compile_target(target)
        for target in load_target_profile(repo_root, profile_path)
    ]
