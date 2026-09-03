# ADR-0012: Derive coverage without unsupported scoring

- Status: Accepted
- Date: 2026-09-03

## Context

The repository declares ATT&CK mappings, logical data sources, Sentinel preview
bindings and Sentinel table contracts in separate authoritative files. Readers
need a concise view of those relationships and any explicit target gaps.

A percentage score would require a defensible denominator such as an approved
threat model, a complete ATT&CK scope or an organization-specific coverage goal.
The project has none of those boundaries and must not invent one.

## Decision

Generate a versioned machine-readable report and a matching human-readable
report from the existing manifests, Sentinel preview and data-source contract.
Report exact declared counts and relationships, including detections without a
Sentinel preview binding. Do not calculate a coverage percentage or import live
environment state.

Tracked generated outputs must be deterministic, schema-valid and protected by
a stale-output check in the aggregate repository validation.

## Consequences

- Readers can inspect ATT&CK and data-source coverage without joining source
  files manually.
- The known Windows telemetry target gap remains visible.
- Source contracts remain authoritative; generated reports are never hand-edited.
- Reported coverage cannot be mistaken for a complete control or threat-model
  assessment.

## Reconsider when

- the project adopts an explicit threat-model denominator;
- authoritative ATT&CK catalogue enrichment is added as a pinned input;
- target-specific readiness needs a separate environment report.
