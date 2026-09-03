"""Render deterministic, disabled Microsoft Sentinel Scheduled rule bodies."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import uuid

try:
    from .sentinel_compiler import (
        CompiledSentinelQuery,
        SentinelCompilationError,
        SentinelTarget,
        compile_profile,
        load_target_profile,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from sentinel_compiler import (  # type: ignore[no-redef]
        CompiledSentinelQuery,
        SentinelCompilationError,
        SentinelTarget,
        compile_profile,
        load_target_profile,
    )


SENTINEL_API_VERSION = "2025-09-01"
SENTINEL_RESOURCE_TYPE = "Microsoft.SecurityInsights/alertRules"
RULE_ID_URL_PREFIX = "https://metesec.com/detections/"
_DETECTION_ID = re.compile(r"^MSEC-DET-[0-9]{4}$")
_DURATION = re.compile(
    r"^P(?=.+)(?:[0-9]+D)?(?:T(?=.+)(?:[0-9]+H)?(?:[0-9]+M)?(?:[0-9]+S)?)?$"
)
_TRIGGER_OPERATORS = {"Equal", "GreaterThan", "LessThan", "NotEqual"}
_EVENT_GROUPING = {"AlertPerResult", "SingleAlert"}
_SEVERITY = {
    "informational": "Informational",
    "low": "Low",
    "medium": "Medium",
    "high": "High",
}
_TACTICS = {
    "Reconnaissance": "Reconnaissance",
    "Resource Development": "ResourceDevelopment",
    "Initial Access": "InitialAccess",
    "Execution": "Execution",
    "Persistence": "Persistence",
    "Privilege Escalation": "PrivilegeEscalation",
    "Defense Evasion": "DefenseEvasion",
    # ATT&CK introduced Defense Impairment and Stealth after the Sentinel
    # 2025-09-01 AttackTactic enum was published. Keep the source mappings exact
    # and omit only unsupported target tactics instead of mislabeling them.
    "Defense Impairment": None,
    "Stealth": None,
    "Credential Access": "CredentialAccess",
    "Discovery": "Discovery",
    "Lateral Movement": "LateralMovement",
    "Collection": "Collection",
    "Command and Control": "CommandAndControl",
    "Exfiltration": "Exfiltration",
    "Impact": "Impact",
}


class SentinelRuleRenderError(ValueError):
    """Raised when a Sentinel rule profile or rendered rule fails closed."""


@dataclass(frozen=True)
class SentinelRuleSettings:
    detection_id: str
    enabled: bool
    query_frequency: str
    query_period: str
    trigger_operator: str
    trigger_threshold: int
    suppression_duration: str
    suppression_enabled: bool
    event_grouping: str
    create_incident: bool
    incident_lookback: str


@dataclass(frozen=True)
class RenderedSentinelRule:
    detection_id: str
    rule_id: str
    query: str
    request_body: dict[str, object]
    render_manifest: dict[str, object]

    def request_body_text(self) -> str:
        return json.dumps(self.request_body, indent=2, ensure_ascii=False) + "\n"

    def render_manifest_text(self) -> str:
        return json.dumps(self.render_manifest, indent=2, ensure_ascii=False) + "\n"


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SentinelRuleRenderError(f"{label}: unable to read JSON: {error}") from error
    if not isinstance(value, dict):
        raise SentinelRuleRenderError(f"{label}: expected a JSON object")
    return value


def _resolve_inside(repo_root: Path, raw_path: object, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise SentinelRuleRenderError(f"{label} must be a non-empty path")
    root = repo_root.resolve()
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise SentinelRuleRenderError(f"{label} escapes the repository") from error
    if not candidate.is_file():
        raise SentinelRuleRenderError(f"{label} does not exist")
    return candidate


def _duration(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or _DURATION.fullmatch(value) is None
    ):
        raise SentinelRuleRenderError(f"{label} is not a supported ISO 8601 duration")
    return value


def load_rule_settings(
    repo_root: Path,
    profile_path: Path,
    expected_ids: list[str],
) -> tuple[Path, list[SentinelRuleSettings]]:
    profile = _load_json(profile_path, profile_path.as_posix())
    expected_keys = {
        "schema_version",
        "target",
        "api_version",
        "source_profile",
        "rules",
    }
    if set(profile) != expected_keys:
        raise SentinelRuleRenderError("analytics-rule profile keys do not match version 1")
    expected_header = {
        "schema_version": 1,
        "target": "microsoft-sentinel",
        "api_version": SENTINEL_API_VERSION,
        "source_profile": "targets/sentinel/preview.json",
    }
    for key, expected in expected_header.items():
        if profile.get(key) != expected:
            raise SentinelRuleRenderError(f"analytics-rule profile {key} must equal {expected!r}")

    source_profile = _resolve_inside(
        repo_root,
        profile["source_profile"],
        "analytics-rule profile source_profile",
    )
    rules = profile.get("rules")
    if not isinstance(rules, list) or not rules:
        raise SentinelRuleRenderError("analytics-rule profile rules must be a non-empty array")

    rule_keys = {
        "id",
        "enabled",
        "query_frequency",
        "query_period",
        "trigger_operator",
        "trigger_threshold",
        "suppression_duration",
        "suppression_enabled",
        "event_grouping",
        "create_incident",
        "incident_lookback",
    }
    settings: list[SentinelRuleSettings] = []
    seen: set[str] = set()
    for index, raw in enumerate(rules):
        label = f"analytics-rule profile rules[{index}]"
        if not isinstance(raw, dict) or set(raw) != rule_keys:
            raise SentinelRuleRenderError(f"{label} keys do not match version 1")
        detection_id = raw.get("id")
        if not isinstance(detection_id, str) or _DETECTION_ID.fullmatch(detection_id) is None:
            raise SentinelRuleRenderError(f"{label}.id is invalid")
        if detection_id in seen:
            raise SentinelRuleRenderError(f"{label}.id is duplicated")
        seen.add(detection_id)

        if raw.get("enabled") is not False:
            raise SentinelRuleRenderError(f"{label}.enabled must remain false")
        if raw.get("suppression_enabled") is not False:
            raise SentinelRuleRenderError(
                f"{label}.suppression_enabled must remain false in the renderer phase"
            )
        if not isinstance(raw.get("create_incident"), bool):
            raise SentinelRuleRenderError(f"{label}.create_incident must be boolean")
        trigger_operator = raw.get("trigger_operator")
        if trigger_operator not in _TRIGGER_OPERATORS:
            raise SentinelRuleRenderError(f"{label}.trigger_operator is invalid")
        trigger_threshold = raw.get("trigger_threshold")
        if (
            isinstance(trigger_threshold, bool)
            or not isinstance(trigger_threshold, int)
            or trigger_threshold < 0
        ):
            raise SentinelRuleRenderError(f"{label}.trigger_threshold is invalid")
        event_grouping = raw.get("event_grouping")
        if event_grouping not in _EVENT_GROUPING:
            raise SentinelRuleRenderError(f"{label}.event_grouping is invalid")

        settings.append(
            SentinelRuleSettings(
                detection_id=detection_id,
                enabled=False,
                query_frequency=_duration(raw.get("query_frequency"), f"{label}.query_frequency"),
                query_period=_duration(raw.get("query_period"), f"{label}.query_period"),
                trigger_operator=str(trigger_operator),
                trigger_threshold=trigger_threshold,
                suppression_duration=_duration(
                    raw.get("suppression_duration"), f"{label}.suppression_duration"
                ),
                suppression_enabled=False,
                event_grouping=str(event_grouping),
                create_incident=raw["create_incident"],
                incident_lookback=_duration(
                    raw.get("incident_lookback"), f"{label}.incident_lookback"
                ),
            )
        )

    actual_ids = [item.detection_id for item in settings]
    if actual_ids != expected_ids:
        raise SentinelRuleRenderError(
            "analytics-rule profile IDs and order must exactly match the source profile: "
            f"expected {expected_ids}, got {actual_ids}"
        )
    return source_profile, settings


def _stable_rule_id(detection_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{RULE_ID_URL_PREFIX}{detection_id}"))


def _entity_mappings(target: SentinelTarget) -> list[dict[str, object]]:
    return [
        {
            "entityType": mapping.entity_type,
            "fieldMappings": [
                {
                    "identifier": field.identifier,
                    "columnName": field.column,
                }
                for field in mapping.field_mappings
            ],
        }
        for mapping in target.output.entity_mappings
    ]


def _target_tactics(attack: object, detection_id: str) -> tuple[list[str], list[str], list[dict[str, str]]]:
    if not isinstance(attack, list):
        raise SentinelRuleRenderError(f"{detection_id}: manifest attack must be an array")
    tactics: list[str] = []
    techniques: list[str] = []
    source_attack: list[dict[str, str]] = []
    for index, item in enumerate(attack):
        if not isinstance(item, dict):
            raise SentinelRuleRenderError(f"{detection_id}: attack[{index}] must be an object")
        technique = item.get("technique_id")
        tactic = item.get("tactic")
        if not isinstance(technique, str) or re.fullmatch(r"T[0-9]{4}(?:\.[0-9]{3})?", technique) is None:
            raise SentinelRuleRenderError(f"{detection_id}: attack[{index}].technique_id is invalid")
        if tactic not in _TACTICS:
            raise SentinelRuleRenderError(f"{detection_id}: unsupported Sentinel tactic {tactic!r}")
        sentinel_tactic = _TACTICS[str(tactic)]
        base_technique = technique.split(".", maxsplit=1)[0]
        if sentinel_tactic is not None and sentinel_tactic not in tactics:
            tactics.append(sentinel_tactic)
        if base_technique not in techniques:
            techniques.append(base_technique)
        source_attack.append({"technique_id": technique, "tactic": str(tactic)})
    return tactics, techniques, source_attack


def _render_one(
    repo_root: Path,
    source_profile: Path,
    target: SentinelTarget,
    compiled: CompiledSentinelQuery,
    settings: SentinelRuleSettings,
) -> RenderedSentinelRule:
    try:
        golden_query = target.golden.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeError) as error:
        raise SentinelRuleRenderError(
            f"{target.detection_id}: unable to read the Golden query: {error}"
        ) from error
    if compiled.query != golden_query:
        raise SentinelRuleRenderError(
            f"{target.detection_id}: compiled query differs from the reviewed Golden query"
        )

    manifest_path = repo_root / "catalog" / "detections" / target.detection_id / "manifest.json"
    manifest = _load_json(manifest_path, manifest_path.as_posix())
    if manifest.get("id") != target.detection_id:
        raise SentinelRuleRenderError(f"{target.detection_id}: manifest identity mismatch")
    title = manifest.get("title")
    description = manifest.get("description")
    severity = manifest.get("severity")
    if not isinstance(title, str) or not isinstance(description, str):
        raise SentinelRuleRenderError(f"{target.detection_id}: manifest text fields are invalid")
    if severity not in _SEVERITY:
        raise SentinelRuleRenderError(
            f"{target.detection_id}: severity {severity!r} is unsupported by Sentinel"
        )

    tactics, techniques, source_attack = _target_tactics(
        manifest.get("attack"), target.detection_id
    )
    rule_id = _stable_rule_id(target.detection_id)
    entity_mappings = _entity_mappings(target)
    request_body: dict[str, object] = {
        "kind": "Scheduled",
        "properties": {
            "displayName": title,
            "description": description,
            "severity": _SEVERITY[str(severity)],
            "enabled": settings.enabled,
            "tactics": tactics,
            "techniques": techniques,
            "query": compiled.query,
            "entityMappings": entity_mappings,
            "queryFrequency": settings.query_frequency,
            "queryPeriod": settings.query_period,
            "triggerOperator": settings.trigger_operator,
            "triggerThreshold": settings.trigger_threshold,
            "suppressionDuration": settings.suppression_duration,
            "suppressionEnabled": settings.suppression_enabled,
            "eventGroupingSettings": {"aggregationKind": settings.event_grouping},
            "incidentConfiguration": {
                "createIncident": settings.create_incident,
                "groupingConfiguration": {
                    "enabled": False,
                    "reopenClosedIncident": False,
                    "lookbackDuration": settings.incident_lookback,
                    "matchingMethod": "AllEntities",
                    "groupByEntities": [],
                    "groupByAlertDetails": [],
                    "groupByCustomDetails": [],
                },
            },
        },
    }
    request_bytes = (json.dumps(request_body, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    query_bytes = compiled.query.encode("utf-8")
    root = repo_root.resolve()
    render_manifest: dict[str, object] = {
        "format_version": 1,
        "target": "microsoft-sentinel",
        "resource_type": SENTINEL_RESOURCE_TYPE,
        "api_version": SENTINEL_API_VERSION,
        "detection_id": target.detection_id,
        "rule_id": rule_id,
        "source": {
            "analytics_rule_profile": profile_relative(source_profile, root),
            "logical_manifest": profile_relative(manifest_path, root),
            "implementation": profile_relative(target.implementation, root),
            "golden_query": profile_relative(target.golden, root),
            "attack": source_attack,
            "output_columns": list(target.output.columns),
            "entity_mappings": entity_mappings,
        },
        "artifacts": {
            "analytics_rule": {
                "path": "analytics-rule.json",
                "sha256": hashlib.sha256(request_bytes).hexdigest(),
            },
            "query": {
                "path": "query.kql",
                "sha256": hashlib.sha256(query_bytes).hexdigest(),
            },
        },
        "deployment": {"implemented": False, "enabled": False},
    }
    return RenderedSentinelRule(
        detection_id=target.detection_id,
        rule_id=rule_id,
        query=compiled.query,
        request_body=request_body,
        render_manifest=render_manifest,
    )


def profile_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as error:
        raise SentinelRuleRenderError(f"render source escapes repository: {path}") from error


def render_profile(repo_root: Path, analytics_profile: Path) -> list[RenderedSentinelRule]:
    repo_root = repo_root.resolve()
    raw_profile = _load_json(analytics_profile, analytics_profile.as_posix())
    raw_rules = raw_profile.get("rules")
    if not isinstance(raw_rules, list):
        raise SentinelRuleRenderError("analytics-rule profile rules must be an array")
    expected_ids = [
        item.get("id") if isinstance(item, dict) else None
        for item in raw_rules
    ]
    if not all(isinstance(item, str) for item in expected_ids):
        raise SentinelRuleRenderError("analytics-rule profile contains an invalid ID")

    source_profile, settings = load_rule_settings(
        repo_root,
        analytics_profile,
        [str(item) for item in expected_ids],
    )
    targets = load_target_profile(repo_root, source_profile)
    compiled = compile_profile(repo_root, source_profile)
    source_ids = [target.detection_id for target in targets]
    configured_ids = [item.detection_id for item in settings]
    if configured_ids != source_ids:
        raise SentinelRuleRenderError(
            "analytics-rule profile IDs and order must exactly match the source profile: "
            f"expected {source_ids}, got {configured_ids}"
        )

    return [
        _render_one(repo_root, analytics_profile, target, query, rule_settings)
        for target, query, rule_settings in zip(targets, compiled, settings, strict=True)
    ]


def write_rendered_rules(rules: list[RenderedSentinelRule], output_root: Path) -> list[Path]:
    written: list[Path] = []
    for rule in rules:
        directory = output_root / rule.detection_id
        directory.mkdir(parents=True, exist_ok=True)
        outputs = {
            directory / "query.kql": rule.query,
            directory / "analytics-rule.json": rule.request_body_text(),
            directory / "render-manifest.json": rule.render_manifest_text(),
        }
        for path, content in outputs.items():
            temporary = path.with_name(f".{path.name}.tmp")
            temporary.write_text(content, encoding="utf-8", newline="\n")
            temporary.replace(path)
            written.append(path)
    return written


__all__ = [
    "RenderedSentinelRule",
    "SENTINEL_API_VERSION",
    "SENTINEL_RESOURCE_TYPE",
    "SentinelCompilationError",
    "SentinelRuleRenderError",
    "load_rule_settings",
    "render_profile",
    "write_rendered_rules",
]
