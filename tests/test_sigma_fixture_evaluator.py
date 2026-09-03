from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.sigma_fixture_evaluator import (
    LocalEvaluationError,
    UnsupportedSigmaFeature,
    evaluate_rule,
    load_single_rule,
    run_fixture_set,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DETECTION_ROOT = REPO_ROOT / "content" / "portable" / "sigma" / "MSEC-DET-0001"


KEYWORD_RULE = """\
title: Unsupported keyword rule
id: 00000000-0000-4000-8000-000000000003
status: test
description: Synthetic unsupported evaluator input.
author: MeteSec
date: 2026-09-03
logsource:
  product: windows
detection:
  keywords:
    - suspicious phrase
  condition: keywords
falsepositives:
  - Synthetic test input only.
level: low
"""

NOT_RULE = """\
title: Supported negation rule
id: 00000000-0000-4000-8000-000000000004
status: test
description: Synthetic negation evaluator input.
author: MeteSec
date: 2026-09-03
logsource:
  product: windows
detection:
  selection:
    EventID: 7045
  filter:
    ImagePath|contains: '\\Program Files\\'
  condition: selection and not filter
falsepositives:
  - Synthetic test input only.
level: low
"""


class SigmaFixtureEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rule = load_single_rule(DETECTION_ROOT / "rule.yml")

    def test_real_fixture_set_passes_all_declared_expectations(self) -> None:
        outcomes = run_fixture_set(REPO_ROOT, DETECTION_ROOT / "tests" / "cases.json")

        self.assertEqual(len(outcomes), 7)
        self.assertEqual(sum(outcome.expectation == "match" for outcome in outcomes), 3)
        self.assertEqual(sum(outcome.expectation == "no_match" for outcome in outcomes), 4)
        self.assertTrue(all(outcome.passed for outcome in outcomes))

    def test_matching_is_case_insensitive(self) -> None:
        event = {
            "Provider_Name": "service control manager",
            "EventID": 7045,
            "ImagePath": "C:\\WINDOWS\\TEMP\\probe.exe",
        }

        self.assertTrue(evaluate_rule(self.rule, event))

    def test_missing_required_rule_field_does_not_match(self) -> None:
        event = {
            "Provider_Name": "Service Control Manager",
            "EventID": 7045,
        }

        self.assertFalse(evaluate_rule(self.rule, event))

    def test_unsupported_keyword_expression_fails_closed(self) -> None:
        with TemporaryDirectory() as temp_directory:
            rule_path = Path(temp_directory) / "rule.yml"
            rule_path.write_text(KEYWORD_RULE, encoding="utf-8")

            with self.assertRaisesRegex(UnsupportedSigmaFeature, "outside the local evaluator subset"):
                load_single_rule(rule_path)

    def test_unary_not_is_evaluated(self) -> None:
        with TemporaryDirectory() as temp_directory:
            rule_path = Path(temp_directory) / "rule.yml"
            rule_path.write_text(NOT_RULE, encoding="utf-8")
            rule = load_single_rule(rule_path)

            self.assertTrue(
                evaluate_rule(
                    rule,
                    {"EventID": 7045, "ImagePath": "C:\\Windows\\Temp\\probe.exe"},
                )
            )
            self.assertFalse(
                evaluate_rule(
                    rule,
                    {"EventID": 7045, "ImagePath": "C:\\Program Files\\Vendor\\agent.exe"},
                )
            )

    def test_fixture_must_explicitly_be_synthetic(self) -> None:
        with TemporaryDirectory() as temp_directory:
            temp_root = Path(temp_directory)
            rule_path = temp_root / "content" / "portable" / "sigma" / "MSEC-DET-0001" / "rule.yml"
            cases_path = rule_path.parent / "tests" / "cases.json"
            fixture_path = cases_path.parent / "fixtures" / "unsafe.json"
            fixture_path.parent.mkdir(parents=True)
            rule_path.write_text((DETECTION_ROOT / "rule.yml").read_text(encoding="utf-8"), encoding="utf-8")
            cases_path.write_text(
                '{"implementation":"content/portable/sigma/MSEC-DET-0001/rule.yml",'
                '"cases":[{"id":"unsafe","expectation":"match",'
                '"fixture":"fixtures/unsafe.json"}]}',
                encoding="utf-8",
            )
            fixture_path.write_text(
                '{"schema_version":1,"synthetic":false,"event":{"EventID":7045}}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(LocalEvaluationError, "synthetic true"):
                run_fixture_set(temp_root, cases_path)


if __name__ == "__main__":
    unittest.main()
