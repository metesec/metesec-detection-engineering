<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:catalogue`. -->

# Detection catalogue

This index is generated deterministically from the versioned detection manifests, implementation-local fixture indexes, and explicit Sentinel preview profile.

## Summary

- Detection packages: **5**
- Implementations: **5**
- Synthetic evidence: **15 positive / 20 negative cases**
- Sentinel preview bindings: **4**

## Coverage

| ID | Detection | Status | Severity | ATT&CK | Data source | Synthetic evidence | Sentinel preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | Windows service installation from a public or temporary path | experimental | medium | `T1543.003` | Windows service installation events | 3 positive / 4 negative | — |
| [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json) | Successful sign-in from a legacy client category | experimental | medium | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | Successful high-risk Microsoft Entra sign-in | experimental | high | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json) | Credential added to a Microsoft Entra service principal | experimental | high | `T1098.001` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) | Application role granted to a Microsoft Entra service principal | experimental | medium | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |

## Records

### MSEC-DET-0001 — Windows service installation from a public or temporary path

Detects a new Windows service whose image path points into a public-user or temporary directory and therefore warrants investigation.

- Lifecycle: `experimental`; created 2026-08-27; review every 90 days
- Severity / confidence: `medium` / `low`
- ATT&CK: `T1543.003` (Persistence)
- Data sources: Windows service installation events (Windows service control manager)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0001/rule.yml](content/portable/sigma/MSEC-DET-0001/rule.yml) — `active`; targets `sentinel`
- Sentinel preview: not bound
- Source: [catalog/detections/MSEC-DET-0001/manifest.json](catalog/detections/MSEC-DET-0001/manifest.json)

### MSEC-DET-0002 — Successful sign-in from a legacy client category

Detects a successful Microsoft Entra sign-in reported through a client category associated with legacy authentication and therefore requiring validation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1078.004` (Initial Access)
- Data sources: Microsoft Entra sign-in logs (Identity authentication)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0002/rule.yml](content/portable/sigma/MSEC-DET-0002/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `SigninLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0002.kql)
- Source: [catalog/detections/MSEC-DET-0002/manifest.json](catalog/detections/MSEC-DET-0002/manifest.json)

### MSEC-DET-0003 — Successful high-risk Microsoft Entra sign-in

Detects a successful Microsoft Entra sign-in that Identity Protection assessed as high risk during the sign-in.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1078.004` (Initial Access)
- Data sources: Microsoft Entra sign-in logs (Identity authentication)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0003/rule.yml](content/portable/sigma/MSEC-DET-0003/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `SigninLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0003.kql)
- Source: [catalog/detections/MSEC-DET-0003/manifest.json](catalog/detections/MSEC-DET-0003/manifest.json)

### MSEC-DET-0004 — Credential added to a Microsoft Entra service principal

Detects a successful Microsoft Entra audit event that adds authentication credentials to a service principal.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1098.001` (Persistence)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0004/rule.yml](content/portable/sigma/MSEC-DET-0004/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0004.kql)
- Source: [catalog/detections/MSEC-DET-0004/manifest.json](catalog/detections/MSEC-DET-0004/manifest.json)

### MSEC-DET-0005 — Application role granted to a Microsoft Entra service principal

Detects a successful Microsoft Entra audit event that grants an application role or API permission to a service principal.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0005/rule.yml](content/portable/sigma/MSEC-DET-0005/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0005.kql)
- Source: [catalog/detections/MSEC-DET-0005/manifest.json](catalog/detections/MSEC-DET-0005/manifest.json)
