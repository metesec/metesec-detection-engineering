# MeteSec Detection Engineering

Detection-as-Code reference implementation for portable, tested, and reviewable security detections.

> **Project status: Foundation**  
> The repository currently establishes its architecture, governance, and delivery model. Detection content and executable validation will be introduced through the milestones in [ROADMAP.md](ROADMAP.md).

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
- **Public distribution:** a future read-only GitHub mirror
- **Project presentation:** a future MeteSec Projects page
- **Engineering stories:** supporting articles on the MeteSec Blog

Forgejo remains the source of truth. A future GitHub mirror will receive only reviewed public content and will not hold deployment credentials or control the MeteSec infrastructure.

## Documentation

- [Project roadmap](ROADMAP.md)
- [Contributor guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Current project handoff](AGENTS.md)
- [Chronological project log](LOGBOOK.md)
- [Architecture decisions](docs/architecture/adr/)

## Current milestone

`0.1 — Functional Foundation`

The immediate next step is to define the minimal detection-package contract and its JSON Schema before adding the first real Sigma rule.

## License

Licensed under the [Apache License 2.0](LICENSE).
