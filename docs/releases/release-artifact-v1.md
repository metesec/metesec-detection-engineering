# Detection Pack release artifact v1

The public release is a deterministic ZIP archive named
`metesec-detection-pack-v<VERSION>.zip`. `VERSION` comes from `package.json`.
The build also produces `SHA256SUMS` for independent integrity verification.
The builder requires matching notes at `docs/releases/v<VERSION>.md`, so a
version change cannot silently reuse notes from an older release.

## Included material

The archive contains the public catalogue, logical manifests, schema contracts,
portable Sigma rules, synthetic positive and negative fixtures, explicit
Microsoft Sentinel preview bindings, reviewed Golden KQL snapshots, essential
scope documentation, Sentinel data-source contract, the security policy and the
generated ATT&CK/data-source coverage report, and the Apache-2.0 license.
The versioned lifecycle and Sentinel runtime-health policies and their schemas
are included; runtime assessments are not.

Data-source and rule-runtime observations and their derived live-health results
are deliberately not packaged. They remain temporary inputs owned by the
consuming environment. Alert and incident counts never enter the public source
artifact as live environment results.

The ZIP is a curated Detection Pack, not a complete repository checkout. The
validators, generators and CI definitions remain in the canonical source
repository. Use `SHA256SUMS` and the internal manifest to verify a downloaded
pack; use a repository checkout when rebuilding or running the complete test
suite.

`RELEASE-MANIFEST.json` records every included source path, normalized byte size
and SHA-256 digest. It also states the catalogue totals and makes the boundary
explicit: the archive contains a Sentinel preview, not a SIEM deployment bundle.

## Reproducibility contract

The builder:

- discovers only an allowlisted set of repository paths;
- rejects missing sources, symlinks, path traversal and non-UTF-8 input;
- normalizes all packaged text to LF line endings;
- sorts every archive member;
- uses one fixed ZIP timestamp and file mode;
- stores members without platform-dependent compression;
- emits no runtime timestamp, workstation path, Git credential or environment ID.

Build and verify from a repository checkout with:

```console
pnpm run build:release
python -m unittest tests.test_release_builder
```

Two independent builds from the same source revision must produce byte-identical
ZIP and `SHA256SUMS` files. A published Forgejo release must point to the exact
validated `main` commit and attach both files. The checksum proves integrity, not
authorship; a future signing milestone may add a cryptographic signature without
changing this format.
