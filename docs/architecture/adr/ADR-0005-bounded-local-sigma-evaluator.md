# ADR-0005: Local Sigma evaluation is deliberately bounded

- Status: Accepted
- Date: 2026-09-03

## Context

Structural Sigma parsing proves that a rule is well formed but does not prove that its positive and negative examples behave as intended. A complete target backend and live SIEM are not part of the Functional Foundation. Building an approximate general-purpose Sigma engine would create a second implementation of the specification and risk false confidence.

## Decision

Use pySigma's parsed condition tree as the source for a small fail-closed local evaluator. Version 1 accepts only one rule and condition, flat explicitly synthetic events, string and number field comparisons, wildcard strings, and Boolean `and`, `or`, and unary `not`. Any other condition or value type raises an unsupported-feature error.

Record local fixture evidence separately from structural parsing, target compilation, and target-SIEM validation. Never use a passing local fixture result as proof of target behavior.

## Consequences

- Positive and negative intent is executable before a target backend exists.
- The evaluator remains small enough to review against the exact rules that use it.
- New Sigma features require an explicit evaluator extension and tests instead of silent approximation.
- The later Sentinel milestone must still compile, inspect, and validate KQL separately.

## Reconsider when

A maintained upstream event-matching implementation provides the needed deterministic fixture semantics, or the growing rule set requires Sigma behavior that cannot remain small and reviewable under this boundary.
