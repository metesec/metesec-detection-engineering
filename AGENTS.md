# MeteSec Detection Engineering — Project Handoff

Last updated: 2026-09-03 (Europe/Berlin)

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
- GitHub distribution mirror: public at `https://github.com/metesec/metesec-detection-engineering`
- Mirror direction: Forgejo `main` to GitHub `main` only; sync on Forgejo commits
- Mirror authentication: repository-scoped SSH deploy key stored by Forgejo; GitHub Actions, Issues, and Wiki are disabled
- MeteSec Projects page: implemented and public at `https://metesec.com/projects/detection-engineering/`
- Current phase: `0.1 — Functional Foundation` complete; `0.2 — Microsoft Sentinel Target` is in progress
- Current development-package version: `0.2.0`; the published `v0.1.0` artifact remains immutable and unchanged
- Logical manifest contract: version 1 implemented as JSON Schema Draft 2020-12
- Contract examples: one valid draft and one deliberately invalid stable-state example
- Structural validation: executable with pinned Ajv `8.17.1`; the valid example is accepted and the invalid example is rejected
- Detection package contract: version 1 documented and enforced through executable filesystem relationship validation
- Fixture-set contract: version 1 schema implemented for future implementation-local positive and negative evidence indexes
- Catalogue: five experimental packages: `MSEC-DET-0001` for Windows service installation from selected public-user or temporary paths, `MSEC-DET-0002` for successful Microsoft Entra sign-ins from selected legacy client categories, `MSEC-DET-0003` for successful Microsoft Entra sign-ins assessed as high risk during sign-in, `MSEC-DET-0004` for successful credential additions to Microsoft Entra service principals, and `MSEC-DET-0005` for successful application-role grants to Microsoft Entra service principals
- Generated discovery catalogue: deterministic `catalog/index.json` and `CATALOGUE.md` are derived from the five manifests, implementation-local fixture indexes, and explicit Sentinel preview profile; neither output contains timestamps, environment identifiers, or live result data
- Catalogue contract and validation: JSON Schema version 1, three generator tests, and a stale-output gate are included in the aggregate repository check; the current output reports five implementations, fifteen positive cases, twenty negative cases, and four Sentinel preview bindings
- Forgejo validation definition: `.forgejo/workflows/validate.yml` runs on trusted pushes and manual dispatch using the repository-specific `metesec-detection-validate` label; it requests read-only contents, removes persisted checkout credentials, references no secrets, pins the sole remote action by commit, verifies exact Node.js `24.19.0` and Python `3.12.13` runner versions, installs pnpm `11.19.0` and exact JavaScript/Sigma dependencies in disposable job paths, then runs the aggregate repository check
- Forgejo workflow contract: four local unit tests verify the trusted trigger set, repository-specific runner selection, permissions, absence of secret and `pull_request_target` use, immutable action references, exact tool versions, disposable installation paths, frozen installation, and the final check command
- Forgejo runtime status: operational on dedicated repository-scoped Runner `metesec-detection-validator`; original proof runs `#1` through `#6` remain recorded, release branch run `#7`, protected-merge main run `#8`, annotated-tag run `#9`, Sentinel renderer branch run `#12` and its protected-main run `#13` all passed
- Branch protection: exact rule `main` disables direct pushes, applies to administrators, blocks rejected reviews and outdated branches, requires zero approvals in the current single-owner phase, and requires exact successful context `Repository validation / Contracts, detections, catalogue, and Sentinel preview (push)`
- First public release: Forgejo tag and release `v0.1.0` target protected main commit `f33f602a2fb6ecbc98475c6de567aa7d9b810ebe`; the release exposes only `metesec-detection-pack-v0.1.0.zip` and `SHA256SUMS`, hides Forgejo's unchecksummed automatic source archives, and the public ZIP is 133,113 bytes with SHA-256 `547f8a66d64d7fac7dc33670a3c3397c77a2a46b737d619a8c498d5abfb2dfc6`
- Release contract: the deterministic uncompressed ZIP has 72 members under one versioned root, including an internal manifest with path, normalized size and SHA-256 for each of 71 allowlisted sources; two independent clean builds and an anonymous post-publication download produced the exact same archive digest
- Portable implementations: five structurally valid Sigma rules, one per package
- Synthetic evidence: fifteen positive and twenty negative flat event fixtures, all explicitly marked synthetic and all passing locally
- Package contract tests: eight passing cases cover the valid draft, identity mismatch, missing implementation, implementation traversal, missing evidence index, valid linked evidence, fixture traversal, and invalid event-fixture structure
- Sigma parser and target toolchain: pySigma `1.5.0`, pySigma Kusto backend `1.0.1`, and every required transitive dependency are pinned in `requirements-sigma.lock`; verified with Python `3.12.13`
- Sigma structural validation: exact-version gate, two-sided in-memory parser self-test, and automatic Package v1 `rule.yml` discovery validate five sources containing five rules
- Sigma validation tests: six passing cases cover valid, missing-condition, malformed-YAML, parser-health, Package v1 discovery, and UTF-8 file paths
- Behavioral test framework: implemented as a deliberately bounded local evaluator over pySigma's condition tree
- Evaluator boundary: flat synthetic events; string and number field comparisons; Sigma wildcard strings; case-insensitive string matching; Boolean `and`, `or`, and unary `not`; unsupported behavior fails closed
- Evaluator tests: six passing unit cases plus thirty-five passing committed fixture expectations
- Sentinel preview compiler: explicit profile binding, safe table-name validation, repository-contained paths, active-manifest relationship check, and deterministic Azure Monitor pipeline output are implemented
- Sentinel preview scope: `MSEC-DET-0002` and `MSEC-DET-0003` are explicitly bound to `SigninLogs`, while `MSEC-DET-0004` and `MSEC-DET-0005` are explicitly bound to `AuditLogs`; all four generated KQL queries match committed Golden snapshots
- Sentinel analytics-rule profile: version 1 JSON Schema and executable loader bind exactly the same four detections to explicit schedule, threshold, suppression, event-grouping and incident settings; missing, additional, duplicated, reordered, active or malformed entries fail closed
- Sentinel analytics-rule renderer: all four bindings produce deterministic Microsoft SecurityInsights API `2025-09-01` Scheduled-rule request bodies plus separate provenance manifests; logical metadata comes from `manifest.json`, KQL comes from the reviewed compiler output, stable rule UUIDs derive from the immutable detection ID, and every rendered rule is disabled
- Renderer output boundary: each ignored `dist/sentinel/<DETECTION-ID>/` directory contains `query.kql`, `analytics-rule.json` and `render-manifest.json`; no Azure resource scope, tenant identifier, credential, HTTP client, authentication flow, deployment command or live-write capability exists
- Renderer publication: Forgejo PR `#7` merged through protected `main` as `e8bebd5d3e72218b32378cd3e4f850d047d778ad`; branch run `#12` and merged-main run `#13` passed, and the GitHub distribution mirror resolved to the exact same commit
- Live target probes: authorized read-only workspace checks confirmed populated source fields and accepted all four exact generated predicates; `MSEC-DET-0002` produced a valid negative result, while `MSEC-DET-0003`, `MSEC-DET-0004`, and `MSEC-DET-0005` produced valid positive results, and no raw row, aggregate count, user, device, tenant, subscription, or workspace identifier was stored in the repository
- `MSEC-DET-0001` remains intentionally unbound because the available target has no suitable Windows event telemetry; it has no Sentinel compatibility claim
- CI pipeline: validation-only Forgejo pipeline is operational for trusted pushes and manual dispatch; public pull-request execution remains intentionally disabled while the dedicated Pod uses Forgejo `host` execution mode without hard per-job container isolation
- Deployment to any SIEM: not implemented and not authorized by this foundation milestone

## Accepted architecture decisions

- Forgejo is the canonical repository and development workflow.
- GitHub is the read-only public distribution mirror, not a development source or deployment dependency.
- Version 1 is Sigma-first but not Sigma-only.
- Native implementations will be added only for genuine platform-specific behavior.
- The first supported compilation target is Microsoft Sentinel KQL, introduced through a bounded non-production preview profile with explicit table bindings.
- Detection-local tests live beside the implementation; reusable test code lives centrally.
- Generated build output is never a manually edited source of truth.
- Package v1 uses the logical manifest as its only authored metadata source; no second package descriptor duplicates identity or lifecycle data.
- ATT&CK is metadata, not the primary physical folder structure.
- Environment overlays may change approved configuration but never detection logic.
- The large enterprise architecture remains a target model; directories are created only when functionality exists.

See `docs/architecture/adr/` for decision records.

## Intended foundation structure

The `0.1` milestone will grow only as functionality is introduced:

```text
catalog/detections/       logical detection packages
catalog/index.json        generated machine-readable discovery index
CATALOGUE.md              generated human-readable discovery index
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
- The GitHub mirror receives only the successful, approved public `main` revision.
- GitHub must receive no Forgejo write credential, cluster credential, registry credential, or infrastructure deployment right.
- The Forgejo push mirror uses a repository-scoped GitHub deploy key and a `main` branch filter. The private key stays in Forgejo; only its public half is registered on GitHub.
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

Package the rendered Microsoft Sentinel rule, query and provenance files into an
immutable checksummed target artifact without adding deployment or live-write
capability. Keep public pull-request execution disabled until the runner gains
hard per-job isolation.
