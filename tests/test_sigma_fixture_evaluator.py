import json
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
from scripts.sigma_validation import parse_sigma_collection


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

        declared = json.loads((DETECTION_ROOT / "tests" / "cases.json").read_text())["cases"]
        self.assertEqual(len(outcomes), len(declared))
        self.assertEqual([outcome.case_id for outcome in outcomes], [case["id"] for case in declared])
        self.assertEqual({outcome.expectation for outcome in outcomes}, {"match", "no_match"})
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

    def test_regex_search_case_and_boundaries(self):
        source = NOT_RULE.replace("EventID: 7045", r"CommandLine|re: '(^|\s)-enc\s+[A-Z]+($|\s)'").replace("selection and not filter", "selection")
        rule = parse_sigma_collection(source).rules[0]
        self.assertTrue(evaluate_rule(rule, {"CommandLine": "powershell\t-enc\tABC"}))
        for text in ("powershell -encode ABC", "powershell -enc abc", "powershell -ENC ABC", "echo-enc ABC"):
            self.assertFalse(evaluate_rule(rule, {"CommandLine": text}), text)
        insensitive = parse_sigma_collection(source.replace("CommandLine|re:", "CommandLine|re|i:")).rules[0]
        self.assertTrue(evaluate_rule(insensitive, {"CommandLine": "powershell -ENC abc"}))
        self.assertFalse(evaluate_rule(insensitive, {"CommandLine": 1}))

    def test_boolean_values_are_not_numbers_or_strings(self):
        for literal, expected in (("true", True), ("false", False)):
            source = NOT_RULE.replace("EventID: 7045", f"ReadOnly: {literal}").replace("selection and not filter", "selection")
            rule = parse_sigma_collection(source).rules[0]
            self.assertTrue(evaluate_rule(rule, {"ReadOnly": expected}))
            for value in (int(expected), str(expected), not expected):
                self.assertFalse(evaluate_rule(rule, {"ReadOnly": value}))

    def test_nonportable_regex_fails_closed(self):
        rule = parse_sigma_collection(NOT_RULE.replace("EventID: 7045", "CommandLine|re: '(?=evil)evil'").replace("selection and not filter", "selection")).rules[0]
        with self.assertRaisesRegex(UnsupportedSigmaFeature, "portable subset"):
            evaluate_rule(rule, {"CommandLine": "evil"})

    def regex_rule(self, pattern):
        source = NOT_RULE.replace("EventID: 7045", "CommandLine|re: " + json.dumps(pattern))
        return parse_sigma_collection(source.replace("selection and not filter", "selection")).rules[0]

    def test_python_only_regex_operators_are_rejected(self):
        patterns = (r"(?>a)", r"a++", r"a*+", r"a?+", r"a{1}+", r"a{1,3}+",
                    r"a{1,}+", r"a\Z", r"(a)\1", r"(a)\\\1", r"(?<=a)b",
                    r"(?P<name>a)", r"(a)(?(1)b|c)", r"[^^](?>a)", r"[]](?>a)")
        for pattern in patterns:
            with self.subTest(pattern=pattern), self.assertRaisesRegex(UnsupportedSigmaFeature, "portable subset"):
                evaluate_rule(self.regex_rule(pattern), {"CommandLine": "aaa"})

    def test_literal_windows_separators_and_regex_punctuation_are_accepted(self):
        examples = (
            (r"(?i)^HKEY_CURRENT_USER\\SOFTWARE\\Office\\16\.0$", r"HKEY_CURRENT_USER\SOFTWARE\Office\16.0"),
            (r"^C:\\Temp\\Z$", "C:\\Temp\\Z"),
            (r"^C:\\Temp\\1$", "C:\\Temp\\1"),
            (r"^C:\\\\Temp$", "C:\\\\Temp"),
            (r"^\(\?>a\)$", "(?>a)"),
            (r"^\+\+$", "++"),
            (r"^\{1\}\+$", "{1}+"),
            (r"^[*+?{}()>=!]+$", "*+?{}()>!"),
            (r"^[]{+?]+$", "]{+?"),
            (r"^a+?$", "aaa"),
        )
        for pattern, value in examples:
            with self.subTest(pattern=pattern):
                self.assertTrue(evaluate_rule(self.regex_rule(pattern), {"CommandLine": value}))


if __name__ == "__main__":
    unittest.main()
