# Contributing

MeteSec Detection Engineering is in its foundation phase. Contributions should remain small, reviewable, and backed by evidence.

## Before proposing a change

1. Read `AGENTS.md` and `ROADMAP.md`.
2. Check existing Issues and architecture decisions.
3. Do not submit confidential telemetry, customer information, credentials, or real operational exceptions.
4. Confirm that any borrowed content permits redistribution and record its lineage and license.

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

The canonical review workflow runs in MeteSec Forgejo. A future GitHub repository will be a distribution mirror until a contribution-import workflow is explicitly implemented.
