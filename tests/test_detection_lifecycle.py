from __future__ import annotations

from contextlib import redirect_stdout
from datetime import date, timedelta
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from scripts.check_detection_lifecycle import main as check_main
from scripts.detection_lifecycle import (
    DetectionLifecycleError,
    LifecycleRecord,
    assess_lifecycle,
    load_baseline_catalogue,
    load_manifest_records,
    load_policy,
    validate_transitions,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = REPO_ROOT / "catalog" / "detections"
POLICY = REPO_ROOT / "governance" / "policies" / "detection-lifecycle-v1.json"
CATALOGUE = REPO_ROOT / "catalog" / "index.json"


class DetectionLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = load_manifest_records(CATALOG_ROOT)
        cls.manifests = [json.loads(path.read_text()) for path in sorted(CATALOG_ROOT.glob('*/manifest.json'))]
        cls.transitions = load_policy(POLICY)

    def _record(self, **changes: object) -> LifecycleRecord:
        values: dict[str, object] = {
            "detection_id": "MSEC-DET-9000",
            "title": "Synthetic lifecycle record",
            "status": "experimental",
            "created": date(2026, 1, 1),
            "modified": date(2026, 2, 1),
            "review_interval_days": 90,
        }
        values.update(changes)
        return LifecycleRecord(**values)  # type: ignore[arg-type]

    def test_current_manifests_have_exact_review_due_dates(self) -> None:
        as_of = max(date.fromisoformat(item["lifecycle"]["modified"]) for item in self.manifests)
        assessments = assess_lifecycle(self.records, as_of)
        self.assertEqual([item.detection_id for item in assessments], [item["id"] for item in self.manifests])
        for manifest, assessment in zip(self.manifests, assessments, strict=True):
            expected_due = date.fromisoformat(manifest["lifecycle"]["modified"]) + timedelta(days=manifest["lifecycle"]["review_interval_days"])
            self.assertEqual(assessment.review_due, expected_due)
            self.assertEqual(assessment.days_until_due, (expected_due - as_of).days)
            self.assertEqual(assessment.review_state, "current" if expected_due > as_of else "due" if expected_due == as_of else "overdue")

    def test_due_and_overdue_boundaries_are_explicit(self) -> None:
        record = self._record()
        due = assess_lifecycle((record,), date(2026, 5, 2))[0]
        overdue = assess_lifecycle((record,), date(2026, 5, 3))[0]
        self.assertEqual((due.review_state, due.days_until_due), ("due", 0))
        self.assertEqual(
            (overdue.review_state, overdue.days_until_due), ("overdue", -1)
        )

    def test_future_modified_date_fails_closed(self) -> None:
        with self.assertRaisesRegex(DetectionLifecycleError, "after assessment date"):
            assess_lifecycle((self._record(),), date(2026, 1, 31))

    def test_policy_allows_forward_and_deprecation_transitions(self) -> None:
        previous = (self._record(status="experimental"),)
        for status in ("stable", "deprecated"):
            with self.subTest(status=status):
                current = (
                    self._record(status=status, modified=date(2026, 2, 2)),
                )
                validate_transitions(current, previous, self.transitions)

    def test_policy_rejects_backward_transition(self) -> None:
        previous = (self._record(status="stable"),)
        current = (self._record(status="experimental", modified=date(2026, 2, 2)),)
        with self.assertRaisesRegex(DetectionLifecycleError, "is not allowed"):
            validate_transitions(current, previous, self.transitions)

    def test_created_date_is_immutable_and_removed_ids_fail(self) -> None:
        previous = (self._record(),)
        changed = (self._record(created=date(2026, 1, 2)),)
        with self.assertRaisesRegex(DetectionLifecycleError, "created date is immutable"):
            validate_transitions(changed, previous, self.transitions)
        with self.assertRaisesRegex(DetectionLifecycleError, "removed instead of deprecated"):
            validate_transitions((), previous, self.transitions)

    def test_lifecycle_change_requires_modified_date_advance(self) -> None:
        previous = (self._record(),)
        changed = (self._record(status="stable"),)
        with self.assertRaisesRegex(DetectionLifecycleError, "requires a later modified"):
            validate_transitions(changed, previous, self.transitions)

    def test_current_catalogue_is_a_valid_transition_baseline(self) -> None:
        baseline = load_baseline_catalogue(CATALOGUE)
        validate_transitions(self.records, baseline, self.transitions)

    def test_cli_json_and_exit_codes_are_deterministic_with_as_of(self) -> None:
        due_dates = [
            date.fromisoformat(item["lifecycle"]["modified"]) + timedelta(days=item["lifecycle"]["review_interval_days"])
            for item in self.manifests
        ]
        dates = [
            max(date.fromisoformat(item["lifecycle"]["modified"]) for item in self.manifests),
            min(due_dates),
            max(due_dates) + timedelta(days=1),
        ]
        scenarios = []
        for assessment_date in dates:
            counts = {
                "current": sum(due > assessment_date for due in due_dates),
                "due": sum(due == assessment_date for due in due_dates),
                "overdue": sum(due < assessment_date for due in due_dates),
            }
            scenarios.append((assessment_date.isoformat(), 2 if counts["due"] or counts["overdue"] else 0, counts))
        for as_of, expected_exit, expected_counts in scenarios:
            output = StringIO()
            with self.subTest(as_of=as_of), mock.patch(
                "sys.argv",
                ["check_detection_lifecycle.py", "--as-of", as_of, "--json"],
            ), redirect_stdout(output):
                self.assertEqual(check_main(), expected_exit)
                rendered = json.loads(output.getvalue())
                for state, count in expected_counts.items():
                    self.assertEqual(rendered["summary"][state], count)

    def test_baseline_loader_rejects_invalid_date_order(self) -> None:
        source = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        source["detections"][0]["lifecycle"]["created"] = (date.fromisoformat(source["detections"][0]["lifecycle"]["modified"]) + timedelta(days=1)).isoformat()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(DetectionLifecycleError, "after modified"):
                load_baseline_catalogue(path)


if __name__ == "__main__":
    unittest.main()
