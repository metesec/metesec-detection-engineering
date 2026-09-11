#!/usr/bin/env python3
"""Cross-file admission gates; source integrity is separate from live efficacy."""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import sys
import uuid

try:
    from .sigma_validation import load_sigma_documents
    from .event_normalization import normalization_name
    from .sigma_fixture_evaluator import load_single_rule, run_fixture_set
except ImportError:
    from sigma_validation import load_sigma_documents
    from event_normalization import normalization_name
    from sigma_fixture_evaluator import load_single_rule, run_fixture_set


class ContentQualityError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContentQualityError(message)


def owned_file(root, relative):
    path = root / relative
    require(path.is_file() and not path.is_symlink(), f"missing or symlinked evidence/source: {relative}")
    require(path.resolve().is_relative_to(root.resolve()), f"path escapes repository: {relative}")
    return path


def validation_input_digest(root, manifest, source):
    """Bind evidence to source, authored metadata and the target build inputs.

    All Python tooling and complete Sentinel profiles are included deliberately:
    even an unrelated profile edit conservatively requires renewed evidence.
    Quality metadata is excluded because it contains the evidence reference and
    changes when evidence is recorded. Relative names and canonical JSON make
    the digest independent of checkout location and manifest key order.
    """
    root = root.resolve()
    require(not source.is_symlink() and source.resolve().is_relative_to(root),
            "validation source escapes repository or is symlinked")
    source_relative = source.resolve().relative_to(root).as_posix()
    required = {
        source_relative,
        "requirements-sigma.lock",
        "targets/sentinel/preview.json",
        "targets/sentinel/analytics-rules.json",
        "targets/sentinel/data-sources.json",
        "scripts/event_normalization.py",
        "scripts/sigma_fixture_evaluator.py",
        "scripts/sigma_validation.py",
        "scripts/sentinel_compiler.py",
        "scripts/sentinel_rule_renderer.py",
    }
    required.update(path.relative_to(root).as_posix() for path in (root / "scripts").rglob("*.py"))
    hashes = {
        relative: hashlib.sha256(owned_file(root, relative).read_bytes()).hexdigest()
        for relative in sorted(required)
    }
    manifest_relative = f"catalog/detections/{manifest['id']}/manifest.json"
    owned_file(root, manifest_relative)
    authored_metadata = {key: value for key, value in manifest.items() if key != "quality"}
    canonical_manifest = json.dumps(authored_metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    hashes[manifest_relative] = hashlib.sha256(canonical_manifest.encode("utf-8")).hexdigest()
    payload = {
        "format_version": 1,
        "inputs": [{"path": path, "sha256": hashes[path]} for path in sorted(hashes)],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def check_content(root):
    manifests = sorted((root / "catalog/detections").glob("*/manifest.json"))
    require(bool(manifests), "catalogue must not be empty")
    sources, uuids = set(), set()
    for path in manifests:
        m = json.loads(path.read_text())
        ident = m["id"]
        require(path.parent.name == ident, f"{ident}: catalogue identity mismatch")
        impl = m["implementations"]
        expected = f"content/portable/sigma/{ident}/rule.yml"
        require(len(impl) == 1 and impl[0]["type"] == "sigma" and impl[0]["status"] == "active" and impl[0]["path"] == expected,
                f"{ident}: exactly one canonical active Sigma implementation is required")
        source = owned_file(root, expected)
        sources.add(source)
        docs = load_sigma_documents(source.read_text())
        require(len(docs) == 1, f"{ident}: exactly one Sigma document is required")
        rule = docs[0]
        uid = str(uuid.UUID(rule["id"]))
        require(uid not in uuids, f"{ident}: duplicate Sigma UUID")
        uuids.add(uid)
        require(rule.get("level") == m["severity"], f"{ident}: severity differs between manifest and Sigma")
        require(rule.get("status") == m["lifecycle"]["status"], f"{ident}: lifecycle differs between manifest and Sigma")
        require(rule.get("author") and rule.get("license") == "Apache-2.0" and rule.get("references"), f"{ident}: author, license and references are required")
        require(all(isinstance(ref, str) and ref.startswith("https://") for ref in rule["references"]), f"{ident}: references must be explicit HTTPS sources")
        tags = set(rule.get("tags", []))
        expected_techniques = {"attack." + item["technique_id"].lower() for item in m["attack"]}
        actual_techniques = {tag for tag in tags if tag.startswith("attack.t")}
        require(expected_techniques == actual_techniques, f"{ident}: ATT&CK techniques differ between manifest and Sigma")
        expected_tactics = {"attack." + item["tactic"].lower().replace(" ", "-") for item in m["attack"]}
        actual_tactics = {tag for tag in tags if tag.startswith("attack.") and not tag.startswith("attack.t")}
        require(expected_tactics == actual_tactics, f"{ident}: ATT&CK tactics differ between manifest and Sigma")
        quality = m.get("quality", {})
        require(quality.get("signal_type") in {"behavior", "configuration-change", "administrative-activity"}, f"{ident}: missing signal classification")
        require(bool(quality.get("limitations")), f"{ident}: limitations must be explicit")
        reviewed = date.fromisoformat(quality["reviewed_on"])
        require(date.fromisoformat(m["lifecycle"]["created"]) <= reviewed <= date.today(), f"{ident}: invalid review date")
        provenance = quality["provenance"]
        require(provenance["license"] == rule["license"], f"{ident}: provenance license mismatch")
        report = owned_file(root, provenance["review"])
        require(ident in report.read_text(), f"{ident}: review report does not mention this detection")
        level = quality.get("validation_level")
        require(level in {"synthetic-only", "target-validated", "production-validated"}, f"{ident}: invalid validation level")
        if level != "synthetic-only":
            evidence = json.loads(owned_file(root, quality.get("evidence", "missing")).read_text())
            require(evidence.get("rule_sha256") == hashlib.sha256(source.read_bytes()).hexdigest(), f"{ident}: validation evidence is stale")
            require(evidence.get("validation_inputs_sha256") == validation_input_digest(root, m, source), f"{ident}: validation inputs evidence is missing or stale")
            require(evidence.get("target_result") == "passed" and evidence.get("reviewer") and evidence.get("test_reference"), f"{ident}: target validation evidence is incomplete")
            if level == "production-validated":
                require(evidence.get("pilot_result") == "accepted" and evidence.get("pilot_days", 0) >= 14 and evidence.get("tuning_reference"), f"{ident}: production pilot evidence is incomplete")
        if m["lifecycle"]["status"] == "stable":
            require(level == "production-validated", f"{ident}: stable requires revision-bound target and production-pilot evidence")
        parsed = load_single_rule(source)
        normalization_name(parsed)
        cases_path = source.parent / "tests/cases.json"
        cases = json.loads(cases_path.read_text())["cases"]
        fixture_paths = {source.parent / "tests" / case["fixture"] for case in cases}
        require(fixture_paths == set((source.parent / "tests/fixtures").glob("*.json")), f"{ident}: orphaned or missing fixtures")
        outcomes = run_fixture_set(root, cases_path)
        require({item.expectation for item in outcomes} == {"match", "no_match"}, f"{ident}: positive and negative evidence required")
        require(all(item.passed for item in outcomes), f"{ident}: regression fixture failed")
    require(sources == set((root / "content/portable/sigma").glob("*/rule.yml")), "orphaned Sigma implementation")
    return len(manifests)


def main():
    try:
        count = check_content(Path(__file__).resolve().parents[1])
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Content quality failed: {error}", file=sys.stderr)
        return 1
    print(f"Content quality passed: {count} reviewed packages; local evidence does not imply live efficacy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
