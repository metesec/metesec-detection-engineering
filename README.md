# MeteSec Detection Engineering

Detection-as-Code reference implementation for portable, tested, and reviewable security detections.

> **Project status: Detection Operations — in progress**
> The Sentinel target is complete and four mapped detections render as deterministic, disabled Scheduled rules. The first operations contract now distinguishes usable telemetry from degraded, unavailable or unknown data without adding Azure access.

## Purpose

This project explores how security detections can be managed with the same discipline as production software:

- stable detection identities;
- portable Sigma implementations where appropriate;
- native implementations where platform capabilities require them;
- positive, negative, edge, and regression tests;
- reproducible compilation and packaging;
- explicit telemetry dependencies;
- reviewable lifecycle and releases.

The first working release will focus on a small, complete Sigma detection pack with executable validation and Microsoft Sentinel compilation. Empty vendor directories and unsupported platform claims are deliberately avoided.

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
- [Logical detection manifest v1](docs/contracts/logical-detection-manifest-v1.md)
- [Detection package v1](docs/contracts/detection-package-v1.md)
- [Generated catalogue contract v1](docs/contracts/detection-catalogue-v1.md)
- [Forgejo repository validation](docs/tooling/forgejo-validation.md)
- [Sigma structural validation](docs/tooling/sigma-validation.md)
- [Local Sigma fixture evaluation](docs/testing/sigma-fixture-evaluation.md)
- [Microsoft Sentinel KQL preview compilation](docs/tooling/sentinel-compilation.md)
- [Microsoft Sentinel analytics-rule profile v1](docs/contracts/sentinel-analytics-rule-profile-v1.md)
- [Microsoft Sentinel data-source contract v1](docs/contracts/sentinel-data-source-contract-v1.md)
- [Detection Pack release artifact v1](docs/releases/release-artifact-v1.md)

## Current milestone

`0.3 — Detection Operations` (in progress)

The logical manifest, compact package contract, pinned pySigma boundary, and bounded local fixture evaluator are implemented and locally verified. `MSEC-DET-0001` covers unusual Windows service installation paths. `MSEC-DET-0002` covers successful sign-ins from reported legacy client categories. `MSEC-DET-0003` covers successful Microsoft Entra sign-ins assessed as high risk during sign-in. `MSEC-DET-0004` covers successful credential additions to Microsoft Entra service principals. `MSEC-DET-0005` covers successful application-role grants to Microsoft Entra service principals. Together they have fifteen positive and twenty negative synthetic cases.

The Sentinel preview pins the Kusto backend, maps `MSEC-DET-0002` and `MSEC-DET-0003` to `SigninLogs`, maps `MSEC-DET-0004` and `MSEC-DET-0005` to `AuditLogs`, and verifies all four generated KQL queries against committed Golden snapshots. Separate authorized read-only target probes accepted every generated predicate: the legacy-client result was negative, while the other three results were positive. No raw telemetry, result count, or target identifier is stored, and these results are not deployment or production-readiness claims.

The human-readable `CATALOGUE.md` and machine-readable `catalog/index.json` are generated from the manifests, fixture indexes, and explicit Sentinel preview profile. They contain no runtime timestamp or environment identifier, and `pnpm run check` fails when either tracked output is stale.

The Forgejo validation workflow runs the same aggregate check on trusted pushes and manual dispatch. Its dedicated repository-scoped runner verifies the pinned Node.js and Python toolchain, installs exact pnpm, JavaScript, and Sigma dependencies in disposable job paths, and receives no deployment, cloud, SIEM, Kubernetes or package-publisher credential. Canonical main validation is operational; automatic public pull-request execution remains disabled while the runner uses Forgejo `host` execution mode.

The first release artifact is a deterministic ZIP containing the public five-rule
Detection Pack, its synthetic evidence and the bounded four-rule Sentinel preview.
It includes an internal per-file digest manifest and is published together with a
separate `SHA256SUMS` file. It is not a deployment bundle.

The four preview-bound detections also render into complete Scheduled-rule REST
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
for `SigninLogs` and `AuditLogs`. It links both tables to their exact consuming
detections, defines required Kusto columns and types, and assesses an explicitly
supplied environment observation as `ready`, `degraded`, `unavailable` or
`unknown`. The repository stores no live observation and has no Azure query or
monitoring client.

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

See the [generated catalogue contract](docs/contracts/detection-catalogue-v1.md), [Forgejo validation guide](docs/tooling/forgejo-validation.md), [Sigma validation guide](docs/tooling/sigma-validation.md), [Sentinel compilation guide](docs/tooling/sentinel-compilation.md), and [Sentinel data-source contract](docs/contracts/sentinel-data-source-contract-v1.md) for the exact scope of each result.

## License

Licensed under the [Apache License 2.0](LICENSE).
