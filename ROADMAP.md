# MeteSec Detection Engineering — Roadmap

The roadmap describes intended capability, not current implementation. Verified current state is maintained in `AGENTS.md`.

## 0.1 — Functional Foundation

Status: **complete**

- [x] Create canonical public Forgejo repository
- [x] Establish project handoff, logbook, roadmap, and ADR process
- [x] Add contribution, security, and licensing baseline
- [x] Publish a one-way public GitHub distribution mirror
- [x] Define minimal logical detection manifest
- [x] Add JSON Schema and valid/invalid examples
- [x] Define compact detection-package layout
- [x] Add Sigma validation toolchain with pinned dependencies
- [x] Implement positive and negative fixture-test model
- [x] Add first complete Sigma detection
- [x] Grow to five reviewed detections (5 of 5 complete)
- [x] Generate a machine-readable and human-readable catalogue
- [x] Add Forgejo validation pipeline definition
- [x] Verify the pipeline on a dedicated restricted Forgejo runner
- [x] Publish first signed or checksummed release artifact

Exit criteria:

- at least five complete detections;
- all stable detections have positive and negative tests;
- clean checkout can validate and build the catalogue with documented commands;
- Forgejo main pipeline passes;
- generated outputs are reproducible and are not hand-edited.

## 0.2 — Microsoft Sentinel Target

Status: **complete**

- [x] Pin pySigma and Microsoft Sentinel Kusto backend/pipeline dependencies
- [x] Compile declared Sigma implementations to KQL
- [x] Add approved Golden snapshots for generated queries
- [x] Add a generic Sentinel analytics-rule renderer
- [x] Define a non-production target profile
- [x] Define explicit analyst output columns and Sentinel entity mappings
- [x] Document consumer-owned temporary rendering and deployment handoff
- [x] Clearly document semantic and platform limitations

Target status: forty-four explicitly bound rules across `SigninLogs`, `AuditLogs`,
`DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents`
compile to reviewed Golden queries and render into deterministic disabled Scheduled-rule
REST bodies with stable rule IDs, governed output fields, entity mappings and
provenance hashes. All forty-four have passed separate read-only live
query-acceptance probes.
Consumers render temporary files in their own pipeline;
MeteSec deliberately publishes no separate prebuilt Sentinel target archive and
implements no deployment.

## 0.3 — Detection Operations

Status: **complete**

- [x] Introduce data-source contracts
- [x] Keep target rendering consumer-owned instead of publishing deployment bundles
- [x] Generate ATT&CK and data-source coverage reports
- [x] Introduce lifecycle and review-cadence validation
- [x] Add rule-execution and alert-outcome health definitions

Current status: `SigninLogs`, `AuditLogs`, `DeviceProcessEvents`,
`DeviceRegistryEvents` and `AADUserRiskEvents` have exact field and type
requirements, freshness expectations, preview-consumer relationships and a
local observation evaluator with explicit `ready`, `degraded`, `unavailable`
and `unknown` states. No live monitor or production-health claim exists.
Environment-specific tuning and exceptions remain consumer-owned and are not a
planned public repository contract.

The generated coverage outputs expose thirty-five declared ATT&CK techniques, eleven
tactics, six logical sources, five Sentinel source contracts and the one
intentional unbound detection without inventing a completeness score.
Lifecycle validation now derives review dates from existing manifest fields,
fails on due or overdue records and can enforce forward-only transitions when a
consumer supplies a previous catalogue baseline. No runtime status file is
committed.

Rule-runtime validation now derives the expected forty-four execution schedules from
the Sentinel analytics-rule profile and evaluates a consumer-supplied local
observation as `healthy`, `degraded`, `failed` or `unknown`. Alert and incident
counts are optional context and never influence health; no Azure client, live
observation or runtime assessment is committed.

## 0.4 — Sigma Detection Pack Expansion

Status: **in progress**

- [x] Make Sigma the only authored detection format through version 1
- [x] Keep Microsoft Sentinel as the only supported and validated target
- [x] Inventory available Sentinel tables and candidate fields read-only
- [ ] Approve and review forty-five additional detections in bounded waves
- [x] Complete Wave 1: 10 of 50 Sigma detections
- [x] Complete Wave 2: 15 of 50 Sigma detections
- [x] Complete Wave 3: 20 of 50 Sigma detections
- [x] Complete Wave 4: 25 of 50 Sigma detections
- [x] Complete Wave 5: 30 of 50 Sigma detections
- [x] Complete Wave 6: 35 of 50 Sigma detections
- [x] Complete Wave 7: 40 of 50 Sigma detections
- [x] Complete Wave 8: 45 of 50 Sigma detections
- [ ] Complete Wave 9: 50 of 50 Sigma detections
- [x] Pass every applicable manifest, package, Sigma, synthetic-fixture,
  Sentinel compilation, Golden-query, disabled-renderer, source, lifecycle and
  coverage gate
- [ ] Publish the protected-main `v1.0.0` release after reproducibility and
  checksum verification

Current status: forty-five of fifty planned Sigma detections exist. Forty-four have
explicit Sentinel bindings and one Windows Event detection remains intentionally
unbound because the available target has no suitable Windows event telemetry.
Wave 8 added CMSTP child-process execution, Odbcconf DLL registration, remote
Msiexec package installation, remote InstallUtil content and suspicious MSBuild
children. Each has three positive and four negative synthetic cases, a reviewed
KQL Golden, an explicit source contract and a disabled Scheduled-rule body. The
complete local validation passes and all five predicates passed the bounded
read-only live query-acceptance probe. Four returned no match in the current
30-day aggregate baseline; the remote-MSI predicate returned a small non-zero
aggregate result across several devices and remains tuning-required. No raw row,
exact count or identifying result was retained. The next milestone is to research
Wave 9 toward 50 of 50; release-readiness review begins only after the complete
fifty-rule pack is verified.

## Future Signal

- historical backtesting;
- query-performance budgets;
- canary deployment and read-back verification;
- drift detection;
- reproducible Atomic Red Team mappings;
- native implementations and a target resolver, only after a concrete
  target-backed Sigma limitation exists;
- additional targets such as Splunk, Elastic, or Google SecOps;
- public contribution synchronization between GitHub and Forgejo.

These capabilities must not receive directories or public support claims before an implementation milestone is approved.
