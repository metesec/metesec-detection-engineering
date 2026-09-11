"""Synthetic overlap tests; no external corpus or Internet dependency."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import contextlib
import io
import json
import unittest

from scripts.audit_rule_overlap import (
    METRICS, PINNED_SIGMAHQ_REF, compare, known_references, load_records,
    main, records_from_bytes, revision, source_summary, verify_report_freshness,
)


RULE = b"""title: Synthetic audit input
id: 00000000-0000-4000-8000-000000000031
status: experimental
description: Synthetic audit fixture, not a real detection.
author: Synthetic fixture author
logsource:
  product: windows
  category: process_creation
detection:
  image:
    FileName: example.exe
  command:
    ProcessCommandLine|contains: test
  condition: image and command
level: low
"""


class RuleOverlapTests(unittest.TestCase):
    def test_identical_file_hits_every_metric(self):
        result = compare(records_from_bytes("local.yml", RULE), records_from_bytes("upstream.yml", RULE))
        self.assertTrue(all(metric["local_documents_matched"] == 1 for metric in result.values()))

    def test_metadata_changes_do_not_hide_predicate_or_uuid_overlap(self):
        changed = RULE.replace(b"Synthetic audit input", b"A different rule title") + b"# changed formatting\n"
        result = compare(records_from_bytes("local.yml", changed), records_from_bytes("upstream.yml", RULE))
        self.assertEqual(result["file_bytes"]["local_documents_matched"], 0)
        for metric in ("sigma_uuid", "detection", "detection_and_logsource", "normalized_condition_and_logsource"):
            self.assertEqual(result[metric]["local_documents_matched"], 1)

    def test_selector_renaming_and_order_are_canonicalized(self):
        changed = RULE.replace(b"image:", b"a:").replace(b"command:", b"b:").replace(b"image and command", b"b and a")
        result = compare(records_from_bytes("local.yml", changed), records_from_bytes("upstream.yml", RULE))
        self.assertEqual(result["detection"]["local_documents_matched"], 0)
        self.assertEqual(result["normalized_condition_and_logsource"]["local_documents_matched"], 1)

    def test_source_fields_values_and_adapter_are_not_erased(self):
        for changed in (
            RULE.replace(b"product: windows", b"product: linux"),
            RULE.replace(b"FileName", b"Image"),
            RULE.replace(b"example.exe", b"different.exe"),
            RULE + b"metesec_normalization: synthetic-adapter-v1\n",
        ):
            with self.subTest(changed=changed):
                result = compare(records_from_bytes("local.yml", changed), records_from_bytes("upstream.yml", RULE))
                self.assertEqual(result["normalized_condition_and_logsource"]["local_documents_matched"], 0)

    def test_case_sensitive_modifier_is_not_erased(self):
        changed = RULE.replace(b"FileName: example.exe", b"FileName|cased: example.exe")
        result = compare(records_from_bytes("local.yml", changed), records_from_bytes("upstream.yml", RULE))
        self.assertEqual(result["normalized_condition_and_logsource"]["local_documents_matched"], 0)

    def test_duplicate_yaml_keys_are_visible_errors(self):
        records, errors = load_records({"bad.yml": RULE + b"level: high\n"})
        self.assertEqual(records, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate YAML key", errors[0]["error"])

    def test_unsupported_normalization_keeps_exact_metrics_and_gap(self):
        source = RULE.replace(b"FileName: example.exe", b"FileName|exists: true")
        record = records_from_bytes("exists.yml", source)[0]
        self.assertIsNotNone(record.normalization_error)
        self.assertNotIn("normalized_condition_and_logsource", record.fingerprints)
        self.assertIn("detection", record.fingerprints)

    def test_option_like_git_reference_is_rejected_without_command(self):
        with self.assertRaises(ValueError):
            revision(Path("does-not-exist"), "--help")

    def test_related_uuid_and_raw_source_keep_upstream_author_attribution(self):
        source = RULE + b"""references:
  - https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/upstream.yml
related:
  - id: 00000000-0000-4000-8000-000000000031
    type: similar
"""
        found = known_references(records_from_bytes("local.yml", source), records_from_bytes("rules/upstream.yml", RULE))
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0]["upstream"]["author"], "Synthetic fixture author")
        self.assertEqual(found[1]["related_sigma_uuid"], "00000000-0000-4000-8000-000000000031")


class RuleOverlapFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.relative = "content/portable/sigma/MSEC-DET-0001/rule.yml"
        self.rule_path = self.root / self.relative
        self.rule_path.parent.mkdir(parents=True)
        self.rule_path.write_bytes(RULE)
        self.report_path = self.root / "overlap.json"
        files = {self.relative: RULE}
        records, errors = load_records(files)
        self.report = {
            "schema_version": 1,
            "upstream": {"repository": "https://github.com/SigmaHQ/sigma", "commit": PINNED_SIGMAHQ_REF,
                         "parse_errors": []},
            "scopes": {"reviewed_worktree": {
                "source": source_summary(files, records, errors),
                "comparisons": {metric: {"local_documents_matched": 0, "matches": []} for metric in METRICS},
            }},
        }
        self.write_report()

    def write_report(self):
        self.report_path.write_text(json.dumps(self.report), encoding="utf-8")

    def test_fresh_extracted_pack_needs_no_git_or_network(self):
        with patch("scripts.audit_rule_overlap.git", side_effect=AssertionError("Git must not run")):
            result = verify_report_freshness(self.root, Path("overlap.json"))
        self.assertEqual(result, {"rule_documents": 1, "exact_matches": 0, "normalized_similarities": 0})

    def test_byte_edit_and_added_or_removed_rule_stale_the_report(self):
        self.rule_path.write_bytes(RULE + b"# edited\n")
        with self.assertRaisesRegex(ValueError, "stale overlap report"):
            verify_report_freshness(self.root, self.report_path)
        self.rule_path.write_bytes(RULE)
        added = self.root / "content/portable/sigma/MSEC-DET-0002/rule.yml"
        added.parent.mkdir()
        added.write_bytes(RULE)
        with self.assertRaisesRegex(ValueError, "stale overlap report"):
            verify_report_freshness(self.root, self.report_path)
        added.unlink()
        self.rule_path.unlink()
        with self.assertRaisesRegex(ValueError, "no local Sigma rule inventory"):
            verify_report_freshness(self.root, self.report_path)

    def test_changed_upstream_pin_and_incomplete_metrics_fail_closed(self):
        self.report["upstream"]["commit"] = "0" * 40
        self.write_report()
        with self.assertRaisesRegex(ValueError, "pinned SigmaHQ"):
            verify_report_freshness(self.root, self.report_path)
        self.report["upstream"]["commit"] = PINNED_SIGMAHQ_REF
        del self.report["scopes"]["reviewed_worktree"]["comparisons"]["detection"]
        self.write_report()
        with self.assertRaisesRegex(ValueError, "unable to verify"):
            verify_report_freshness(self.root, self.report_path)

    def test_stored_local_parse_gap_and_rehashed_invalid_rule_fail(self):
        source = self.report["scopes"]["reviewed_worktree"]["source"]
        source["parse_errors"] = [{"path": self.relative, "error": "not reviewed"}]
        self.write_report()
        with self.assertRaisesRegex(ValueError, "unhandled local"):
            verify_report_freshness(self.root, self.report_path)
        broken = RULE.replace(b"  condition: image and command\n", b"")
        self.rule_path.write_bytes(broken)
        # Merely refreshing a digest cannot make invalid local predicates audited.
        files = {self.relative: broken}
        source.update(source_summary(files, *load_records(files)))
        source["normalization_unsupported"] = []
        source["normalization_supported"] = 1
        self.write_report()
        with self.assertRaisesRegex(ValueError, "current local rules"):
            verify_report_freshness(self.root, self.report_path)

    def test_every_exact_metric_rejects_current_overlap(self):
        comparisons = self.report["scopes"]["reviewed_worktree"]["comparisons"]
        for metric in METRICS[:-1]:
            with self.subTest(metric=metric):
                comparisons[metric] = {"local_documents_matched": 1, "matches": [{"synthetic": True}]}
                self.write_report()
                with self.assertRaisesRegex(ValueError, "exact upstream overlap"):
                    verify_report_freshness(self.root, self.report_path)
                comparisons[metric] = {"local_documents_matched": 0, "matches": []}

    def test_normalized_similarity_is_disclosed_without_automatic_rejection(self):
        self.report["scopes"]["reviewed_worktree"]["comparisons"][METRICS[-1]] = {
            "local_documents_matched": 1, "matches": [{"synthetic": True}]}
        self.write_report()
        result = verify_report_freshness(self.root, self.report_path)
        self.assertEqual(result["normalized_similarities"], 1)

    def test_cli_exit_status_and_mutually_exclusive_modes(self):
        args = ["audit_rule_overlap", "--repo-root", str(self.root), "--check-report", "overlap.json"]
        with patch("sys.argv", args), contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(main(), 0)
        self.assertIn("current for 1 rules", stdout.getvalue())
        self.rule_path.write_bytes(RULE + b"# stale\n")
        with patch("sys.argv", args), contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(main(), 1)
        self.assertIn("stale overlap report", stderr.getvalue())
        with patch("sys.argv", args + ["--upstream", "unused"]), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                main()
        self.assertEqual(result.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
