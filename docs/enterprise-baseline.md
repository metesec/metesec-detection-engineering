# Enterprise adoption guide

This is a tested detection-as-code baseline, not an enabled managed detection
service. All 67 current rules are experimental. The repository has 66 disabled
Sentinel bindings across ten explicit source contracts. MSEC-DET-0001 needs
Windows System Event 7045 telemetry and has no Sentinel binding.

## Choose signals deliberately

Use `quality.signal_type`, severity, confidence, limitations and triage guidance
in each manifest. Administrative operations are deliberately retained as
change-monitoring or enrichment signals. Encoded PowerShell and routine WinRM
execution are not high-confidence compromise verdicts. High severity denotes
potential impact, not proof of an incident.

The catalogue exposes source requirements and tests. Neither ATT&CK mappings
nor the number of rules measures effective coverage. Missing audit settings,
licensing, platform gaps and unlogged behavior can leave blind spots.

## Admission and enablement

1. Confirm the required connectors, tables, exact field types, audit settings and
   licensing. New AzureActivity, AWSCloudTrail and endpoint source contracts are
   documentation-backed, not verified against your tenant.
2. Run the complete local check. Review source changes, synthetic positives,
   near-miss negatives, provenance and generated query differences.
3. Execute the full generated query in a non-production target. Test real-schema
   representative positive and negative events, entity mapping, regex behavior,
   nulls, adapter output and resource consumption. A predicate-only aggregate
   probe is insufficient for the full scheduled artifact.
4. Measure ingestion latency and ensure `ingestion_time()` is populated. Tune
   the one-hour lookback and 15-minute slice to actual sources. The schedule
   tolerates bounded delay but does not guarantee exactly-once alert delivery;
   skipped runs, replay, long delays and multi-target audit events need policy.
5. Observe for at least 14 days in a controlled pilot. Record workload, alert
   volume, triage outcomes, measured latency, costs and scoped expiring exclusions.
   Review with the service owner. Do not make a global allowlist from one benign
   event or suppress an entire technique just to reduce alert counts.
6. Only then enable selected rules and incident creation in a consumer-owned
   deployment. Maintain rollback, an owner, escalation routing and execution/
   ingestion health monitoring. Zero alerts is not proof that a rule is healthy.

The renderer ships disabled and does not deploy. Existing historical live
acceptance notes apply only to the tested historical queries, not automatically
to the rewritten 1.1 sources, adapters or schedules.

## Evidence gates

`quality.validation_level` starts at `synthetic-only`. For `target-validated`,
add a reviewed `governance/evidence/<id>.json` containing `rule_sha256`,
`validation_inputs_sha256`,
`target_result: passed`, `reviewer` and a non-sensitive `test_reference`.
For `production-validated`, also require `pilot_result: accepted`, `pilot_days`
of at least 14 and `tuning_reference`. Only that last level can accompany
`lifecycle.status: stable`. References may identify controlled private evidence;
do not commit customer telemetry, secrets or tenant identifiers. Evidence is an
auditable assertion, not something the local gate can independently authenticate.

The validation-input digest binds rule bytes, logical metadata excluding quality,
all Python tooling, the Sigma dependency lock and all three Sentinel profiles.
`validation_input_digest` in the gate computes it deterministically. Changes to
adapters, compiler, scheduling, fields or dependencies invalidate prior evidence;
even an unrelated profile change conservatively requires renewed review.

## Adapter exception: Entra delegated grants

0021 rejects missing/malformed properties and duplicate property names. It uses
only string `newValue` values on one ServicePrincipal; old values and display
names cannot satisfy the permission selector. A matching target is also the
target shown to analysts. Multiple matching targets produce multiple target
rows; the local event assertion means at least one matching row, not exactly one.
Other Sigma consumers must honor `metesec_normalization`, not ignore it.

## Provenance and maintenance

All 100 unique candidate IDs have a written decision in the three review reports.
The 33 deferred additions are not installed as active content. Known related
SigmaHQ/Microsoft work stays referenced. The pinned-corpus overlap audit is a
copy-screening aid, not proof of internet-wide uniqueness or a legal opinion.
Retain LICENSE and NOTICE when redistributing the pack.

CI checks that the committed overlap report still covers the exact current
rule inventory and bytes. It does not access the network. After changing source
rules, rerun the documented pinned-corpus audit and review its results; do not
replace a stale report with an unsupported authorship assertion.

The [Microsoft ingestion-delay guidance](https://learn.microsoft.com/en-us/azure/sentinel/ingestion-delay)
describes the lookback-plus-ingestion-slice pattern. Microsoft's
[scheduled-rule reference](https://learn.microsoft.com/en-us/azure/sentinel/scheduled-rules-overview)
documents scheduling and grouping tradeoffs. These defaults still need a target pilot.
