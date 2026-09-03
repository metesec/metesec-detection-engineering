# ADR-0015: Sigma-only authoring and Sentinel-first validation for version 1

- Status: Accepted
- Date: 2026-09-03
- Supersedes: [ADR-0003](ADR-0003-sigma-first-not-sigma-only.md) for the version 1 release scope

## Context

The project currently has five portable Sigma detections and one real target
available for validation: Microsoft Sentinel. Adding a native-rule contract and
target resolver now would create a second authoring path without a target-backed
need. It would also make the first main release harder to understand and test.

The intended first main release is a useful modular foundation with thirty
reviewed detections, not a demonstration of every possible target abstraction.

## Decision

Through the first main release, all detection logic is authored as Sigma. KQL is
generated target output and is never a second hand-authored source of detection
truth.

Microsoft Sentinel is the only supported compilation and target-validation
boundary for version 1. A detection receives a Sentinel compatibility claim only
when its data-source binding, generated KQL, output contract and disabled
analytics-rule rendering pass the repository's Sentinel checks.

The version 1 release target is thirty Sigma detections. Each supported rule must
pass the existing manifest, package, Sigma structure, synthetic positive and
negative fixture, Sentinel compilation, Golden-query, disabled-renderer,
data-source, lifecycle and coverage gates that apply to it.

Native implementations, a multi-implementation resolver and additional SIEM
targets are removed from the active version 1 roadmap. They may be reconsidered
only after a real target and a concrete detection requirement demonstrate that
Sigma cannot represent the necessary behavior safely.

## Consequences

- One logical detection has one authored Sigma implementation in version 1.
- Consumers can adapt the same portable source instead of choosing between
  duplicate authored rules.
- Sentinel remains the only platform for which this repository makes generated
  query and renderer claims.
- A proposed detection that cannot be expressed faithfully in Sigma is deferred
  instead of being implemented as native KQL before version 1.
- Support for Splunk, Elastic, Google SecOps or another SIEM requires later
  target access, explicit bindings, target-specific tests and a new decision.

## Reconsider when

- a real target-backed detection requirement cannot be represented safely in
  Sigma;
- another SIEM is available for repeatable compilation and runtime validation;
- the thirty-rule version 1 pack and its Sentinel validation boundary are
  complete.
