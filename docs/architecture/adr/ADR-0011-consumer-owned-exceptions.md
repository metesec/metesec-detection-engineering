# ADR-0011: Keep environment exceptions consumer-owned

- Status: Accepted
- Date: 2026-09-03

## Context

The project is intended to provide a modular Detection-as-Code foundation.
Exceptions, allowlists and local tuning depend on a consumer's identities,
business processes, risk decisions and approval model. A public exception model
would prescribe policy that cannot be correct for every environment and could
encourage copying unsuitable exclusions.

## Decision

Do not add a public exception-object contract to the current project. Keep
environment-specific tuning, exclusions, allowlists and exceptions in the
consumer's own reviewed pipeline or configuration layer.

The public repository continues to provide stable detection identities,
portable implementations, synthetic tests, deterministic target rendering and
explicit data-source requirements. Consumers may adapt those modules for their
environment without a MeteSec-specific exception format.

## Consequences

- The reference implementation stays small and modular.
- No customer identity, local value or policy decision belongs in the public
  repository.
- The project does not validate exception ownership, approval or expiry.
- Consumers remain responsible for testing and reviewing every local change.

## Reconsider when

- interoperable exception exchange becomes a concrete project requirement;
- a real consumer workflow demonstrates that a shared contract is useful;
- a future deployment layer needs a vendor-neutral exception boundary.
