"""Admission-gate regressions against isolated, fully synthetic package copies."""
from __future__ import annotations

import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

import yaml

from scripts.check_content_quality import ContentQualityError, check_content, validation_input_digest


REPO_ROOT = Path(__file__).resolve().parents[1]
DETECTION_ID = "MSEC-DET-0001"


class ContentQualityTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for relative in (f"catalog/detections/{DETECTION_ID}", f"content/portable/sigma/{DETECTION_ID}"):
            shutil.copytree(REPO_ROOT / relative, self.root / relative)
        validation_files = [
            *sorted((REPO_ROOT / "scripts").rglob("*.py")),
            REPO_ROOT / "requirements-sigma.lock",
            *(REPO_ROOT / "targets/sentinel" / name for name in ("preview.json", "analytics-rules.json", "data-sources.json")),
        ]
        for source in validation_files:
            destination = self.root / source.relative_to(REPO_ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        self.manifest_path = self.root / f"catalog/detections/{DETECTION_ID}/manifest.json"
        self.source_path = self.root / f"content/portable/sigma/{DETECTION_ID}/rule.yml"
        self.cases_path = self.source_path.parent / "tests/cases.json"
        manifest = self.manifest()
        # Keep the test self-contained rather than depending on review content
        # or target observations from the surrounding development repository.
        manifest["quality"]["reviewed_on"] = date.today().isoformat()
        manifest["quality"]["provenance"]["review"] = "docs/reviews/synthetic-review.md"
        self.write_manifest(manifest)
        review = self.root / "docs/reviews/synthetic-review.md"
        review.parent.mkdir(parents=True)
        review.write_text(f"Synthetic unit-test review for {DETECTION_ID}.\n", encoding="utf-8")

    def manifest(self):
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest):
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def source(self):
        return yaml.safe_load(self.source_path.read_text(encoding="utf-8"))

    def write_source(self, source):
        self.source_path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")

    def evidence(self, *, production=False, digest=None):
        manifest = self.manifest()
        manifest["quality"]["validation_level"] = "production-validated" if production else "target-validated"
        manifest["quality"]["evidence"] = "tests/synthetic-validation-evidence.json"
        self.write_manifest(manifest)
        evidence = {
            "rule_sha256": digest or hashlib.sha256(self.source_path.read_bytes()).hexdigest(),
            "validation_inputs_sha256": validation_input_digest(self.root, manifest, self.source_path),
            "target_result": "passed",
            "reviewer": "Synthetic unit-test reviewer",
            "test_reference": "synthetic-test-only:target-acceptance",
        }
        if production:
            evidence.update(pilot_result="accepted", pilot_days=14,
                            tuning_reference="synthetic-test-only:pilot-review")
        path = self.root / manifest["quality"]["evidence"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(evidence), encoding="utf-8")
        return path

    def test_complete_reviewed_package_passes(self):
        self.assertEqual(check_content(self.root), 1)

    def test_duplicate_sigma_uuid_in_second_package_fails(self):
        other_id = "MSEC-DET-0002"
        manifest = self.manifest()
        other_source_dir = self.root / f"content/portable/sigma/{other_id}"
        shutil.copytree(self.source_path.parent, other_source_dir)
        manifest["id"] = other_id
        manifest["implementations"][0]["path"] = f"content/portable/sigma/{other_id}/rule.yml"
        other_manifest = self.root / f"catalog/detections/{other_id}/manifest.json"
        other_manifest.parent.mkdir(parents=True)
        other_manifest.write_text(json.dumps(manifest), encoding="utf-8")
        cases = json.loads(self.cases_path.read_text(encoding="utf-8"))
        cases["detection_id"] = other_id
        cases["implementation"] = manifest["implementations"][0]["path"]
        (other_source_dir / "tests/cases.json").write_text(json.dumps(cases), encoding="utf-8")
        review = self.root / manifest["quality"]["provenance"]["review"]
        review.write_text(f"Synthetic review: {DETECTION_ID}, {other_id}.\n", encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "duplicate Sigma UUID"):
            check_content(self.root)

    def test_manifest_and_sigma_metadata_must_agree(self):
        original = self.manifest()
        variants = []
        severity = copy.deepcopy(original)
        severity["severity"] = "high"
        variants.append((severity, "severity differs"))
        lifecycle = copy.deepcopy(original)
        lifecycle["lifecycle"]["status"] = "draft"
        variants.append((lifecycle, "lifecycle differs"))
        technique = copy.deepcopy(original)
        technique["attack"][0]["technique_id"] = "T1059.001"
        variants.append((technique, "ATT&CK techniques differ"))
        tactic = copy.deepcopy(original)
        tactic["attack"][0]["tactic"] = "Execution"
        variants.append((tactic, "ATT&CK tactics differ"))
        for manifest, message in variants:
            with self.subTest(message=message):
                self.write_manifest(manifest)
                with self.assertRaisesRegex(ContentQualityError, message):
                    check_content(self.root)

    def test_missing_license_is_rejected(self):
        source = self.source()
        source.pop("license")
        self.write_source(source)
        with self.assertRaisesRegex(ContentQualityError, "author, license and references"):
            check_content(self.root)

    def test_missing_or_unrelated_review_is_rejected(self):
        manifest = self.manifest()
        review = self.root / manifest["quality"]["provenance"]["review"]
        review.unlink()
        with self.assertRaisesRegex(ContentQualityError, "missing or symlinked evidence/source"):
            check_content(self.root)
        review.write_text("Synthetic review of a different detection only.\n", encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "does not mention this detection"):
            check_content(self.root)

    def test_missing_limitations_are_rejected(self):
        manifest = self.manifest()
        for value in ([], None):
            manifest["quality"]["limitations"] = value
            self.write_manifest(manifest)
            with self.subTest(value=value), self.assertRaisesRegex(ContentQualityError, "limitations must be explicit"):
                check_content(self.root)

    def test_orphaned_sigma_source_is_rejected(self):
        orphan = self.root / "content/portable/sigma/MSEC-DET-0999/rule.yml"
        orphan.parent.mkdir(parents=True)
        shutil.copyfile(self.source_path, orphan)
        with self.assertRaisesRegex(ContentQualityError, "orphaned Sigma implementation"):
            check_content(self.root)

    def test_orphaned_and_missing_fixtures_are_rejected(self):
        fixture_dir = self.source_path.parent / "tests/fixtures"
        orphan = fixture_dir / "unreferenced.json"
        orphan.write_text('{"schema_version":1,"synthetic":true,"event":{"EventID":7045}}', encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "orphaned or missing fixtures"):
            check_content(self.root)
        orphan.unlink()
        first_case = json.loads(self.cases_path.read_text(encoding="utf-8"))["cases"][0]
        (self.cases_path.parent / first_case["fixture"]).unlink()
        with self.assertRaisesRegex(ContentQualityError, "orphaned or missing fixtures"):
            check_content(self.root)

    def test_stable_promotion_without_pilot_evidence_is_rejected(self):
        manifest = self.manifest()
        manifest["lifecycle"]["status"] = "stable"
        self.write_manifest(manifest)
        source = self.source()
        source["status"] = "stable"
        self.write_source(source)
        with self.assertRaisesRegex(ContentQualityError, "stable requires revision-bound"):
            check_content(self.root)
        self.evidence()
        with self.assertRaisesRegex(ContentQualityError, "stable requires revision-bound"):
            check_content(self.root)

    def test_target_validation_is_bound_to_source_revision(self):
        self.evidence(digest="0" * 64)
        with self.assertRaisesRegex(ContentQualityError, "validation evidence is stale"):
            check_content(self.root)
        self.evidence()
        self.assertEqual(check_content(self.root), 1)
        # Even a source revision whose fixtures still pass must be revalidated.
        source = self.source()
        source["description"] += " Synthetic later revision."
        self.write_source(source)
        with self.assertRaisesRegex(ContentQualityError, "validation evidence is stale"):
            check_content(self.root)

    def test_validation_inputs_reject_stale_adapter_profiles_and_toolchain(self):
        inputs = ("scripts/event_normalization.py", "scripts/sentinel_compiler.py",
                  "scripts/sentinel_rule_renderer.py", "requirements-sigma.lock",
                  "targets/sentinel/preview.json", "targets/sentinel/analytics-rules.json",
                  "targets/sentinel/data-sources.json")
        for relative in inputs:
            with self.subTest(input=relative):
                self.evidence()
                path = self.root / relative
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                with self.assertRaisesRegex(ContentQualityError, "validation inputs evidence is missing or stale"):
                    check_content(self.root)
                path.write_bytes(original)
                self.assertEqual(check_content(self.root), 1)

    def test_validation_inputs_include_recursive_tooling_and_authored_metadata(self):
        self.evidence()
        nested = self.root / "scripts/synthetic_adapter/nested.py"
        nested.parent.mkdir(parents=True)
        nested.write_text("# Synthetic additional build input\n", encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "validation inputs evidence is missing or stale"):
            check_content(self.root)
        self.evidence()
        self.assertEqual(check_content(self.root), 1)
        manifest = self.manifest()
        manifest["description"] += " Synthetic changed authored metadata."
        self.write_manifest(manifest)
        with self.assertRaisesRegex(ContentQualityError, "validation inputs evidence is missing or stale"):
            check_content(self.root)

    def test_validation_digest_excludes_quality_and_manifest_serialization(self):
        path = self.evidence()
        expected = json.loads(path.read_text())["validation_inputs_sha256"]
        manifest = self.manifest()
        manifest["quality"]["limitations"].append("Synthetic additional review note.")
        self.manifest_path.write_text(json.dumps(dict(reversed(list(manifest.items()))), indent=4), encoding="utf-8")
        self.assertEqual(validation_input_digest(self.root, self.manifest(), self.source_path), expected)
        self.assertEqual(check_content(self.root), 1)
        with TemporaryDirectory() as directory:
            relocated = Path(directory) / "relocated"
            shutil.copytree(self.root, relocated)
            relocated_source = relocated / self.source_path.relative_to(self.root)
            self.assertEqual(validation_input_digest(relocated, manifest, relocated_source), expected)

    def test_missing_input_hash_or_required_file_fails_closed(self):
        evidence_path = self.evidence()
        evidence = json.loads(evidence_path.read_text())
        evidence.pop("validation_inputs_sha256")
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "validation inputs evidence is missing or stale"):
            check_content(self.root)
        self.evidence()
        for relative in ("scripts/event_normalization.py", "requirements-sigma.lock", "targets/sentinel/preview.json"):
            path = self.root / relative
            original = path.read_bytes()
            path.unlink()
            with self.subTest(input=relative), self.assertRaisesRegex(ContentQualityError, "missing or symlinked evidence/source"):
                check_content(self.root)
            path.write_bytes(original)

    def test_incomplete_target_and_production_evidence_are_rejected(self):
        path = self.evidence()
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["target_result"] = "failed"
        path.write_text(json.dumps(evidence), encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "target validation evidence is incomplete"):
            check_content(self.root)
        path = self.evidence(production=True)
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["pilot_days"] = 13
        path.write_text(json.dumps(evidence), encoding="utf-8")
        with self.assertRaisesRegex(ContentQualityError, "production pilot evidence is incomplete"):
            check_content(self.root)

    def test_stable_accepts_complete_current_revision_pilot_evidence(self):
        manifest = self.manifest()
        manifest["lifecycle"]["status"] = "stable"
        self.write_manifest(manifest)
        source = self.source()
        source["status"] = "stable"
        self.write_source(source)
        self.evidence(production=True)
        self.assertEqual(check_content(self.root), 1)


if __name__ == "__main__":
    unittest.main()
