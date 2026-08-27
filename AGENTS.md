# MeteSec Detection Engineering — Project Handoff

Last updated: 2026-08-27 (Europe/Berlin)

Read this file completely before changing the repository, its pipeline, public mirror, schemas, or detection content. Keep `LOGBOOK.md` and `ROADMAP.md` accurate after every completed and verified milestone.

## Collaboration model

- Explain a proposed architecture change before implementing it.
- Work in bounded, verifiable milestones.
- Prefer real, tested functionality over speculative directory trees.
- Use read-only inspection before changing external state.
- Preserve working behavior until its replacement is verified.
- Record failures and corrections in `LOGBOOK.md`; do not hide unsuccessful attempts.
- Do not mark planned capabilities as implemented.

## Project objective

Build a public Detection-as-Code reference implementation that treats detections as versioned, testable, reviewable software artifacts.

The target model separates:

1. detection intent and stable identity;
2. portable or native implementation;
3. validation and behavioral tests;
4. target compilation and packaging;
5. controlled deployment;
6. telemetry and detection health.

The architectural rule is: one logical detection has one stable identity but may have multiple technical implementations. A target resolver must eventually select exactly one approved implementation for a target platform.

## Current state

- Public Forgejo repository: `metesec/metesec-detection-engineering`
- Canonical source of truth: MeteSec Forgejo
- GitHub mirror: planned, not implemented
- MeteSec Projects page: planned, not implemented
- Current phase: `0.1 — Functional Foundation`
- Detection content: not yet implemented
- Test framework: not yet implemented
- CI pipeline: not yet implemented
- Deployment to any SIEM: not implemented and not authorized by this foundation milestone

## Accepted architecture decisions

- Forgejo is the canonical repository and development workflow.
- GitHub will be a read-only public distribution mirror, not a deployment dependency.
- Version 1 is Sigma-first but not Sigma-only.
- Native implementations will be added only for genuine platform-specific behavior.
- The first supported compilation target will be Microsoft Sentinel KQL.
- Detection-local tests live beside the implementation; reusable test code lives centrally.
- Generated build output is never a manually edited source of truth.
- ATT&CK is metadata, not the primary physical folder structure.
- Environment overlays may change approved configuration but never detection logic.
- The large enterprise architecture remains a target model; directories are created only when functionality exists.

See `docs/architecture/adr/` for decision records.

## Intended foundation structure

The `0.1` milestone will grow only as functionality is introduced:

```text
catalog/detections/       logical detection packages
content/portable/sigma/  portable Sigma implementations
governance/schemas/      machine-readable contracts
tests/                    shared validation framework and fixtures
scripts/                  reproducible developer commands
dist/                     generated artifacts only; never hand-edited
docs/                     architecture and operating guidance
```

## Detection-package principles

Each logical detection will eventually include:

- immutable detection ID;
- hypothesis and intended behavior;
- ownership and lifecycle state;
- data-source dependencies;
- severity, confidence, and ATT&CK mappings;
- triage and validation guidance;
- at least one approved implementation;
- positive and negative tests before stable status.

Do not create fifteen files for a trivial rule. Add artifacts only when they carry actual information or executable behavior.

## Testing principles

Keep three claims separate:

1. **Structural validation:** files and metadata satisfy declared schemas.
2. **Behavioral fixture tests:** defined events should or should not match the local evaluator.
3. **Target validation:** a compiled query is accepted and behaves as expected on its target platform.

Compiler success alone is not proof of detection quality or production readiness. Local fixture matching must not be presented as universal SIEM behavior.

## Security and privacy rules

- Never commit credentials, tokens, private keys, cookies, tenant identifiers, customer names, internal addresses, confidential telemetry, or production query results.
- Test fixtures must be synthetic, redacted, or explicitly licensed for public use.
- Do not include real customer exceptions, watchlist values, or operational thresholds.
- Do not run attack simulations against systems without explicit authorization and scope.
- Do not deploy to a production SIEM from this repository without a separately reviewed deployment milestone.
- Dependency and upstream-rule licenses must be recorded before importing content.
- Public examples must distinguish simulated evidence from real incidents.

## Source and mirror boundaries

- Changes are authored, reviewed, tested, and released from Forgejo.
- A future GitHub mirror may receive only a successful, approved public main revision.
- GitHub must receive no Forgejo write credential, cluster credential, registry credential, or infrastructure deployment right.
- Contributions received outside Forgejo require an explicit, documented import workflow before they become canonical.

## Documentation responsibilities

After every completed milestone:

1. verify the implemented behavior;
2. append a chronological entry to `LOGBOOK.md`;
3. update this file to the current verified state;
4. update progress and next action in `ROADMAP.md`;
5. create or supersede an ADR when architecture changes;
6. verify that documentation contains no secret or confidential data;
7. commit documentation with the milestone or immediately afterward.

`AGENTS.md` describes what is true now. `LOGBOOK.md` preserves what happened. `ROADMAP.md` describes what is planned. ADRs explain why important decisions were made.

## Immediate next milestone

Define the minimal logical detection manifest, its JSON Schema, and one valid plus one invalid example. Validate them locally before introducing the first Sigma rule.
