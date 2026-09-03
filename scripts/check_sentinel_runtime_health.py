#!/usr/bin/env python3
"""Validate or assess the bounded Sentinel runtime-health contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from .sentinel_runtime_health import (
        SentinelRuntimeHealthError,
        assess_runtime_health,
        assessment_document,
        load_expectations,
        load_observation,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from sentinel_runtime_health import (  # type: ignore[no-redef]
        SentinelRuntimeHealthError,
        assess_runtime_health,
        assessment_document,
        load_expectations,
        load_observation,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY = REPO_ROOT / "governance" / "policies" / "sentinel-runtime-health-v1.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observation",
        type=Path,
        help="Environment-local runtime observation JSON; omit for contract validation only.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        policy, expectations = load_expectations(REPO_ROOT, POLICY)
        if args.observation is None:
            print(
                "Sentinel runtime-health contract passed: "
                f"{len(expectations)} scheduled rule expectation(s)."
            )
            print("No environment observation was supplied; this is not a live health claim.")
            return 0
        observed_at, observations = load_observation(args.observation)
        assessments = assess_runtime_health(
            policy, expectations, observed_at, observations
        )
        document = assessment_document(observed_at, assessments)
    except SentinelRuntimeHealthError as error:
        print(f"Sentinel runtime-health check failed: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        for item in assessments:
            print(
                f"{item.detection_id}: {item.status} "
                f"({', '.join(item.reasons)})"
            )
    return 0 if all(item.status == "healthy" for item in assessments) else 2


if __name__ == "__main__":
    raise SystemExit(main())
