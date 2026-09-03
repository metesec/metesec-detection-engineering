# Contributing

MeteSec Detection Engineering is a public Detection-as-Code reference project.
Contributions should remain small, reviewable, and backed by evidence.

## Before proposing a change

1. Read `AGENTS.md` and `ROADMAP.md`.
2. Check existing Issues and architecture decisions.
3. Do not submit confidential telemetry, customer information, credentials, or real operational exceptions.
4. Confirm that any borrowed content permits redistribution and record its lineage and license.
5. Install the pinned development dependencies and run `pnpm run check` before proposing a change.

## Detection-quality expectations

A stable detection will eventually require:

- a clear hypothesis;
- a stable ID;
- declared data dependencies;
- positive and negative tests;
- triage guidance;
- references and provenance;
- an explicit lifecycle status;
- transparent platform limitations.

Formatting success or successful compilation alone does not establish detection quality.

## Change workflow

- Create a focused branch.
- Add or update tests with behavior changes.
- Run the documented validation command.
- Explain detection impact and false-positive considerations in the Pull Request.
- Update durable documentation when architecture or project state changes.
- Treat the Forgejo validation result as required evidence, not as permission to deploy.

The canonical review workflow runs in internal MeteSec Forgejo. The public GitHub repository is a read-only distribution mirror; GitHub contributions are not canonical until a contribution-import workflow is explicitly implemented.
