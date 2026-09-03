# ADR-0013: Evaluate lifecycle at validation time

- Status: Accepted
- Date: 2026-09-03

## Context

Each detection manifest already records its lifecycle status, creation date,
modified date and review interval. Those fields were structurally validated but
did not yet cause a review reminder or reject impossible date relationships.

A tracked status report containing `overdue` would change merely because time
passed and would make otherwise identical source revisions produce different
generated files.

## Decision

Calculate review due dates during validation from the authored manifest fields.
Use the current UTC date for the normal check and allow an explicit assessment
date for deterministic testing. Fail the check when a record is due or overdue,
but do not commit a runtime assessment.

Store only the versioned transition policy. When a consumer supplies a previous
generated catalogue as a baseline, additionally reject removed identities,
changed creation dates, backward modified dates and forbidden status
transitions. Do not infer Git history or contact a repository service.

## Consequences

- Review cadence is operational rather than decorative metadata.
- The same source tree still produces the same tracked files and release bytes.
- The normal current-state check cannot validate cross-revision transitions
  without an explicit baseline.
- A passing date check confirms timing and structure, not the quality of the
  human review.

## Reconsider when

- the canonical pipeline can provide a trustworthy previous reviewed catalogue;
- signed review evidence becomes a concrete requirement;
- deprecated records need a separate retention cadence.
