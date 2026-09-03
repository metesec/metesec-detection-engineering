# Microsoft Sentinel data-source contract v1

The contract at `targets/sentinel/data-sources.json` defines what the current
Sentinel detections need from `SigninLogs` and `AuditLogs`. Its JSON Schema is
`governance/schemas/sentinel-data-source-contract-v1.schema.json`.

This is a telemetry dependency contract, not a connector deployment, live
monitor or production-readiness claim.

## Contract contents

Each source declares a stable source ID, exact table, display name, consuming
detection IDs, event-time column, required columns with Kusto types and two
freshness thresholds. The validator requires every table and consumer to match
the version 2 Sentinel preview exactly.

The initial reference expectation is:

| State boundary | Age of latest observed event |
| --- | ---: |
| `ready` | at most 6 hours |
| `degraded` | more than 6 hours and at most 1 day |
| `unavailable` | more than 1 day |

These values are explicit reference assumptions, not Microsoft guarantees or an
environment SLA. A low-volume or differently operated environment must review
them before use.

## Observation and states

An environment-local observation follows
`governance/schemas/sentinel-data-source-observation-v1.schema.json`. It contains
only:

- one UTC observation time;
- source ID and table;
- whether the table exists;
- the latest event timestamp or `null`;
- observed column names and Kusto types.

The evaluator produces:

| State | Meaning |
| --- | --- |
| `ready` | Table, freshness, required columns and types satisfy the contract. |
| `degraded` | Freshness crossed the first threshold, or a required field is missing or mistyped. |
| `unavailable` | Table is absent, no event was observed, or freshness crossed the final threshold. |
| `unknown` | The observation did not include this contracted source. |

Unavailable and unknown are never converted into a healthy zero. An unavailable
result based on latest event time means the source cannot currently satisfy the
declared expectation; it does not by itself prove that an Azure connector is
broken.

## Local use

Validate the public contract and its relationship to the Sentinel bindings:

```powershell
python scripts/check_sentinel_data_sources.py
```

Assess an uncommitted local observation:

```powershell
python scripts/check_sentinel_data_sources.py --observation <local-observation.json>
python scripts/check_sentinel_data_sources.py --observation <local-observation.json> --json
```

Exit code `0` means every source is ready, `2` means at least one source is
degraded, unavailable or unknown, and `1` means the contract or observation is
invalid. Machine-readable output contains only derived status information.

A consumer can collect the required inputs through its own approved read-only
Azure process. `getschema | project ColumnName, ColumnType` provides the schema
shape, and `summarize LatestEvent=max(TimeGenerated)` provides the freshness
input for an existing table. The repository deliberately does not authenticate,
query a workspace or store an observation.

Environment observations can reveal operational state. Keep them in temporary
pipeline storage and do not commit them to the public repository.
