from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
import zipfile

from scripts.build_release import (
    FIXED_ZIP_TIMESTAMP,
    ReleaseBuildError,
    _display_path,
    build_release,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReleaseBuilderTests(unittest.TestCase):
    def test_display_path_supports_external_output_directory(self) -> None:
        with TemporaryDirectory() as directory:
            external = Path(directory) / "release.zip"
            self.assertEqual(
                _display_path(external, REPO_ROOT), external.resolve().as_posix()
            )

    def test_two_independent_builds_are_byte_identical(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            first, first_sums = build_release(REPO_ROOT, root / "first")
            second, second_sums = build_release(REPO_ROOT, root / "second")

            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_sums.read_bytes(), second_sums.read_bytes())

    def test_archive_manifest_matches_every_packaged_source(self) -> None:
        with TemporaryDirectory() as directory:
            archive_path, _ = build_release(REPO_ROOT, Path(directory))
            expected_root = archive_path.stem
            with zipfile.ZipFile(archive_path) as archive:
                infos = archive.infolist()
                names = [info.filename for info in infos]
                self.assertEqual(names, sorted(names))
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(all(info.date_time == FIXED_ZIP_TIMESTAMP for info in infos))
                self.assertTrue(all(name.startswith(f"{expected_root}/") for name in names))
                self.assertTrue(all(".." not in Path(name).parts for name in names))

                manifest_name = f"{expected_root}/RELEASE-MANIFEST.json"
                manifest = json.loads(archive.read(manifest_name))
                self.assertEqual(manifest["format_version"], 1)
                package = json.loads((REPO_ROOT / "package.json").read_text())
                catalogue = json.loads((REPO_ROOT / "catalog/index.json").read_text())
                self.assertEqual(manifest["release"], f"v{package['version']}")
                self.assertEqual(manifest["summary"], catalogue["summary"])
                self.assertTrue(manifest["scope"]["validation_tooling"])
                self.assertTrue(manifest["scope"]["dependency_locks"])
                self.assertTrue(manifest["scope"]["sentinel_data_source_contract"])
                self.assertTrue(manifest["scope"]["coverage_report"])
                self.assertTrue(manifest["scope"]["lifecycle_policy"])
                self.assertTrue(
                    manifest["scope"]["sentinel_runtime_health_contract"]
                )
                self.assertFalse(manifest["scope"]["siem_deployment"])

                declared = {item["path"]: item for item in manifest["files"]}
                packaged = {
                    name.removeprefix(f"{expected_root}/")
                    for name in names
                    if name != manifest_name
                }
                self.assertIn("COVERAGE.md", packaged)
                self.assertIn("coverage/index.json", packaged)
                self.assertIn(
                    "governance/policies/detection-lifecycle-v1.json", packaged
                )
                self.assertIn(
                    "governance/policies/sentinel-runtime-health-v1.json", packaged
                )
                self.assertIn(
                    "docs/tooling/sentinel-source-inventory.md", packaged
                )
                self.assertIn(f"docs/releases/v{package['version']}.md", packaged)
                for dependency in (
                    "NOTICE", "docs/reviews/upstream-overlap.json",
                    "package.json", "pnpm-lock.yaml", "requirements-sigma.lock",
                    "scripts/build_release.py", "scripts/test_sigma_fixtures.py",
                    "scripts/lib/package-contract.mjs", "tests/test_release_builder.py",
                    "examples/manifests/valid/draft-windows-service-install.json",
                    ".forgejo/workflows/validate.yml",
                ):
                    self.assertIn(dependency, packaged)
                self.assertEqual(set(declared), packaged)
                for relative, item in declared.items():
                    content = archive.read(f"{expected_root}/{relative}")
                    self.assertEqual(item["size_bytes"], len(content))
                    self.assertEqual(item["sha256"], hashlib.sha256(content).hexdigest())
                    if relative.startswith("content/portable/sigma/") and "/tests/fixtures/" in relative:
                        self.assertIs(json.loads(content)["synthetic"], True)
                    if relative.startswith("catalog/detections/") and relative.endswith("/manifest.json"):
                        detection = json.loads(content)
                        self.assertEqual(detection["lifecycle"]["status"], "experimental")
                analytics = json.loads(archive.read(f"{expected_root}/targets/sentinel/analytics-rules.json"))
                self.assertTrue(analytics["rules"])
                self.assertTrue(all(rule["enabled"] is False for rule in analytics["rules"]))
                self.assertFalse(any("node_modules" in Path(name).parts or "__pycache__" in Path(name).parts or ".git" in Path(name).parts or "/dist/" in name for name in names))

    def test_extracted_archive_rebuilds_without_the_source_checkout(self) -> None:
        """Every allowlisted input needed by a subsequent build ships in the ZIP."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path, _ = build_release(REPO_ROOT, root / "first")
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(root / "extracted")
            extracted = root / "extracted" / archive_path.stem
            rebuilt, _ = build_release(extracted, root / "rebuilt")
            self.assertEqual(archive_path.read_bytes(), rebuilt.read_bytes())

    def test_extracted_archive_can_run_its_own_behavioral_validation(self) -> None:
        """Exercise packaged imports/data, not modules from the source checkout."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path, _ = build_release(REPO_ROOT, root / "release")
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(root / "extracted")
            extracted = root / "extracted" / archive_path.stem
            environment = dict(os.environ)
            environment.pop("PYTHONPATH", None)
            result = subprocess.run(
                [sys.executable, "scripts/test_sigma_fixtures.py"],
                cwd=extracted,
                env=environment,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Local Sigma fixture evaluation passed", result.stdout)

    def test_external_checksum_verifies_archive(self) -> None:
        with TemporaryDirectory() as directory:
            archive_path, checksum_path = build_release(REPO_ROOT, Path(directory))
            digest, filename = checksum_path.read_text(encoding="utf-8").strip().split(
                "  ", maxsplit=1
            )
            self.assertEqual(filename, archive_path.name)
            self.assertEqual(digest, hashlib.sha256(archive_path.read_bytes()).hexdigest())

    def test_current_version_release_notes_are_required(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                '{"version": "1.0.0"}\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ReleaseBuildError,
                r"current release notes are missing: docs/releases/v1\.0\.0\.md",
            ):
                build_release(root, root / "out")


if __name__ == "__main__":
    unittest.main()
