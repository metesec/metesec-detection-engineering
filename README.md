# MeteSec Detection Engineering

Detection-as-Code reference implementation for portable, tested, and reviewable security detections.

> **Project status: Functional Foundation**
> The repository now includes the versioned logical-detection contract, the compact package contract, executable relationship validation, five locally tested experimental Sigma detections, and a bounded Microsoft Sentinel KQL preview for four explicitly mapped rules. Deployment remains a future milestone tracked in [ROADMAP.md](ROADMAP.md).

## Purpose

This project explores how security detections can be managed with the same discipline as production software:

- stable detection identities;
- portable Sigma implementations where appropriate;
- native implementations where platform capabilities require them;
- positive, negative, edge, and regression tests;
- reproducible compilation and packaging;
- explicit telemetry dependencies;
- reviewable lifecycle, exceptions, and releases.

The first working release will focus on a small, complete Sigma detection pack with executable validation and Microsoft Sentinel compilation. Empty vendor directories and unsupported platform claims are deliberately avoided.

## Delivery model

- **Canonical source:** self-hosted MeteSec Forgejo
- **Public distribution:** [GitHub read-only mirror](https://github.com/metesec/metesec-detection-engineering)
- **Project presentation:** the public [MeteSec Projects page](https://metesec.com/projects/detection-engineering/)
- **Engineering stories:** supporting articles on the MeteSec Blog

Forgejo remains the source of truth. GitHub receives only the reviewed public `main` branch through a one-way push mirror and holds no deployment credential or control over MeteSec infrastructure. Public visitors should use GitHub; authoring and review remain internal to Forgejo.

## Documentation

- [Project roadmap](ROADMAP.md)
- [Contributor guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Current project handoff](AGENTS.md)
- [Chronological project log](LOGBOOK.md)
- [Architecture decisions](docs/architecture/adr/)
- [Logical detection manifest v1](docs/contracts/logical-detection-manifest-v1.md)
- [Detection package v1](docs/contracts/detection-package-v1.md)
- [Sigma structural validation](docs/tooling/sigma-validation.md)
- [Local Sigma fixture evaluation](docs/testing/sigma-fixture-evaluation.md)
- [Microsoft Sentinel KQL preview compilation](docs/tooling/sentinel-compilation.md)

## Current milestone

`0.1 — Functional Foundation`

The logical manifest, compact package contract, pinned pySigma boundary, and bounded local fixture evaluator are implemented and locally verified. `MSEC-DET-0001` covers unusual Windows service installation paths. `MSEC-DET-0002` covers successful sign-ins from reported legacy client categories. `MSEC-DET-0003` covers successful Microsoft Entra sign-ins assessed as high risk during sign-in. `MSEC-DET-0004` covers successful credential additions to Microsoft Entra service principals. `MSEC-DET-0005` covers successful application-role grants to Microsoft Entra service principals. Together they have fifteen positive and twenty negative synthetic cases.

The Sentinel preview pins the Kusto backend, maps `MSEC-DET-0002` and `MSEC-DET-0003` to `SigninLogs`, maps `MSEC-DET-0004` and `MSEC-DET-0005` to `AuditLogs`, and verifies all four generated KQL queries against committed Golden snapshots. Separate authorized read-only target probes accepted every generated predicate: the legacy-client result was negative, while the other three results were positive. No raw telemetry, result count, or target identifier is stored, and these results are not deployment or production-readiness claims.

Run the current contract validation with:

```console
pnpm install --frozen-lockfile
python -m venv .venv
.venv\Scripts\activate
pnpm run setup:sigma
pnpm run check
```

See the [Sigma validation guide](docs/tooling/sigma-validation.md) and [Sentinel compilation guide](docs/tooling/sentinel-compilation.md) for the exact scope of each result.

## License

Licensed under the [Apache License 2.0](LICENSE).
