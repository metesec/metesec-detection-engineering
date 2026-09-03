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
    "MSEC-DET-0021",
    "MSEC-DET-0022",
    "MSEC-DET-0023",
    "MSEC-DET-0024",
    "MSEC-DET-0025",
    "MSEC-DET-0026",
    "MSEC-DET-0027",
    "MSEC-DET-0028",
    "MSEC-DET-0029",
    "MSEC-DET-0030",
    "MSEC-DET-0031",
    "MSEC-DET-0032",
    "MSEC-DET-0033",
    "MSEC-DET-0034",
    "MSEC-DET-0035",
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
    "MSEC-DET-0011": "fb53221b-1f90-5e11-88e0-546644d2b40d",
    "MSEC-DET-0012": "9217df00-bcf9-5728-a1d7-e7cfc105fc47",
    "MSEC-DET-0013": "927ef83f-8be3-57e8-a3df-823c7bf58fa2",
    "MSEC-DET-0014": "ae998d96-08ea-5450-b11c-90e22f12617e",
    "MSEC-DET-0015": "1744748d-113d-55e9-9e16-d3e5da54bef0",
    "MSEC-DET-0016": "97ff01f7-43f9-5fba-9790-4eb49f30f006",
    "MSEC-DET-0017": "b1f2169b-f1b7-5b26-8cca-645aca9aea9b",
    "MSEC-DET-0018": "f8e1357b-e280-5024-b0d8-a585a276d485",
    "MSEC-DET-0019": "6b550a1b-fcdd-5357-848f-31fd31820c25",
    "MSEC-DET-0020": "69c1dc01-b17a-5ed3-b893-03ac105ec17c",
    "MSEC-DET-0021": "553e034a-3152-52eb-aebe-3a8a26d812cd",
    "MSEC-DET-0022": "5a54ab68-a6c6-5861-9999-2d5bcae69bcb",
    "MSEC-DET-0023": "93340f83-dceb-5590-ac68-1b090933d5f0",
    "MSEC-DET-0024": "b78540d6-f5f8-5ef4-836f-4b22e7fa2aa4",
    "MSEC-DET-0025": "65d7aaa9-403b-5fe1-8ee0-5ae1d796ebfa",
    "MSEC-DET-0026": "6922469a-cd13-5831-a7e6-cf094a4df4b3",
    "MSEC-DET-0027": "d4d1ef61-099b-555b-8ede-8ac59397a859",
    "MSEC-DET-0028": "4d1f6ff8-728a-5b8c-9e0f-afee0a5ea803",
    "MSEC-DET-0029": "5a58ba42-f707-5c18-97e4-3fd52be8772c",
    "MSEC-DET-0030": "0574fb14-9e43-53d5-8651-775cabebf006",
    "MSEC-DET-0031": "847b9e91-09cf-5fed-83e5-82dfb9d48286",
    "MSEC-DET-0032": "f035bc04-83d7-5fea-be4a-acbcc0ae9f7e",
    "MSEC-DET-0033": "40b747a2-7eca-5be7-9db9-a9ad96a92f6b",
    "MSEC-DET-0034": "e97b2c50-09f7-56cd-a4c7-7b592653fdae",
    "MSEC-DET-0035": "bf9bf449-c952-50c6-9494-89bc93024ceb",
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
AUDIT_INITIATOR_ENTITY_MAPPINGS = AUDIT_ENTITY_MAPPINGS[:3]


class SentinelRuleRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = render_profile(REPO_ROOT, PROFILE)

    def test_current_profile_renders_thirty_four_disabled_scheduled_rules(self) -> None:
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
            "MSEC-DET-0011": ("High", ["CredentialAccess"], ["T1003"]),
            "MSEC-DET-0012": ("High", ["DefenseEvasion"], ["T1218"]),
            "MSEC-DET-0013": ("Medium", ["DefenseEvasion"], ["T1218"]),
            "MSEC-DET-0014": ("Medium", ["DefenseEvasion"], ["T1556"]),
            "MSEC-DET-0015": ("Medium", ["PrivilegeEscalation"], ["T1098"]),
            "MSEC-DET-0016": ("High", ["Impact"], ["T1490"]),
            "MSEC-DET-0017": ("High", [], ["T1685"]),
            "MSEC-DET-0018": ("High", [], ["T1685"]),
            "MSEC-DET-0019": ("High", ["PrivilegeEscalation"], ["T1484"]),
            "MSEC-DET-0020": ("Medium", ["CommandAndControl"], ["T1105"]),
            "MSEC-DET-0021": ("High", ["Persistence", "PrivilegeEscalation"], ["T1098"]),
            "MSEC-DET-0022": ("Medium", ["Persistence", "CredentialAccess"], ["T1556"]),
            "MSEC-DET-0023": ("High", ["CredentialAccess"], ["T1003"]),
            "MSEC-DET-0024": ("Medium", ["Execution"], ["T1047"]),
            "MSEC-DET-0025": ("Medium", ["Persistence", "Execution"], ["T1197"]),
            "MSEC-DET-0026": ("Medium", ["InitialAccess"], ["T1078"]),
            "MSEC-DET-0027": ("High", [], ["T1218"]),
            "MSEC-DET-0028": (
                "Medium",
                ["Execution", "Persistence", "PrivilegeEscalation"],
                ["T1053"],
            ),
            "MSEC-DET-0029": (
                "High",
                ["Persistence", "PrivilegeEscalation"],
                ["T1098"],
            ),
            "MSEC-DET-0030": ("High", ["CredentialAccess"], ["T1003"]),
            "MSEC-DET-0031": ("High", ["Persistence"], ["T1505"]),
            "MSEC-DET-0032": ("High", [], ["T1685"]),
            "MSEC-DET-0033": ("High", [], ["T1686"]),
            "MSEC-DET-0034": (
                "High",
                ["Persistence", "PrivilegeEscalation"],
                ["T1543"],
            ),
            "MSEC-DET-0035": ("Medium", [], ["T1140"]),
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
                "MSEC-DET-0011": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0012": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0013": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0014": AUDIT_INITIATOR_ENTITY_MAPPINGS,
                "MSEC-DET-0015": AUDIT_INITIATOR_ENTITY_MAPPINGS,
                "MSEC-DET-0016": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0017": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0018": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0019": AUDIT_INITIATOR_ENTITY_MAPPINGS,
                "MSEC-DET-0020": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0021": AUDIT_ENTITY_MAPPINGS,
                "MSEC-DET-0022": AUDIT_ACCOUNT_ENTITY_MAPPINGS,
                "MSEC-DET-0023": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0024": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0025": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0026": SIGNIN_ENTITY_MAPPINGS,
                "MSEC-DET-0027": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0028": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0029": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0030": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0031": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0032": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0033": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0034": DEVICE_ENTITY_MAPPINGS,
                "MSEC-DET-0035": DEVICE_ENTITY_MAPPINGS,
            }[item.detection_id]
            properties = item.request_body["properties"]
            self.assertEqual(properties["entityMappings"], expected)
            self.assertEqual(item.render_manifest["source"]["entity_mappings"], expected)
            output_columns = set(item.render_manifest["source"]["output_columns"])
            for mapping in expected:
                for field in mapping["fieldMappings"]:
                    self.assertIn(field["columnName"], output_columns)

    def test_owner_change_target_remains_a_neutral_resource(self) -> None:
        owner_change = next(
            item for item in self.rendered if item.detection_id == "MSEC-DET-0015"
        )
        output_columns = set(owner_change.render_manifest["source"]["output_columns"])
        self.assertTrue(
            {"TargetResourceType", "TargetResourceId", "TargetResourceName"}
            <= output_columns
        )
        self.assertNotIn("TargetApplicationName", owner_change.query)
        self.assertEqual(
            owner_change.request_body["properties"]["entityMappings"],
            AUDIT_INITIATOR_ENTITY_MAPPINGS,
        )

    def test_current_attack_tactic_is_not_mislabeled_for_older_sentinel_enum(self) -> None:
        defense_impairment = {
            item.detection_id: item
            for item in self.rendered
            if item.detection_id in {"MSEC-DET-0017", "MSEC-DET-0018", "MSEC-DET-0019"}
        }
        self.assertEqual(
            defense_impairment["MSEC-DET-0017"].request_body["properties"]["tactics"],
            [],
        )
        self.assertEqual(
            defense_impairment["MSEC-DET-0018"].request_body["properties"]["tactics"],
            [],
        )
        self.assertEqual(
            defense_impairment["MSEC-DET-0019"].request_body["properties"]["tactics"],
            ["PrivilegeEscalation"],
        )
        for item in defense_impairment.values():
            source_tactics = {
                mapping["tactic"]
                for mapping in item.render_manifest["source"]["attack"]
            }
            self.assertIn("Defense Impairment", source_tactics)
            self.assertNotIn("DefenseEvasion", item.request_body["properties"]["tactics"])

        bits = next(
            item for item in self.rendered if item.detection_id == "MSEC-DET-0025"
        )
        self.assertEqual(
            bits.request_body["properties"]["tactics"],
            ["Persistence", "Execution"],
        )
        source_tactics = {
            mapping["tactic"] for mapping in bits.render_manifest["source"]["attack"]
        }
        self.assertIn("Stealth", source_tactics)
        self.assertNotIn("DefenseEvasion", bits.request_body["properties"]["tactics"])

        rundll32_mshtml = next(
            item for item in self.rendered if item.detection_id == "MSEC-DET-0027"
        )
        self.assertEqual(
            rundll32_mshtml.request_body["properties"]["tactics"],
            [],
        )
        source_tactics = {
            mapping["tactic"]
            for mapping in rundll32_mshtml.render_manifest["source"]["attack"]
        }
        self.assertIn("Stealth", source_tactics)
        self.assertNotIn(
            "DefenseEvasion",
            rundll32_mshtml.request_body["properties"]["tactics"],
        )

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
