# ADR-0010: Separate data-source health from detection results

- Status: Accepted
- Date: 2026-09-03

## Context

A detection that returns no result can mean either that no matching activity
occurred or that its table, fields or recent telemetry are unavailable. Treating
both conditions as a healthy zero would create false confidence.

The logical manifests name fields per detection, but the Sentinel target had no
single executable contract covering the union of fields, their target types,
freshness expectations or every rule that consumes a table.

## Decision

Create version 1 of a Microsoft Sentinel data-source contract. Each source has a
stable `MSEC-SDS-####` identity and declares:

- its exact Sentinel table and consuming detection IDs;
- the event-time column;
- every required column and Kusto type;
- a degraded and unavailable freshness threshold.

Keep environment observations separate from the public contract. An observation
contains only the observation time, table availability, latest event time and
observed column names and types. It contains no rows, counts, users, tenants or
workspace identifiers and must not be committed.

The local evaluator derives exactly four states:

- `ready` when the table is present, fresh and structurally complete;
- `degraded` when data is stale beyond the first threshold or a required column
  is missing or has the wrong type;
- `unavailable` when the table is absent, has no observed event or exceeds the
  final freshness threshold;
- `unknown` when no observation was supplied for the contracted source.

The initial reference thresholds are six hours for degradation and one day for
unavailability. They are explicit expectations, not Microsoft guarantees or a
production SLA. A consumer that needs different expectations must change and
review the contract for its environment.

## Consequences

- A missing observation can never be reported as healthy.
- The two Sentinel source contracts cover all four currently bound detections
  exactly and fail when preview bindings drift.
- Schema drift and telemetry staleness can be checked without reading or storing
  event rows.
- The repository still has no Azure client, credential, target scope, scheduler
  or live health claim.

## Reconsider when

- real operational baselines justify different freshness thresholds;
- connector-health telemetry provides a stronger signal than latest event time;
- more than one ingestion path supplies the same logical data source;
- detection health needs to combine telemetry, execution and alert outcomes.
