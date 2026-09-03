#!/usr/bin/env python3
"""Compile or verify the bounded Microsoft Sentinel preview target."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from .sentinel_compiler import SentinelCompilationError, compile_profile
except ImportError:  # Support direct execution from the scripts directory.
    from sentinel_compiler import SentinelCompilationError, compile_profile


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = REPO_ROOT / "targets" / "sentinel" / "preview.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare generated KQL with committed Golden snapshots without writing dist.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        compiled = compile_profile(REPO_ROOT, DEFAULT_PROFILE)
    except SentinelCompilationError as error:
        print(f"Sentinel compilation failed: {error}", file=sys.stderr)
        return 1

    if args.check:
        failures = []
        for item in compiled:
            expected = item.golden.read_text(encoding="utf-8").replace("\r\n", "\n")
            if item.query != expected:
                failures.append(
                    f"{item.detection_id}: generated KQL differs from "
                    f"{item.golden.relative_to(REPO_ROOT).as_posix()}"
                )
        if failures:
            print("Sentinel Golden snapshot verification failed:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1

        if len(compiled) == 1:
            summary = "1 query matches its pinned Golden snapshot."
        else:
            summary = f"{len(compiled)} queries match their pinned Golden snapshots."
        print(f"Sentinel compilation passed: {summary}")
        print(
            "This proves deterministic compilation only; live target behavior is a "
            "separate validation claim."
        )
        return 0

    output_root = REPO_ROOT / "dist" / "sentinel"
    for item in compiled:
        output_path = output_root / item.detection_id / "query.kql"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(item.query, encoding="utf-8", newline="\n")
        print(f"WROTE {output_path.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
