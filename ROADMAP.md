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

Target status: four explicitly bound rules across `SigninLogs` and `AuditLogs`
compile to reviewed Golden queries, have passed separate read-only live
query-acceptance probes, and render into deterministic disabled Scheduled-rule
REST bodies with stable rule IDs, governed output fields, entity mappings and
provenance hashes. Consumers render temporary files in their own pipeline;
MeteSec deliberately publishes no separate prebuilt Sentinel target archive and
implements no deployment.

## 0.3 — Detection Operations

Status: **in progress**

- [x] Introduce data-source contracts
- [x] Keep target rendering consumer-owned instead of publishing deployment bundles
- [x] Generate ATT&CK and data-source coverage reports
- [x] Introduce lifecycle and review-cadence validation
- [ ] Add rule-execution and alert-outcome health definitions

Current status: `SigninLogs` and `AuditLogs` have exact field and type
requirements, freshness expectations, preview-consumer relationships and a
local observation evaluator with explicit `ready`, `degraded`, `unavailable`
and `unknown` states. No live monitor or production-health claim exists.
Environment-specific tuning and exceptions remain consumer-owned and are not a
planned public repository contract.

The generated coverage outputs expose four declared ATT&CK techniques, three
tactics, three logical sources, two Sentinel source contracts and the one
intentional unbound detection without inventing a completeness score.
Lifecycle validation now derives review dates from existing manifest fields,
fails on due or overdue records and can enforce forward-only transitions when a
consumer supplies a previous catalogue baseline. No runtime status file is
committed.

## 0.4 — Native Implementations and Resolution

Status: **future**

- [ ] Define native implementation contract
- [ ] Add native Sentinel implementation only where Sigma is insufficient
- [ ] Implement one-target native-precedence resolver
- [ ] Fail on missing or multiple selected implementations
- [ ] Prevent environment overlays from changing query logic

## Future Signal

- historical backtesting;
- query-performance budgets;
- canary deployment and read-back verification;
- drift detection;
- reproducible Atomic Red Team mappings;
- additional targets such as Splunk, Elastic, or Google SecOps;
- public contribution synchronization between GitHub and Forgejo.

These capabilities must not receive directories or public support claims before an implementation milestone is approved.
