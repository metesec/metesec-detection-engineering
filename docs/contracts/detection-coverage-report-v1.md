# Generated detection coverage report v1

The repository publishes one machine-readable `coverage/index.json` and one
human-readable `COVERAGE.md`. Both files are deterministic projections of
existing source contracts and must never become independently authored facts.

## Sources

The generator reads:

- `catalog/detections/<ID>/manifest.json` for declared ATT&CK mappings and
  logical data-source requirements;
- `targets/sentinel/preview.json` for explicit target bindings;
- `targets/sentinel/data-sources.json` for target table, consumer, field, type
  and freshness contracts.

It includes no runtime timestamp, target identifier, environment observation,
live health status, result count or production telemetry.

## Report contents

The report contains exact counts and relationships for:

- declared ATT&CK mappings grouped by technique and tactic;
- logical data sources, required fields and consuming detections;
- Sentinel data-source contracts and their bound detections;
- detections that intentionally have no Sentinel preview binding.

The report deliberately provides no coverage percentage. The repository does
not define a complete ATT&CK, platform or organization-specific denominator, so
such a percentage would imply unsupported completeness.

## Interpretation boundary

`COVERAGE.md` is a repository inventory. It does not prove complete MITRE ATT&CK
coverage, current telemetry availability, detection effectiveness or production
readiness. A missing Sentinel binding is a visible target gap, not a failed
detection and not proof that a consumer lacks that data source.

## Generation and validation

```console
pnpm run build:coverage
pnpm run test:coverage
pnpm run validate:coverage
```

The generated JSON must satisfy
`governance/schemas/detection-coverage-report-v1.schema.json`. The stale-output
gate rebuilds the expected report in memory and fails when either tracked output
differs.
