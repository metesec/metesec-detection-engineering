# ADR-0016: Expand the version 1 release target to fifty Sigma rules

- Status: Accepted
- Date: 2026-09-03
- Supersedes: [ADR-0015](ADR-0015-sigma-only-sentinel-first-v1.md) only for the version 1 rule-count and release-readiness threshold

## Context

The original thirty-rule target established a useful Sigma-only, Sentinel-first
foundation. Once Wave 5 reached that boundary, the same contracts, fixtures,
compiler, Golden review and disabled renderer continued to support additional
bounded rule waves without adding another authoring path or target abstraction.

The user chose to continue the main pack to fifty rules before the first main
release. Starting release preparation at thirty would therefore create a public
milestone that no longer matches the intended content scope.

## Decision

The version 1 release target is fifty authored Sigma detections. Expansion
continues in five-rule waves, and every supported rule must pass all applicable
manifest, package, Sigma structure, synthetic fixture, Sentinel compilation,
Golden-query, disabled-renderer, source, lifecycle and coverage gates.

Microsoft Sentinel remains the only supported target. KQL remains generated
output rather than a second authored rule source. Native rules, additional SIEMs,
environment-specific exception objects, prebuilt target artifacts and deployment
automation remain outside this scope.

Release-readiness review and protected-main `v1.0.0` publication begin only after
the fifty-rule pack is complete and verified.

## Consequences

- Waves 6 through 9 extend the existing pack from thirty to fifty rules.
- The repository may describe 30/50 as a historical checkpoint, but not as a
  completed version 1 release boundary.
- Candidate selection remains evidence-led and bounded; the count does not
  justify weak, duplicate or target-incompatible detections.
- The existing one intentionally unbound Windows Event rule keeps its explicit
  unsupported Sentinel status until suitable telemetry exists.

## Reconsider when

- all fifty rules and their Sentinel validation boundary are complete;
- a target-backed requirement cannot be represented safely in Sigma;
- another SIEM is available for repeatable compilation and target validation.
