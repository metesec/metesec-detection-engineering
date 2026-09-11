#!/usr/bin/env python3
"""Reproduce a bounded rule-overlap comparison against a pinned SigmaHQ tree.

This measures shared bytes, identities and predicates. It does not establish
copyright ownership, independently authored intent or absence of Internet copies.
No network access is used, and no upstream rule content is copied to the report.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any
from urllib.parse import unquote, urlparse

from sigma.conditions import (
    ConditionAND, ConditionOR, ConditionNOT, ConditionFieldEqualsValueExpression,
    ConditionValueExpression, SigmaCondition,
)
from sigma.rule import SigmaRule
from sigma.types import SigmaBool, SigmaNumber, SigmaString, SigmaCasedString, SigmaRegularExpression

try:
    from .sigma_validation import load_sigma_documents
except ImportError:
    from sigma_validation import load_sigma_documents


PINNED_SIGMAHQ_REF = "5c9b21756f4e3ba137c1773ac9ba5a8332188961"
BASELINE_REF = "bea9b71d6399a17c3ae393c65c0a8c72c52eb96b"
METRICS = ("file_bytes", "sigma_uuid", "detection_and_logsource", "detection",
           "normalized_condition_and_logsource")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def canonical_value(value: Any) -> Any:
    # Preserve value types and wildcard-vs-literal distinctions. Sigma's normal
    # strings are case insensitive, while regex case behavior is explicit.
    if isinstance(value, SigmaBool):
        return ["bool", value.boolean]
    if isinstance(value, SigmaNumber):
        return ["number", value.number]
    if isinstance(value, SigmaRegularExpression):
        return ["regex", str(value.regexp), sorted(str(flag) for flag in value.flags)]
    if isinstance(value, SigmaString):
        cased = isinstance(value, SigmaCasedString)
        return ["cased_string" if cased else "string",
                [["text", part if cased else part.lower()] if isinstance(part, str)
                 else ["special", part.name] for part in value.s]]
    raise ValueError(f"unsupported predicate value: {type(value).__name__}")


def canonical_condition(node: Any) -> Any:
    if isinstance(node, (ConditionAND, ConditionOR)):
        kind = "and" if isinstance(node, ConditionAND) else "or"
        children = []
        for arg in node.args:
            child = canonical_condition(arg)
            if child[0] == kind:
                children.extend(child[1])
            else:
                children.append(child)
        # Ordering, grouping and duplicate operands do not change AND/OR truth.
        return [kind, [json.loads(item) for item in sorted(set(map(canonical, children)))]]
    if isinstance(node, ConditionNOT):
        return ["not", canonical_condition(node.args[0])]
    if isinstance(node, ConditionFieldEqualsValueExpression):
        return ["field", node.field, canonical_value(node.value)]
    if isinstance(node, ConditionValueExpression):
        return ["keyword", canonical_value(node.value)]
    raise ValueError(f"unsupported predicate node: {type(node).__name__}")


@dataclass(frozen=True)
class RuleRecord:
    path: str
    document: int
    title: str
    author: str
    uuid: str | None
    references: tuple[str, ...]
    related: tuple[str, ...]
    fingerprints: dict[str, str]
    normalization_error: str | None

    def identity(self) -> dict[str, Any]:
        return {"path": self.path, "document": self.document, "title": self.title,
                "sigma_uuid": self.uuid, "author": self.author}


def records_from_bytes(path: str, raw: bytes) -> list[RuleRecord]:
    records = []
    for index, document in enumerate(load_sigma_documents(raw.decode("utf-8")), start=1):
        if not isinstance(document, dict) or not all(key in document for key in ("logsource", "detection")):
            continue
        fingerprints = {
            "file_bytes": hashlib.sha256(raw).hexdigest(),
            "detection": digest(document["detection"]),
            "detection_and_logsource": digest({"logsource": document["logsource"], "detection": document["detection"]}),
        }
        uuid = str(document["id"]).lower() if document.get("id") else None
        if uuid:
            fingerprints["sigma_uuid"] = uuid
        error = None
        try:
            rule = SigmaRule.from_dict(document)
            conditions = [canonical_condition(SigmaCondition(c, rule.detection).parse())
                          for c in rule.detection.condition]
            fingerprints["normalized_condition_and_logsource"] = digest({
                "logsource": document["logsource"],
                "conditions": sorted(conditions, key=canonical),
                "normalization": document.get("metesec_normalization"),
            })
        except Exception as exc:
            # Exact comparisons still apply. Unsupported semantic comparisons
            # are explicit gaps, never silently classified as non-overlap.
            error = f"{type(exc).__name__}: {exc}"
        records.append(RuleRecord(path, index, str(document.get("title", "")),
                                  str(document.get("author", "")), uuid,
                                  tuple(document.get("references") or []),
                                  tuple(str(item.get("id", "")).lower() for item in document.get("related", [])
                                        if isinstance(item, dict)), fingerprints, error))
    return records


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def revision(repo: Path, ref: str) -> str:
    # Disallow option-like revisions, and bind every caller to a commit object.
    if not ref or ref.startswith("-") or any(c in ref for c in "\r\n\x00"):
        raise ValueError("invalid Git revision")
    return git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()


def load_records(files: dict[str, bytes]) -> tuple[list[RuleRecord], list[dict[str, str]]]:
    records, failures = [], []
    for path, raw in sorted(files.items()):
        try:
            records.extend(records_from_bytes(path, raw))
        except Exception as exc:
            failures.append({"path": path, "error": f"{type(exc).__name__}: {exc}"})
    return records, failures


def dataset_digest(files: dict[str, bytes]) -> str:
    return digest({path: hashlib.sha256(raw).hexdigest() for path, raw in sorted(files.items())})


def source_summary(files: dict[str, bytes], records: list[RuleRecord], errors: list[dict[str, str]]) -> dict[str, Any]:
    return {"yaml_files": len(files), "rule_documents": len(records),
            "dataset_sha256": dataset_digest(files), "parse_errors": errors,
            "normalization_supported": sum(r.normalization_error is None for r in records),
            "normalization_unsupported": [dict(r.identity(), reason=r.normalization_error)
                                          for r in records if r.normalization_error is not None]}


def compare(local: list[RuleRecord], upstream: list[RuleRecord]) -> dict[str, Any]:
    output = {}
    for metric in METRICS:
        index: dict[str, list[RuleRecord]] = {}
        for record in upstream:
            if metric in record.fingerprints:
                index.setdefault(record.fingerprints[metric], []).append(record)
        matches = []
        for record in local:
            found = index.get(record.fingerprints.get(metric, ""), [])
            if found:
                matches.append({"local": record.identity(), "upstream": [r.identity() for r in found]})
        output[metric] = {"local_documents_matched": len(matches), "matches": matches}
    return output


def known_references(local: list[RuleRecord], upstream: list[RuleRecord]) -> list[dict[str, Any]]:
    by_path = {record.path: record for record in upstream}
    by_uuid = {record.uuid: record for record in upstream if record.uuid}
    references = []
    for record in local:
        for url in record.references:
            if not isinstance(url, str):
                continue
            parsed = urlparse(url)
            if parsed.netloc.lower() == "github.com" and parsed.path.startswith("/SigmaHQ/sigma/blob/"):
                prefix = "/SigmaHQ/sigma/blob/"
            elif parsed.netloc.lower() == "raw.githubusercontent.com" and parsed.path.startswith("/SigmaHQ/sigma/"):
                prefix = "/SigmaHQ/sigma/"
            else:
                continue
            suffix = unquote(parsed.path[len(prefix):])
            if "/" not in suffix:
                continue
            _, path = suffix.split("/", 1)
            references.append({"local_path": record.path, "reference": url,
                               "upstream": by_path[path].identity() if path in by_path else None})
        for uuid in record.related:
            if uuid in by_uuid:
                references.append({"local_path": record.path, "related_sigma_uuid": uuid,
                                   "upstream": by_uuid[uuid].identity()})
    return references


def make_report(repo: Path, upstream: Path, upstream_ref: str, baseline_ref: str) -> dict[str, Any]:
    pinned = revision(upstream, upstream_ref)
    # Read pinned Git objects rather than trusting the upstream working tree.
    upstream_names = git(upstream, "ls-tree", "-r", "--name-only", pinned).decode().splitlines()
    upstream_names = [p for p in upstream_names if p.endswith((".yml", ".yaml"))
                      and (p.split("/")[0].startswith("rules") or p.split("/")[0] in {"deprecated", "unsupported"})]
    upstream_files = {p: git(upstream, "show", f"{pinned}:{p}") for p in upstream_names}
    baseline = revision(repo, baseline_ref)
    names = git(repo, "ls-tree", "-r", "--name-only", baseline, "--", "content/portable/sigma").decode().splitlines()
    baseline_files = {p: git(repo, "show", f"{baseline}:{p}") for p in names if p.endswith("/rule.yml")}
    current_files = {p.relative_to(repo).as_posix(): p.read_bytes()
                     for p in sorted((repo / "content/portable/sigma").glob("*/rule.yml"))}
    upstream_rules, upstream_errors = load_records(upstream_files)
    scopes = {}
    for name, files in (("original_baseline", baseline_files), ("reviewed_worktree", current_files)):
        records, errors = load_records(files)
        scopes[name] = {"source": source_summary(files, records, errors),
                        "comparisons": compare(records, upstream_rules),
                        "known_sigmahq_references": known_references(records, upstream_rules)}
    return {
        "schema_version": 1,
        "method": "Pinned-source overlap inventory; no network, fuzzy scoring or legal clearance.",
        "upstream": {"repository": "https://github.com/SigmaHQ/sigma", "commit": pinned,
                     "license": "Detection Rule License 1.1", "license_reference": "https://github.com/SigmaHQ/Detection-Rule-License",
                     "scope": "All tracked YAML under rules*, deprecated and unsupported at the pinned commit.",
                     **source_summary(upstream_files, upstream_rules, upstream_errors)},
        "original_baseline_commit": baseline,
        "metrics": {
            "file_bytes": "SHA-256 of complete original file bytes; comments, metadata and formatting retained.",
            "sigma_uuid": "Exact case-normalized Sigma rule UUID; not the repository logical detection ID.",
            "detection_and_logsource": "Parsed YAML detection plus logsource, dictionary keys sorted; selector names and list order retained.",
            "detection": "Parsed YAML detection only; selector names and list order retained.",
            "normalized_condition_and_logsource": "pySigma condition tree: selector names removed; AND/OR operands flattened, sorted and deduplicated; string case normalized; field names, value types, regex flags, logsource and normalization adapter retained. Not a complete Boolean equivalence proof.",
        },
        "limitations": [
            "A finite pinned SigmaHQ corpus does not search the whole Internet or every upstream revision.",
            "No-match results cannot establish independent authorship, license rights or absence of modified copies.",
            "Common documented behavior and short predicates naturally overlap; similarity alone is not rejection evidence.",
            "Unsupported normalization and parse errors are listed explicitly; exact metrics remain narrower than semantic similarity.",
            "Known references identify related source and attribution to review; a reference alone does not prove text was imported.",
        ],
        "scopes": scopes,
    }


def verify_report_freshness(repo_root: Path, report_path: Path) -> dict[str, int]:
    """Check committed copy-screen evidence offline, including extracted packs.

    Source digests establish freshness of reviewed evidence, not that the report
    is independently authenticated or that zero overlap proves authorship.
    """
    repo_root = repo_root.resolve()
    report_path = report_path if report_path.is_absolute() else repo_root / report_path
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report["schema_version"] != 1:
            raise ValueError("unsupported overlap report version")
        upstream = report["upstream"]
        if (upstream["repository"] != "https://github.com/SigmaHQ/sigma"
                or upstream["commit"] != PINNED_SIGMAHQ_REF):
            raise ValueError("overlap report does not identify the pinned SigmaHQ corpus")
        if upstream["parse_errors"] != []:
            raise ValueError("overlap report contains upstream YAML parse gaps")
        scope = report["scopes"]["reviewed_worktree"]
        source = scope["source"]
        if source["parse_errors"] != [] or source["normalization_unsupported"] != []:
            raise ValueError("overlap report contains unhandled local parse or normalization gaps")
        files = {path.relative_to(repo_root).as_posix(): path.read_bytes()
                 for path in sorted((repo_root / "content/portable/sigma").glob("*/rule.yml"))}
        if not files:
            raise ValueError("no local Sigma rule inventory found")
        if source["yaml_files"] != len(files) or source["dataset_sha256"] != dataset_digest(files):
            raise ValueError("stale overlap report: local rule inventory or bytes changed; rerun the pinned-source audit")
        records, errors = load_records(files)
        if errors or any(record.normalization_error is not None for record in records):
            raise ValueError("current local rules have unhandled parse or normalization gaps")
        if any(sum(record.path == path for record in records) != 1 for path in files):
            raise ValueError("each local rule file must contain exactly one auditable Sigma document")
        if source["rule_documents"] != len(records) or source["normalization_supported"] != len(records):
            raise ValueError("stale overlap report: local rule coverage counts differ")
        counts = {}
        for metric in METRICS:
            result = scope["comparisons"][metric]
            count, matches = result["local_documents_matched"], result["matches"]
            if (type(count) is not int or count < 0 or not isinstance(matches, list)
                    or count != len(matches) or count > len(records)):
                raise ValueError(f"invalid overlap evidence for {metric}")
            counts[metric] = count
        exact_matches = [metric for metric in METRICS[:-1] if counts[metric]]
        if exact_matches:
            raise ValueError("exact upstream overlap requires review: " + ", ".join(exact_matches))
        return {"rule_documents": len(records), "exact_matches": 0,
                "normalized_similarities": counts["normalized_condition_and_logsource"]}
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError(f"unable to verify overlap report: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--upstream", type=Path)
    mode.add_argument("--check-report", type=Path, help="verify stored overlap evidence without Git or network")
    parser.add_argument("--upstream-ref", default=PINNED_SIGMAHQ_REF)
    parser.add_argument("--baseline-ref", default=BASELINE_REF)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.check_report is not None:
        if args.output is not None:
            parser.error("--output cannot be combined with --check-report")
        try:
            result = verify_report_freshness(args.repo_root, args.check_report)
        except ValueError as exc:
            print(f"Overlap evidence check failed: {exc}", file=sys.stderr)
            return 1
        print(f"Overlap evidence is current for {result['rule_documents']} rules; "
              f"0 exact matches; {result['normalized_similarities']} normalized similarities "
              "(disclosed, not automatically rejected).")
        return 0
    report = make_report(args.repo_root.resolve(), args.upstream.resolve(), args.upstream_ref, args.baseline_ref)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    failed = report["upstream"]["parse_errors"] or any(scope["source"]["parse_errors"] for scope in report["scopes"].values())
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
