from __future__ import annotations

import copy
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from scripts.check_sentinel_runtime_health import main as check_main
from scripts.sentinel_runtime_health import (
    SentinelRuntimeHealthError,
    assess_runtime_health,
    load_expectations,
    load_observation,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY = REPO_ROOT / "governance" / "policies" / "sentinel-runtime-health-v1.json"


class SentinelRuntimeHealthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy, cls.expectations = load_expectations(REPO_ROOT, POLICY)

    def _observation(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "target": "microsoft-sentinel",
            "observed_at": "2026-09-03T12:00:00Z",
            "rules": [
                {
                    "id": "MSEC-DET-0002",
                    "rule_exists": True,
                    "enabled": True,
                    "last_execution_at": "2026-09-03T11:30:00Z",
                    "last_execution_status": "succeeded",
                    "alert_outcome": {
                        "window_start": "2026-09-03T11:00:00Z",
                        "window_end": "2026-09-03T12:00:00Z",
                        "alerts_created": 0,
                        "incidents_created": 0,
                    },
                },
                *[
                    {
                        "id": detection_id,
                        "rule_exists": True,
                        "enabled": True,
                        "last_execution_at": "2026-09-03T11:59:00Z",
                        "last_execution_status": "succeeded",
                        "alert_outcome": {
                            "window_start": "2026-09-03T11:00:00Z",
                            "window_end": "2026-09-03T12:00:00Z",
                            "alerts_created": 0,
                            "incidents_created": 0,
                        },
                    }
                    for detection_id in (
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
                    )
                ],
            ],
        }

    def _assess(self, observation: dict[str, object]):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            path.write_text(json.dumps(observation), encoding="utf-8")
            observed_at, observations = load_observation(path)
            return assess_runtime_health(
                self.policy, self.expectations, observed_at, observations
            )

    def test_expectations_come_from_exact_sentinel_schedule(self) -> None:
        self.assertEqual(
            [
                (item.detection_id, item.query_frequency)
                for item in self.expectations
            ],
            [
                ("MSEC-DET-0002", "PT1H"),
                ("MSEC-DET-0003", "PT5M"),
                ("MSEC-DET-0004", "PT5M"),
                ("MSEC-DET-0005", "PT5M"),
                ("MSEC-DET-0006", "PT5M"),
                ("MSEC-DET-0007", "PT5M"),
                ("MSEC-DET-0008", "PT5M"),
                ("MSEC-DET-0009", "PT5M"),
                ("MSEC-DET-0010", "PT5M"),
                ("MSEC-DET-0011", "PT5M"),
                ("MSEC-DET-0012", "PT5M"),
                ("MSEC-DET-0013", "PT5M"),
                ("MSEC-DET-0014", "PT5M"),
                ("MSEC-DET-0015", "PT5M"),
                ("MSEC-DET-0016", "PT5M"),
                ("MSEC-DET-0017", "PT5M"),
                ("MSEC-DET-0018", "PT5M"),
                ("MSEC-DET-0019", "PT5M"),
                ("MSEC-DET-0020", "PT5M"),
                ("MSEC-DET-0021", "PT5M"),
                ("MSEC-DET-0022", "PT5M"),
                ("MSEC-DET-0023", "PT5M"),
                ("MSEC-DET-0024", "PT5M"),
                ("MSEC-DET-0025", "PT5M"),
            ],
        )

    def test_fresh_successful_rules_are_healthy_even_with_zero_alerts(self) -> None:
        assessments = self._assess(self._observation())
        self.assertEqual([item.status for item in assessments], ["healthy"] * 24)
        self.assertTrue(
            all(item.reasons == ("execution_healthy",) for item in assessments)
        )
        self.assertTrue(
            all(item.alert_outcome is not None for item in assessments)
        )
        self.assertTrue(
            all(item.alert_outcome.alerts_created == 0 for item in assessments)
        )

    def test_missing_observation_is_unknown(self) -> None:
        observation = self._observation()
        observation["rules"].pop()
        assessment = self._assess(observation)[-1]
        self.assertEqual(assessment.status, "unknown")
        self.assertEqual(assessment.reasons, ("observation_missing",))

    def test_missing_rule_is_failed(self) -> None:
        observation = self._observation()
        observation["rules"][0].update(
            {
                "rule_exists": False,
                "enabled": None,
                "last_execution_at": None,
                "last_execution_status": "unknown",
                "alert_outcome": None,
            }
        )
        assessment = self._assess(observation)[0]
        self.assertEqual(assessment.status, "failed")
        self.assertEqual(assessment.reasons, ("rule_missing",))

    def test_disabled_rule_is_degraded(self) -> None:
        observation = self._observation()
        observation["rules"][1]["enabled"] = False
        assessment = self._assess(observation)[1]
        self.assertEqual(assessment.status, "degraded")
        self.assertEqual(assessment.reasons, ("rule_disabled",))

    def test_failed_execution_is_failed(self) -> None:
        observation = self._observation()
        observation["rules"][2]["last_execution_status"] = "failed"
        assessment = self._assess(observation)[2]
        self.assertEqual(assessment.status, "failed")
        self.assertEqual(assessment.reasons, ("execution_failed",))

    def test_missing_or_unknown_execution_evidence_is_unknown(self) -> None:
        missing = self._observation()
        missing["rules"][1].update(
            {
                "last_execution_at": None,
                "last_execution_status": "unknown",
                "alert_outcome": None,
            }
        )
        missing_assessment = self._assess(missing)[1]
        self.assertEqual(missing_assessment.status, "unknown")
        self.assertEqual(
            missing_assessment.reasons,
            ("execution_missing", "execution_status_unknown"),
        )

        unknown = self._observation()
        unknown["rules"][1]["last_execution_status"] = "unknown"
        unknown_assessment = self._assess(unknown)[1]
        self.assertEqual(unknown_assessment.status, "unknown")
        self.assertEqual(
            unknown_assessment.reasons,
            ("execution_status_unknown",),
        )

    def test_five_minute_rule_crosses_late_then_stale_boundaries(self) -> None:
        late = self._observation()
        late["rules"][1]["last_execution_at"] = "2026-09-03T11:49:59Z"
        late_assessment = self._assess(late)[1]
        self.assertEqual(late_assessment.status, "degraded")
        self.assertEqual(late_assessment.reasons, ("execution_late",))

        stale = self._observation()
        stale["rules"][1]["last_execution_at"] = "2026-09-03T11:34:59Z"
        stale_assessment = self._assess(stale)[1]
        self.assertEqual(stale_assessment.status, "failed")
        self.assertEqual(stale_assessment.reasons, ("execution_stale",))

    def test_invalid_times_and_unknown_rules_fail_closed(self) -> None:
        future = self._observation()
        future["rules"][0]["last_execution_at"] = "2026-09-03T12:00:01Z"
        with self.assertRaisesRegex(SentinelRuntimeHealthError, "in the future"):
            self._assess(future)

        invalid_window = self._observation()
        invalid_window["rules"][0]["alert_outcome"]["window_end"] = (
            "2026-09-03T12:00:01Z"
        )
        with self.assertRaisesRegex(SentinelRuntimeHealthError, "after observed_at"):
            self._assess(invalid_window)

        unknown = self._observation()
        unknown["rules"][0]["id"] = "MSEC-DET-9999"
        with self.assertRaisesRegex(SentinelRuntimeHealthError, "unknown rules"):
            self._assess(unknown)

    def test_cli_distinguishes_healthy_from_nonhealthy(self) -> None:
        observations = [
            (self._observation(), 0, {"healthy": 24, "unknown": 0}),
            (
                {
                    **self._observation(),
                    "rules": copy.deepcopy(self._observation()["rules"][:-1]),
                },
                2,
                {"healthy": 23, "unknown": 1},
            ),
        ]
        with TemporaryDirectory() as directory:
            for index, (observation, expected_exit, expected_summary) in enumerate(
                observations
            ):
                path = Path(directory) / f"observation-{index}.json"
                path.write_text(json.dumps(observation), encoding="utf-8")
                output = StringIO()
                with self.subTest(expected_exit=expected_exit), mock.patch(
                    "sys.argv",
                    [
                        "check_sentinel_runtime_health.py",
                        "--observation",
                        str(path),
                        "--json",
                    ],
                ), redirect_stdout(output):
                    self.assertEqual(check_main(), expected_exit)
                    rendered = json.loads(output.getvalue())
                    for key, value in expected_summary.items():
                        self.assertEqual(rendered["summary"][key], value)


if __name__ == "__main__":
    unittest.main()
