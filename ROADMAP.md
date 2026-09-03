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

Target status: forty-nine explicitly bound rules across `SigninLogs`, `AuditLogs`,
`DeviceProcessEvents`, `DeviceRegistryEvents` and `AADUserRiskEvents`
compile to reviewed Golden queries and render into deterministic disabled Scheduled-rule
REST bodies with stable rule IDs, governed output fields, entity mappings and
provenance hashes. All forty-nine have passed separate read-only live
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

The generated coverage outputs expose the declared ATT&CK techniques and tactics,
six logical sources, five Sentinel source contracts and the one intentional
unbound detection without inventing a completeness score.
Lifecycle validation now derives review dates from existing manifest fields,
fails on due or overdue records and can enforce forward-only transitions when a
consumer supplies a previous catalogue baseline. No runtime status file is
committed.

Rule-runtime validation now derives the expected forty-nine execution schedules from
the Sentinel analytics-rule profile and evaluates a consumer-supplied local
observation as `healthy`, `degraded`, `failed` or `unknown`. Alert and incident
counts are optional context and never influence health; no Azure client, live
observation or runtime assessment is committed.

## 0.4 — Sigma Detection Pack Expansion

Status: **complete; `v1.0.0` published through protected main**

- [x] Make Sigma the only authored detection format through version 1
- [x] Keep Microsoft Sentinel as the only supported and validated target
- [x] Inventory available Sentinel tables and candidate fields read-only
- [x] Approve and review forty-five additional detections in bounded waves
- [x] Complete Wave 1: 10 of 50 Sigma detections
- [x] Complete Wave 2: 15 of 50 Sigma detections
- [x] Complete Wave 3: 20 of 50 Sigma detections
- [x] Complete Wave 4: 25 of 50 Sigma detections
- [x] Complete Wave 5: 30 of 50 Sigma detections
- [x] Complete Wave 6: 35 of 50 Sigma detections
- [x] Complete Wave 7: 40 of 50 Sigma detections
- [x] Complete Wave 8: 45 of 50 Sigma detections
- [x] Complete Wave 9: 50 of 50 Sigma detections
- [x] Pass every applicable manifest, package, Sigma, synthetic-fixture,
  Sentinel compilation, Golden-query, disabled-renderer, source, lifecycle and
  coverage gate
- [x] Complete the `v1.0.0` version transition, release notes, clean-clone
  validation and deterministic checksum review
- [x] Publish the protected-main `v1.0.0` release after reproducibility and
  checksum verification

Current status: all fifty planned Sigma detections exist. Forty-nine have explicit
Sentinel bindings and one Windows Event detection remains intentionally unbound
because the available target has no suitable Windows event telemetry. Wave 9
added suspicious script or LOLBin payloads in Run keys, non-default Winlogon
Shell or Userinit values, suspicious local scheduled-task creation, Mavinject
process injection and Netsh PortProxy creation. The broad Run/RunOnce candidate
was narrowed after its aggregate baseline proved too noisy, while a blanket
successful Device Code sign-in candidate was rejected and replaced because its
legitimate baseline could not be separated faithfully in a portable single-event
Sigma rule. Each final package has three positive and four negative synthetic
cases, a reviewed KQL Golden, an explicit source contract and a disabled
Scheduled-rule body. All five final predicates passed the bounded read-only live
query-acceptance probe and returned no match in the current 30-day aggregate
baseline. No raw row, exact count or identifying result was retained. The
published `v1.0.0` tag targets protected main commit
`708a45eda108265a3bb0b7d94485a7d667b21d43`. Release branch run `#16`, canonical
main run `#17` and annotated-tag run `#18` passed. Clean main and tag rebuilds
reproduced the reviewed 1,040,114-byte archive with 589 members and SHA-256
`4565d5001281d0694c3891337fc362b1e8ad0b29b6957433ff6ce5bc7773703d`.
The public release contains only that ZIP and `SHA256SUMS`; a final anonymous
download matched the published checksum. GitHub `main` mirrors the exact release
commit. No Sentinel rule or cloud configuration was deployed or enabled.

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
