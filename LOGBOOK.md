# MeteSec Detection Engineering — Logbook

This file is an append-only chronological record of completed and verified project milestones. Current state belongs in `AGENTS.md`; future work belongs in `ROADMAP.md`.

## 2026-08-27 — Project direction accepted

### Starting state

MeteSec had no dedicated public project repository. An extensive target architecture for Detection-as-Code had been drafted, covering portable and native implementations, testing, telemetry contracts, deployment, drift, health, and multiple SIEM platforms.

### Decision

- Start a real public Detection-as-Code project.
- Keep the comprehensive architecture as a target model rather than creating a large empty enterprise scaffold.
- Deliver a small functional foundation first: Sigma content, executable tests, generated catalogue, and Microsoft Sentinel compilation.
- Keep Forgejo as the canonical source of truth.
- Add a read-only GitHub mirror later for discoverability and community distribution.
- Present the project through a dedicated MeteSec Projects page and use Blog articles for engineering deep dives.

### Result

The project direction and phased delivery model were accepted. No repository or external service was changed in this decision-only milestone.

## 2026-08-27 — Repository foundation created

### Starting state

The repository name `metesec/metesec-detection-engineering` was available in Forgejo and no local checkout existed.

### Changes

- Created the public Forgejo repository `metesec/metesec-detection-engineering` with anonymous read intent, Issues enabled, Pull Requests enabled, Wiki disabled, and no generated starter commit.
- Added the project README, Apache-2.0 license, contributor guide, security policy, editor configuration, and ignore rules.
- Added separate durable project-control artifacts: `AGENTS.md`, `LOGBOOK.md`, `ROADMAP.md`, and the first architecture decision records.
- Recorded Forgejo as canonical source, GitHub as a future read-only mirror, Sigma-first delivery, and the functional-foundation scope.

### Problems and corrections

- The first repository-creation request used the Forgejo organization endpoint. Forgejo correctly reported that `metesec` is a user rather than an organization. The request was repeated through the user-repository endpoint and succeeded.

### Verification

- The repository was returned by Forgejo as public.
- The empty repository cloned successfully into the local MeteSec workspace.
- Documentation structure and internal links were checked before the initial commit.

### Explicitly untouched

- No GitHub repository or mirror was created.
- No CI pipeline was enabled.
- No detection rule, test framework, compiler, deployment credential, or SIEM integration was created.
- No existing Blog, infrastructure, or production service was changed.

### Result

Foundation documentation is ready for its initial commit. The next milestone is the minimal detection-manifest contract and schema.

## 2026-08-27 — Logical detection manifest v1 verified

### Starting state

The repository documented the intended separation between detection intent and technical implementation but had no machine-readable contract, example manifests, or executable validation.

### Changes

- Added the JSON Schema Draft 2020-12 contract for a version 1 logical detection manifest.
- Defined stable identity, hypothesis, ownership, lifecycle, severity, confidence, telemetry dependencies, ATT&CK mappings, triage, validation state, and implementation references.
- Added a lifecycle guardrail: `stable` requires at least one active implementation plus completed positive and negative tests.
- Added a valid draft example using synthetic Windows service-installation context without claiming an implementation exists.
- Added a deliberately invalid stable example that has no active implementation and no completed behavioral tests.
- Added a small Node.js validator backed by pinned Ajv `8.17.1` and a reproducible pnpm lockfile.
- Documented the contract boundary and local validation commands.

### Problems and corrections

- The workspace did not expose Node.js through the ordinary Windows command path. Validation was run with the bundled project runtime added to the process-local path; no system configuration was changed.
- Ajv strict mode initially rejected nested conditional schema fragments that omitted their explicit object and array types. The schema was corrected rather than weakening strict validation.

### Verification

- The schema compiled successfully under Ajv strict mode.
- `draft-windows-service-install.json` was accepted as valid.
- `stable-without-implementation.json` was rejected for missing positive tests, negative tests, and an active implementation.
- The validation command exited successfully only after both expected outcomes were observed.
- No real telemetry, customer data, credentials, implementation rule, SIEM query, or deployment configuration was introduced.

### Result

The repository now has its first executable quality boundary. The next milestone is the compact detection-package layout; Sigma implementation and behavioral tests remain explicitly pending.

## 2026-08-27 — Public GitHub distribution mirror activated

### Decision

- Keep self-hosted Forgejo as the internal canonical authoring and review system.
- Present GitHub as the only public source-code destination on the MeteSec Website.
- Mirror only the approved `main` branch from Forgejo to GitHub.

### Changes

- Created public repository `metesec/metesec-detection-engineering` on GitHub.
- Disabled GitHub Actions, Issues, and Wiki so the mirror cannot become a parallel workflow or deployment path.
- Performed the initial publication of exact Forgejo `main` revision `03d837931300ce73fd5ac2dd3fb5fe5dc3487b6e`.
- Configured a Forgejo SSH push mirror filtered to `main` with synchronization on new Forgejo commits and no periodic polling.
- Registered only the generated public key as a writable deploy key on the single GitHub repository; the private key remains stored by Forgejo.

### Verification

- Forgejo and GitHub initially resolved to the exact same `main` commit.
- GitHub reported the repository public with `main` as default branch.
- GitHub Actions reported disabled; Issues and Wiki reported disabled.
- No GitHub personal access token, Forgejo credential, deployment credential, or infrastructure access was stored in either repository.

### Result

GitHub is the public distribution surface while Forgejo remains canonical. This documentation commit is also the functional test for automatic post-merge synchronization.

## 2026-09-03 — Compact detection package v1 verified locally

### Starting state

The repository had an executable logical-manifest schema and two contract examples, but no real catalogue package, implementation relationship checks, fixture index contract, or package-level test suite.

### Decision

- Keep the logical manifest as the only authored source for detection identity, intent, lifecycle, telemetry requirements, triage, and implementation references.
- Define Package v1 as an executable filesystem contract rather than introducing a second descriptor with duplicated metadata.
- Allow a compact draft package to contain only `catalog/detections/<ID>/manifest.json`.
- Create implementation and fixture directories only when real executable behavior exists.
- Keep structural package integrity, local behavioral fixture results, and target-platform validation as separate claims.

### Changes

- Added the first real catalogue draft at `catalog/detections/MSEC-DET-0001/manifest.json` for unusual Windows service installation.
- Added `docs/contracts/detection-package-v1.md` with the compact Sigma layout and eight enforced relationship rules.
- Added the machine-readable fixture-set v1 schema for future implementation-local `tests/cases.json` indexes.
- Added a reusable package-contract module and a catalogue validator that checks directory identity, manifest validity, implementation type and path, file existence, evidence claims, fixture identity, unique case IDs, expected case categories, and fixture containment.
- Extended manifest validation to cover real catalogue manifests in addition to valid and deliberately invalid examples.
- Added seven package-contract tests, including repository and fixture path traversal rejection.
- Added one `pnpm run check` command for manifest validation, package-contract tests, and live catalogue validation.
- Updated the README and Roadmap to mark the compact package layout complete and identify the pinned Sigma validation toolchain as the next step.

### Reference input

- Reviewed the user-provided Microsoft Sentinel tables reference as a useful future source for Sentinel telemetry contracts, synthetic target fixtures, field checks, and KQL work.
- Did not copy the document into the repository because Package v1 remains platform-neutral, the document is intentionally Sentinel-specific, and it correctly identifies the live target-workspace schema as the final authority.

### Problems and corrections

- Dependency installation first encountered the sandboxed network boundary. The unchanged frozen lockfile then installed successfully after the approved network retry.
- The first two aggregate `pnpm run check` attempts could not resolve `node` from the ordinary Windows command path. No repository code failed. The existing bundled Node directory was added only to the process-local path, after which the documented aggregate command passed unchanged.

### Verification

- Ajv strict mode compiled both version 1 schemas.
- The valid manifest example and real `MSEC-DET-0001` catalogue manifest were accepted; the deliberately invalid stable manifest remained rejected.
- All seven package-contract tests passed, including valid linked positive/negative evidence and both implementation and fixture traversal rejection.
- Live catalogue validation accepted exactly one draft package with zero implementations.
- `git diff --check` passed and a scoped public-safety scan found no credential, private key, customer, tenant, subscription, or synthetic-domain value in the new catalogue, contract, validator, or tests.
- No Sigma rule, behavioral evaluator, compiled query, deployment configuration, customer data, production telemetry, SIEM change, commit, push, mirror update, Website change, or production rollout occurred.

### Result

The repository now has a compact, executable package boundary and its first real logical catalogue entry without overstating implementation readiness. The next milestone is the pinned Sigma validation toolchain.
