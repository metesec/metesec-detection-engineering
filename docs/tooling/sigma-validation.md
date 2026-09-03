# Sigma structural validation

The repository pins `pySigma 1.5.0` as its portable Sigma parser. This validator checks source structure only. It does not compile a query, execute detection logic, prove fixture behavior, or contact a SIEM.

## Environment

- Python 3.10 or newer is required by pySigma.
- The checked lock was resolved and verified with Python 3.12.13.
- `requirements-sigma.lock` pins the direct pySigma and Kusto-backend requirements plus every required dependency in that environment.
- Target compilation uses the pinned Kusto backend through the repository's explicit Python entry point; `sigma-cli` is not required.

Create an isolated environment and install the exact lock:

```console
python -m venv .venv
```

On Windows:

```console
.venv\Scripts\activate
pnpm run setup:sigma
```

On Linux or macOS:

```console
source .venv/bin/activate
pnpm run setup:sigma
```

## Quality boundary

`pnpm run validate:sigma` performs three checks:

1. the installed pySigma version is exactly `1.5.0`;
2. an in-memory valid rule must parse and a deliberately invalid rule must fail;
3. every Package v1 entry point at `content/portable/sigma/<ID>/rule.yml` must parse without a collected pySigma error.

The self-test is always executed, including while the repository has no portable implementation. A successful zero-rule run proves the pinned parser works; it does not claim that a detection exists.

Run the focused Python tests and structural validator:

```console
pnpm run test:sigma-validation
pnpm run validate:sigma
```

Run every current repository quality check:

```console
pnpm run check
```

Structural validation is only the first layer. The first real detection must separately provide positive and negative synthetic fixtures, pass the explicitly bounded local evaluator, and later pass target compilation and target-platform validation before the corresponding manifest may claim those evidence states.

## Upstream references

- [SigmaHQ pySigma](https://github.com/SigmaHQ/pySigma)
- [pySigma on PyPI](https://pypi.org/project/pySigma/)
- [pySigma Kusto backend](https://github.com/AttackIQ/pySigma-backend-kusto)
