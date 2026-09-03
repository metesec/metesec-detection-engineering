#!/usr/bin/env python3
"""Validate or assess the bounded Microsoft Sentinel data-source contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from .sentinel_data_source_health import (
        SentinelDataSourceError,
        assess_data_sources,
        load_contract,
        load_observation,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from sentinel_data_source_health import (  # type: ignore[no-redef]
        SentinelDataSourceError,
        assess_data_sources,
        load_contract,
        load_observation,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = REPO_ROOT / "targets" / "sentinel" / "data-sources.json"
DEFAULT_PREVIEW = REPO_ROOT / "targets" / "sentinel" / "preview.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observation",
        type=Path,
        help="Environment-local observation JSON to assess; omit to validate the contract only.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable assessment JSON.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        contracts = load_contract(DEFAULT_CONTRACT, DEFAULT_PREVIEW)
        if args.observation is None:
            print(
                "Sentinel data-source contract passed: "
                f"{len(contracts)} source(s) cover "
                f"{sum(len(item.consumers) for item in contracts)} detection binding(s)."
            )
            print(
                "No environment observation was supplied; this is not a live health claim."
            )
            return 0

        observed_at, observations = load_observation(args.observation)
        assessments = assess_data_sources(contracts, observed_at, observations)
    except SentinelDataSourceError as error:
        print(f"Sentinel data-source check failed: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "target": "microsoft-sentinel",
                    "assessments": [item.to_dict() for item in assessments],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for item in assessments:
            print(
                f"{item.source_id} {item.table}: {item.status} "
                f"({', '.join(item.reasons)})"
            )

    return 0 if all(item.status == "ready" for item in assessments) else 2


if __name__ == "__main__":
    raise SystemExit(main())
