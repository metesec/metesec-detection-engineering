# Read-only Microsoft Sentinel source inventory

This inventory identifies which tables and fields can support the next Sigma
detections. It is a planning input, not a health report, query-performance test
or production-readiness claim.

## Safety boundary

- Run the queries manually in the intended Microsoft Sentinel Logs workspace
  with read-only query permissions.
- Return only table names, column names, column types and coarse freshness
  states. Do not project raw events or identity, device, address, tenant,
  subscription, workspace or customer values.
- Do not commit copied query results, screenshots or environment identifiers.
- Do not use an unrestricted `search *` inventory. It can scan raw data across
  many tables and is unnecessary for this purpose.
- Treat `Usage` as an hourly ingestion-usage signal, not proof that a detection's
  required event semantics or fields are present.

## 1. Find tables with recent ingestion usage

```kusto
Usage
| where TimeGenerated >= ago(30d)
| summarize LastUsageWindow = max(EndTime) by TableName = DataType
| extend Freshness = case(
    LastUsageWindow >= ago(6h), "recent",
    LastUsageWindow >= ago(1d), "delayed",
    "stale"
  )
| project TableName, Freshness
| order by TableName asc
```

The result deliberately omits usage volume, resource URIs and exact timestamps.
It is sufficient to build a candidate-table list without collecting event
content.

## 2. Inspect a candidate table's schema

Replace `CandidateTable` with one reviewed table name from the first query.

```kusto
CandidateTable
| getschema
| project ColumnName, ColumnType
| order by ColumnName asc
```

The schema result may be compared locally with a proposed rule's required
fields. Record only the fields the rule actually needs.

## 3. Classify event freshness without returning an event

```kusto
CandidateTable
| summarize LatestEvent = max(TimeGenerated)
| extend Freshness = case(
    isnull(LatestEvent), "no-data",
    LatestEvent >= ago(6h), "recent",
    LatestEvent >= ago(1d), "delayed",
    "stale"
  )
| project Freshness
```

This query returns only a coarse state. It does not prove completeness,
continuity or correct field population.

## 4. Turn the observation into a rule backlog

Keep the environment-specific worksheet outside the public repository. For each
candidate detection, record only:

- proposed stable detection title;
- Sigma-expressible hypothesis;
- candidate Sentinel table;
- minimum required fields and types;
- current coarse freshness state;
- positive and negative synthetic fixture ideas;
- whether a safe aggregate acceptance probe is possible.

A rule enters an implementation wave only when its hypothesis is useful, its
required fields are observable and its logic can be represented in Sigma. A
table name alone is not sufficient evidence.

## Current repository boundary

`SigninLogs`, `AuditLogs`, `DeviceProcessEvents` and `AADUserRiskEvents` have
explicit contracts and fourteen reviewed Sentinel preview consumers. The
Windows service-installation detection remains portable but intentionally
unbound because the available target has no suitable Windows event telemetry.
