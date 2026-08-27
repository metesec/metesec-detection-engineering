# ADR-0001: Forgejo is the canonical source of truth

- Status: Accepted
- Date: 2026-08-27

## Context

MeteSec operates a self-hosted Forgejo platform and wants the Detection-as-Code project to remain operable without depending on an external code-hosting provider. GitHub offers valuable discoverability and familiar public collaboration surfaces.

## Decision

Forgejo is the canonical repository, review workflow, pipeline origin, and release source. A future GitHub repository will be an automatically synchronized read-only public mirror.

## Consequences

- Development and release remain under MeteSec control.
- GitHub availability does not block canonical work.
- Mirror automation must be one-way and must not receive infrastructure credentials.
- GitHub-originated contributions require a later explicit import design.

## Reconsider when

A secure bidirectional contribution workflow is designed and its ownership, conflict handling, and security boundaries are documented.
