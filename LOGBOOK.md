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
