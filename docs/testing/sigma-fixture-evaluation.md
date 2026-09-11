# Local Sigma fixture evaluation

The local evaluator answers one narrow question before target compilation: does a portable Sigma rule produce the expected result for small, explicitly synthetic events under the documented subset below?

It is a development guardrail, not a general Sigma engine and not a replacement for Microsoft Sentinel validation.

## Fixture model

Each implementation-local `tests/cases.json` binds a Sigma source to named expectations. Every referenced fixture must satisfy `synthetic-event-fixture-v1.schema.json`:

```json
{
  "schema_version": 1,
  "synthetic": true,
  "event": {
    "EventID": 7045,
    "ImagePath": "C:\\Users\\Public\\example.exe"
  }
}
```

Only invented, redacted, or explicitly licensed public evidence may be committed. Version 1 intentionally uses a flat event object with string, number, or Boolean values.

## Supported Sigma subset

The evaluator consumes pySigma's parsed condition tree and supports:

- field equality for strings, numbers and strict booleans (not interchangeable with 0/1 or strings);
- Sigma string wildcards produced by modifiers such as `contains`, `startswith`, and `endswith`;
- case-insensitive Sigma string comparison;
- regex search with explicit flags; regex is case-sensitive unless `re|i` or an inline flag requests otherwise;
- `and`, `or`, and unary `not` condition nodes;
- exactly one rule and one condition per `rule.yml`.

Field names must match the synthetic event exactly. A missing field does not match.

Everything outside this subset fails closed with an explicit error instead of receiving an approximate result. Unsupported examples include keyword conditions, correlations, aggregations, time windows, lookarounds/backreferences and other excluded regex constructs, field references, general backend mappings, and platform-specific null or array behavior. Python regex tests do not prove Kusto equivalence (Unicode, escaping, anchors and performance must be validated on target).

`MSEC-DET-0021` explicitly declares `metesec_normalization: entra-delegated-grant-v1`.
Its flat fixture envelope contains raw `TargetResources` as a JSON string. The
versioned adapter validates the structure and exposes same-target string values
before condition evaluation; it does not search serialized JSON. Duplicate keys
in rule YAML are rejected. See [the adoption guide](../enterprise-baseline.md).

## Evidence meaning

A `match` case proves that the local evaluator matched the committed synthetic event. A `no_match` case proves that the same evaluator did not match it. Neither result proves that a compiled query is valid, performant, or semantically identical in a target SIEM.

Target compilation and execution must be recorded separately before a deployment or target-readiness claim is made.

## Commands

Run the evaluator unit tests:

```console
pnpm run test:sigma-evaluator
```

Run every committed fixture expectation:

```console
pnpm run test:sigma-fixtures
```

Run the complete current quality chain:

```console
pnpm run check
```
