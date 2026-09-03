#!/usr/bin/env python3
"""Validate or write disabled Microsoft Sentinel Scheduled rule artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from .sentinel_rule_renderer import (
        SentinelCompilationError,
        SentinelRuleRenderError,
        render_profile,
        write_rendered_rules,
    )
except ImportError:  # Support direct execution from the scripts directory.
    from sentinel_rule_renderer import (  # type: ignore[no-redef]
        SentinelCompilationError,
        SentinelRuleRenderError,
        render_profile,
        write_rendered_rules,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = REPO_ROOT / "targets" / "sentinel" / "analytics-rules.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate rendered rules without writing dist output.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "dist" / "sentinel",
        help="Directory for generated Sentinel rule artifacts.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        rendered = render_profile(REPO_ROOT, DEFAULT_PROFILE)
    except (SentinelCompilationError, SentinelRuleRenderError) as error:
        print(f"Sentinel analytics-rule rendering failed: {error}", file=sys.stderr)
        return 1

    if args.check:
        print(
            "Sentinel analytics-rule rendering passed: "
            f"{len(rendered)} disabled Scheduled rule body/bodies validated."
        )
        print(
            "This proves deterministic rendering only; deployment and live enablement "
            "are not implemented."
        )
        return 0

    written = write_rendered_rules(rendered, args.output_dir)
    for path in written:
        try:
            display = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            display = path.resolve().as_posix()
        print(f"WROTE {display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
