# ADR-0007: Publish a deterministic checksummed Detection Pack

- Status: Accepted
- Date: 2026-09-03

## Context

The functional foundation is validated on canonical Forgejo `main`, but a Git
checkout is not a bounded release product. Consumers need one inspectable bundle
whose exact bytes can be reproduced and verified without implying that the
contained preview queries are approved for deployment.

## Decision

- Publish version `0.1.0` as a deterministic ZIP plus `SHA256SUMS`.
- Package only allowlisted public detection sources, contracts, synthetic
  evidence, catalogue data and the bounded Sentinel preview.
- Normalize text, sort members and fix ZIP metadata so the same source revision
  produces byte-identical output across supported checkouts.
- Include an internal manifest with a SHA-256 digest for every packaged source.
- Keep release generation credential-free in the repository workflow. A trusted
  operator attaches the verified files to the Forgejo release only after the
  protected `main` commit passes validation.
- Do not describe the archive as a deployment bundle or production-ready rule set.

## Consequences

The first release can be downloaded and independently checked while Forgejo
remains the canonical release source. The public GitHub mirror receives the tag
only if its existing main-only mirror policy is deliberately expanded later;
that distribution change is not part of this decision.

Checksums detect accidental or malicious byte changes but do not establish
authorship. Signing can be added later as a separate, reviewed trust milestone.

## Reconsider when

Add a second artifact format only when a real target consumer requires it. Add
release signing when a protected signing identity and rotation/revocation process
exist; do not place a signing credential on the current host-mode runner.
