# Microsoft Sentinel runtime health v1

This contract answers one operational question for the thirty-nine Sentinel-bound
detections: is the scheduled rule present, enabled and executing on time?

It deliberately treats alert and incident volume as context, not health. A rule
that executes successfully and creates zero alerts is healthy.

## Sources and boundaries

The public policy is
`governance/policies/sentinel-runtime-health-v1.json`. Its schedule source is
`targets/sentinel/analytics-rules.json`; no second frequency list is maintained.
The policy expects intentionally deployed rules to be enabled and uses two and
five missed schedule intervals as its initial degraded and failed boundaries.

Those multipliers are reviewable reference assumptions, not Microsoft service
guarantees or an environment SLA. The repository's rendered analytics-rule
bodies remain disabled by design. Runtime health applies only after a consumer
has reviewed, deployed and deliberately enabled a rule in its own environment.

The repository contains no Azure client, credential, workspace identifier,
scheduled monitor or live observation. A consumer-owned adapter may create a
temporary observation matching
`governance/schemas/sentinel-runtime-observation-v1.schema.json`. The contract
does not mandate one platform API or guess a vendor response field.

## Assessment states

For each rule, execution age is measured from `observed_at` using the exact
`query_frequency` in the Sentinel analytics-rule profile.

| State | Meaning |
| --- | --- |
| `healthy` | The rule exists, is enabled, last execution succeeded and its age is no more than two schedule intervals. |
| `degraded` | The rule is disabled, or its last execution is more than two but no more than five schedule intervals old. |
| `failed` | The rule is missing, the last execution failed, or it is more than five schedule intervals old. |
| `unknown` | The expected rule has no observation, no execution record, or no known execution result and no stronger condition applies. |

The current reference boundaries therefore resolve to:

| Query frequency | Degraded after | Failed after |
| --- | ---: | ---: |
| `PT1H` | more than 2 hours | more than 5 hours |
| `PT5M` | more than 10 minutes | more than 25 minutes |

When conditions overlap, failed takes precedence over degraded, and degraded
takes precedence over unknown. Missing, duplicated, future-dated or unexpected
rule observations fail contract validation instead of being silently ignored.

## Alert outcome context

An observation may include one bounded window with non-negative counts for
alerts and incidents created. Those numbers are copied into the assessment but
never change its state. In particular:

- zero alerts can accompany a healthy execution;
- many alerts do not prove a healthy rule;
- no outcome window is not an execution failure;
- the contract does not assess detection quality, tuning or incident handling.

## Commands

Validate the public policy, schemas and schedule relationship without making a
live claim:

```console
pnpm run validate:sentinel-runtime-contract
pnpm run validate:sentinel-runtime-health
```

Evaluate a consumer-created local observation:

```console
python scripts/check_sentinel_runtime_health.py --observation <observation.json>
python scripts/check_sentinel_runtime_health.py --observation <observation.json> --json
```

The assessment command returns `0` only when every expected rule is healthy,
`2` when at least one state is degraded, failed or unknown, and `1` for invalid
input. Without `--observation`, it returns `0` only for contract validation and
prints that no live-health claim was made.

Observation and assessment files are environment-local operational evidence.
They must not be committed to this public repository or included in its release.
