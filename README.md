# MeteSec Detection Engineering

A reviewable detection-as-code baseline for enterprise security teams.
One authored Sigma source per detection, executable regression tests, explicit
telemetry contracts and reproducible Microsoft Sentinel output.

**Current release: 1.1.0 — 67 experimental rules,
66 disabled Sentinel bindings, 10 source contracts.** This is an engineering
baseline, not a production-certified detection service.

## What this repository demonstrates

- Stable logical IDs, owned hypotheses, triage guidance and documented limitations.
- Positive, negative, edge and regression evidence kept next to each source.
- Pinned Sigma/Kusto tooling, strict metadata gates and deterministic query snapshots.
- Explicit distinction between suspicious behavior, sensitive changes and routine administration.
- Source-health, execution-health and lifecycle contracts; no alert-volume success score.
- Recorded provenance, preserved licenses and a reproducible release archive.

The 2026-09-11 review examined all fifty existing rules and all fifty additional
candidate IDs in the supplied archives. Seventeen additions were admitted after
rework; thirty-three were deferred. Existing rules were corrected and reclassified
where their predicates or claims were too broad. Familiar detection techniques
are welcome; copied attribution or invented originality is not.

## Start here

Read the [enterprise adoption guide](docs/enterprise-baseline.md) before choosing
rules. Browse the [generated catalogue](CATALOGUE.md) for every rule's signal
class, confidence, limitations, source fields and test counts. The
[coverage report](COVERAGE.md) describes mappings, not measured attack coverage.

- [Existing rules 0001–0025](docs/reviews/existing-0001-0025.md)
- [Existing rules 0026–0050](docs/reviews/existing-0026-0050.md)
- [All additional candidates 0051–0100](docs/reviews/candidates-0051-0100.md)
- [Provenance and overlap audit](docs/reviews/provenance.md)
- [1.1.0 changes and limits](docs/releases/v1.1.0.md)
- [Architecture decisions](docs/architecture/adr/)
- [Contributing](CONTRIBUTING.md) and [security policy](SECURITY.md)

## Validate and build

Use Node.js 24.19.0, Python 3.12.13 and pnpm 11.19.0, matching the trusted CI
toolchain. Dependencies are pinned. From a checkout or extracted 1.1 source pack:

```sh
python3 -m venv .venv
. .venv/bin/activate
pnpm install --frozen-lockfile
python -m pip install --requirement requirements-sigma.lock
pnpm run check
pnpm run render:sentinel
pnpm run build:release
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell.
Generated temporary artifacts live under `dist/`; the source pack includes a
per-file digest manifest and a separate SHA256SUMS. Never hand-edit Goldens to
silence a failing test; review the source and the generated predicate first.

The aggregate check verifies contracts, canonical ownership, unique UUIDs,
metadata parity, provenance/reviews, synthetic semantics, Golden queries,
disabled rendering, source/runtime health and reproducible packaging.
The offline overlap-report gate rejects stale copy-screening evidence after a
source change; rebuilding the audit requires the documented pinned SigmaHQ clone.
Unsupported evaluator features fail closed. Target execution remains a separate
required evidence level.

## Target and operations boundary

Microsoft Sentinel is the only implemented target adapter. KQL is generated,
not a second authored rule. MSEC-DET-0021 explicitly requires the versioned
Entra raw-event adapter; other Sigma consumers must implement its contract.
MSEC-DET-0001 remains unbound because its Windows System Event dependency is not
implemented in the Sentinel profile.

Scheduled artifacts start disabled, with no automatic incident creation, a
15-minute frequency and a one-hour lookback plus ingestion-time slicing.
These are pilot defaults requiring latency, correctness and volume checks in
the consumer's environment. Current revisions have synthetic evidence only.
Historical v1.0 live probes do not certify rewritten rules or the new schedule.

Environment-specific exclusions, deployment, rollback, incident routing and
monitoring are consumer-owned. Do not commit real telemetry, credentials,
customer identifiers or operational allowlists. Zero alerts does not prove
that a rule is healthy. See the [source contract](docs/contracts/sentinel-data-source-contract-v1.md),
[runtime contract](docs/contracts/sentinel-runtime-health-v1.md) and
[compilation guide](docs/tooling/sentinel-compilation.md).

## Delivery and licensing

MeteSec Forgejo is the canonical authoring/review source. The
[GitHub repository](https://github.com/metesec/metesec-detection-engineering)
is a read-only distribution mirror of reviewed main. The trusted Forgejo
workflow has no deployment credentials and does not execute untrusted PR code.
The reviewed 1.1 source is published on protected canonical `main`, mirrored to
GitHub and packaged by the versioned `v1.1.0` release. [PR #11](https://git.metesec.com/metesec/metesec-detection-engineering/pulls/11)
passed trusted branch and merged-main validation. Published v1.0.0 and v0.1.0
tags/assets remain immutable.

Licensed under [Apache-2.0](LICENSE); retain [NOTICE](NOTICE) and source
attributions. The overlap audit is scoped to a pinned public corpus and does
not establish internet-wide uniqueness or provide a legal clearance.
