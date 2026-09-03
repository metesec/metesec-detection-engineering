from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.sigma_validation import (
    SigmaDocumentError,
    discover_sigma_rules,
    validate_sigma_path,
    validate_sigma_text,
    verify_parser_health,
)


VALID_RULE = """\
title: Unit test rule
id: 00000000-0000-4000-8000-000000000002
status: test
description: Synthetic unit-test input.
author: MeteSec
date: 2026-09-03
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: '\\unit-test.exe'
  condition: selection
falsepositives:
  - Synthetic test input only.
level: low
"""

INVALID_RULE = """\
title: Missing condition
logsource:
  product: windows
detection:
  selection:
    Image: unit-test.exe
"""


class SigmaValidationTests(unittest.TestCase):
    def test_valid_rule_is_accepted(self) -> None:
        result = validate_sigma_text(VALID_RULE, "valid.yml")
        self.assertEqual(result.rule_count, 1)
        self.assertEqual(result.source, "valid.yml")

    def test_rule_without_condition_is_rejected(self) -> None:
        with self.assertRaisesRegex(SigmaDocumentError, "at least one condition"):
            validate_sigma_text(INVALID_RULE, "invalid.yml")

    def test_non_yaml_input_is_rejected(self) -> None:
        with self.assertRaises(SigmaDocumentError):
            validate_sigma_text("not: [valid", "broken.yml")

    def test_parser_health_check_proves_both_paths(self) -> None:
        verify_parser_health()

    def test_package_v1_discovery_ignores_nested_test_yaml(self) -> None:
        with TemporaryDirectory() as temp_directory:
            repo_root = Path(temp_directory)
            rule_path = (
                repo_root
                / "content"
                / "portable"
                / "sigma"
                / "MSEC-DET-0001"
                / "rule.yml"
            )
            nested_path = rule_path.parent / "tests" / "not-a-rule.yml"
            nested_path.parent.mkdir(parents=True)
            rule_path.write_text(VALID_RULE, encoding="utf-8")
            nested_path.write_text(INVALID_RULE, encoding="utf-8")

            self.assertEqual(discover_sigma_rules(repo_root), [rule_path])

    def test_utf8_rule_file_is_validated(self) -> None:
        with TemporaryDirectory() as temp_directory:
            rule_path = Path(temp_directory) / "rule.yml"
            rule_path.write_text(VALID_RULE, encoding="utf-8")

            result = validate_sigma_path(rule_path)

            self.assertEqual(result.rule_count, 1)


if __name__ == "__main__":
    unittest.main()
