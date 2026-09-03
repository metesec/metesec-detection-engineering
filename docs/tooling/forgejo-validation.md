# Forgejo repository validation

The workflow at `.forgejo/workflows/validate.yml` runs the same aggregate repository check used by contributors. It is validation only: it does not compile a release, deploy a detection, query a SIEM, publish an artifact, or change repository content.

## Events

The workflow runs for:

- every push from an authorized repository writer;
- a deliberate manual dispatch.

Automatic pull-request execution is intentionally absent. The current dedicated
runner uses Forgejo's `host` execution mode inside a locked-down Kubernetes Pod,
which does not provide a fresh job container. Running arbitrary public pull
request code there would expose the persistent runner process and registration
to untrusted code. External contributions must therefore be reviewed and tested
locally before an authorized writer pushes the accepted commit.

## Pinned environment

The dedicated runner provides exact Node.js and Python versions and the workflow
fails immediately if either version drifts:

| Component | Version |
| --- | --- |
| Node.js | `24.19.0` |
| pnpm | `11.19.0` |
| Python | `3.12.13` |
| JavaScript dependencies | `pnpm-lock.yaml` with frozen-lockfile enforcement |
| Sigma toolchain | exact packages in `requirements-sigma.lock` |

The sole remote action uses a fully qualified `data.forgejo.org` URL and an
immutable commit identifier. Its comment records the reviewed release tag.
Updating it therefore requires an explicit source review and workflow-test
change.

## Security boundary

- The workflow requests only `contents: read`.
- Checkout removes persisted repository credentials before project commands run.
- No repository, organization, deployment, cloud, or SIEM secret is referenced.
- No production endpoint is contacted by repository tests.
- The job requires the repository-specific label `metesec-detection-validate`.
- The runner has no Kubernetes token or RBAC, no host path, no container-runtime
  socket, no BuildKit socket, no deployment credential, no package-publisher
  credential and no SIEM or cloud secret.
- `host` mode means there is no hard job-container isolation. This is accepted
  only for the current single-owner, trusted-push workflow and must be replaced
  by a containerized or ephemeral design before enabling public pull requests.

Forgejo documents the workflow directory and runner requirement in its [Actions overview](https://forgejo.org/docs/latest/user/actions/overview/), recommends fully qualified action URLs in [Using Actions](https://forgejo.org/docs/latest/user/actions/actions/), and describes pull-request and runner isolation risks in [Actions security](https://forgejo.org/docs/latest/user/actions/security/).

## Validation path

The workflow verifies the runner toolchain, creates a disposable Python virtual
environment, and then performs the same repository validation used locally:

```console
npm install --global --prefix "$RUNNER_TEMP/pnpm" pnpm@11.19.0
python -m venv "$RUNNER_TEMP/venv"
pnpm install --frozen-lockfile
python -m pip install --requirement requirements-sigma.lock
pnpm run check
```

The aggregate check includes a workflow contract test. It rejects a changed
trusted trigger set, a different runner label, missing read-only permission,
persisted checkout credentials, an unpinned remote action, changed tool
versions, or a command that no longer runs the complete repository validation.

Local checks prove the YAML can be parsed and that the documented safety contract is present. A successful run on the actual Forgejo runner is still required before the server-side pipeline is considered operational or used as a release gate.
