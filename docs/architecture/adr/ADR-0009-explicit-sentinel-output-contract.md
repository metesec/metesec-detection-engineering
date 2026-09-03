# ADR-0009: Govern Sentinel output columns and entity mappings together

- Status: Accepted
- Date: 2026-09-03

## Context

ADR-0008 introduced deterministic disabled Scheduled-rule bodies, but deferred
entity mappings until the generated KQL columns had an executable contract.
Mapping arbitrary source fields directly would make an alert depend on implicit
backend output and could confuse an Entra object ID with an application ID.

The repository also does not need a second immutable Sentinel release artifact.
Consumers may need to adapt target settings to their own workspace and should
render the reviewed source inside their own controlled pipeline.

## Decision

Extend the explicit Sentinel preview profile to version 2. Every bound detection
must declare:

- bounded `extend` expressions that create normalized output columns;
- the exact ordered query output columns;
- Sentinel entity mappings whose column names exist in that output list.

The compiler appends the declared `extend` and `project` operators after the
Sigma-generated predicate. The complete result remains subject to Golden-query
review. The renderer copies only those governed mappings into the Scheduled-rule
REST body and records both the output columns and mappings in its provenance.

Account mappings use name, UPN suffix and Entra user ID where available. IP
addresses use the IP entity. Applications use application ID and name only when
the source field has that meaning. A target service-principal object ID remains
available as an output column but is not mapped as a CloudApplication AppId.

Generated Sentinel files remain ignored, temporary local or pipeline output.
The repository documents a consumer-owned render-and-deploy handoff but ships no
separate prebuilt Sentinel target archive and contains no deployment client.

## Consequences

- Analysts receive predictable columns and usable Account, IP and
  CloudApplication entities.
- A mapping cannot reference a column that the final query does not return.
- The complete enriched query is reviewed, deterministic and regression tested.
- Consumers can adapt the authored target profile before rendering in their own
  pipeline.
- Deployment scope, credentials, approval, validation and enablement remain the
  consumer's responsibility.

## Reconsider when

- Microsoft changes the Scheduled-rule entity-mapping contract;
- a new entity type requires identifiers outside the current allowlist;
- multiple verified ingestion paths need reusable output transformations;
- a real consumer requires a separately versioned target artifact.
