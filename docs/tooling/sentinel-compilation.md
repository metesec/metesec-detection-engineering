# Microsoft Sentinel KQL preview compilation

The first target compiler is deliberately narrow. It converts only the Sigma implementations listed in `targets/sentinel/preview.json` with the pinned Kusto backend and the Azure Monitor processing pipeline.

Each version 2 entry supplies an explicit Log Analytics table plus its exact
output contract. The compiler never guesses a table because the same logical
fields can be normalized differently across Sentinel workspaces and connectors.
Table names are restricted to Kusto identifiers, source and Golden paths must
remain inside the repository, and a source must produce exactly one query.

The output contract declares bounded `extend` expressions, the ordered final
columns and the Account, IP or CloudApplication mappings that may consume those
columns. The compiler appends one `project` operator, so the Golden KQL covers
both the Sigma-generated predicate and the complete analyst-facing result shape.
A mapping to an undeclared output column, unsupported identifier, duplicate
field or multi-statement expression fails closed.

The contract follows Microsoft's current
[entity-mapping guidance](https://learn.microsoft.com/azure/sentinel/map-data-fields-to-entities),
[entity identifier reference](https://learn.microsoft.com/azure/sentinel/entities-reference),
[SigninLogs schema](https://learn.microsoft.com/azure/azure-monitor/reference/tables/signinlogs),
[AuditLogs schema](https://learn.microsoft.com/azure/azure-monitor/reference/tables/auditlogs),
[DeviceProcessEvents schema](https://learn.microsoft.com/defender-xdr/advanced-hunting-deviceprocessevents-table),
[DeviceRegistryEvents schema](https://learn.microsoft.com/defender-xdr/advanced-hunting-deviceregistryevents-table)
and
[AADUserRiskEvents schema](https://learn.microsoft.com/azure/azure-monitor/reference/tables/aaduserriskevents).
The rendered request shape follows the stable
[Scheduled alert-rule REST API](https://learn.microsoft.com/rest/api/securityinsights/alert-rules/create-or-update?view=rest-securityinsights-2025-09-01).

## Install and validate

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements-sigma.lock
.\.venv\Scripts\python.exe -m unittest tests.test_sentinel_compiler
.\.venv\Scripts\python.exe scripts\compile_sentinel.py --check
```

`--check` recompiles from source and compares the result with the reviewed Golden KQL under `tests/golden/sentinel/`. It does not write to `dist/`.

To create the ignored local build output:

```powershell
.\.venv\Scripts\python.exe scripts\compile_sentinel.py
```

Generated queries are written to `dist/sentinel/<DETECTION-ID>/query.kql`. They are build artifacts, never hand-edited source.

## Render complete analytics-rule bodies

The separate `targets/sentinel/analytics-rules.json` profile adds explicit
Scheduled-rule frequency, period, threshold, suppression, event-grouping and
incident settings to the same forty-four bindings. Validate its JSON Schema and the
complete renderer with:

```powershell
pnpm run validate:sentinel-profile
python -m unittest tests.test_sentinel_rule_renderer
python scripts/render_sentinel_rules.py --check
```

To create ignored local artifacts:

```powershell
python scripts/render_sentinel_rules.py
```

Each `dist/sentinel/<DETECTION-ID>/` directory then contains the exact Golden
`query.kql`, a disabled `analytics-rule.json` REST request body and a
`render-manifest.json` with stable rule identity, sources and artifact hashes.
The renderer uses Microsoft SecurityInsights API version `2025-09-01` and emits
no subscription, resource-group, workspace or tenant identifier.

The current stable API's `techniques` field receives the ATT&CK base technique.
The logical manifest remains authoritative for the full sub-technique, which is
also retained in the render manifest. Entity mappings are derived only from the
version 2 output contract and use columns returned by the exact Golden query.
Alert overrides and custom details remain out of scope.

ATT&CK's current `Defense Impairment` tactic is retained exactly in the logical
manifest and render provenance. Microsoft SecurityInsights API `2025-09-01`
does not expose that tactic in its `AttackTactic` enum. The renderer therefore
omits only that unsupported target tactic instead of mislabeling it as
`DefenseEvasion`; supported tactics on the same rule remain present.

## Consumer-owned pipeline handoff

The repository deliberately does not publish a second immutable Sentinel target
archive. A consumer who needs environment-specific changes should edit the
versioned target profiles in a reviewed branch and run this sequence inside its
own deployment pipeline:

1. run the complete repository check;
2. render the disabled Sentinel rules to temporary pipeline storage;
3. inspect or validate the generated request bodies against the intended Azure
   scope;
4. deploy through the consumer's separately approved Azure tooling;
5. discard the temporary rendered files.

The consumer owns the Azure identity, target scope, approval gates, post-deploy
read-back and any decision to enable a rule. The MeteSec repository supplies the
reviewed source and deterministic renderer, not those operational controls.

## Validation boundary

Compiler and Golden-snapshot success prove deterministic source translation only. They do not prove that a query can run in a particular workspace, that the required table is populated, or that a production analytics rule should be deployed.

Renderer success proves only that complete disabled Scheduled-rule request bodies
can be derived deterministically from the reviewed sources. The repository still
contains no Azure client, authentication flow, target scope, deployment command
or live-write capability.

The completed read-only live probes for the first thirty-nine bound detections used only
aggregate counts in an existing user-authorized Microsoft Sentinel workspace.
They established that the bound `SigninLogs`, `AuditLogs`,
`DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents` fields were queryable and that all
those thirty-nine generated predicates were accepted. The five Wave 8 predicates
still await the same bounded live acceptance check. No raw rows, user
identifiers, tenant identifiers, workspace identifiers or result counts are
stored here. None of these results proves that a detection is production-ready.
