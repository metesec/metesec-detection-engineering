# ADR-0008: Render disabled Sentinel rule bodies before deployment

- Status: Accepted
- Date: 2026-09-03

## Context

Four detections already compile through explicit table bindings to deterministic
Golden KQL, but a query alone is not a Microsoft Sentinel analytics rule. A
Scheduled rule also needs stable identity, display metadata, severity, schedule,
threshold, suppression, grouping and incident behavior.

Putting those target settings into the logical manifest would mix portable
detection intent with vendor runtime behavior. Adding deployment at the same
time would also make it difficult to prove the renderer independently and would
cross the existing no-write boundary for the user-authorized Sentinel target.

## Decision

Use a separate versioned Sentinel analytics-rule profile for target-only runtime
settings. Render each profile entry together with the logical manifest and the
already Golden-verified KQL into an exact REST request body and a separate
provenance manifest.

Rendered rules are always disabled in version 1. Rule IDs are deterministic
UUIDv5 values derived from the immutable MeteSec detection ID. The API version is
pinned to stable `2025-09-01`. The renderer maps only values supported by the
stable Scheduled-rule contract and fails closed on unsupported severities,
tactics, durations or incomplete binding sets.

The stable API exposes a `techniques` array but no separate `subTechniques`
property. The request body therefore receives the base technique ID, while the
full source sub-technique remains in the provenance manifest. Entity mappings
and dynamic alert fields are deferred until generated KQL columns are governed
by an executable contract.

## Consequences

- A reviewer can inspect a complete Sentinel rule body without Azure access.
- The same source commit produces byte-identical rule, query and provenance
  files.
- A generated file cannot silently arrive enabled.
- Target schedule choices remain separate from portable detection logic.
- The output still requires a later reviewed packaging and deployment layer to
  supply Azure resource scope and perform validation or writes.

## Reconsider when

- the project introduces a deployment bundle or controlled Azure what-if step;
- entity mappings receive an executable output-column contract;
- Microsoft changes the stable Scheduled alert-rule API shape;
- a target needs rule-specific behavior that the version 1 profile cannot
  represent safely.
