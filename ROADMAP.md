# MeteSec Detection Engineering — Roadmap

The roadmap describes intended capability, not current implementation. Verified current state is maintained in `AGENTS.md`.

## 0.1 — Functional Foundation

Status: **in progress**

- [x] Create canonical public Forgejo repository
- [x] Establish project handoff, logbook, roadmap, and ADR process
- [x] Add contribution, security, and licensing baseline
- [x] Publish a one-way public GitHub distribution mirror
- [x] Define minimal logical detection manifest
- [x] Add JSON Schema and valid/invalid examples
- [x] Define compact detection-package layout
- [x] Add Sigma validation toolchain with pinned dependencies
- [ ] Implement positive and negative fixture-test model
- [ ] Add first complete Sigma detection
- [ ] Grow to five reviewed detections
- [ ] Generate a machine-readable and human-readable catalogue
- [ ] Add Forgejo validation pipeline
- [ ] Publish first signed or checksummed release artifact

Exit criteria:

- at least five complete detections;
- all stable detections have positive and negative tests;
- clean checkout can validate and build the catalogue with documented commands;
- Forgejo main pipeline passes;
- generated outputs are reproducible and are not hand-edited.

## 0.2 — Microsoft Sentinel Target

Status: **planned**

- [ ] Pin pySigma and Microsoft Sentinel backend/pipeline dependencies
- [ ] Compile declared Sigma implementations to KQL
- [ ] Add approved Golden snapshots for generated queries
- [ ] Add a generic Sentinel analytics-rule renderer
- [ ] Define a non-production target profile
- [ ] Package immutable Sentinel release artifacts
- [ ] Clearly document semantic and platform limitations

## 0.3 — Detection Operations

Status: **planned**

- [ ] Introduce data-source contracts
- [ ] Add deployment bundles by detection ID
- [ ] Add versioned exception objects with expiry
- [ ] Generate ATT&CK and data-source coverage reports
- [ ] Introduce lifecycle and review-cadence validation
- [ ] Add telemetry-health definitions

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
