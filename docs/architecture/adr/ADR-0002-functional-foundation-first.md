# ADR-0002: Build a functional foundation before the full platform

- Status: Accepted
- Date: 2026-08-27

## Context

The target architecture includes multiple SIEM adapters, implementation resolution, telemetry contracts, exceptions, backtesting, deployment, health, drift, and observability. Creating all planned directories immediately would make the repository appear more complete than its functioning capabilities.

## Decision

Version 0.1 will implement a compact but complete vertical slice: logical detection contract, Sigma implementation, executable fixture tests, generated catalogue, Forgejo validation, and later Microsoft Sentinel compilation. Additional modules are introduced only with working behavior and verification.

## Consequences

- Early releases remain understandable and credible.
- Target architecture is preserved in the roadmap without empty scaffolding.
- New platform claims require an implementation milestone.

## Reconsider when

The functional foundation exit criteria are satisfied and the next target requires a new module.
