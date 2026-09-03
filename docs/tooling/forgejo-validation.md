# Forgejo repository validation

The workflow at `.forgejo/workflows/validate.yml` runs the same aggregate repository check used by contributors. It is validation only: it does not compile a release, deploy a detection, query a SIEM, publish an artifact, or change repository content.

## Events

The workflow runs for:

- every push;
- every pull request using the read-only `pull_request` context;
- a deliberate manual dispatch.

The `pull_request_target` event is intentionally absent because it would grant the workflow the base repository's broader context while reviewing incoming work.

## Pinned environment

The job installs exact versions instead of inheriting whatever happens to be available on the runner:

| Component | Version |
| --- | --- |
| Node.js | `24.19.0` |
| pnpm | `11.19.0` |
| Python | `3.12.13` |
| JavaScript dependencies | `pnpm-lock.yaml` with frozen-lockfile enforcement |
| Sigma toolchain | exact packages in `requirements-sigma.lock` |

Remote actions use fully qualified `data.forgejo.org` URLs and immutable commit identifiers. Their comments record the reviewed release tag. Updating an action therefore requires an explicit source review and workflow-test change.

## Security boundary

- The workflow requests only `contents: read`.
- Checkout removes persisted repository credentials before project commands run.
- No repository, organization, deployment, cloud, or SIEM secret is referenced.
- No production endpoint is contacted by repository tests.
- The job requires a runner labelled `docker`; that label must map to a fresh isolated container and must not expose a host container socket, host credentials, or unrelated persistent workspace.
- Public pull requests execute incoming repository code. They are suitable only for the isolated, secret-free runner described above.

Forgejo documents the workflow directory and runner requirement in its [Actions overview](https://forgejo.org/docs/latest/user/actions/overview/), recommends fully qualified action URLs in [Using Actions](https://forgejo.org/docs/latest/user/actions/actions/), and describes pull-request and runner isolation risks in [Actions security](https://forgejo.org/docs/latest/user/actions/security/).

## Validation path

The workflow performs four steps after checkout and tool setup:

```console
npm install --global pnpm@11.19.0
pnpm install --frozen-lockfile
python -m pip install --requirement requirements-sigma.lock
pnpm run check
```

The aggregate check includes a workflow contract test. It rejects a changed trigger set, a non-container runner label, missing read-only permission, persisted checkout credentials, unpinned remote actions, changed tool versions, or a command that no longer runs the complete repository validation.

Local checks prove the YAML can be parsed and that the documented safety contract is present. A successful run on the actual Forgejo runner is still required before the server-side pipeline is considered operational or used as a release gate.
