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

## Validation boundary

Compiler and Golden-snapshot success prove deterministic source translation only. They do not prove that a query can run in a particular workspace, that the required table is populated, or that a production analytics rule should be deployed.

The read-only live probes for `MSEC-DET-0002`, `MSEC-DET-0003`, and `MSEC-DET-0004` used only aggregate counts in an existing user-authorized Microsoft Sentinel workspace. They established that the bound `SigninLogs` and `AuditLogs` fields were queryable and that all three compiled predicates were accepted. The legacy-client query produced a valid negative result; the high-risk sign-in and service-principal credential queries produced valid positive results. No raw rows, user identifiers, tenant identifiers, workspace identifiers, or result counts are stored here. None of these results proves that a detection is production-ready.
