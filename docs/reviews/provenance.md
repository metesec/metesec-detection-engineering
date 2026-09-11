# Source provenance and bounded overlap audit

Reviewed 2026-09-11. The reproducible [overlap inventory](upstream-overlap.json)
compares the original 50 rules at repository commit
`bea9b71d6399a17c3ae393c65c0a8c72c52eb96b` and the reviewed 67-rule working tree
against [SigmaHQ commit 5c9b21756f4e3ba137c1773ac9ba5a8332188961](https://github.com/SigmaHQ/sigma/tree/5c9b21756f4e3ba137c1773ac9ba5a8332188961).
The upstream corpus contains 4,042 YAML files with 4,045 rule documents under
`rules*`, `deprecated` and `unsupported`. All selected YAML files parse; some
contain more than one rule document.

| Comparison | Original 50 | Reviewed 67 |
| --- | ---: | ---: |
| Complete file bytes identical | 0 | 0 |
| Sigma rule UUID identical | 0 | 0 |
| Parsed detection and logsource identical | 0 | 0 |
| Parsed detection identical | 0 | 0 |
| Normalized condition and logsource identical within the supported subset | 0 | 0 |

The first four checks cover all 4,045 upstream rule documents. The normalized
condition check supports all local rules and 3,766 upstream documents. The
remaining 279 upstream documents use unsupported predicate types or condition
features and are listed individually in the inventory. They are comparison
gaps, not proven non-matches. This check removes selector names and normalizes
AND/OR ordering, grouping and duplicate operands while retaining field names,
value types, regular-expression flags, logsource and required normalization.
It is not a general Boolean-equivalence or field-alias analysis.

These results support a narrow statement: no exact matches were found by the
listed methods in this pinned SigmaHQ corpus. They do not establish that the
whole Internet was searched, that a renamed-field implementation is conceptually
different, or that every original author has been identified. Similar short
predicates for a documented platform event are expected. Rule quality, telemetry
contracts, tests and honest deployment limits matter more than novelty.

Known relationships remain visible. The inventory records 31 resolved explicit
SigmaHQ URL or `related`-UUID references, including upstream author metadata.
For example:

- 0012 references Nasreddine Bencherchali's [mshta HTTP rule](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/rules/windows/process_creation/proc_creation_win_mshta_http.yml); both concern a remote resource, with different telemetry predicates.
- 0022 references @ionsor's [MFA-disablement rule](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/rules/cloud/azure/audit_logs/azure_mfa_disabled.yml). Both select the same successful documented audit operation using different source field names. This is a known conceptual near-equivalent, not a claim of a new detection idea.
- 0039 references Florian Roth's [PowerShell download-and-execution rule](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/rules/windows/process_creation/proc_creation_win_powershell_download_iex.yml); the local implementation uses explicit process identity and bounded tokens but shares a familiar behavior hypothesis.
- 0076 references vitaliy0x1's [CloudTrail logging rule](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/rules/cloud/aws/cloudtrail/aws_cloudtrail_disable_logging.yml); successful logging interruption remains a well-known security-control signal.

Four stale upstream URLs in 0037, 0039, 0040 and 0047 were replaced with verified,
commit-pinned references. Historical unresolved links remain visible in the
original-baseline portion of the inventory rather than being rewritten as history.

The newly admitted rules derive from the supplied Hardened 23 archive, which
declares Apache-2.0 licensing. Their source attribution, modified-file notices
and declared license are retained; the admission decisions and evidence limits
are recorded in [the candidate review](candidates-0051-0100.md). The separate
50-rule bundle has no license declaration established by this review and is not
imported as source content.

[SigmaHQ's license declaration](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/LICENSE)
identifies the [Detection Rule License 1.1](https://github.com/SigmaHQ/Detection-Rule-License)
for upstream rules. Related-source references and retained upstream author
metadata are attribution evidence, not permission to relabel imported SigmaHQ
content as Apache-2.0. Any later direct import or adaptation must retain the
applicable upstream attribution and license requirements. This review does not
provide a rights guarantee for undocumented ancestry in supplied files.

Reproduce from a checkout with the pinned Python dependencies installed and a
local SigmaHQ clone containing the pinned commit:

```sh
python scripts/audit_rule_overlap.py --upstream /path/to/sigma --output docs/reviews/upstream-overlap.json
python scripts/audit_rule_overlap.py --check-report docs/reviews/upstream-overlap.json
python -m unittest tests.test_rule_overlap_audit
```

The auditor reads upstream and baseline Git objects without changing either
checkout or accessing the network. Working-tree rule bytes are hashed separately,
so subsequent local edits require a rerun. Reports contain repository-relative
paths and deterministic fingerprints; they contain no private telemetry,
workstation paths or runtime timestamps. The offline `--check-report` gate verifies
the pinned corpus, exact local file inventory and digest, and complete local parsing
coverage without Git or network access. Changed rule bytes make the evidence stale.
Recorded exact matches fail the gate; normalized similarities are disclosed and
require contextual review rather than automatic rejection. Passing this gate
establishes freshness of the evidence, not a general authorship or rights guarantee.

Sixteen isolated tests verify overlap
detection, selector normalization, meaningful distinctions, explicit gaps,
duplicate-key rejection, upstream author-reference retention and offline freshness.
