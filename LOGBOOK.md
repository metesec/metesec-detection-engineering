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

## 2026-09-03 — Pinned Sigma structural validation verified locally

### Starting state

The repository could validate logical manifests and package relationships but had no installed or pinned Sigma parser. A future `rule.yml` could therefore exist without an executable Sigma syntax and structure check.

### Decision

- Pin pySigma as the smallest vendor-neutral parsing boundary required by the current milestone.
- Defer `sigma-cli`, conversion backends, processing pipelines, KQL output, and SIEM connectivity until a real target-compilation milestone uses them.
- Require an exact pySigma runtime version and pin every transitive dependency observed during the verified resolution.
- Make a zero-rule validation run meaningful through a two-sided parser self-test while explicitly refusing to treat it as a detection implementation or behavioral result.

### Changes

- Added `requirements-sigma.lock` with pySigma `1.5.0` and all resolved direct and transitive packages fixed to exact versions.
- Added reusable Sigma validation code for UTF-8 sources, collected pySigma parser errors, Package v1 source discovery, and parser health verification.
- Added a command that rejects the wrong pySigma version, proves a valid synthetic rule parses, proves a deliberately invalid synthetic rule fails, and validates every future `content/portable/sigma/<ID>/rule.yml` entry point.
- Added six standard-library unit tests for valid input, missing condition, malformed YAML, parser-health behavior, exact Package v1 discovery, and UTF-8 file validation.
- Added setup and validation commands to the existing pnpm workflow and documented the structural-only boundary.
- Updated the README, Roadmap, and project handoff to mark the pinned parser milestone complete and retain the first real Sigma implementation as the next milestone.

### Problems and corrections

- The first package-index query encountered the sandboxed network boundary and returned no distributions. The same read-only query succeeded after the approved network retry and confirmed pySigma `1.5.0` and sigma-cli `3.1.0` as the available current releases.
- Sigma CLI was considered but deliberately not installed: its present role is conversion and plugin-backed target output, neither of which this milestone implements.

### Verification

- pySigma `1.5.0` installed successfully in the repository-local ignored virtual environment under Python `3.12.13`.
- All six Sigma-validation unit tests passed.
- The valid in-memory parser probe produced exactly one rule and the deliberately invalid probe was rejected for its missing condition.
- Repository Sigma validation passed with zero source files and printed the explicit no-behavior-claim notice.
- `pip check` reported no broken requirements.
- No Sigma implementation, fixture evidence, local evaluator, compiled query, target backend, deployment configuration, customer data, production telemetry, SIEM change, push, mirror update, Website change, or production rollout was introduced.

### Result

The repository now has a pinned and executable Sigma structural-validation boundary without overstating rule, behavior, compiler, or target readiness. The next milestone is the first portable implementation and explicitly synthetic positive and negative evidence for `MSEC-DET-0001`.

## 2026-09-03 — First complete experimental Sigma detection verified locally

### Starting state

`MSEC-DET-0001` existed only as a draft logical record. The repository could parse future Sigma files but had no rule, synthetic event contract, local behavior evaluator, or positive and negative evidence.

### Decision

- Narrow the original broad service-installation hypothesis to Service Control Manager event 7045 with an image path in selected public-user or temporary directories.
- Use pySigma's parsed condition tree rather than re-parsing Sigma YAML into a second ad hoc rule model.
- Implement only a documented, fail-closed local subset instead of presenting a partial evaluator as a complete Sigma engine.
- Keep the detection `experimental` and keep local fixture evidence separate from future KQL compilation and Sentinel validation.

### Source basis

- The official Sigma rule specification defines case-insensitive string values, field maps, Boolean conditions, and modifier-derived wildcard behavior.
- SigmaHQ's public rule catalogue confirms the Windows System log-source convention with `Provider_Name: Service Control Manager` and `EventID: 7045` for service installation.
- MITRE ATT&CK T1543.003 documents Windows service creation or modification as persistence and possible privilege escalation behavior.

### Changes

- Added the first portable rule at `content/portable/sigma/MSEC-DET-0001/rule.yml` with one stable Sigma UUID, Windows System log source, event/provider selection, and three path indicators.
- Added three positive and four negative synthetic event fixtures covering public-user, Windows Temp, user-profile Temp, Program Files, a different event ID, a different provider, and System32.
- Added a version 1 synthetic-event JSON Schema requiring an explicit `synthetic: true` declaration and a non-empty flat event object.
- Extended package validation to parse and validate every referenced event fixture and added an eighth package-contract regression test.
- Added a bounded evaluator over pySigma's condition tree with string, number, wildcard, case-insensitive, `and`, `or`, and unary `not` support. Unsupported Sigma behavior fails closed.
- Added six evaluator unit tests and one repository command that executes every implementation-local fixture expectation.
- Updated the manifest to `experimental`, declared the Sigma source active, recorded the exact field contract, and marked positive and negative local tests complete only after all committed cases passed.
- Added ADR-0005, the evaluator boundary guide, and updated the package contract, README, Roadmap, and project handoff.

### Problems and corrections

- The first strict Ajv compilation rejected the event schema's array form of the JSON Schema `type` keyword. The schema was rewritten with explicit `anyOf` branches; strict mode remained enabled and then compiled successfully.
- The first scoped public-safety command passed a nested PowerShell array to `Select-String`, which emitted a non-terminating type error and therefore did not perform the intended scan. The check was immediately repeated against the committed diff with a terminating failure path; it passed, and every synthetic computer name was separately confirmed to use the reserved `example.invalid` domain.

### Verification

- Manifest validation accepted the experimental catalogue entry and retained the deliberately invalid stable-example rejection.
- Package validation accepted one package with one implementation and validated all seven referenced event fixtures.
- All eight package-contract tests passed, including rejection of a fixture that does not satisfy the synthetic-event schema.
- pySigma `1.5.0` structurally accepted the single rule.
- All six parser tests and all six evaluator unit tests passed.
- All seven committed fixture expectations passed: three expected matches and four expected non-matches.
- The case-insensitive path/provider example matched; missing fields and unsupported keyword expressions failed safely.
- The aggregate `pnpm run check`, Python bytecode compilation, and `git diff --check` passed.
- The corrected committed-diff sensitive-value scan and reserved synthetic-hostname check passed.
- No real event, customer value, credential, production telemetry, KQL, target backend, deployment configuration, SIEM connection, push, mirror update, Website change, or production rollout was introduced.

### Result

`MSEC-DET-0001` is the repository's first complete experimental Sigma package with executable local behavior evidence. The next Functional Foundation work is to repeat the reviewed package pattern toward five detections before target compilation and deployment are claimed.

## 2026-09-03 — Second detection and bounded Sentinel preview verified locally and read-only

### Starting state

The repository had one portable Windows event detection with local synthetic evidence but no target compiler, table binding, Golden KQL, or target-platform validation. The authorized Microsoft Sentinel environment contained real data but no Windows event table suitable for `MSEC-DET-0001`.

### Decision

- Keep `MSEC-DET-0001` unchanged and make no target claim where its required telemetry is absent.
- Add a second detection that uses a populated Sentinel-native identity table rather than manufacturing a positive result for the first rule.
- Bind target tables explicitly in a non-production preview profile; never let the compiler guess a workspace table.
- Keep compiler success, local fixture behavior, read-only target acceptance, and deployment as separate claims.
- Store no production row, result count, target identifier, user, device, address, or customer value in the public repository.

### Source basis

- Microsoft documents `SigninLogs.ClientAppUsed` as the reported client used for sign-in activity and `ResultType` value `0` as success.
- Microsoft's legacy-authentication workbook treats specific mail-protocol client categories such as Exchange ActiveSync as legacy authentication indicators requiring review.
- The official Sigma plugin directory and Kusto backend identify the Azure Monitor processing pipeline as an available KQL compilation route.

### Changes

- Added experimental package `MSEC-DET-0002` for a successful Microsoft Entra sign-in from one of seven selected legacy client categories.
- Added three positive and four negative synthetic fixtures covering successful legacy categories, failed legacy activity, modern browser and desktop clients, and a missing client category.
- Pinned pySigma Kusto backend `1.0.1` beside pySigma `1.5.0`.
- Added a bounded Sentinel preview profile that maps only `MSEC-DET-0002` to `SigninLogs` and records no tenant or workspace value.
- Added deterministic Python compilation with an exact backend-version gate, safe Kusto table identifiers, repository path containment, active-manifest relationship validation, and exactly-one-query enforcement.
- Added one reviewed Golden KQL snapshot, three compiler tests, a no-write Golden verification command, and an ignored local `dist` build command.
- Added ADR-0006 and a tooling guide explaining why target table bindings are explicit and why the preview is not a deployment claim.
- Updated the aggregate project check, README, Roadmap, package documentation, and handoff.

### Problems and corrections

- Azure CLI and the Azure PowerShell modules were unavailable locally. No system tool was installed; the target check used the already authenticated Microsoft security portal in read-only mode.
- The temporarily installed generic Sigma CLI could produce a predicate without a table but refused both Azure Monitor and Sentinel ASIM conversion because it could not infer the query table. The repository compiler now passes the reviewed `SigninLogs` binding directly to the Python pipeline; the unused CLI and its extra dependencies were removed from the local environment and are not part of the lock.
- The first browser query edit appended the new text to the preceding aggregate query and produced a syntax error before any data query ran. The separate test editor was cleared through its own select-all action, the complete query text was verified, and the corrected query then executed.
- A service-action coverage query returned no applicable rows, confirming that the available target could not validate `MSEC-DET-0001`; the rule was not weakened or remapped to force a result.
- One local Sigma validation invocation included a stale executable path. The Sigma validation and fixture commands still completed, but the invocation itself was treated as invalid and was not used as final evidence.
- The first aggregate project check resolved Windows' unusable `python` alias instead of the repository virtual environment. The same unchanged check was rerun with `.venv\\Scripts` first on the process-local path and passed.

### Verification

- Manifest validation accepted both catalogue packages and retained rejection of the deliberately invalid stable example.
- Package validation accepted two packages and all eight package-contract unit tests passed.
- pySigma `1.5.0` structurally accepted two rules and all six parser tests passed.
- All six bounded-evaluator unit tests passed.
- All fourteen committed synthetic expectations passed: six positive and eight negative.
- All three Sentinel compiler tests passed, including rejection of repository traversal and an unsafe table value.
- Generated KQL matched the committed Golden snapshot exactly and the ignored local build wrote `dist/sentinel/MSEC-DET-0002/query.kql`.
- A read-only 30-day target control confirmed that the relevant `SigninLogs` fields were populated. The exact generated detection predicate was accepted and returned a valid negative aggregate result. No raw event or operational value was copied into the repository.
- The complete repository check passed after the process-local Python correction.

### Explicitly untouched

- No analytics rule, custom detection, automation rule, connector, workspace setting, identity setting, exception, alert, incident, or other cloud resource was created or changed.
- No production query result or target identifier was committed.
- No positive activity was simulated against the environment.
- No commit, push, Forgejo update, GitHub mirror update, Website change, or production rollout occurred.

### Result

The project now has two complete experimental Sigma packages and its first bounded, reproducible Microsoft Sentinel KQL preview. `MSEC-DET-0002` has separate local behavioral evidence, deterministic compilation evidence, and read-only target query-acceptance evidence; it is not deployed or declared production-ready. Three more reviewed detections remain for the Functional Foundation exit criterion.

## 2026-09-03 — Third detection and positive Sentinel target probe verified locally

### Starting state

The repository had two complete experimental detections. Only the legacy-client identity rule was bound to the Sentinel preview, and its valid live result was negative. The authorized workspace had no Windows event telemetry suitable for validating the service-installation rule.

### Decision

- Add a second precise identity signal from the populated `SigninLogs` table instead of weakening the Windows rule or forcing a noisy web-application event into the catalogue.
- Detect only a successful sign-in whose risk at sign-in time is `high`; treat the result as an investigation signal rather than proof of compromise.
- Keep every local behavior example synthetic and store only the positive or negative live-validation outcome, never the operational count or target identity.
- Preserve compilation, Golden comparison, read-only target acceptance, and deployment as separate claims.

### Source basis

- Microsoft documents `SigninLogs.ResultType` value `0` as success and `RiskLevelDuringSignIn` values including `high`.
- Microsoft Entra ID Protection describes sign-in risk as the probability that an authentication request was not made by the account owner and recommends investigating risk details, sign-in context, and adjacent activity.
- MITRE ATT&CK T1078.004 covers adversary use of valid cloud accounts.

### Changes

- Added experimental package `MSEC-DET-0003` for a successful Microsoft Entra sign-in assessed as high risk during sign-in.
- Added three positive and four negative synthetic fixtures covering case-insensitive high risk, additional investigation context, failed authentication, medium risk, no risk, and a missing risk field.
- Added an explicit `SigninLogs` Sentinel preview binding and a second reviewed Golden KQL snapshot.
- Extended the compiler regression test to verify the ordered output and Golden content for both preview detections.
- Updated the README, Roadmap, package contract, Sentinel compilation guide, and project handoff to record three of five detections and the separate positive live result.

### Problems and corrections

- An initial Application Gateway WAF candidate based on anomaly-score rule `949110` was rejected after a read-only aggregate check showed that it represented a very high-volume threshold event, not a precise attack technique. Microsoft also documents `949110` as the anomaly-score aggregation decision rather than the specific rule that caused the score. No WAF detection was added.
- A browser tab became stale while refining the WAF query. The stale handle was discarded and the work continued in a fresh query tab; no cloud setting or data was changed.
- The first high-risk query attempt occurred before the new query editor had finished loading and timed out before execution. The editor was allowed to finish, then the complete query was entered and verified.
- The first reserved-identity fixture scan used a look-ahead without enabling ripgrep's PCRE2 engine and therefore failed before checking any file. The same scan was rerun with PCRE2 enabled and passed; only reserved example domains and documentation address ranges are present in the synthetic identity fixtures.

### Verification

- Manifest and package validation accepted three catalogue packages and all twenty-one referenced event fixtures.
- pySigma `1.5.0` structurally accepted three Sigma rules.
- All twenty-one synthetic expectations passed: nine expected matches and twelve expected non-matches.
- All three Sentinel compiler unit tests passed, and both generated queries matched their committed Golden snapshots exactly.
- The exact generated `MSEC-DET-0003` predicate ran in the authorized workspace inside a read-only 30-day aggregate query and returned a positive result. No individual event was opened or copied.
- The complete repository check, Python bytecode compilation, whitespace validation, and public-safety scan passed.

### Explicitly untouched

- No analytics rule, custom detection, automation rule, connector, workspace setting, identity setting, Conditional Access policy, incident, or other cloud resource was created or changed.
- No production query row, count, user, IP address, tenant, subscription, or workspace identifier was committed.
- No commit was pushed, and no Forgejo, GitHub mirror, Website, image, infrastructure, or production rollout changed.

### Result

`MSEC-DET-0003` is the third complete experimental package. It now has synthetic positive and negative behavior evidence, deterministic Sentinel compilation evidence, and a separate positive read-only target-acceptance result. Two reviewed detections remain for the Functional Foundation exit criterion.

## 2026-09-03 — Fourth detection for service-principal credentials verified locally and read-only

### Starting state

The repository had three complete experimental detections and two `SigninLogs` rules in the bounded Sentinel preview. A fourth detection still needed a precise hypothesis, executable local evidence, deterministic target output, and separate target validation.

### Decision

- Use the populated Microsoft Entra `AuditLogs` source to represent a different identity behavior rather than adding a third sign-in rule.
- Detect only the successful `Add service principal credentials` operation; do not alert on every high-volume service-principal update.
- Treat legitimate onboarding and credential rotation as expected triage paths, while preserving high severity because an unauthorized credential can provide persistent application access.
- Store no live result count, audit record, initiator, target application, credential detail, or environment identifier.

### Source basis

- Microsoft's Entra audit activity reference lists `Add service principal credentials` under ApplicationManagement.
- Microsoft's application-security operations guidance classifies credentials added to existing applications as high risk and recommends monitoring application credential changes.
- Microsoft documents `AuditLogs.OperationName`, `Result`, `InitiatedBy`, `TargetResources`, and `CorrelationId` as audit fields needed for detection and investigation.
- MITRE ATT&CK T1098.001 describes adding cloud credentials to service principals or applications for persistence and possible privilege escalation.

### Changes

- Added experimental package `MSEC-DET-0004` for a successful credential addition to a Microsoft Entra service principal.
- Added three positive and four negative synthetic fixtures covering case-insensitive matching, contextual fields, failed additions, removals, general updates, and a missing result.
- Added an explicit `AuditLogs` Sentinel preview binding and a third reviewed Golden KQL snapshot.
- Extended the compiler regression test to verify all three ordered target outputs against their corresponding Golden queries.
- Updated the README, Roadmap, package contract, Sentinel compilation guide, and project handoff to record four of five detections.

### Problems and corrections

- The first keyword summary used Kusto's term-based `has_any` with singular `credential`, which did not match the plural `credentials` token. A neutral top-operation summary exposed the exact documented operation name without inspecting any event row.
- The first audit-table control query was appended to the existing editor contents by the portal editor and produced a parse error before executing. The editor was explicitly selected and cleared, then the complete query was entered and verified.
- The broad `Update service principal` operation dominated the aggregate source and was deliberately rejected as too unspecific. The rule uses only the exact credential-addition operation.

### Verification

- Manifest and package validation accepted four catalogue packages and all twenty-eight referenced event fixtures.
- pySigma `1.5.0` structurally accepted four Sigma rules.
- All twenty-eight synthetic expectations passed: twelve expected matches and sixteen expected non-matches.
- All three Sentinel compiler unit tests passed, and all three generated queries matched their committed Golden snapshots exactly.
- The exact generated `MSEC-DET-0004` predicate ran in the authorized workspace inside a read-only 30-day aggregate query and returned a positive result. No individual audit event was opened or copied.
- The complete repository check, Python bytecode compilation, whitespace validation, target-identifier scan, and synthetic-data safety scan passed.

### Explicitly untouched

- No analytics rule, custom detection, automation rule, connector, workspace setting, application, service principal, credential, identity policy, incident, or other cloud resource was created or changed.
- No production query row, result count, initiator, target application, tenant, subscription, or workspace identifier was committed.
- No push, Forgejo update, GitHub mirror update, Website change, image build, infrastructure change, or production rollout occurred.

### Result

`MSEC-DET-0004` is the fourth complete experimental package. It has local synthetic behavior evidence, deterministic Sentinel compilation evidence, and a separate positive read-only target-acceptance result. One reviewed detection remains for the Functional Foundation exit criterion.

## 2026-09-03 — Five-detection foundation completed with application-role grant coverage

### Starting state

The repository had four complete experimental detections. The final package needed to add a distinct security hypothesis without claiming support for a data source that was absent from the authorized workspace.

### Decision

- Check `AzureActivity` first for successful Azure RBAC assignment writes, then check `OfficeActivity` for Exchange rule changes, but make no target claim when both tables have no recent rows.
- Use the populated Entra `AuditLogs` source and distinguish permission grants from the credential-addition behavior already covered by `MSEC-DET-0004`.
- Detect only the successful `Add app role assignment to service principal` operation instead of every general directory-role or service-principal change.
- Use medium severity because the operation identifies a new application permission but does not by itself establish that the permission is privileged or unauthorized.

### Source basis

- Microsoft's Entra application-security guidance identifies `Add app role assignment to service principal` as the audit activity for application permissions and recommends investigation of highly privileged grants.
- Microsoft's Entra audit activity reference lists the same operation under ApplicationManagement.
- Microsoft documents the required `AuditLogs` detection and investigation fields.
- MITRE ATT&CK T1098.003 describes cloud-role or permission additions that can provide persistence or privilege escalation.

### Changes

- Added experimental package `MSEC-DET-0005` for a successful application-role grant to a Microsoft Entra service principal.
- Added three positive and four negative synthetic fixtures covering case-insensitive matching, contextual fields, failed assignments, removals, delegated grants, and a missing result.
- Added an explicit `AuditLogs` Sentinel preview binding and a fourth reviewed Golden KQL snapshot.
- Extended the compiler regression test to verify all four ordered target outputs against their corresponding Golden queries.
- Updated the README, Roadmap, package contract, Sentinel compilation guide, and project handoff to record the completed five-detection foundation.

### Problems and corrections

- `AzureActivity` returned no rows for the authorized 30-day window, so the proposed Azure RBAC assignment rule received no compatibility claim and was not added.
- `OfficeActivity` also returned no rows for the authorized 30-day window, so the proposed Exchange forwarding-rule detection was not added.
- A previously used browser tab stopped responding before the exact final validation query could be entered. The stale tab was discarded and the same aggregate query completed in a fresh authenticated tab; no cloud state changed.
- A broad Entra directory-role addition was considered but rejected because the simple operation alone did not identify the assigned role or its privilege. The narrower service-principal app-role event was selected instead.

### Verification

- Manifest and package validation accepted five catalogue packages and all thirty-five referenced event fixtures.
- pySigma `1.5.0` structurally accepted five Sigma rules.
- All thirty-five synthetic expectations passed: fifteen expected matches and twenty expected non-matches.
- All three Sentinel compiler unit tests passed, and all four generated queries matched their committed Golden snapshots exactly.
- The exact generated `MSEC-DET-0005` predicate ran in the authorized workspace inside a read-only 30-day aggregate query and returned a positive result. No individual audit event was opened or copied.
- The complete repository check, Python bytecode compilation, whitespace validation, target-identifier scan, and synthetic-data safety scan passed.

### Explicitly untouched

- No analytics rule, custom detection, automation rule, connector, workspace setting, application permission, service principal, identity policy, incident, or other cloud resource was created or changed.
- No production query row, result count, initiator, service principal, permission, tenant, subscription, or workspace identifier was committed.
- No push, Forgejo update, GitHub mirror update, Website change, image build, infrastructure change, or production rollout occurred.

### Result

`MSEC-DET-0005` completes the first five reviewed experimental detection packages. Four have deterministic Sentinel compilation and separate read-only target-acceptance evidence; `MSEC-DET-0001` remains intentionally local-only because the available target has no suitable Windows event telemetry. The next Functional Foundation milestone is reproducible machine-readable and human-readable catalogue generation.

## 2026-09-03 — Deterministic machine and human detection catalogue verified locally

### Starting state

The repository contained five complete detection packages and four explicit Sentinel preview bindings, but users and tooling still had to inspect individual manifests, fixture indexes, and the target profile separately. The Roadmap still listed aggregate catalogue generation as incomplete, and `dist/README.md` still described the obsolete empty foundation state.

### Decision

- Keep each detection manifest as the only authored source of identity, lifecycle, severity, ATT&CK, data-source, and implementation metadata.
- Derive fixture counts from each implementation-local `tests/cases.json` and target information only from the explicit Sentinel preview profile.
- Publish a tracked JSON discovery index for tools and an equivalent Markdown index for people.
- Omit timestamps, Git revisions, environment identifiers, live result counts, and telemetry so the same source revision produces byte-identical output.
- Fail the aggregate repository check whenever either generated file is missing or stale.

### Changes

- Added the reusable catalogue builder and command-line generator.
- Added JSON Schema version 1 for the generated machine catalogue.
- Added `catalog/index.json` and `CATALOGUE.md`, both generated from repository sources rather than maintained independently.
- Added generator tests for stable ordering, exact aggregate evidence, Sentinel mapping, schema conformance, and byte-for-byte tracked output freshness.
- Added dedicated build, test, and validation commands and included the catalogue gates in `pnpm run check`.
- Documented the source boundary and refreshed the README, Roadmap, package contract, generated-output guidance, and project handoff.

### Problems and corrections

- No implementation defect was found during the first generation. The generated outputs satisfied their schema and matched a second in-memory rendering exactly.
- The existing `dist/README.md` still claimed the directory was empty for the repository-foundation milestone. It was corrected to distinguish ignored target or release builds from the two tracked public discovery indexes.

### Verification

- Catalogue unit tests passed all three cases.
- Schema and stale-output validation accepted exactly five detections, five implementations, fifteen positive cases, twenty negative cases, and four Sentinel preview bindings.
- A repeated generation produced byte-identical JSON and Markdown files.
- The complete repository check, Python bytecode compilation, whitespace validation, repository-link validation, and public-safety scan passed.

### Explicitly untouched

- No detection hypothesis, Sigma rule, fixture, Golden KQL query, live target result, or target profile binding changed.
- No production telemetry, result count, user, device, tenant, subscription, or workspace identifier was added.
- No pipeline, deployment, Forgejo setting, GitHub mirror, Website, image, infrastructure, or production state changed.
- No commit was pushed.

### Result

The five packages now have one reproducible discovery surface for readers and one schema-controlled index for tooling without creating a second authored source of truth. The next Functional Foundation milestone is the Forgejo validation pipeline.

## 2026-09-03 — Forgejo validation workflow defined and contract-tested locally

### Starting state

All repository checks were available through one local command, but no Forgejo workflow invoked them. A changed manifest, stale catalogue, broken fixture, invalid Sigma source, or changed Sentinel Golden query therefore had no automatic canonical-repository gate.

### Decision

- Run the existing aggregate check instead of creating a second CI-specific validation path.
- Trigger validation for pushes, pull requests, and deliberate manual runs.
- Require a runner labelled `docker` and document that it must map to a fresh isolated container without host sockets, unrelated persistent storage, or operational credentials.
- Give the workflow only read access, remove persisted checkout credentials, reference no secrets, and add no deployment, target-query, release, or publication step.
- Pin Node.js, pnpm, Python, JavaScript packages, Python packages, and every remote action to reviewed exact versions or immutable commits.
- Keep local workflow-contract validation separate from an actual Forgejo runner result.

### Source basis

- Forgejo documents `.forgejo/workflows` as its native workflow location and requires a matching online runner label.
- Forgejo recommends fully qualified action URLs and commit identifiers rather than ambiguous shorthand or movable tags.
- Forgejo documents that public pull-request content is untrusted, pull-request tokens are read-only, container isolation depends on correct runner configuration, and host runners provide no real isolation.

### Changes

- Added `.forgejo/workflows/validate.yml` with read-only push, pull-request, and manual validation.
- Pinned the Forgejo checkout, Node setup, and Python setup actions to the exact commits corresponding to reviewed releases.
- Pinned the CI runtime to Node.js `24.19.0`, pnpm `11.19.0`, and Python `3.12.13`; frozen JavaScript and exact Python dependency files remain authoritative.
- Added four workflow-contract tests for triggers and runner selection, least privilege and secret absence, immutable remote action references, and the complete pinned command sequence.
- Added the workflow test to `pnpm run check` and recorded pnpm `11.19.0` as the repository package manager.
- Added the Forgejo validation guide and updated contributor, README, Roadmap, and handoff documentation.

### Problems and corrections

- The initial read-only action-reference lookup could not reach `data.forgejo.org` from the restricted local sandbox. The same public `git ls-remote` query was repeated through the approved network boundary and resolved the reviewed release tags to full commit identifiers.
- No local `forgejo-runner`, Actions emulator, or Docker runtime was available. The YAML, safety contract, and complete command path were verified locally, but the documentation and Roadmap explicitly retain a real isolated Forgejo run as pending.

### Verification

- All four Forgejo workflow-contract tests passed.
- YAML parsing confirmed the push, pull-request, and manual triggers and the single `docker` validation job.
- The aggregate repository check passed, including five package validations, thirty-five synthetic fixture expectations, catalogue freshness, five Sigma sources, four Sentinel Goldens, and the new workflow contract.
- Python bytecode compilation and whitespace validation passed.
- A frozen pnpm installation accepted the existing lockfile and package-manager declaration without changing the dependency graph.
- The source scan found no workflow secret reference, deployment command, live target query, or known environment identifier.

### Explicitly untouched

- No Forgejo repository setting, runner, branch protection, secret, variable, mirror, or workflow run changed.
- No detection, fixture, generated catalogue record, Sentinel query, live workspace, cloud resource, or production state changed.
- No release artifact was generated or published.
- No commit was pushed.

### Result

The repository now contains a minimal, immutable, secret-free Forgejo validation definition that is enforced by its own local tests. It is not yet an operational release gate; the next milestone is a successful run on a correctly isolated canonical Forgejo runner.

## 2026-09-03 — Dedicated Forgejo validation runner proven on canonical main

### Starting state

The validation workflow and its local contract passed, but Forgejo had no runner
allowed to execute the repository. The existing Blog runner combined a Blog-only
identity with BuildKit and publication capability and was therefore outside this
repository's validation boundary.

### Decision

- Use a separate repository-scoped runner and the unique
  `metesec-detection-validate` label.
- Give the runner no Kubernetes token or RBAC, host path, runtime or BuildKit
  socket, deployment credential, publisher credential, cloud credential or SIEM
  credential.
- Run only trusted pushes and manual dispatch while Forgejo `host` mode lacks
  hard per-job container isolation. Do not execute public pull-request code.
- Verify both a complete pass and a deliberate readable failure before accepting
  the pipeline as operational.

### Changes

- Bound the workflow to the dedicated runner label and removed the automatic
  pull-request trigger.
- Reused exact Node.js `24.19.0` and Python `3.12.13` runner toolchains, while
  pnpm `11.19.0` and the Python virtual environment are created under the
  disposable job directory.
- Updated the workflow contract and operator guide to enforce the trusted trigger
  set, runner label, exact toolchain, immutable checkout action and complete
  repository validation command.
- Merged Forgejo Pull Request `#3` as
  `6157d748c7b36889fa4048dffdec5880da464a07`.

### Problems and corrections

- The installed Forgejo CLI models `--secret-stdin` as a string option. The first
  registration used the bare form, which consumed the following scope argument
  and briefly created a global runner. The Deployment was immediately paused,
  the exact cause was confirmed from Forgejo `15.0.6` source, and registration
  was corrected with `--secret-stdin=true` before any repository job ran.
- The first runtime start copied Python's `/usr/local` tree but omitted Alpine
  libraries under `/usr/lib`; the Python smoke test failed on `libsqlite3.so.0`.
  The rollback trap returned the Deployment to zero replicas. A separate
  read-only library volume and `LD_LIBRARY_PATH` fixed the runtime before the
  runner was accepted.
- The public run API returned status but not job-detail logs. The public Forgejo
  Actions view was therefore used to confirm the exact human-readable validation
  error.

### Verification

- Live runner checks confirmed exact repository scope, label, toolchain versions,
  zero restarts, missing Kubernetes token and runtime sockets, zero Service and
  zero RoleBinding; the Blog runner remained Ready and unchanged.
- Branch run `#1` for commit `c6768c3d1cefda6732c99f2866a9906168dcc379`
  passed the full aggregate repository check.
- Isolated run `#2` for commit
  `c2a1373a6be3662168ed05ace7351fba9298ea8e` failed as intended and displayed
  `valid/draft-windows-service-install.json: /schema_version must be equal to
  constant`.
- Cleanup run `#3` passed after restoring the valid example, and canonical main
  run `#4` passed after Pull Request `#3` merged.
- The separate infrastructure state was protected by a verified Forgejo logical
  database backup before registration. No credential value was printed or added
  to this repository.

### Explicitly untouched

- No branch protection was enabled and no release artifact was published.
- No detection logic, committed fixture, generated catalogue entry, Sentinel
  Golden query, live workspace, cloud resource or SIEM deployment changed.
- The Blog runner, mirror direction, GitHub settings, Website and production Blog
  remained unchanged.

### Result

The canonical Forgejo repository now has a proven validation-only pipeline with
both successful main execution and readable rejection behavior. It can be used
for trusted changes; public pull-request execution remains out of scope until
hard job isolation is implemented.
