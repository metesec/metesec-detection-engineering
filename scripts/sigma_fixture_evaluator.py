"""Deliberately bounded local evaluator for synthetic Sigma fixtures."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from sigma.conditions import (
    ConditionAND,
    ConditionFieldEqualsValueExpression,
    ConditionNOT,
    ConditionOR,
    SigmaCondition,
)
from sigma.rule import SigmaRule
from sigma.types import SigmaNumber, SigmaString

try:
    from .sigma_validation import parse_sigma_collection
except ImportError:  # Support direct execution from the scripts directory.
    from sigma_validation import parse_sigma_collection


class LocalEvaluationError(ValueError):
    """Raised when fixture data or paths violate the local test contract."""


class UnsupportedSigmaFeature(LocalEvaluationError):
    """Raised instead of guessing at Sigma behavior outside the supported subset."""


@dataclass(frozen=True)
class FixtureOutcome:
    case_id: str
    expectation: str
    actual_match: bool
    fixture: str

    @property
    def passed(self) -> bool:
        return self.actual_match is (self.expectation == "match")


def _validate_condition_node(node: Any) -> None:
    if isinstance(node, (ConditionAND, ConditionOR)):
        if not node.args:
            raise UnsupportedSigmaFeature("empty boolean condition is not supported")
        for argument in node.args:
            _validate_condition_node(argument)
        return

    if isinstance(node, ConditionNOT):
        if len(node.args) != 1:
            raise UnsupportedSigmaFeature("NOT must contain exactly one argument")
        _validate_condition_node(node.args[0])
        return

    if isinstance(node, ConditionFieldEqualsValueExpression):
        if not node.field:
            raise UnsupportedSigmaFeature("fieldless expressions are not supported")
        if not isinstance(node.value, (SigmaString, SigmaNumber)):
            raise UnsupportedSigmaFeature(
                f"field {node.field} uses unsupported value type {type(node.value).__name__}"
            )
        return

    raise UnsupportedSigmaFeature(
        f"condition node {type(node).__name__} is outside the local evaluator subset"
    )


def _condition_tree(rule: SigmaRule) -> Any:
    conditions = rule.detection.condition
    if len(conditions) != 1:
        raise UnsupportedSigmaFeature(
            "the local evaluator requires exactly one Sigma condition"
        )

    condition = SigmaCondition(conditions[0], rule.detection).parse()
    if condition is None:
        raise UnsupportedSigmaFeature("Sigma condition produced no expression tree")
    _validate_condition_node(condition)
    return condition


def _match_sigma_value(expected: SigmaString | SigmaNumber, actual: Any) -> bool:
    if isinstance(expected, SigmaString):
        if not isinstance(actual, str):
            return False
        pattern = expected.to_regex().regexp.to_plain_regex()
        return re.fullmatch(pattern, actual, flags=re.IGNORECASE | re.DOTALL) is not None

    if isinstance(expected, SigmaNumber):
        return (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and actual == expected.number
        )

    raise UnsupportedSigmaFeature(
        f"value type {type(expected).__name__} is outside the local evaluator subset"
    )


def _evaluate_condition(node: Any, event: dict[str, Any]) -> bool:
    if isinstance(node, ConditionAND):
        return all(_evaluate_condition(argument, event) for argument in node.args)
    if isinstance(node, ConditionOR):
        return any(_evaluate_condition(argument, event) for argument in node.args)
    if isinstance(node, ConditionNOT):
        return not _evaluate_condition(node.args[0], event)
    if isinstance(node, ConditionFieldEqualsValueExpression):
        if node.field not in event:
            return False
        return _match_sigma_value(node.value, event[node.field])

    raise UnsupportedSigmaFeature(
        f"condition node {type(node).__name__} is outside the local evaluator subset"
    )


def load_single_rule(rule_path: Path) -> SigmaRule:
    try:
        yaml_text = rule_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise LocalEvaluationError(f"unable to read {rule_path}: {error}") from error

    collection = parse_sigma_collection(yaml_text, rule_path.as_posix())
    if len(collection.rules) != 1:
        raise UnsupportedSigmaFeature(
            f"{rule_path}: expected exactly one rule, found {len(collection.rules)}"
        )

    rule = collection.rules[0]
    _condition_tree(rule)
    return rule


def evaluate_rule(rule: SigmaRule, event: dict[str, Any]) -> bool:
    """Evaluate one flat synthetic event against the supported Sigma subset."""

    return _evaluate_condition(_condition_tree(rule), event)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise LocalEvaluationError(f"unable to read JSON {path}: {error}") from error


def _resolve_inside(parent: Path, relative_path: str, label: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise LocalEvaluationError(f"{label} must be a non-empty relative path")

    parent = parent.resolve()
    normalized_parts = relative_path.replace("\\", "/").split("/")
    candidate = parent.joinpath(*normalized_parts).resolve()
    try:
        candidate.relative_to(parent)
    except ValueError as error:
        raise LocalEvaluationError(f"{label} escapes its owned directory") from error
    return candidate


def _load_synthetic_event(fixture_path: Path) -> dict[str, Any]:
    fixture = _read_json(fixture_path)
    if not isinstance(fixture, dict):
        raise LocalEvaluationError(f"{fixture_path}: fixture must be an object")
    if set(fixture) != {"schema_version", "synthetic", "event"}:
        raise LocalEvaluationError(
            f"{fixture_path}: fixture must contain only schema_version, synthetic, and event"
        )
    if fixture["schema_version"] != 1 or fixture["synthetic"] is not True:
        raise LocalEvaluationError(
            f"{fixture_path}: fixture must declare schema_version 1 and synthetic true"
        )
    if not isinstance(fixture["event"], dict) or not fixture["event"]:
        raise LocalEvaluationError(f"{fixture_path}: event must be a non-empty object")
    if any(
        not isinstance(value, (str, int, float, bool))
        for value in fixture["event"].values()
    ):
        raise LocalEvaluationError(
            f"{fixture_path}: event values must be flat string, number, or boolean values"
        )
    return fixture["event"]


def run_fixture_set(repo_root: Path, cases_path: Path) -> list[FixtureOutcome]:
    """Run one implementation-local fixture index against its Sigma rule."""

    fixture_set = _read_json(cases_path)
    if not isinstance(fixture_set, dict) or not isinstance(fixture_set.get("cases"), list):
        raise LocalEvaluationError(f"{cases_path}: invalid fixture-set structure")
    if not fixture_set["cases"]:
        raise LocalEvaluationError(f"{cases_path}: fixture set contains no cases")

    implementation_path = _resolve_inside(
        repo_root,
        fixture_set.get("implementation"),
        f"{cases_path}: implementation",
    )
    rule = load_single_rule(implementation_path)
    fixtures_root = (cases_path.parent / "fixtures").resolve()
    outcomes = []

    for test_case in fixture_set["cases"]:
        if not isinstance(test_case, dict):
            raise LocalEvaluationError(f"{cases_path}: every case must be an object")
        case_id = test_case.get("id")
        expectation = test_case.get("expectation")
        fixture_reference = test_case.get("fixture")
        if not isinstance(case_id, str) or expectation not in {"match", "no_match"}:
            raise LocalEvaluationError(f"{cases_path}: invalid case identity or expectation")
        if not isinstance(fixture_reference, str) or not fixture_reference.startswith("fixtures/"):
            raise LocalEvaluationError(f"{cases_path}: case {case_id} has an invalid fixture path")

        fixture_path = _resolve_inside(
            fixtures_root,
            fixture_reference.removeprefix("fixtures/"),
            f"{cases_path}: case {case_id} fixture",
        )
        event = _load_synthetic_event(fixture_path)
        outcomes.append(
            FixtureOutcome(
                case_id=case_id,
                expectation=expectation,
                actual_match=evaluate_rule(rule, event),
                fixture=fixture_reference,
            )
        )

    return outcomes


def discover_fixture_sets(repo_root: Path) -> list[Path]:
    sigma_root = repo_root / "content" / "portable" / "sigma"
    if not sigma_root.exists():
        return []
    return sorted(sigma_root.glob("*/tests/cases.json"))
