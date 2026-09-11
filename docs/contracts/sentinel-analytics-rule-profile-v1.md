# Microsoft Sentinel analytics-rule profile v1

The analytics-rule profile adds only Microsoft Sentinel Scheduled-rule settings
to detections that already have an explicit table binding and a reviewed Golden
KQL query. It does not duplicate logical title, description, severity, ATT&CK
mapping, ownership or triage metadata from `manifest.json`.

The executable JSON Schema is
`governance/schemas/sentinel-analytics-rule-profile-v1.schema.json`; the current
profile is `targets/sentinel/analytics-rules.json`.

## Contract

The profile header fixes:

- schema version `1`;
- target `microsoft-sentinel`;
- stable Microsoft SecurityInsights API version `2025-09-01`;
- source profile `targets/sentinel/preview.json`.

Every rule entry must correspond exactly, and in the same order, to one binding
in the source profile. It supplies:

- query frequency and lookback period as ISO 8601 durations;
- trigger operator and non-negative threshold;
- suppression duration and state;
- event grouping mode;
- incident creation state and grouping lookback.

Version 1 requires both the rule and suppression to remain disabled. The Python
loader independently enforces the same restriction as the JSON Schema and fails
on missing, additional, duplicated or reordered rule bindings.

The loader also requires 5 minutes <= frequency <= period <= 14 days,
suppression duration of 5 minutes–1 day and incident lookback of 5 minutes–7 days.
Current pilot settings are 15-minute frequency, one-hour period, disabled rules
and no automatic incident creation. A syntactically valid duration is not enough.

## Derived fields

The renderer derives the remaining values instead of introducing a second
source of truth:

- display name, description and severity from the logical manifest;
- KQL from the pinned compiler and reviewed Golden query, then a deterministic
  event-time lookback and ingestion-time slice derived from schedule settings;
- entity mappings from the source profile's governed output contract;
- Sentinel tactic names from the manifest ATT&CK mapping;
- stable rule UUID as UUIDv5 of
  `https://metesec.com/detections/<DETECTION-ID>`;
- base ATT&CK technique IDs for the stable API's `techniques` property.

The complete sub-technique mapping remains in the generated provenance
manifest. Version 2 of the source profile supplies the exact KQL output columns
and entity mappings; the renderer cannot invent or override them. Custom details
and alert overrides remain absent. The renderer itself compares the compiled
query with the Golden file before it constructs any rule body, so the safety
check does not depend on command order.

## Rendered output

`python scripts/render_sentinel_rules.py` writes three generated files per bound
detection under `dist/sentinel/<DETECTION-ID>/`:

- `query.kql` — the derived scheduled query, not the unwindowed hunting Golden;
- `analytics-rule.json` — the exact Scheduled alert-rule REST request body;
- `render-manifest.json` — API version, stable rule ID, source paths, output
  columns, entity mappings, complete ATT&CK provenance and SHA-256 hashes for
  both generated artifacts.

The JSON request body matches the body used with:

```text
PUT .../providers/Microsoft.SecurityInsights/alertRules/{ruleId}?api-version=2025-09-01
```

No subscription, resource group, workspace, tenant or credential is rendered.
No HTTP client, Azure authentication or deployment command exists in this
milestone.

The time filters are inserted directly after the table, before adapters and
projection. The manifest includes the source Golden hash and hashes the final
scheduled artifact. Ingestion policy/nulls, scheduler gaps, replay, late data and
multiple target rows require consumer validation; no exactly-once guarantee is
made. See [the adoption guide](../enterprise-baseline.md).

Generated files are temporary consumer-owned pipeline output. They are not a
separate published Sentinel release artifact and remain ignored by the source
repository.
