# Microsoft Sentinel KQL preview compilation

The first target compiler is deliberately narrow. It converts only the Sigma implementations listed in `targets/sentinel/preview.json` with the pinned Kusto backend and the Azure Monitor processing pipeline.

Each entry supplies an explicit Log Analytics table. The compiler never guesses a table because the same logical fields can be normalized differently across Sentinel workspaces and connectors. Table names are restricted to Kusto identifiers, source and Golden paths must remain inside the repository, and a source must produce exactly one query.

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
incident settings to the same four bindings. Validate its JSON Schema and the
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
also retained in the render manifest. Entity mappings and alert overrides remain
out of scope until the relevant output columns have their own tested contract.

## Validation boundary

Compiler and Golden-snapshot success prove deterministic source translation only. They do not prove that a query can run in a particular workspace, that the required table is populated, or that a production analytics rule should be deployed.

Renderer success proves only that complete disabled Scheduled-rule request bodies
can be derived deterministically from the reviewed sources. The repository still
contains no Azure client, authentication flow, target scope, deployment command
or live-write capability.

The read-only live probes for `MSEC-DET-0002` through `MSEC-DET-0005` used only aggregate counts in an existing user-authorized Microsoft Sentinel workspace. They established that the bound `SigninLogs` and `AuditLogs` fields were queryable and that all four compiled predicates were accepted. The legacy-client query produced a valid negative result; the high-risk sign-in, service-principal credential, and app-role assignment queries produced valid positive results. No raw rows, user identifiers, tenant identifiers, workspace identifiers, or result counts are stored here. None of these results proves that a detection is production-ready.
