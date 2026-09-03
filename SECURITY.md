# Security Policy

## Reporting a vulnerability

Do not publish credentials, exploitable infrastructure details, personal data, customer data, or an unpatched vulnerability in a public Issue.

Until a dedicated private reporting channel is published, use the contact method listed on the MeteSec website and include only the minimum information required to establish contact. Sensitive technical evidence should be exchanged only after a private channel has been agreed.

## Repository boundaries

This public repository must never contain:

- production credentials or tokens;
- private keys or certificates with private material;
- tenant, subscription, workspace, or customer identifiers;
- confidential telemetry or production query results;
- real allowlists, watchlists, exceptions, or internal network values;
- unredacted incident evidence;
- instructions to execute attack simulations outside an explicitly authorized lab.

All fixtures must be synthetic, safely redacted, or explicitly licensed for public redistribution.

## Supported versions

Security fixes apply to the current `main` branch and the latest published
release. Older release lines are unsupported unless a release note explicitly
states otherwise. Detection content remains experimental and the Detection Pack
is not a production deployment bundle.
