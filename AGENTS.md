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
2. portable Sigma implementation;
3. validation and behavioral tests;
4. target compilation and packaging;
5. controlled deployment;
6. telemetry and detection health.

The version 1 architectural rule is: one logical detection has one stable
identity and one authored Sigma implementation. Target adapters may compile and
package that source, but generated KQL is not a second authored detection and no
multi-implementation resolver belongs in the active version 1 design.

## Current state

- Public Forgejo repository: `metesec/metesec-detection-engineering`
- Canonical source of truth: MeteSec Forgejo
- GitHub distribution mirror: public at `https://github.com/metesec/metesec-detection-engineering`
- Mirror direction: Forgejo `main` to GitHub `main` only; sync on Forgejo commits
- Mirror authentication: repository-scoped SSH deploy key stored by Forgejo; GitHub Actions, Issues, and Wiki are disabled
- MeteSec Projects page: implemented and public at `https://metesec.com/projects/detection-engineering/`
- Current phase: `0.1 — Functional Foundation`, `0.2 — Microsoft Sentinel Target` and `0.3 — Detection Operations` are complete; `0.4 — Sigma Detection Pack Expansion` is in progress
- Current development-package version: `0.4.0`; the published `v0.1.0` artifact remains immutable and unchanged
- Version 1 release direction: fifty authored Sigma detections, Microsoft Sentinel as the only supported target, and no native-rule or resolver path in the active roadmap
- Expansion baseline: forty-five of fifty planned Sigma detections are implemented; Waves 1 through 7 are complete, Wave 8 is locally implemented and awaits only its bounded live query-acceptance probe, and Wave 9 remains the final expansion milestone
- Logical manifest contract: version 1 implemented as JSON Schema Draft 2020-12
- Contract examples: one valid draft and one deliberately invalid stable-state example
- Structural validation: executable with pinned Ajv `8.17.1`; the valid example is accepted and the invalid example is rejected
- Detection package contract: version 1 documented and enforced through executable filesystem relationship validation
- Fixture-set contract: version 1 schema implemented for future implementation-local positive and negative evidence indexes
- Catalogue: forty-five experimental packages. `MSEC-DET-0001` through `MSEC-DET-0005` retain the original Windows service, Entra sign-in and Entra application-change coverage; Waves 1 through 7 add `MSEC-DET-0006` through `MSEC-DET-0040`; Wave 8 adds `MSEC-DET-0041` CMSTP child-process execution, `MSEC-DET-0042` Odbcconf REGSVR DLL registration, `MSEC-DET-0043` remote Msiexec package installation, `MSEC-DET-0044` remote InstallUtil content and `MSEC-DET-0045` suspicious MSBuild child processes
- Generated discovery catalogue: deterministic `catalog/index.json` and `CATALOGUE.md` are derived from the forty-five manifests, implementation-local fixture indexes, and explicit Sentinel preview profile; neither output contains timestamps, environment identifiers, or live result data
- Catalogue contract and validation: JSON Schema version 1, three generator tests, and a stale-output gate are included in the aggregate repository check; the current output reports forty-five implementations, one hundred thirty-five positive cases, one hundred eighty negative cases, and forty-four Sentinel preview bindings
- Forgejo validation definition: `.forgejo/workflows/validate.yml` runs on trusted pushes and manual dispatch using the repository-specific `metesec-detection-validate` label; it requests read-only contents, removes persisted checkout credentials, references no secrets, pins the sole remote action by commit, verifies exact Node.js `24.19.0` and Python `3.12.13` runner versions, installs pnpm `11.19.0` and exact JavaScript/Sigma dependencies in disposable job paths, then runs the aggregate repository check
- Forgejo workflow contract: four local unit tests verify the trusted trigger set, repository-specific runner selection, permissions, absence of secret and `pull_request_target` use, immutable action references, exact tool versions, disposable installation paths, frozen installation, and the final check command
- Forgejo runtime status: operational on dedicated repository-scoped Runner `metesec-detection-validator`; original proof runs `#1` through `#6` remain recorded, release branch run `#7`, protected-merge main run `#8`, annotated-tag run `#9`, Sentinel renderer branch run `#12` and its protected-main run `#13` all passed
- Branch protection: exact rule `main` disables direct pushes, applies to administrators, blocks rejected reviews and outdated branches, requires zero approvals in the current single-owner phase, and requires exact successful context `Repository validation / Contracts, detections, catalogue, and Sentinel preview (push)`
- First public release: Forgejo tag and release `v0.1.0` target protected main commit `f33f602a2fb6ecbc98475c6de567aa7d9b810ebe`; the release exposes only `metesec-detection-pack-v0.1.0.zip` and `SHA256SUMS`, hides Forgejo's unchecksummed automatic source archives, and the public ZIP is 133,113 bytes with SHA-256 `547f8a66d64d7fac7dc33670a3c3397c77a2a46b737d619a8c498d5abfb2dfc6`
- Release contract: the deterministic uncompressed ZIP has 72 members under one versioned root, including an internal manifest with path, normalized size and SHA-256 for each of 71 allowlisted sources; two independent clean builds and an anonymous post-publication download produced the exact same archive digest
- Local `v0.4.0` candidate: the deterministic release build contains 533 members, including 532 allowlisted sources, all forty-five Sigma packages, 315 synthetic fixtures, forty-four Golden KQL queries and the read-only Sentinel inventory guide; its current size is 935,115 bytes and SHA-256 is `e68926d53051f888f1a1d1e263896986f0bdb307f36cf32c367252b80253df04`, while the published `v0.1.0` remains unchanged
- Portable implementations: forty-five structurally valid Sigma rules, one per package
- Synthetic evidence: one hundred thirty-five positive and one hundred eighty negative flat event fixtures, all explicitly marked synthetic and all passing locally
- Package contract tests: eight passing cases cover the valid draft, identity mismatch, missing implementation, implementation traversal, missing evidence index, valid linked evidence, fixture traversal, and invalid event-fixture structure
- Sigma parser and target toolchain: pySigma `1.5.0`, pySigma Kusto backend `1.0.1`, and every required transitive dependency are pinned in `requirements-sigma.lock`; verified with Python `3.12.13`
- Sigma structural validation: exact-version gate, two-sided in-memory parser self-test, and automatic Package v1 `rule.yml` discovery validate forty-five sources containing forty-five rules
- Sigma validation tests: six passing cases cover valid, missing-condition, malformed-YAML, parser-health, Package v1 discovery, and UTF-8 file paths
- Behavioral test framework: implemented as a deliberately bounded local evaluator over pySigma's condition tree
- Evaluator boundary: flat synthetic events; string and number field comparisons; Sigma wildcard strings; case-insensitive string matching; Boolean `and`, `or`, and unary `not`; unsupported behavior fails closed
- Evaluator tests: six passing unit cases plus 315 passing committed fixture expectations
- Sentinel preview compiler: version 2 implements explicit profile binding, safe table-name validation, repository-contained paths, active-manifest relationship checks, bounded output expressions, exact ordered output columns, entity-mapping validation and deterministic Azure Monitor pipeline output
- Sentinel preview scope: forty-four rules are explicitly bound across `SigninLogs`, `AuditLogs`, `DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents`; all forty-four complete analyst-facing KQL queries match committed Golden snapshots. Audit bindings project initiators as supported entities and keep variable target-resource data neutral unless the resource type is guaranteed; sign-in bindings project normalized Account, IP and CloudApplication context; endpoint bindings project only the observed account name
- Sentinel analytics-rule profile: version 1 JSON Schema and executable loader bind exactly the same forty-four detections to explicit schedule, threshold, suppression, event-grouping and incident settings; missing, additional, duplicated, reordered, active or malformed entries fail closed
- Sentinel analytics-rule renderer: all forty-four bindings produce deterministic Microsoft SecurityInsights API `2025-09-01` Scheduled-rule request bodies plus separate provenance manifests; logical metadata comes from `manifest.json`, KQL and entity mappings come from the reviewed compiler output contract, stable rule UUIDs derive from the immutable detection ID, and every rendered rule is disabled. Current ATT&CK `Defense Impairment` and `Stealth` source mappings remain exact in provenance but are omitted from the older target tactic enum rather than mislabeled as another tactic
- Sentinel entity output: sign-in rules return normalized Account, IP and CloudApplication fields; audit rules return initiating entities and explicitly typed neutral target fields where a target entity would be ambiguous; process rules map the observed account name and the registry rule maps the initiating account name; the user-risk rule maps the Entra account. No Windows SID is mislabeled as an Entra object ID
- Sentinel data-source contract: version 1 covers `SigninLogs`, `AuditLogs`, `DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents` with stable source IDs, exact preview consumers, event-time columns, required Kusto fields and types, and explicit six-hour degraded and one-day unavailable reference thresholds
- Data-source observation evaluator: a separate uncommitted observation can produce only `ready`, `degraded`, `unavailable` or `unknown`; missing observations are never treated as healthy, schema or binding drift fails closed, and eight unit tests cover structure, freshness, missing tables, missing or mistyped fields, future timestamps, unknown sources and CLI exit behavior
- Generated coverage report: deterministic `coverage/index.json` and `COVERAGE.md` derive only from logical manifests, the Sentinel preview and the Sentinel data-source contract; the report records sixty ATT&CK mappings across thirty-five techniques and eleven tactics, six logical data sources, five Sentinel source contracts and the one intentionally unbound detection without a percentage score or live state
- Coverage contract and validation: JSON Schema version 1, six generator tests and a stale-output gate are included in the aggregate repository check; generated coverage output is part of the general Detection Pack release allowlist
- Lifecycle policy: version 1 defines forward-only `draft`, `experimental`, `stable` and `deprecated` transitions and is kept consistent with the logical manifest schema
- Review-cadence validator: existing manifest dates and intervals produce runtime-only `current`, `due` or `overdue` assessments; current validation rejects future or contradictory dates and fails on due or overdue records, while an optional previous catalogue enables identity and transition checks; ten Python tests plus one machine-output schema test cover dates, boundaries, transitions, immutability, removal, CLI exit behavior and the JSON contract
- Sentinel runtime-health contract: a versioned policy derives the expected forty-four rule schedules from `targets/sentinel/analytics-rules.json`; a separate consumer-supplied observation produces only `healthy`, `degraded`, `failed` or `unknown`, using reference boundaries of more than two and more than five missed runs without storing live state
- Alert-outcome boundary: optional alert and incident counts are preserved as informational context only and never influence runtime health; a successful on-time execution with zero alerts is healthy, while missing, disabled, failed or stale rules remain independently visible
- Renderer output boundary: each ignored `dist/sentinel/<DETECTION-ID>/` directory contains `query.kql`, `analytics-rule.json` and `render-manifest.json`; no Azure resource scope, tenant identifier, credential, HTTP client, authentication flow, deployment command or live-write capability exists
- Renderer publication: Forgejo PR `#7` merged through protected `main` as `e8bebd5d3e72218b32378cd3e4f850d047d778ad`; branch run `#12` and merged-main run `#13` passed, and the GitHub distribution mirror resolved to the exact same commit
- Live target probes: authorized read-only workspace checks accepted the first thirty-nine generated predicates in bounded aggregate form. Waves 1 through 6 retain their previously documented mixed baseline results. In Wave 7, `MSEC-DET-0036`, `MSEC-DET-0037`, `MSEC-DET-0038` and `MSEC-DET-0040` returned no match in the current 30-day aggregate baseline; `MSEC-DET-0039` returned a small non-zero aggregate result across several devices and is explicitly tuning-required rather than treated as confirmed malicious activity. The complete generated `DeviceRegistryEvents` query also executed successfully with zero results in the current portal time range. Wave 8 live query acceptance remains pending because the current Defender browser sessions could not be attached and no authenticated Azure CLI was available; no live result is claimed for `MSEC-DET-0041` through `MSEC-DET-0045`. No exact count, raw row, user, device, tenant, subscription or workspace identifier is stored in the repository
- Read-only expansion inventory: workspace metadata confirmed recent candidate source families for Entra identity, Defender endpoint, email, network and Sentinel operations; selected schema-only checks confirmed the fields needed to review a first Sigma wave, while no raw event, live output, environment identifier or copied result is stored in the repository
- Inventory operating guide: `docs/tooling/sentinel-source-inventory.md` provides metadata-only `Usage`, `getschema` and coarse freshness queries, explicitly forbids unrestricted raw-data search and keeps all environment-specific worksheets outside the repository
- `MSEC-DET-0001` remains intentionally unbound because the available target has no suitable Windows event telemetry; it has no Sentinel compatibility claim
- CI pipeline: validation-only Forgejo pipeline is operational for trusted pushes and manual dispatch; public pull-request execution remains intentionally disabled while the dedicated Pod uses Forgejo `host` execution mode without hard per-job container isolation
- Deployment to any SIEM: not implemented and not authorized by this foundation milestone
- Current local validation: the complete aggregate repository check passes with 83 unit tests plus all structural, generated-output and Golden gates; all 315 synthetic fixture expectations pass, forty-four disabled Sentinel rule bodies render successfully and two consecutive deterministic `v0.4.0` release builds produced the same 935,115-byte archive and SHA-256 `e68926d53051f888f1a1d1e263896986f0bdb307f36cf32c367252b80253df04`

## Accepted architecture decisions

- Forgejo is the canonical repository and development workflow.
- GitHub is the read-only public distribution mirror, not a development source or deployment dependency.
- Version 1 uses Sigma as its only authored detection format and targets fifty reviewed rules for the first main release; ADR-0016 supersedes the thirty-rule threshold in ADR-0015 while retaining its Sigma-only, Sentinel-first scope.
- Native implementations and a target resolver are future research only after a concrete target-backed Sigma limitation exists.
- Microsoft Sentinel KQL is the only supported compilation target in version 1, introduced through a bounded non-production preview profile with explicit table bindings.
- Additional SIEMs receive no support claim until real target access, explicit bindings and target-specific validation exist.
- Sentinel output columns and entity mappings are governed together by the version 2 preview profile and the complete generated KQL remains Golden-reviewed.
- Consumers render ignored temporary Sentinel files inside their own controlled pipeline; the project publishes no separate prebuilt Sentinel target archive and implements no Azure deployment client.
- Data-source health is evaluated separately from detection results; an empty or missing observation cannot become a healthy zero.
- Rule execution health is evaluated separately from alert volume; zero alerts never make a successfully executing rule unhealthy.
- Environment-specific tuning, exclusions, allowlists and exceptions are consumer-owned; the public repository provides no customer policy layer.
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

Complete the bounded read-only live query-acceptance probe for `MSEC-DET-0041`
through `MSEC-DET-0045` without storing raw rows, exact counts or target
identifiers. Then research and review Wave 9 toward 50 of 50 Sigma detections
from confirmed target telemetry, adding only non-duplicate mechanisms that
remain faithful and useful as portable Sigma. Do not add native KQL, deploy or
enable Sentinel rules, publish a separate target archive or store raw live query
output. Release readiness begins only after the fifty-rule pack is complete.
Keep public pull-request execution disabled until the runner gains hard per-job
isolation.
