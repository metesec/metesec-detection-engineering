# ADR-0017: Reviewed enterprise baseline, not a rule-count target

Status: accepted for local 1.1 development, 2026-09-11.

## Context

The owner requested a full review of the existing fifty rules and both supplied
archives, with authority to change content and quality gates. The objective is
a defensible enterprise starting point, not novelty or a fixed number of rules.
Archive instructions are input documentation, not execution authority.

## Decision

Keep one immutable logical ID and one authored Sigma source per detection.
Retain all fifty existing concepts after review and correction. Admit seventeen
bounded new concepts and defer thirty-three; the two archives overlap in IDs
and do not constitute seventy-three additional unique detections.

Classify each signal as behavior, configuration-change or administrative-activity.
Require explicit limitations, source references, licensing and a per-ID review.
No current revision is promoted beyond experimental/synthetic-only. Stable
promotion needs revision-bound target evidence and an accepted, documented pilot.

Extend the local evaluator with strict booleans and a bounded regex subset.
Reject duplicate YAML keys and unsupported regex constructs. Python test results
do not imply Kusto semantic equivalence.

For MSEC-DET-0021, use an explicitly declared, versioned raw-event adapter:
`entra-delegated-grant-v1`. It structurally pairs new Scope and ConsentType values
inside the same ServicePrincipal. Its Python reference and generated KQL are
owned tooling, not a second authored detection. Other engines must implement
that adapter before claiming support for this rule. No arbitrary user-supplied
KQL snippets or generic normalization engine are introduced.

Keep hunting Golden queries unwindowed. Derive disabled scheduled queries by
adding event-time lookback and ingestion-time slicing before source filters or
projection. Default to a 15-minute frequency, one-hour period and no automatic
incident creation. This is an unvalidated pilot default, not an enterprise SLA.

Preserve the canonical Forgejo trust boundary and immutable published releases.
Make the 1.1 source pack self-contained for local validation and rebuilding.

## Consequences

More negative tests and stricter gates can reject previously accepted content.
Changes in a source invalidate evidence tied to that source hash. Per-environment
schema checks, KQL execution, latency measurement and false-positive tuning are
still mandatory before enablement. The unbound Windows System-event rule 0001
remains available as source but is not silently rendered to an invented table.

Related decisions: ADR-0005, ADR-0008, ADR-0015 and ADR-0016. The historical
fifty-rule 1.0 release remains intact; its scope is not the future admission gate.
