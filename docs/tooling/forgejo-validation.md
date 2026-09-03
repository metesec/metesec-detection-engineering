# Forgejo repository validation

The workflow at `.forgejo/workflows/validate.yml` runs the same aggregate repository check used by contributors and builds a credential-free release candidate. It does not deploy a detection, query a SIEM, publish an artifact, or change repository content.

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
pnpm run build:release
```

The aggregate check includes a workflow contract test. It rejects a changed
trusted trigger set, a different runner label, missing read-only permission,
persisted checkout credentials, an unpinned remote action, changed tool
versions, or a command that no longer runs the complete repository validation.
It also requires the deterministic release candidate build after validation.
The aggregate check now also validates the public Sentinel data-source contract,
its exact relationship to the preview bindings, and the fail-closed health
evaluator. It supplies no environment observation, so the pipeline proves the
contract and evaluator rather than making a live telemetry-health claim.
The same check regenerates ATT&CK and data-source coverage in memory and rejects
stale tracked report output.
It also evaluates each manifest's review cadence against the current UTC date.
The job begins failing when any review becomes due or overdue; no time-dependent
assessment file is written. Cross-revision transition validation requires an
explicit previous catalogue and is not claimed by the default workflow.
Finally, it validates the Sentinel runtime-health policy, its exact relationship
to the forty-nine scheduled-rule definitions, the fail-closed evaluator and its
machine-output schema. CI supplies no rule observation, so this proves only the
portable contract. It neither queries Sentinel nor claims that a deployed rule
is healthy.

The live Forgejo pipeline is operational. Branch run `#1` and canonical main run
`#4` completed the original full aggregate check successfully. Isolated verification run
`#2` changed only the valid example's schema version and failed with the direct
message `valid/draft-windows-service-install.json: /schema_version must be equal
to constant`; cleanup run `#3` restored the valid source and passed. These runs
prove dispatch, toolchain, pass behavior, failure behavior and readable output.
They do not add SIEM deployment capability or make `host` mode safe for public
pull-request code.

## Protected main and release evidence

Forgejo protects exact branch `main`. Direct pushes are disabled, the rule applies
to administrators, rejected reviews and outdated branches block merging, and the
current single-owner phase requires zero approvals. A merge requires the exact
successful status context `Repository validation / Contracts, detections,
catalogue, and Sentinel preview (push)`.

Release branch run `#7` validated commit
`6bafe3c1d7a7e5cb58b707b9cd3364b8e84e7ad3`. Pull Request `#5` then merged only
through the protected path. Canonical main run `#8` validated merge commit
`f33f602a2fb6ecbc98475c6de567aa7d9b810ebe`, and tag run `#9` validated the same
commit through annotated tag `v0.1.0`. The workflow generated the deterministic
candidate but held no publication credential; a trusted operator uploaded the
two locally and independently verified assets after all three results passed.
