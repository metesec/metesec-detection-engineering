# Sigma structural validation

The repository pins `pySigma 1.5.0` as its portable Sigma parser. This milestone validates source structure only. It does not compile a query, execute detection logic, prove fixture behavior, or contact a SIEM.

## Environment

- Python 3.10 or newer is required by pySigma.
- The checked lock was resolved and verified with Python 3.12.13.
- `requirements-sigma.lock` pins the direct pySigma requirement and every dependency observed in that environment.
- `sigma-cli` and target backends are intentionally absent until the first compilation-target milestone.

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
- [SigmaHQ sigma-cli](https://github.com/SigmaHQ/sigma-cli)

The CLI is listed for the future conversion milestone, not as an installed capability of the current repository.
