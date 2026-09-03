"""Reusable structural validation for portable Sigma source files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sigma.collection import SigmaCollection


EXPECTED_PYSIGMA_VERSION = "1.5.0"

_VALID_PROBE = """\
title: MeteSec Sigma parser probe
id: 00000000-0000-4000-8000-000000000001
status: test
description: Synthetic parser health check with no production meaning.
author: MeteSec
date: 2026-09-03
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: '\\sc.exe'
    CommandLine|contains: ' create '
  condition: selection
falsepositives:
  - Synthetic validation probe only.
level: medium
"""

_INVALID_PROBE = """\
title: Deliberately invalid parser probe
logsource:
  product: windows
detection:
  selection:
    Image: sc.exe
"""


@dataclass(frozen=True)
class SigmaValidationResult:
    """A successfully parsed Sigma source and its rule count."""

    source: str
    rule_count: int


class SigmaDocumentError(ValueError):
    """Raised when pySigma cannot accept a source as a valid collection."""


def validate_sigma_text(yaml_text: str, source: str = "<memory>") -> SigmaValidationResult:
    """Parse a Sigma YAML document and reject every collected parser error."""

    try:
        collection = SigmaCollection.from_yaml(yaml_text, collect_errors=True)
    except Exception as error:  # pySigma exposes multiple format-specific errors.
        raise SigmaDocumentError(f"{source}: {type(error).__name__}: {error}") from error

    if collection.errors:
        details = "; ".join(
            f"{type(error).__name__}: {error}" for error in collection.errors
        )
        raise SigmaDocumentError(f"{source}: {details}")

    if not collection.rules:
        raise SigmaDocumentError(f"{source}: document contains no Sigma rule")

    return SigmaValidationResult(source=source, rule_count=len(collection.rules))


def validate_sigma_path(path: Path) -> SigmaValidationResult:
    """Read and validate one UTF-8 Sigma source file."""

    try:
        yaml_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SigmaDocumentError(f"{path}: unable to read UTF-8 source: {error}") from error

    return validate_sigma_text(yaml_text, path.as_posix())


def discover_sigma_rules(repo_root: Path) -> list[Path]:
    """Return only Package v1 portable Sigma entry points."""

    sigma_root = repo_root / "content" / "portable" / "sigma"
    if not sigma_root.exists():
        return []

    return sorted(sigma_root.glob("*/rule.yml"))


def verify_parser_health() -> None:
    """Prove the pinned parser accepts valid input and rejects invalid input."""

    result = validate_sigma_text(_VALID_PROBE, "<valid-parser-probe>")
    if result.rule_count != 1:
        raise RuntimeError(
            f"valid parser probe produced {result.rule_count} rules instead of one"
        )

    try:
        validate_sigma_text(_INVALID_PROBE, "<invalid-parser-probe>")
    except SigmaDocumentError:
        return

    raise RuntimeError("pySigma accepted the deliberately invalid parser probe")
