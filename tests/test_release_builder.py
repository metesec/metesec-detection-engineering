from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile

from scripts.build_release import (
    FIXED_ZIP_TIMESTAMP,
    build_release,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReleaseBuilderTests(unittest.TestCase):
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
                self.assertEqual(manifest["release"], "v0.3.0")
                self.assertEqual(manifest["summary"]["detections"], 5)
                self.assertEqual(manifest["summary"]["sentinel_preview_bindings"], 4)
                self.assertTrue(manifest["scope"]["sentinel_data_source_contract"])
                self.assertTrue(manifest["scope"]["coverage_report"])
                self.assertTrue(manifest["scope"]["lifecycle_policy"])
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
                self.assertEqual(set(declared), packaged)
                for relative, item in declared.items():
                    content = archive.read(f"{expected_root}/{relative}")
                    self.assertEqual(item["size_bytes"], len(content))
                    self.assertEqual(item["sha256"], hashlib.sha256(content).hexdigest())

    def test_external_checksum_verifies_archive(self) -> None:
        with TemporaryDirectory() as directory:
            archive_path, checksum_path = build_release(REPO_ROOT, Path(directory))
            digest, filename = checksum_path.read_text(encoding="utf-8").strip().split(
                "  ", maxsplit=1
            )
            self.assertEqual(filename, archive_path.name)
            self.assertEqual(digest, hashlib.sha256(archive_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
