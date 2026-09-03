from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from scripts.sentinel_compiler import CompiledSentinelQuery, compile_profile as compile_queries
from scripts.sentinel_rule_renderer import (
    SENTINEL_API_VERSION,
    SENTINEL_RESOURCE_TYPE,
    SentinelRuleRenderError,
    load_rule_settings,
    render_profile,
    write_rendered_rules,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "targets" / "sentinel" / "analytics-rules.json"
EXPECTED_IDS = [
    "MSEC-DET-0002",
    "MSEC-DET-0003",
    "MSEC-DET-0004",
    "MSEC-DET-0005",
    "MSEC-DET-0006",
    "MSEC-DET-0007",
    "MSEC-DET-0008",
    "MSEC-DET-0009",
    "MSEC-DET-0010",
]
EXPECTED_RULE_IDS = {
    "MSEC-DET-0002": "249adb3e-5bd1-5348-82ba-00a0ade97c7d",
    "MSEC-DET-0003": "f336023f-4aa7-582e-99f5-da072f591623",
    "MSEC-DET-0004": "014e057f-ad92-56c5-801f-0e3f00689d90",
    "MSEC-DET-0005": "395d6ea0-0706-511c-878b-e430c44f8c55",
    "MSEC-DET-0006": "d93b2104-9ec4-514e-bfe9-7b5c8a61a58e",
    "MSEC-DET-0007": "946f440a-507f-5d6d-b8aa-16242f00c4cd",
    "MSEC-DET-0008": "e6278947-b6ee-55ec-b967-c70b930158b0",
    "MSEC-DET-0009": "f2d6f91c-fd6e-5a33-9912-853e8f438c10",
    "MSEC-DET-0010": "7ff5a2bc-a328-5335-9e16-d5554513fe83",
}
SIGNIN_ENTITY_MAPPINGS = [
    {
        "entityType": "Account",
        "fieldMappings": [
            {"identifier": "Name", "columnName": "AccountName"},
            {"identifier": "UPNSuffix", "columnName": "AccountUPNSuffix"},
            {"identifier": "AadUserId", "columnName": "UserId"},
        ],
    },
    {
        "entityType": "IP",
        "fieldMappings": [
            {"identifier": "Address", "columnName": "SourceIPAddress"},
        ],
    },
    {
        "entityType": "CloudApplication",
        "fieldMappings": [
            {"identifier": "AppId", "columnName": "ApplicationId"},
            {"identifier": "Name", "columnName": "ApplicationName"},
        ],
    },
]
AUDIT_ENTITY_MAPPINGS = [
    {
        "entityType": "Account",
        "fieldMappings": [
            {"identifier": "Name", "columnName": "InitiatingAccountName"},
            {
                "identifier": "UPNSuffix",
                "columnName": "InitiatingAccountUPNSuffix",
            },
            {"identifier": "AadUserId", "columnName": "InitiatingUserId"},
        ],
    },
    {
        "entityType": "IP",
        "fieldMappings": [
            {"identifier": "Address", "columnName": "InitiatingIPAddress"},
        ],
    },
    {
        "entityType": "CloudApplication",
        "fieldMappings": [
            {"identifier": "AppId", "columnName": "InitiatingApplicationId"},
            {"identifier": "Name", "columnName": "InitiatingApplicationName"},
        ],
    },
    {
        "entityType": "CloudApplication",
        "fieldMappings": [
            {"identifier": "Name", "columnName": "TargetServicePrincipalName"},
        ],
    },
]
DEVICE_ENTITY_MAPPINGS = [
    {
        "entityType": "Account",
        "fieldMappings": [
            {"identifier": "Name", "columnName": "AccountName"},
        ],
    },
]
AUDIT_ACCOUNT_ENTITY_MAPPINGS = [
    *AUDIT_ENTITY_MAPPINGS[:3],
    {
        "entityType": "Account",
        "fieldMappings": [
            {"identifier": "AadUserId", "columnName": "TargetObjectId"},
        ],
    },
]
RISK_ENTITY_MAPPINGS = [
    {
        "entityType": "Account",
        "fieldMappings": [
            {"identifier": "Name", "columnName": "AccountName"},
            {"identifier": "UPNSuffix", "columnName": "AccountUPNSuffix"},
            {"identifier": "AadUserId", "columnName": "UserId"},
        ],
    },
]


class SentinelRuleRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = render_profile(REPO_ROOT, PROFILE)

    def test_current_profile_renders_nine_disabled_scheduled_rules(self) -> None:
        self.assertEqual(
            [item.detection_id for item in self.rendered],
            EXPECTED_IDS,
        )
        self.assertEqual(
            {item.detection_id: item.rule_id for item in self.rendered},
            EXPECTED_RULE_IDS,
        )
        for item in self.rendered:
            self.assertEqual(set(item.request_body), {"kind", "properties"})
            self.assertEqual(item.request_body["kind"], "Scheduled")
            properties = item.request_body["properties"]
            self.assertIsInstance(properties, dict)
            self.assertFalse(properties["enabled"])
            self.assertFalse(properties["suppressionEnabled"])
            self.assertEqual(properties["triggerOperator"], "GreaterThan")
            self.assertEqual(properties["triggerThreshold"], 0)
            self.assertEqual(
                properties["eventGroupingSettings"],
                {"aggregationKind": "AlertPerResult"},
            )
            self.assertTrue(properties["incidentConfiguration"]["createIncident"])

    def test_manifest_metadata_and_attack_mapping_are_deterministic(self) -> None:
        expected = {
            "MSEC-DET-0002": ("Medium", ["InitialAccess"], ["T1078"]),
            "MSEC-DET-0003": ("High", ["InitialAccess"], ["T1078"]),
            "MSEC-DET-0004": ("High", ["Persistence"], ["T1098"]),
            "MSEC-DET-0005": ("Medium", ["PrivilegeEscalation"], ["T1098"]),
            "MSEC-DET-0006": ("High", ["Execution"], ["T1059"]),
            "MSEC-DET-0007": ("High", ["Execution"], ["T1059"]),
            "MSEC-DET-0008": ("High", ["PrivilegeEscalation"], ["T1098"]),
            "MSEC-DET-0009": ("Medium", ["Persistence"], ["T1098"]),
            "MSEC-DET-0010": ("High", ["InitialAccess"], ["T1078"]),
        }
        for item in self.rendered:
            properties = item.request_body["properties"]
            severity, tactics, techniques = expected[item.detection_id]
            self.assertEqual(properties["severity"], severity)
            self.assertEqual(properties["tactics"], tactics)
            self.assertEqual(properties["techniques"], techniques)
            self.assertNotIn("subscription", item.request_body_text().lower())
            self.assertNotIn("workspace", item.request_body_text().lower())
            self.assertNotIn("tenant", item.request_body_text().lower())

    def test_rendered_query_is_the_reviewed_golden_query(self) -> None:
        for item in self.rendered:
            golden = (
                REPO_ROOT
                / "tests"
                / "golden"
                / "sentinel"
                / f"{item.detection_id}.kql"
            ).read_text(encoding="utf-8").replace("\r\n", "\n")
            self.assertEqual(item.query, golden)
            self.assertEqual(item.request_body["properties"]["query"], golden)

    def test_output_columns_drive_exact_entity_mappings(self) -> None:
        for item in self.rendered:
            expected = {
                "MSEC-DET-0002": SIGNIN_ENTITY_MAPPINGS,
                "MSEC-DET-0003": SIGNIN_ENTITY_MAPPINGS,
                "MSEC-DET-0004": AUDIT_ENTITY_MAPPINGS,
                "MSEC-DET-0005": AUDIT_ENTITY_MAPPINGS,
                "MSEC-DET-0006": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0007": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0008": AUDIT_ACCOUNT_ENTITY_MAPPINGS,
                "MSEC-DET-0009": AUDIT_ACCOUNT_ENTITY_MAPPINGS,
                "MSEC-DET-0010": RISK_ENTITY_MAPPINGS,
            }[item.detection_id]
            properties = item.request_body["properties"]
            self.assertEqual(properties["entityMappings"], expected)
            self.assertEqual(item.render_manifest["source"]["entity_mappings"], expected)
            output_columns = set(item.render_manifest["source"]["output_columns"])
            for mapping in expected:
                for field in mapping["fieldMappings"]:
                    self.assertIn(field["columnName"], output_columns)

    def test_renderer_rejects_query_that_differs_from_golden(self) -> None:
        source_profile = REPO_ROOT / "targets" / "sentinel" / "preview.json"
        compiled = compile_queries(REPO_ROOT, source_profile)
        changed = [
            CompiledSentinelQuery(
                detection_id=compiled[0].detection_id,
                query=compiled[0].query + "// unreviewed change\n",
                golden=compiled[0].golden,
            ),
            *compiled[1:],
        ]

        with mock.patch(
            "scripts.sentinel_rule_renderer.compile_profile",
            return_value=changed,
        ):
            with self.assertRaisesRegex(
                SentinelRuleRenderError,
                "differs from the reviewed Golden query",
            ):
                render_profile(REPO_ROOT, PROFILE)

    def test_render_manifest_hashes_both_generated_artifacts(self) -> None:
        for item in self.rendered:
            manifest = item.render_manifest
            self.assertEqual(manifest["api_version"], SENTINEL_API_VERSION)
            self.assertEqual(manifest["resource_type"], SENTINEL_RESOURCE_TYPE)
            self.assertEqual(manifest["rule_id"], item.rule_id)
            self.assertEqual(
                manifest["artifacts"]["analytics_rule"]["sha256"],
                hashlib.sha256(item.request_body_text().encode("utf-8")).hexdigest(),
            )
            self.assertEqual(
                manifest["artifacts"]["query"]["sha256"],
                hashlib.sha256(item.query.encode("utf-8")).hexdigest(),
            )
            self.assertEqual(
                manifest["deployment"],
                {"implemented": False, "enabled": False},
            )

    def test_two_writes_are_byte_identical_and_complete(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            write_rendered_rules(self.rendered, first)
            write_rendered_rules(render_profile(REPO_ROOT, PROFILE), second)
            for item in self.rendered:
                for filename in (
                    "query.kql",
                    "analytics-rule.json",
                    "render-manifest.json",
                ):
                    first_bytes = (first / item.detection_id / filename).read_bytes()
                    second_bytes = (second / item.detection_id / filename).read_bytes()
                    self.assertEqual(first_bytes, second_bytes)
                    if filename.endswith(".json"):
                        json.loads(first_bytes)

    def test_profile_rejects_enabled_rule(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        profile["rules"][0]["enabled"] = True
        with TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            with self.assertRaisesRegex(SentinelRuleRenderError, "enabled must remain false"):
                load_rule_settings(REPO_ROOT, path, EXPECTED_IDS)

    def test_profile_rejects_duplicate_or_missing_binding(self) -> None:
        original = json.loads(PROFILE.read_text(encoding="utf-8"))
        variants = []
        duplicate = copy.deepcopy(original)
        duplicate["rules"][1]["id"] = duplicate["rules"][0]["id"]
        variants.append((duplicate, "duplicated"))
        missing = copy.deepcopy(original)
        missing["rules"].pop()
        variants.append((missing, "must exactly match"))

        with TemporaryDirectory() as directory:
            for index, (profile, message) in enumerate(variants):
                path = Path(directory) / f"profile-{index}.json"
                path.write_text(json.dumps(profile), encoding="utf-8")
                with self.subTest(message=message):
                    if message == "duplicated":
                        with self.assertRaisesRegex(SentinelRuleRenderError, message):
                            load_rule_settings(REPO_ROOT, path, EXPECTED_IDS)
                    else:
                        with self.assertRaisesRegex(SentinelRuleRenderError, message):
                            render_profile(REPO_ROOT, path)

    def test_profile_rejects_source_change_and_invalid_duration(self) -> None:
        original = json.loads(PROFILE.read_text(encoding="utf-8"))
        path_escape = copy.deepcopy(original)
        path_escape["source_profile"] = "../outside.json"
        bad_duration = copy.deepcopy(original)
        bad_duration["rules"][0]["query_frequency"] = "one hour"
        empty_time_duration = copy.deepcopy(original)
        empty_time_duration["rules"][0]["query_frequency"] = "P1DT"

        with TemporaryDirectory() as directory:
            for index, (profile, message) in enumerate(
                (
                    (path_escape, "source_profile must equal"),
                    (bad_duration, "ISO 8601"),
                    (empty_time_duration, "ISO 8601"),
                )
            ):
                path = Path(directory) / f"profile-{index}.json"
                path.write_text(json.dumps(profile), encoding="utf-8")
                with self.subTest(message=message):
                    with self.assertRaisesRegex(SentinelRuleRenderError, message):
                        load_rule_settings(REPO_ROOT, path, EXPECTED_IDS)


if __name__ == "__main__":
    unittest.main()
