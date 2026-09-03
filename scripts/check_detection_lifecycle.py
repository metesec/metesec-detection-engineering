#!/usr/bin/env python3
"""Validate logical detection lifecycle and review cadence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

try:
    from .detection_lifecycle import (
        DetectionLifecycleError,
        assess_lifecycle,
        assessment_document,
        load_baseline_catalogue,
        load_manifest_records,
        load_policy,
        parse_date,
        validate_transitions,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from detection_lifecycle import (  # type: ignore[no-redef]
        DetectionLifecycleError,
        assess_lifecycle,
        assessment_document,
        load_baseline_catalogue,
        load_manifest_records,
        load_policy,
        parse_date,
        validate_transitions,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = REPO_ROOT / "catalog" / "detections"
POLICY = REPO_ROOT / "governance" / "policies" / "detection-lifecycle-v1.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--as-of",
        help="UTC assessment date as YYYY-MM-DD; defaults to the current UTC date.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Optional previous catalog/index.json used to validate lifecycle transitions.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        as_of = (
            parse_date(args.as_of, "--as-of")
            if args.as_of is not None
            else datetime.now(timezone.utc).date()
        )
        transitions = load_policy(POLICY)
        records = load_manifest_records(CATALOG_ROOT)
        baseline_checked = args.baseline is not None
        if args.baseline is not None:
            baseline = load_baseline_catalogue(args.baseline)
            validate_transitions(records, baseline, transitions)
        assessments = assess_lifecycle(records, as_of)
        document = assessment_document(assessments, as_of, baseline_checked)
    except DetectionLifecycleError as error:
        print(f"Detection lifecycle check failed: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        print(f"Detection lifecycle review as of {document['as_of']}:")
        for item in assessments:
            print(
                f"{item.detection_id}: {item.review_state}; modified {item.modified}; "
                f"review due {item.review_due}"
            )
        if baseline_checked:
            print("Lifecycle transition baseline: checked.")
        else:
            print("Lifecycle transition baseline: not supplied; current-state checks only.")

    return 2 if document["summary"]["due"] or document["summary"]["overdue"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
