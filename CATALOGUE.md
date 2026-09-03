<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:catalogue`. -->

# Detection catalogue

This index is generated deterministically from the versioned detection manifests, implementation-local fixture indexes, and explicit Sentinel preview profile.

## Summary

- Detection packages: **15**
- Implementations: **15**
- Synthetic evidence: **45 positive / 60 negative cases**
- Sentinel preview bindings: **14**

## Coverage

| ID | Detection | Status | Severity | ATT&CK | Data source | Synthetic evidence | Sentinel preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | Windows service installation from a public or temporary path | experimental | medium | `T1543.003` | Windows service installation events | 3 positive / 4 negative | — |
| [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json) | Successful sign-in from a legacy client category | experimental | medium | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | Successful high-risk Microsoft Entra sign-in | experimental | high | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json) | Credential added to a Microsoft Entra service principal | experimental | high | `T1098.001` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) | Application role granted to a Microsoft Entra service principal | experimental | medium | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json) | Office application starts a command or script interpreter | experimental | high | `T1059` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json) | PowerShell process uses an encoded-command flag | experimental | high | `T1059.001` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json) | Permanent Microsoft Entra role assignment outside PIM | experimental | high | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json) | Security information registered for a Microsoft Entra account | experimental | medium | `T1098.001` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | High-risk Microsoft Entra user risk event remains active | experimental | high | `T1078.004` | Microsoft Entra user risk events | 3 positive / 4 negative | `AADUserRiskEvents` |
| [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json) | Potential LSASS memory dump through rundll32 and comsvcs | experimental | high | `T1003.001` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json) | Mshta executes content from a remote location | experimental | high | `T1218.005` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) | Regsvr32 references a remote scriptlet or DLL | experimental | medium | `T1218.010` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json) | Microsoft Entra Conditional Access policy deleted | experimental | medium | `T1556.009` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) | Owner added to a Microsoft Entra application or service principal | experimental | medium | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |

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

### MSEC-DET-0006 — Office application starts a command or script interpreter

Detects a Microsoft Office application starting a selected command, script, or signed-binary interpreter in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1059` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0006/rule.yml](content/portable/sigma/MSEC-DET-0006/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0006.kql)
- Source: [catalog/detections/MSEC-DET-0006/manifest.json](catalog/detections/MSEC-DET-0006/manifest.json)

### MSEC-DET-0007 — PowerShell process uses an encoded-command flag

Detects Windows PowerShell or PowerShell Core command lines containing selected encoded-command flags in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1059.001` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0007/rule.yml](content/portable/sigma/MSEC-DET-0007/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0007.kql)
- Source: [catalog/detections/MSEC-DET-0007/manifest.json](catalog/detections/MSEC-DET-0007/manifest.json)

### MSEC-DET-0008 — Permanent Microsoft Entra role assignment outside PIM

Detects a successful permanent Microsoft Entra role assignment made outside Privileged Identity Management.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0008/rule.yml](content/portable/sigma/MSEC-DET-0008/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0008.kql)
- Source: [catalog/detections/MSEC-DET-0008/manifest.json](catalog/detections/MSEC-DET-0008/manifest.json)

### MSEC-DET-0009 — Security information registered for a Microsoft Entra account

Detects successful administrator or user registration of security information for a Microsoft Entra account.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1098.001` (Persistence)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0009/rule.yml](content/portable/sigma/MSEC-DET-0009/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0009.kql)
- Source: [catalog/detections/MSEC-DET-0009/manifest.json](catalog/detections/MSEC-DET-0009/manifest.json)

### MSEC-DET-0010 — High-risk Microsoft Entra user risk event remains active

Detects a high-risk Microsoft Entra Identity Protection user risk event whose state is at risk or confirmed compromised.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1078.004` (Initial Access)
- Data sources: Microsoft Entra user risk events (Identity risk)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0010/rule.yml](content/portable/sigma/MSEC-DET-0010/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AADUserRiskEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0010.kql)
- Source: [catalog/detections/MSEC-DET-0010/manifest.json](catalog/detections/MSEC-DET-0010/manifest.json)

### MSEC-DET-0011 — Potential LSASS memory dump through rundll32 and comsvcs

Detects rundll32 invoking the comsvcs MiniDump export or ordinal 24, a documented process-dump primitive that can target LSASS. The process event alone does not resolve the target PID.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1003.001` (Credential Access)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0011/rule.yml](content/portable/sigma/MSEC-DET-0011/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0011.kql)
- Source: [catalog/detections/MSEC-DET-0011/manifest.json](catalog/detections/MSEC-DET-0011/manifest.json)

### MSEC-DET-0012 — Mshta executes content from a remote location

Detects mshta command lines that reference HTTP, HTTPS or FTP content in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1218.005` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0012/rule.yml](content/portable/sigma/MSEC-DET-0012/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0012.kql)
- Source: [catalog/detections/MSEC-DET-0012/manifest.json](catalog/detections/MSEC-DET-0012/manifest.json)

### MSEC-DET-0013 — Regsvr32 references a remote scriptlet or DLL

Detects regsvr32 command lines that combine the install flag with an HTTP, HTTPS or FTP resource in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.010` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0013/rule.yml](content/portable/sigma/MSEC-DET-0013/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0013.kql)
- Source: [catalog/detections/MSEC-DET-0013/manifest.json](catalog/detections/MSEC-DET-0013/manifest.json)

### MSEC-DET-0014 — Microsoft Entra Conditional Access policy deleted

Detects a successful Microsoft Entra audit operation that deletes a Conditional Access policy.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1556.009` (Defense Evasion)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0014/rule.yml](content/portable/sigma/MSEC-DET-0014/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0014.kql)
- Source: [catalog/detections/MSEC-DET-0014/manifest.json](catalog/detections/MSEC-DET-0014/manifest.json)

### MSEC-DET-0015 — Owner added to a Microsoft Entra application or service principal

Detects a successful Microsoft Entra audit operation that adds an owner to an application registration or enterprise application service principal.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0015/rule.yml](content/portable/sigma/MSEC-DET-0015/rule.yml) — `active`; targets `sentinel`
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0015.kql)
- Source: [catalog/detections/MSEC-DET-0015/manifest.json](catalog/detections/MSEC-DET-0015/manifest.json)
