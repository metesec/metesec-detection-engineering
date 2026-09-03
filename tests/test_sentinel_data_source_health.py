from __future__ import annotations

import copy
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from scripts.check_sentinel_data_sources import main as check_main
from scripts.sentinel_data_source_health import (
    SentinelDataSourceError,
    assess_data_sources,
    load_contract,
    load_observation,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT = REPO_ROOT / "targets" / "sentinel" / "data-sources.json"
PREVIEW = REPO_ROOT / "targets" / "sentinel" / "preview.json"


class SentinelDataSourceHealthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract_data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.contracts = load_contract(CONTRACT, PREVIEW)

    def _columns(self, source_id: str) -> list[dict[str, str]]:
        source = next(
            item
            for item in self.contract_data["sources"]
            if item["id"] == source_id
        )
        return copy.deepcopy(source["required_columns"])

    def _observation(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "target": "microsoft-sentinel",
            "observed_at": "2026-09-03T12:00:00Z",
            "sources": [
                {
                    "id": "MSEC-SDS-0001",
                    "table": "SigninLogs",
                    "table_exists": True,
                    "latest_event_at": "2026-09-03T11:30:00Z",
                    "columns": self._columns("MSEC-SDS-0001"),
                },
                {
                    "id": "MSEC-SDS-0002",
                    "table": "AuditLogs",
                    "table_exists": True,
                    "latest_event_at": "2026-09-03T11:00:00Z",
                    "columns": self._columns("MSEC-SDS-0002"),
                },
                {
                    "id": "MSEC-SDS-0003",
                    "table": "DeviceProcessEvents",
                    "table_exists": True,
                    "latest_event_at": "2026-09-03T11:45:00Z",
                    "columns": self._columns("MSEC-SDS-0003"),
                },
                {
                    "id": "MSEC-SDS-0004",
                    "table": "AADUserRiskEvents",
                    "table_exists": True,
                    "latest_event_at": "2026-09-03T11:15:00Z",
                    "columns": self._columns("MSEC-SDS-0004"),
                },
                {
                    "id": "MSEC-SDS-0005",
                    "table": "DeviceRegistryEvents",
                    "table_exists": True,
                    "latest_event_at": "2026-09-03T11:50:00Z",
                    "columns": self._columns("MSEC-SDS-0005"),
                },
            ],
        }

    def _assess(self, observation: dict[str, object]):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            path.write_text(json.dumps(observation), encoding="utf-8")
            observed_at, sources = load_observation(path)
            return assess_data_sources(self.contracts, observed_at, sources)

    def test_contract_covers_exact_preview_bindings(self) -> None:
        self.assertEqual(
            [(item.source_id, item.table, item.consumers) for item in self.contracts],
            [
                (
                    "MSEC-SDS-0001",
                    "SigninLogs",
                    ("MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0026"),
                ),
                (
                    "MSEC-SDS-0002",
                    "AuditLogs",
                    (
                        "MSEC-DET-0004",
                        "MSEC-DET-0005",
                        "MSEC-DET-0008",
                        "MSEC-DET-0009",
                        "MSEC-DET-0014",
                        "MSEC-DET-0015",
                        "MSEC-DET-0019",
                        "MSEC-DET-0021",
                        "MSEC-DET-0022",
                    ),
                ),
                (
                    "MSEC-SDS-0003",
                    "DeviceProcessEvents",
                    (
                        "MSEC-DET-0006",
                        "MSEC-DET-0007",
                        "MSEC-DET-0011",
                        "MSEC-DET-0012",
                        "MSEC-DET-0013",
                        "MSEC-DET-0016",
                        "MSEC-DET-0017",
                        "MSEC-DET-0018",
                        "MSEC-DET-0020",
                        "MSEC-DET-0023",
                        "MSEC-DET-0024",
                        "MSEC-DET-0025",
                        "MSEC-DET-0027",
                        "MSEC-DET-0028",
                        "MSEC-DET-0029",
                        "MSEC-DET-0030",
                        "MSEC-DET-0031",
                        "MSEC-DET-0032",
                        "MSEC-DET-0033",
                        "MSEC-DET-0034",
                        "MSEC-DET-0035",
                        "MSEC-DET-0036",
                        "MSEC-DET-0037",
                        "MSEC-DET-0038",
                        "MSEC-DET-0039",
                        "MSEC-DET-0041",
                        "MSEC-DET-0042",
                        "MSEC-DET-0043",
                        "MSEC-DET-0044",
                        "MSEC-DET-0045",
                        "MSEC-DET-0048",
                        "MSEC-DET-0049",
                        "MSEC-DET-0050",
                    ),
                ),
                (
                    "MSEC-SDS-0004",
                    "AADUserRiskEvents",
                    ("MSEC-DET-0010",),
                ),
                (
                    "MSEC-SDS-0005",
                    "DeviceRegistryEvents",
                    ("MSEC-DET-0040", "MSEC-DET-0046", "MSEC-DET-0047"),
                ),
            ],
        )

    def test_complete_fresh_observation_is_ready(self) -> None:
        assessments = self._assess(self._observation())
        self.assertEqual([item.status for item in assessments], ["ready"] * 5)
        self.assertTrue(
            all(item.reasons == ("contract_satisfied",) for item in assessments)
        )

    def test_missing_or_wrong_column_is_degraded(self) -> None:
        observation = self._observation()
        sign_in = observation["sources"][0]
        sign_in["columns"] = [
            column
            for column in sign_in["columns"]
            if column["name"] != "UserPrincipalName"
        ]
        next(
            column
            for column in sign_in["columns"]
            if column["name"] == "UserId"
        )["type"] = "dynamic"

        assessment = self._assess(observation)[0]
        self.assertEqual(assessment.status, "degraded")
        self.assertEqual(assessment.missing_columns, ("UserPrincipalName",))
        self.assertEqual(
            assessment.type_mismatches,
            ("UserId: expected string, got dynamic",),
        )

    def test_stale_source_crosses_degraded_then_unavailable_threshold(self) -> None:
        degraded = self._observation()
        degraded["sources"][0]["latest_event_at"] = "2026-09-03T05:59:59Z"
        self.assertEqual(self._assess(degraded)[0].status, "degraded")

        unavailable = self._observation()
        unavailable["sources"][0]["latest_event_at"] = "2026-09-02T11:59:59Z"
        self.assertEqual(self._assess(unavailable)[0].status, "unavailable")

    def test_missing_table_or_empty_table_is_unavailable(self) -> None:
        observation = self._observation()
        observation["sources"][0].update(
            {"table_exists": False, "latest_event_at": None, "columns": []}
        )
        observation["sources"][1]["latest_event_at"] = None
        assessments = self._assess(observation)
        self.assertEqual(
            [item.reasons[0] for item in assessments[:2]],
            ["table_missing", "no_observed_events"],
        )
        self.assertEqual(
            [item.status for item in assessments[:2]],
            ["unavailable", "unavailable"],
        )

    def test_missing_observation_is_unknown_not_ready(self) -> None:
        observation = self._observation()
        observation["sources"].pop()
        assessments = self._assess(observation)
        self.assertEqual(assessments[-1].status, "unknown")
        self.assertEqual(assessments[-1].reasons, ("observation_missing",))

    def test_future_event_and_unknown_source_fail_closed(self) -> None:
        future = self._observation()
        future["sources"][0]["latest_event_at"] = "2026-09-03T12:00:01Z"
        with self.assertRaisesRegex(SentinelDataSourceError, "in the future"):
            self._assess(future)

        unknown = self._observation()
        unknown["sources"][0]["id"] = "MSEC-SDS-9999"
        with self.assertRaisesRegex(SentinelDataSourceError, "unknown sources"):
            self._assess(unknown)

    def test_cli_exit_codes_distinguish_ready_from_unknown(self) -> None:
        observations = [
            (self._observation(), 0, ["ready"] * 5),
            (
                {
                    **self._observation(),
                    "sources": self._observation()["sources"][:1],
                },
                2,
                ["ready", "unknown", "unknown", "unknown", "unknown"],
            ),
        ]
        with TemporaryDirectory() as directory:
            for index, (observation, expected_exit, expected_states) in enumerate(
                observations
            ):
                path = Path(directory) / f"observation-{index}.json"
                path.write_text(json.dumps(observation), encoding="utf-8")
                output = StringIO()
                with self.subTest(expected_exit=expected_exit), mock.patch(
                    "sys.argv",
                    ["check_sentinel_data_sources.py", "--observation", str(path), "--json"],
                ), redirect_stdout(output):
                    self.assertEqual(check_main(), expected_exit)
                    rendered = json.loads(output.getvalue())
                    self.assertEqual(
                        [item["status"] for item in rendered["assessments"]],
                        expected_states,
                    )


if __name__ == "__main__":
    unittest.main()
