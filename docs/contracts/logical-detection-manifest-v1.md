# Logical detection manifest v1

The logical detection manifest is the source-of-truth record for one detection idea. It describes **what** should be detected and **why**, without embedding a Sigma rule, target query, tenant setting, or customer-specific exception.

## Why JSON

Version 1 uses JSON because it is unambiguous, directly validated by JSON Schema, and keeps the contract visibly separate from the later Sigma YAML implementation. This decision applies to the logical manifest only; it does not replace Sigma.

## Contract boundary

The manifest records:

- a stable `MSEC-DET-####` identity;
- hypothesis, rationale, and detection goal;
- owner, reviewers, and lifecycle dates;
- severity and confidence;
- required data sources and fields;
- ATT&CK mappings;
- analyst triage and expected false positives;
- validation state;
- references to technical implementations.

The schema retains its original generic path allowance for future native work,
but the active version 1 release authors and packages only implementations under
`content/portable/sigma/`. No native implementation, resolver or support claim
exists. Generated target queries remain build output and never become the
manually edited source of truth.

## Lifecycle guardrail

Draft and experimental manifests may exist before their implementation is complete. A manifest may claim `stable` only when:

1. at least one implementation is declared `active`;
2. positive behavioral tests are complete; and
3. negative behavioral tests are complete.

The schema enforces these minimum conditions. It does not claim that an implementation is operationally effective in every SIEM; target validation remains a separate evidence layer.

## Examples

- `examples/manifests/valid/draft-windows-service-install.json` is a valid draft with no fabricated implementation claim.
- `examples/manifests/invalid/stable-without-implementation.json` deliberately violates the stable-state guardrail and must be rejected.

Both examples use synthetic, public-safe content.

## Validation

Install the pinned development dependency once:

```console
pnpm install --frozen-lockfile
```

Run the contract test:

```console
pnpm run validate:manifests
```

The command succeeds only when every file under `examples/manifests/valid/` is accepted and every file under `examples/manifests/invalid/` is rejected. The first Sigma rule is intentionally outside this milestone.
