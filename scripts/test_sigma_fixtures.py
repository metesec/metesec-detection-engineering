#!/usr/bin/env python3
"""Run all implementation-local synthetic Sigma fixture sets."""

from __future__ import annotations

from pathlib import Path
import sys

try:
    from .sigma_fixture_evaluator import (
        LocalEvaluationError,
        discover_fixture_sets,
        run_fixture_set,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from sigma_fixture_evaluator import (
        LocalEvaluationError,
        discover_fixture_sets,
        run_fixture_set,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    fixture_sets = discover_fixture_sets(REPO_ROOT)
    if not fixture_sets:
        print(
            "No Sigma fixture sets exist yet; no local detection-behavior claim was tested."
        )
        return 0

    failures = []
    case_count = 0

    for cases_path in fixture_sets:
        try:
            outcomes = run_fixture_set(REPO_ROOT, cases_path)
        except LocalEvaluationError as error:
            failures.append(str(error))
            continue

        for outcome in outcomes:
            case_count += 1
            actual = "match" if outcome.actual_match else "no_match"
            if outcome.passed:
                print(f"PASS {outcome.case_id}: expected {outcome.expectation}, got {actual}")
            else:
                failures.append(
                    f"{outcome.case_id}: expected {outcome.expectation}, got {actual}"
                )

    if failures:
        print("Sigma fixture evaluation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        f"Local Sigma fixture evaluation passed: {len(fixture_sets)} fixture set(s), "
        f"{case_count} synthetic case(s)."
    )
    print(
        "This proves only the documented local evaluator subset; it is not target-SIEM validation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
