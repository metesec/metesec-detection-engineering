# MeteSec Detection Engineering

Detection-as-Code reference implementation for portable, tested, and reviewable security detections.

> **Project status: Sigma Detection Pack Expansion — 50 of 50 rules implemented**
> Microsoft Sentinel is the only supported target, with forty-nine current rules rendering as deterministic, disabled Scheduled rules and one explicit unsupported Windows Event dependency.

## Purpose

This project explores how security detections can be managed with the same discipline as production software:

- stable detection identities;
- one portable Sigma implementation per detection through version 1;
- positive, negative, edge, and regression tests;
- reproducible compilation and packaging;
- explicit telemetry dependencies;
- reviewable lifecycle and releases.

The first main release targets fifty complete Sigma detections with executable validation and Microsoft Sentinel compilation. KQL is generated output rather than a second authored rule source. Other SIEMs and native implementations remain future work until a real target-backed requirement justifies them. Empty vendor directories and unsupported platform claims are deliberately avoided.

## Delivery model

- **Canonical source:** self-hosted MeteSec Forgejo
- **Public distribution:** [GitHub read-only mirror](https://github.com/metesec/metesec-detection-engineering)
- **Project presentation:** the public [MeteSec Projects page](https://metesec.com/projects/detection-engineering/)
- **Engineering stories:** supporting articles on the MeteSec Blog

Forgejo remains the source of truth. GitHub receives only the reviewed public `main` branch through a one-way push mirror and holds no deployment credential or control over MeteSec infrastructure. Public visitors should use GitHub; authoring and review remain internal to Forgejo.

Environment-specific tuning, exclusions and allowlists belong to the consumer's
own reviewed pipeline. This repository supplies the modular contracts, rules,
tests and rendering boundary without prescribing customer policy.

## Documentation

- [Project roadmap](ROADMAP.md)
- [Contributor guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Current project handoff](AGENTS.md)
- [Chronological project log](LOGBOOK.md)
- [Architecture decisions](docs/architecture/adr/)
- [Generated detection catalogue](CATALOGUE.md)
- [Machine-readable detection catalogue](catalog/index.json)
- [Generated ATT&CK and data-source coverage](COVERAGE.md)
- [Machine-readable coverage report](coverage/index.json)
- [Logical detection manifest v1](docs/contracts/logical-detection-manifest-v1.md)
- [Detection package v1](docs/contracts/detection-package-v1.md)
- [Generated catalogue contract v1](docs/contracts/detection-catalogue-v1.md)
- [Forgejo repository validation](docs/tooling/forgejo-validation.md)
- [Sigma structural validation](docs/tooling/sigma-validation.md)
- [Local Sigma fixture evaluation](docs/testing/sigma-fixture-evaluation.md)
- [Microsoft Sentinel KQL preview compilation](docs/tooling/sentinel-compilation.md)
- [Read-only Microsoft Sentinel source inventory](docs/tooling/sentinel-source-inventory.md)
- [Microsoft Sentinel analytics-rule profile v1](docs/contracts/sentinel-analytics-rule-profile-v1.md)
- [Microsoft Sentinel data-source contract v1](docs/contracts/sentinel-data-source-contract-v1.md)
- [Generated detection coverage report v1](docs/contracts/detection-coverage-report-v1.md)
- [Detection lifecycle and review cadence v1](docs/contracts/detection-lifecycle-v1.md)
- [Microsoft Sentinel runtime health v1](docs/contracts/sentinel-runtime-health-v1.md)
- [Detection Pack release artifact v1](docs/releases/release-artifact-v1.md)

## Current milestone

`0.4 — Sigma Detection Pack Expansion` (in progress)

The version 1 direction is deliberately narrow: all detection logic is authored
as Sigma, Microsoft Sentinel is the only supported target, and the first main
release requires fifty reviewed detections. The existing target compiler,
Golden queries and disabled analytics-rule renderer remain the Sentinel proof
boundary. Native rules and a multi-implementation resolver are not part of the
active version 1 roadmap.

A read-only Sentinel source inventory has now confirmed candidate Entra,
endpoint, email, network and Sentinel operating-data families. The inventory
returned only table metadata, selected schema fields and coarse freshness
states; no raw event, identity, device, tenant, subscription, workspace or
customer value is stored in this repository. Nine bounded implementation waves
have now selected only sources whose fields are available and whose behavior can
be expressed and tested faithfully in Sigma. Wave 7 also introduced the first
explicit `DeviceRegistryEvents` contract after its required fields and current
target availability were verified read-only.

The logical manifest, compact package contract, pinned pySigma boundary, and bounded local fixture evaluator are implemented and locally verified. The catalogue now contains fifty authored Sigma detections. Wave 9 adds suspicious script or LOLBin payloads in Run keys, non-default Winlogon Shell or Userinit values, suspicious local scheduled-task creation, Mavinject process injection and Netsh PortProxy creation. The initial broad Run/RunOnce candidate was rejected as too noisy and retained only after narrowing it to behavior-bearing script and LOLBin payloads. A blanket successful Device Code sign-in candidate was also rejected because legitimate use could not be separated faithfully in a portable single-event Sigma rule; Netsh PortProxy creation replaced it. Together the catalogue has one hundred fifty positive and two hundred negative synthetic cases.

The Sentinel preview pins the Kusto backend and binds forty-nine detections across `SigninLogs`, `AuditLogs`, `DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents`; all forty-nine generated KQL queries match committed Golden snapshots. Separate authorized read-only target probes accepted all forty-nine generated predicates in bounded aggregate form. All five final Wave 9 predicates returned no match in the current 30-day aggregate baseline. Earlier mixed baseline results, including the Wave 8 remote-MSI tuning signal, remain query-acceptance evidence rather than confirmed malicious activity. No raw telemetry, exact result count, target identifier or identifying result is stored, and no result is a deployment or production-readiness claim.

The human-readable `CATALOGUE.md` and machine-readable `catalog/index.json` are generated from the manifests, fixture indexes, and explicit Sentinel preview profile. They contain no runtime timestamp or environment identifier, and `pnpm run check` fails when either tracked output is stale.

The Forgejo validation workflow runs the same aggregate check on trusted pushes and manual dispatch. Its dedicated repository-scoped runner verifies the pinned Node.js and Python toolchain, installs exact pnpm, JavaScript, and Sigma dependencies in disposable job paths, and receives no deployment, cloud, SIEM, Kubernetes or package-publisher credential. Canonical main validation is operational; automatic public pull-request execution remains disabled while the runner uses Forgejo `host` execution mode.

The first release artifact is a deterministic ZIP containing the public five-rule
Detection Pack, its synthetic evidence and the bounded four-rule Sentinel preview.
It includes an internal per-file digest manifest and is published together with a
separate `SHA256SUMS` file. It is not a deployment bundle.

The forty-nine preview-bound detections also render into complete Scheduled-rule REST
request bodies through the versioned Sentinel analytics-rule profile. Logical
metadata continues to come from each detection manifest, KQL must match its
reviewed Golden query, and each stable Sentinel rule UUID is derived from the
immutable detection ID. Every rendered rule is disabled and contains no Azure
scope or credential. The preview profile governs the final analyst-facing KQL
columns and exact Account, IP and CloudApplication mappings. Generated rule,
query and provenance files remain ignored temporary output. Consumers render
and deploy them inside their own reviewed pipeline; no separate prebuilt
Sentinel target archive or deployment client is shipped here.

The first Detection Operations capability is an executable data-source contract
for `SigninLogs`, `AuditLogs`, `DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents`. It links each table to its exact consuming
detections, defines required Kusto columns and types, and assesses an explicitly
supplied environment observation as `ready`, `degraded`, `unavailable` or
`unknown`. The repository stores no live observation and has no Azure query or
monitoring client.

The generated coverage report now joins those declarations into one factual
view of the declared ATT&CK techniques and tactics, six logical data sources,
five Sentinel source contracts and one intentionally unbound Sentinel detection.
It reports exact repository relationships rather than an invented coverage
percentage and contains no live environment state.

Lifecycle metadata is now executable rather than decorative. The local and CI
check derives each review due date from the manifest's modified date and review
interval, rejects future or contradictory dates, and fails when a review is due
or overdue. An optional previous catalogue enables forward-only status and
identity checks without embedding Git or Forgejo access in the tool.

The final operations contract derives expected rule executions from the forty-nine
Sentinel schedules. A consumer-supplied local observation distinguishes
`healthy`, `degraded`, `failed` and `unknown` rules using explicit missed-run
boundaries. Optional alert and incident counts are informational only: a
successful execution with zero alerts is healthy. The repository stores no live
observation and contains no Sentinel monitoring client.

Run the current contract validation with:

```console
pnpm install --frozen-lockfile
python -m venv .venv
.venv\Scripts\activate
pnpm run setup:sigma
pnpm run check
pnpm run render:sentinel
pnpm run build:release
```

See the [generated catalogue contract](docs/contracts/detection-catalogue-v1.md), [Forgejo validation guide](docs/tooling/forgejo-validation.md), [Sigma validation guide](docs/tooling/sigma-validation.md), [Sentinel compilation guide](docs/tooling/sentinel-compilation.md), [read-only source-inventory guide](docs/tooling/sentinel-source-inventory.md), [Sentinel data-source contract](docs/contracts/sentinel-data-source-contract-v1.md), and [Sentinel runtime-health contract](docs/contracts/sentinel-runtime-health-v1.md) for the exact scope of each result.

## License

Licensed under the [Apache License 2.0](LICENSE).
