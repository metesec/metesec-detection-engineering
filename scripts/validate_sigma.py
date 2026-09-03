#!/usr/bin/env python3
"""Validate the pinned pySigma runtime and every portable Sigma rule."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys

from sigma_validation import (
    EXPECTED_PYSIGMA_VERSION,
    SigmaDocumentError,
    discover_sigma_rules,
    validate_sigma_path,
    verify_parser_health,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        installed_version = version("pySigma")
    except PackageNotFoundError:
        print(
            "Sigma validation failed: pySigma is not installed. "
            "Run `python -m pip install --requirement requirements-sigma.lock`.",
            file=sys.stderr,
        )
        return 1

    if installed_version != EXPECTED_PYSIGMA_VERSION:
        print(
            "Sigma validation failed: expected pySigma "
            f"{EXPECTED_PYSIGMA_VERSION}, found {installed_version}.",
            file=sys.stderr,
        )
        return 1

    try:
        verify_parser_health()
    except (RuntimeError, SigmaDocumentError) as error:
        print(f"Sigma parser health check failed: {error}", file=sys.stderr)
        return 1

    rule_paths = discover_sigma_rules(REPO_ROOT)
    results = []
    failures = []

    for path in rule_paths:
        try:
            results.append(validate_sigma_path(path))
        except SigmaDocumentError as error:
            failures.append(str(error))

    if failures:
        print("Sigma source validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    rule_count = sum(result.rule_count for result in results)
    print(
        f"Sigma validation passed with pySigma {installed_version}: "
        f"parser self-test passed; {len(rule_paths)} source file(s), "
        f"{rule_count} rule(s) validated."
    )
    if not rule_paths:
        print(
            "No portable Sigma source exists yet; this result proves the "
            "toolchain only and makes no detection-behavior claim."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
