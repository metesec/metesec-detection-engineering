# ADR-0004: Behavioral tests live near implementations

- Status: Accepted
- Date: 2026-08-27

## Context

Detection behavior is easiest to review when the rule and its positive, negative, edge, and regression examples evolve together. Test execution and schema validation should remain reusable rather than duplicated per rule.

## Decision

Implementation-specific fixtures and assertions live beside their implementation. Shared evaluators, validators, and integration harnesses live under the central `tests/` framework.

## Consequences

- Behavioral intent is visible during rule review.
- Shared tooling avoids per-rule test-code duplication.
- Structural, local fixture, compiler, and target-platform claims remain explicitly separated.

## Reconsider when

Repository scale or fixture reuse demonstrates that a different physical layout materially improves ownership without separating tests from reviewed behavior.
