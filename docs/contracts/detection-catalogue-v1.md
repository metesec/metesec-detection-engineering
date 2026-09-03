# Generated detection catalogue v1

The repository publishes one machine-readable `catalog/index.json` and one human-readable `CATALOGUE.md`. Both are deterministic projections of existing source files and must never become independent authored detection metadata.

## Sources

The generator reads:

- `catalog/detections/<ID>/manifest.json` for identity, intent, lifecycle, severity, confidence, ATT&CK, data sources, and implementations;
- implementation-local `tests/cases.json` indexes for positive and negative synthetic evidence counts;
- `targets/sentinel/preview.json` for explicit Sentinel table and Golden-query bindings.

No runtime timestamp, Git revision, target identifier, live result count, or production telemetry is included. The same source tree must produce byte-identical catalogue files on every supported machine.

## Outputs

`catalog/index.json` satisfies `governance/schemas/detection-catalogue-v1.schema.json`. It is a compact discovery index, not a replacement for the full logical manifest.

`CATALOGUE.md` presents the same records as a summary table and concise per-detection sections with repository links.

Regenerate and validate with:

```console
pnpm run build:catalogue
pnpm run test:catalogue
pnpm run validate:catalogue
```

`validate:catalogue` builds the expected content in memory, validates the JSON structure, and fails if either tracked output differs. The aggregate repository check includes the unit tests and stale-output gate.
