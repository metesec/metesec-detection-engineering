# Detection lifecycle and review cadence v1

The lifecycle validator turns the existing `created`, `modified`, `status` and
`review_interval_days` manifest fields into an enforceable review process. It
does not add a second lifecycle record.

## Review calculation

For every logical detection:

```text
review_due = modified + review_interval_days
```

The assessment state is:

| State | Meaning |
| --- | --- |
| `current` | The assessment date is before the due date. |
| `due` | The assessment date equals the due date. |
| `overdue` | The assessment date is after the due date. |

The normal repository check uses the current UTC date. It exits successfully
only when every detection is current. Due or overdue records return exit code
`2`; malformed or impossible lifecycle data returns `1`.

All fifty version 1 records were modified on 3 September 2026 and use a 90-day
interval, so their next review date is 2 December 2026. The executable
validator, rather than this summary sentence, remains authoritative as records
change.

## Transition policy

`governance/policies/detection-lifecycle-v1.json` defines the allowed forward
status transitions:

- `draft` may remain draft, become experimental or be deprecated;
- `experimental` may remain experimental, become stable or be deprecated;
- `stable` may remain stable or be deprecated;
- `deprecated` remains deprecated.

For cross-revision validation, supply a previous generated
`catalog/index.json` with `--baseline`. The validator then also rejects:

- a removed detection ID that was not deprecated first;
- a changed immutable creation date;
- a modified date that moves backwards;
- a backward or otherwise forbidden status transition;
- a status or interval change without a later modified date.

The default check has no historical input and therefore performs current-state
and review-cadence validation only. Consumers that require transition enforcement
must supply the previous reviewed catalogue from their own pipeline.

## Commands

```console
python scripts/check_detection_lifecycle.py
python scripts/check_detection_lifecycle.py --as-of 2026-09-03 --json
python scripts/check_detection_lifecycle.py --baseline <previous-catalogue.json>
```

`--as-of` exists for deterministic tests and historical review. JSON output is a
runtime-only assessment described by
`governance/schemas/detection-lifecycle-assessment-v1.schema.json`; it must not
be committed as current state.

Updating only the modified date cannot prove that a meaningful review occurred.
Human review and normal source control approval remain required.
