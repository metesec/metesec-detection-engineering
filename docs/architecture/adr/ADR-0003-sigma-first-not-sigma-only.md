# ADR-0003: Sigma-first, not Sigma-only

- Status: Accepted
- Date: 2026-08-27

## Context

Sigma provides a portable detection format and an established ecosystem, but some detections require target-specific joins, baselines, entity mappings, watchlists, or incident behavior.

## Decision

General detection logic is authored in Sigma where the semantics are portable. A native implementation may represent the same stable detection identity when genuine platform capabilities are required. The future target resolver must select exactly one approved implementation per detection and target.

## Consequences

- Portability is preferred without pretending all detection semantics are portable.
- Native implementations require an explicit reason and shared detection identity.
- Simple field translation belongs in adapters, not duplicate native rules.

## Reconsider when

Practical implementation experience shows that the identity or precedence model cannot represent required platform behavior safely.
