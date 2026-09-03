#!/usr/bin/env python3
"""Build the deterministic public Detection Pack release archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ARCHIVE_BASENAME = "metesec-detection-pack"
EXACT_SOURCES = (
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "CATALOGUE.md",
    "catalog/index.json",
    "COVERAGE.md",
    "coverage/index.json",
    "targets/sentinel/preview.json",
    "targets/sentinel/analytics-rules.json",
    "targets/sentinel/data-sources.json",
    "docs/testing/sigma-fixture-evaluation.md",
    "docs/tooling/sentinel-compilation.md",
)
SOURCE_GLOBS = (
    "catalog/detections/*/manifest.json",
    "content/portable/sigma/*/rule.yml",
    "content/portable/sigma/*/tests/cases.json",
    "content/portable/sigma/*/tests/fixtures/*.json",
    "docs/contracts/*.md",
    "docs/releases/*.md",
    "governance/schemas/*.json",
    "tests/golden/sentinel/*.kql",
)


class ReleaseBuildError(RuntimeError):
    """Raised when the release source or destination violates the contract."""


def _normalized_text(path: Path) -> bytes:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseBuildError(f"release source is not UTF-8 text: {path}") from error
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _source_paths(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for relative in EXACT_SOURCES:
        path = repo_root / relative
        if not path.is_file():
            raise ReleaseBuildError(f"required release source is missing: {relative}")
        paths.add(path)

    for pattern in SOURCE_GLOBS:
        matches = [path for path in repo_root.glob(pattern) if path.is_file()]
        if not matches:
            raise ReleaseBuildError(f"release source pattern matched no files: {pattern}")
        paths.update(matches)

    root = repo_root.resolve()
    validated: list[Path] = []
    for path in paths:
        if path.is_symlink():
            raise ReleaseBuildError(f"release source must not be a symlink: {path}")
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise ReleaseBuildError(f"release source escapes repository: {path}") from error
        validated.append(path)

    return sorted(validated, key=lambda item: item.relative_to(repo_root).as_posix())


def _version(repo_root: Path) -> str:
    package = json.loads((repo_root / "package.json").read_text(encoding="utf-8"))
    version = package.get("version")
    if not isinstance(version, str) or re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        raise ReleaseBuildError("package.json version must be a three-part numeric version")
    return version


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits |= 0x800
    return info


def build_release(repo_root: Path, output_dir: Path) -> tuple[Path, Path]:
    repo_root = repo_root.resolve()
    version = _version(repo_root)
    archive_root = f"{ARCHIVE_BASENAME}-v{version}"
    archive_name = f"{archive_root}.zip"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / archive_name
    checksum_path = output_dir / "SHA256SUMS"

    members: dict[str, bytes] = {}
    manifest_files = []
    for path in _source_paths(repo_root):
        relative = path.relative_to(repo_root).as_posix()
        if PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts:
            raise ReleaseBuildError(f"unsafe release path: {relative}")
        content = _normalized_text(path)
        members[relative] = content
        manifest_files.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(content).hexdigest(),
                "size_bytes": len(content),
            }
        )

    catalogue = json.loads(members["catalog/index.json"].decode("utf-8"))
    manifest = {
        "format_version": 1,
        "project": "MeteSec Detection Engineering",
        "release": f"v{version}",
        "license": "Apache-2.0",
        "summary": catalogue["summary"],
        "scope": {
            "portable_sigma": True,
            "synthetic_fixture_evidence": True,
            "sentinel_preview": True,
            "sentinel_data_source_contract": True,
            "coverage_report": True,
            "siem_deployment": False,
        },
        "files": manifest_files,
    }
    members["RELEASE-MANIFEST.json"] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")

    temporary_archive = output_dir / f".{archive_name}.tmp"
    with zipfile.ZipFile(temporary_archive, "w", allowZip64=True) as archive:
        for relative in sorted(members):
            archive.writestr(_zip_info(f"{archive_root}/{relative}"), members[relative])
    temporary_archive.replace(archive_path)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    temporary_checksum = output_dir / ".SHA256SUMS.tmp"
    temporary_checksum.write_text(
        f"{digest}  {archive_name}\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary_checksum.replace(checksum_path)
    return archive_path, checksum_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "dist" / "release",
        help="Directory for the ZIP archive and SHA256SUMS file.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        archive, checksums = build_release(REPO_ROOT, args.output_dir)
    except (OSError, KeyError, json.JSONDecodeError, ReleaseBuildError) as error:
        print(f"Release build failed: {error}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    print(f"WROTE {archive.relative_to(REPO_ROOT).as_posix()}")
    print(f"WROTE {checksums.relative_to(REPO_ROOT).as_posix()}")
    print(f"SHA256 {digest}  {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
