# ADR-0014: Separate rule execution health from alert volume

- Status: Accepted
- Date: 2026-09-03

## Context

A scheduled detection can execute correctly and find nothing. Conversely, a
non-zero alert count does not prove that the current rule exists, is enabled or
continues to execute on schedule. Using alert volume as a health signal would
therefore create false failures during quiet periods and false confidence during
stale or broken operation.

The public repository also cannot know a consumer's workspace, deployment
state, collection method or acceptable operational thresholds.

## Decision

Assess runtime health only from consumer-supplied evidence that an expected rule
exists, is enabled and has a recent execution result. Derive expected frequency
from the authored Sentinel analytics-rule profile and apply explicit reference
missed-run multipliers from a separate versioned policy.

Carry optional alert and incident counts as informational outcome context only.
They never promote or reduce health. Keep observations and assessments outside
the repository and require each consumer to supply its own collection adapter.
Do not add Azure authentication, querying or deployment behavior.

## Consequences

- A successful zero-alert execution is healthy.
- Missing, disabled, failed or late rules are distinguishable from quiet rules.
- Contract validation in CI cannot be mistaken for live operational monitoring.
- Consumers may adjust the reference multipliers in their own reviewed pipeline.
- Detection effectiveness, tuning quality and response outcomes remain separate
  concerns.

## Reconsider when

- a portable vendor-supported execution-evidence interface becomes stable;
- a concrete canary or read-back milestone is approved;
- the project defines performance or outcome-quality contracts separately.
