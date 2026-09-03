# MeteSec Detection Engineering

Detection-as-Code reference implementation for portable, tested, and reviewable security detections.

> **Project status: Functional Foundation**
> The repository now includes the versioned logical-detection contract, the compact package contract, executable relationship validation, and its first real catalogue draft. Detection implementations and executable behavioral tests remain future milestones tracked in [ROADMAP.md](ROADMAP.md).

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

## Current milestone

`0.1 — Functional Foundation`

The logical manifest and compact package contracts are implemented and locally verified. `MSEC-DET-0001` is a real catalogue draft with no implementation claim. The next step is to pin the Sigma validation toolchain before adding its first portable rule.

Run the current contract validation with:

```console
pnpm install --frozen-lockfile
pnpm run check
```

## License

Licensed under the [Apache License 2.0](LICENSE).
