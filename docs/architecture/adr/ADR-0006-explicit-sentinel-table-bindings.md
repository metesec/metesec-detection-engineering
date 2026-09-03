# ADR-0006: Require explicit Microsoft Sentinel table bindings

- Status: Accepted
- Date: 2026-09-03

## Context

Sigma expresses detection intent and fields but does not always identify the concrete table used by a particular Microsoft Sentinel workspace. The Kusto backend can infer a table only for mappings it knows. Guessing `Event`, `WindowsEvent`, `SigninLogs`, or another table would make successful compilation look more authoritative than the real telemetry contract.

The first live target available to the project contains populated Microsoft Entra, Microsoft Defender, cloud, email, and Application Gateway data but no Windows event table suitable for `MSEC-DET-0001`.

## Decision

- A Sentinel preview profile must name every included detection, its exact Sigma source, its Log Analytics table, and its reviewed Golden query.
- The compiler passes that table explicitly to the pinned Azure Monitor processing pipeline.
- Table values must be plain Kusto identifiers; implementation and Golden paths must remain inside the repository.
- The implementation must be declared as an active Sentinel Sigma source in the matching logical manifest.
- A rule absent from the preview profile is not silently compiled and receives no Sentinel compatibility claim.
- Compiler, Golden-snapshot, live query-acceptance, behavioral, and deployment results remain separate claims.

## Consequences

`MSEC-DET-0002` can compile deterministically to `SigninLogs` without encoding a private workspace identifier. `MSEC-DET-0001` remains portable and locally tested but is intentionally excluded until suitable telemetry and a reviewed table or field mapping exist. Adding another rule to the Sentinel preview requires an explicit reviewed binding and Golden snapshot.

## Reconsider when

Introduce reusable log-source mappings only after multiple verified detections demonstrate that the mapping is stable across supported Sentinel ingestion paths. Do not weaken the explicit binding merely to increase the number of compiled rules.
