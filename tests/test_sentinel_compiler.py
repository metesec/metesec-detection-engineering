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
            [
                "MSEC-DET-0002",
                "MSEC-DET-0003",
                "MSEC-DET-0004",
                "MSEC-DET-0005",
                "MSEC-DET-0006",
                "MSEC-DET-0007",
                "MSEC-DET-0008",
                "MSEC-DET-0009",
                "MSEC-DET-0010",
                "MSEC-DET-0011",
                "MSEC-DET-0012",
                "MSEC-DET-0013",
                "MSEC-DET-0014",
                "MSEC-DET-0015",
                "MSEC-DET-0016",
                "MSEC-DET-0017",
                "MSEC-DET-0018",
                "MSEC-DET-0019",
                "MSEC-DET-0020",
            ],
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
                        "schema_version": 2,
                        "target": "microsoft-sentinel",
                        "backend": "kusto",
                        "pipeline": "azure_monitor",
                        "detections": [
                            {
                                "id": "MSEC-DET-0002",
                                "implementation": "../outside.yml",
                                "query_table": "SigninLogs",
                                "golden": "golden.kql",
                                "output": {
                                    "extend": [],
                                    "columns": ["TimeGenerated"],
                                    "entity_mappings": [],
                                },
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
                        "schema_version": 2,
                        "target": "microsoft-sentinel",
                        "backend": "kusto",
                        "pipeline": "azure_monitor",
                        "detections": [
                            {
                                "id": "MSEC-DET-0002",
                                "implementation": "rule.yml",
                                "query_table": "SigninLogs | take 1",
                                "golden": "golden.kql",
                                "output": {
                                    "extend": [],
                                    "columns": ["TimeGenerated"],
                                    "entity_mappings": [],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(SentinelCompilationError, "query_table"):
                load_target_profile(root, profile)

    def test_profile_rejects_entity_mapping_outside_output_contract(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        profile["detections"][0]["output"]["entity_mappings"][0][
            "field_mappings"
        ][0]["column"] = "UndeclaredColumn"

        with TemporaryDirectory() as directory:
            path = Path(directory) / "preview.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            with self.assertRaisesRegex(
                SentinelCompilationError,
                "not a declared output column",
            ):
                load_target_profile(REPO_ROOT, path)

    def test_profile_rejects_unbounded_output_expression(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        profile["detections"][0]["output"]["extend"][0][
            "expression"
        ] = "tostring(UserPrincipalName) | take 1"

        with TemporaryDirectory() as directory:
            path = Path(directory) / "preview.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            with self.assertRaisesRegex(
                SentinelCompilationError,
                "one bounded KQL expression",
            ):
                load_target_profile(REPO_ROOT, path)


if __name__ == "__main__":
    unittest.main()
