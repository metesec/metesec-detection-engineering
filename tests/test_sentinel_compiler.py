from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.sentinel_compiler import (
    SentinelCompilationError,
    compile_profile,
    load_target_profile,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "targets" / "sentinel" / "preview.json"


class SentinelCompilerTests(unittest.TestCase):
    def test_preview_profile_compiles_to_golden_query(self) -> None:
        compiled = compile_profile(REPO_ROOT, PROFILE)

        self.assertEqual(
            [item.detection_id for item in compiled],
            ["MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0004"],
        )
        for item in compiled:
            expected = item.golden.read_text(encoding="utf-8").replace(
                "\r\n", "\n"
            )
            self.assertEqual(item.query, expected)

    def test_profile_rejects_repository_path_traversal(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "preview.json"
            profile.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "target": "microsoft-sentinel",
                        "backend": "kusto",
                        "pipeline": "azure_monitor",
                        "detections": [
                            {
                                "id": "MSEC-DET-0002",
                                "implementation": "../outside.yml",
                                "query_table": "SigninLogs",
                                "golden": "golden.kql",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                SentinelCompilationError, "escapes the repository"
            ):
                load_target_profile(root, profile)

    def test_profile_rejects_unsafe_table_name(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "preview.json"
            profile.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "target": "microsoft-sentinel",
                        "backend": "kusto",
                        "pipeline": "azure_monitor",
                        "detections": [
                            {
                                "id": "MSEC-DET-0002",
                                "implementation": "rule.yml",
                                "query_table": "SigninLogs | take 1",
                                "golden": "golden.kql",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(SentinelCompilationError, "query_table"):
                load_target_profile(root, profile)


if __name__ == "__main__":
    unittest.main()
