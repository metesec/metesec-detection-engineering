# Detection package v1

A detection package connects one logical detection identity to the implementation and behavioral evidence that exist today. It is a filesystem contract rather than a second metadata document: `manifest.json` remains the only authored source of detection identity, intent, ownership, lifecycle, telemetry requirements, triage, and implementation references.

## Compact layout

```text
catalog/detections/MSEC-DET-0001/
└── manifest.json

content/portable/sigma/MSEC-DET-0001/
├── rule.yml
└── tests/
    ├── cases.json
    └── fixtures/
        ├── suspicious-service-install.json
        └── approved-software-install.json
```

Only `catalog/detections/<ID>/manifest.json` is required for a draft without an
implementation. The implementation and test paths are created when executable
behavior is added. The active version 1 pack authors only Sigma under
`content/portable/sigma/<ID>/`; native implementations, their file convention
and any resolver remain outside the release scope until a real target-backed
milestone justifies them.

## Package rules

The package validator enforces these repository relationships:

1. Every catalogue directory is named with the manifest's immutable `MSEC-DET-####` ID.
2. Every manifest satisfies the logical detection manifest v1 schema.
3. Every declared implementation path is repository-relative, exists as a file, uses the prefix required by its declared type, and contains the same detection ID as a complete path segment.
4. An implementation is not declared merely to reserve future structure. If the file does not exist, the manifest keeps the implementation absent.
5. Behavioral evidence lives beside its implementation in `tests/cases.json` and `tests/fixtures/`.
6. A manifest may claim positive or negative tests only when a valid fixture set exists and contains the matching expectation.
7. Fixture paths remain inside the implementation-local `tests/fixtures/` directory and point to existing JSON files.
8. Fixture case IDs are unique inside one set.

These checks establish package integrity. They do not execute Sigma logic or prove behavior in a target SIEM.

The package manifests and their linked evidence also feed the derived [generated detection catalogue v1](detection-catalogue-v1.md). That index is never an independent authored metadata source.

## Fixture-set boundary

`governance/schemas/detection-fixture-set-v1.schema.json` defines the evidence index. A fixture set identifies the detection, the exact implementation path, and one or more synthetic cases with either `match` or `no_match` as the expected local result. `governance/schemas/synthetic-event-fixture-v1.schema.json` requires every referenced event to declare itself synthetic and contain one non-empty flat event object.

The schema deliberately does not define a field vocabulary. Field names belong to the implementation and its declared log source. The bounded local evaluator and its supported Sigma subset are documented in [Local Sigma fixture evaluation](../testing/sigma-fixture-evaluation.md). Local results must not be presented as universal target-platform behavior.

## Current package set

The version 1 pack contains fifty experimental packages. Every package has one
Sigma implementation plus three positive and four negative synthetic cases,
for one hundred fifty positive and two hundred negative expectations in total.
Forty-nine packages have an explicit Microsoft Sentinel preview binding;
`MSEC-DET-0001` remains visibly unbound because the verified target has no
suitable Windows event telemetry.

The generated [CATALOGUE.md](../../CATALOGUE.md) is the current per-detection
index. This contract deliberately avoids duplicating fifty descriptions that
would become stale independently of the manifests and generated catalogue.

## Validation

Run all current repository checks:

```console
pnpm run check
```

The command validates manifest examples and the real packages, tests the package validator's boundary cases, validates every event fixture, checks that both generated catalogue outputs are current, parses every Sigma source, executes every declared synthetic fixture expectation, and verifies the Sentinel Golden queries.
