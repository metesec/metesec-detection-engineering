<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:catalogue`. -->

# Detection catalogue

This index is generated deterministically from the versioned detection manifests, implementation-local fixture indexes, and explicit Sentinel preview profile.

## Summary

- Detection packages: **67**
- Implementations: **67**
- Synthetic evidence: **264 positive / 441 negative cases**
- Sentinel preview bindings: **66**

## Coverage

| ID | Detection | Status | Severity | ATT&CK | Data source | Synthetic evidence | Sentinel preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | Windows service installation from a public or temporary path | experimental | medium | `T1543.003` | Windows service installation events | 4 positive / 6 negative | — |
| [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json) | Successful sign-in from a legacy client category | experimental | low | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | Successful high-risk Microsoft Entra sign-in | experimental | high | `T1078.004` | Microsoft Entra sign-in logs | 3 positive / 4 negative | `SigninLogs` |
| [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json) | Credential added to a Microsoft Entra service principal | experimental | medium | `T1098.001` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) | Application role granted to a Microsoft Entra service principal | experimental | low | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json) | Office application starts a command or script interpreter | experimental | medium | `T1059` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json) | PowerShell process uses an encoded-command flag | experimental | low | `T1059.001` | Microsoft Defender for Endpoint process events | 6 positive / 7 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json) | Permanent Microsoft Entra role assignment outside PIM | experimental | medium | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json) | Security information registered for a Microsoft Entra account | experimental | low | `T1098.001` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | High-risk Microsoft Entra user risk event remains active | experimental | high | `T1078.004` | Microsoft Entra user risk events | 3 positive / 4 negative | `AADUserRiskEvents` |
| [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json) | Potential LSASS memory dump through rundll32 and comsvcs | experimental | high | `T1003.001` | Microsoft Defender for Endpoint process events | 4 positive / 6 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json) | Mshta command references a remote resource | experimental | high | `T1218.005` | Microsoft Defender for Endpoint process events | 3 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) | Regsvr32 references a remote scriptlet or DLL | experimental | medium | `T1218.010` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json) | Microsoft Entra Conditional Access policy deleted | experimental | medium | `T1556.009` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) | Owner added to a Microsoft Entra application or service principal | experimental | medium | `T1098.003` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0016`](catalog/detections/MSEC-DET-0016/manifest.json) | Native Windows utility attempts to inhibit system recovery | experimental | high | `T1490` | Microsoft Defender for Endpoint process events | 7 positive / 7 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0017`](catalog/detections/MSEC-DET-0017/manifest.json) | Process attempts to clear a Windows event log | experimental | high | `T1685.005` | Microsoft Defender for Endpoint process events | 5 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0018`](catalog/detections/MSEC-DET-0018/manifest.json) | PowerShell attempts to weaken Microsoft Defender Antivirus | experimental | high | `T1685` | Microsoft Defender for Endpoint process events | 6 positive / 10 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json) | Microsoft Entra federation trust configuration changed | experimental | high | `T1484.002`, `T1484.002` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0020`](catalog/detections/MSEC-DET-0020/manifest.json) | Certutil forces retrieval of remote URL cache content | experimental | medium | `T1105` | Microsoft Defender for Endpoint process events | 3 positive / 8 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json) | Highly privileged delegated permission granted for all users | experimental | high | `T1098.003`, `T1098.003` | Microsoft Entra audit logs | 5 positive / 11 negative | `AuditLogs` |
| [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json) | Microsoft Entra strong authentication disabled | experimental | medium | `T1556.006`, `T1556.006`, `T1556.006` | Microsoft Entra audit logs | 3 positive / 4 negative | `AuditLogs` |
| [`MSEC-DET-0023`](catalog/detections/MSEC-DET-0023/manifest.json) | Reg.exe exports the SAM or SECURITY registry hive | experimental | high | `T1003.002` | Microsoft Defender for Endpoint process events | 5 positive / 6 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0024`](catalog/detections/MSEC-DET-0024/manifest.json) | WMI or CIM process creation with an explicit target selector | experimental | medium | `T1047` | Microsoft Defender for Endpoint process events | 5 positive / 6 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json) | BITSAdmin requests a remote transfer or adds a remote file | experimental | medium | `T1197`, `T1197`, `T1197` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0026`](catalog/detections/MSEC-DET-0026/manifest.json) | Successful Microsoft Entra ROPC sign-in | experimental | low | `T1078.004` | Microsoft Entra sign-in logs | 4 positive / 5 negative | `SigninLogs` |
| [`MSEC-DET-0027`](catalog/detections/MSEC-DET-0027/manifest.json) | Rundll32 invokes inline script through MSHTML | experimental | high | `T1218.011` | Microsoft Defender for Endpoint process events | 4 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json) | Remote scheduled task creation command | experimental | medium | `T1053.005`, `T1053.005`, `T1053.005` | Microsoft Defender for Endpoint process events | 4 positive / 6 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json) | Local Administrators membership addition command | experimental | high | `T1098.007`, `T1098.007` | Microsoft Defender for Endpoint process events | 6 positive / 9 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0030`](catalog/detections/MSEC-DET-0030/manifest.json) | NTDSutil installation-media creation command | experimental | high | `T1003.003` | Microsoft Defender for Endpoint process events | 4 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0031`](catalog/detections/MSEC-DET-0031/manifest.json) | Suspicious process spawned by a web server | experimental | high | `T1505.003` | Microsoft Defender for Endpoint process events | 4 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0032`](catalog/detections/MSEC-DET-0032/manifest.json) | Windows audit-policy clear command | experimental | high | `T1685.001` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0033`](catalog/detections/MSEC-DET-0033/manifest.json) | Windows Firewall profile disable command | experimental | high | `T1686.003` | Microsoft Defender for Endpoint process events | 5 positive / 6 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json) | Remote Windows service creation command through SC | experimental | medium | `T1543.003`, `T1543.003` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0035`](catalog/detections/MSEC-DET-0035/manifest.json) | Certutil file decode command | experimental | medium | `T1140` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0036`](catalog/detections/MSEC-DET-0036/manifest.json) | ProcDump command targets LSASS by name | experimental | high | `T1003.001` | Microsoft Defender for Endpoint process events | 3 positive / 7 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json) | Fodhelper spawns a suspicious child process | experimental | high | `T1548.002`, `T1548.002` | Microsoft Defender for Endpoint process events | 3 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0038`](catalog/detections/MSEC-DET-0038/manifest.json) | WinRM host spawns a command or administrative process | experimental | low | `T1021.006` | Microsoft Defender for Endpoint process events | 4 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0039`](catalog/detections/MSEC-DET-0039/manifest.json) | PowerShell download-and-execute cradle | experimental | medium | `T1059.001` | Microsoft Defender for Endpoint process events | 5 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) | Accessibility feature IFEO debugger hijack | experimental | high | `T1546.008`, `T1546.008` | Microsoft Defender for Endpoint registry events | 3 positive / 8 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0041`](catalog/detections/MSEC-DET-0041/manifest.json) | CMSTP spawns a child process | experimental | medium | `T1218.003` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0042`](catalog/detections/MSEC-DET-0042/manifest.json) | Odbcconf REGSVR registration command | experimental | medium | `T1218.008` | Microsoft Defender for Endpoint process events | 5 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json) | Msiexec remote web package installation command | experimental | medium | `T1218.007`, `T1105` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json) | InstallUtil remote assembly argument | experimental | medium | `T1218.004`, `T1105` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) | MSBuild spawns a suspicious child process | experimental | medium | `T1127.001`, `T1127.001` | Microsoft Defender for Endpoint process events | 4 positive / 4 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0046`](catalog/detections/MSEC-DET-0046/manifest.json) | Suspicious script or LOLBin payload in a Run key | experimental | medium | `T1547.001`, `T1547.001` | Microsoft Defender for Endpoint registry events | 3 positive / 6 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0047`](catalog/detections/MSEC-DET-0047/manifest.json) | Winlogon Shell or Userinit value hijack | experimental | high | `T1547.004`, `T1547.004` | Microsoft Defender for Endpoint registry events | 4 positive / 8 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0048`](catalog/detections/MSEC-DET-0048/manifest.json) | Suspicious local scheduled task creation command | experimental | medium | `T1053.005`, `T1053.005`, `T1053.005` | Microsoft Defender for Endpoint process events | 5 positive / 8 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0049`](catalog/detections/MSEC-DET-0049/manifest.json) | Mavinject process injection command | experimental | high | `T1218.013` | Microsoft Defender for Endpoint process events | 4 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0050`](catalog/detections/MSEC-DET-0050/manifest.json) | Netsh PortProxy addition command | experimental | medium | `T1090.001` | Microsoft Defender for Endpoint process events | 5 positive / 5 negative | `DeviceProcessEvents` |
| [`MSEC-DET-0054`](catalog/detections/MSEC-DET-0054/manifest.json) | Azure diagnostic or Activity Log export deleted | experimental | medium | `T1685.002` | Azure Activity administrative events | 4 positive / 7 negative | `AzureActivity` |
| [`MSEC-DET-0055`](catalog/detections/MSEC-DET-0055/manifest.json) | SilentProcessExit monitor configured with an interpreter or staging path | experimental | high | `T1546.012` | Microsoft Defender for Endpoint registry events | 3 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0056`](catalog/detections/MSEC-DET-0056/manifest.json) | LSASS loads a DLL from a staging or remote location | experimental | high | `T1547.005` | Microsoft Defender for Endpoint image-load events | 4 positive / 11 negative | `DeviceImageLoadEvents` |
| [`MSEC-DET-0057`](catalog/detections/MSEC-DET-0057/manifest.json) | System-named process connects publicly from a staging or remote location | experimental | high | `T1036.005` | Microsoft Defender for Endpoint network events | 4 positive / 9 negative | `DeviceNetworkEvents` |
| [`MSEC-DET-0060`](catalog/detections/MSEC-DET-0060/manifest.json) | NTDS database filename created in a staging or remote location | experimental | high | `T1003.003` | Microsoft Defender for Endpoint file events | 4 positive / 8 negative | `DeviceFileEvents` |
| [`MSEC-DET-0063`](catalog/detections/MSEC-DET-0063/manifest.json) | Defender Antivirus engine loads a DLL from a staging or remote location | experimental | high | `T1574.001` | Microsoft Defender for Endpoint image-load events | 4 positive / 11 negative | `DeviceImageLoadEvents` |
| [`MSEC-DET-0064`](catalog/detections/MSEC-DET-0064/manifest.json) | RunAsPPL explicitly zeroed or removed | experimental | medium | `T1685` | Microsoft Defender for Endpoint registry events | 5 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0066`](catalog/detections/MSEC-DET-0066/manifest.json) | Azure soft-deleted Key Vault purged | experimental | high | `T1485` | Azure Activity administrative events | 3 positive / 7 negative | `AzureActivity` |
| [`MSEC-DET-0068`](catalog/detections/MSEC-DET-0068/manifest.json) | Credential Guard registry configuration explicitly zeroed | experimental | medium | `T1685` | Microsoft Defender for Endpoint registry events | 4 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0073`](catalog/detections/MSEC-DET-0073/manifest.json) | LSASS credential-theft ASR rule configured as disabled | experimental | medium | `T1685` | Microsoft Defender for Endpoint registry events | 3 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0076`](catalog/detections/MSEC-DET-0076/manifest.json) | AWS CloudTrail logging stopped or trail deleted | experimental | high | `T1685.002` | AWS CloudTrail management events | 3 positive / 14 negative | `AWSCloudTrail` |
| [`MSEC-DET-0080`](catalog/detections/MSEC-DET-0080/manifest.json) | Office 16 Trusted Location configured in a high-risk directory | experimental | medium | `T1553` | Microsoft Defender for Endpoint registry events | 4 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0081`](catalog/detections/MSEC-DET-0081/manifest.json) | AWS GuardDuty detector deleted | experimental | high | `T1685` | AWS CloudTrail management events | 2 positive / 14 negative | `AWSCloudTrail` |
| [`MSEC-DET-0083`](catalog/detections/MSEC-DET-0083/manifest.json) | Azure tenant-root access elevation succeeded | experimental | high | `T1098.003` | Azure Activity administrative events | 3 positive / 7 negative | `AzureActivity` |
| [`MSEC-DET-0085`](catalog/detections/MSEC-DET-0085/manifest.json) | Netsh helper DLL registered from a staging or remote path | experimental | high | `T1546.007` | Microsoft Defender for Endpoint registry events | 4 positive / 10 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0089`](catalog/detections/MSEC-DET-0089/manifest.json) | Print port monitor DLL registered from a staging or remote path | experimental | high | `T1547.010` | Microsoft Defender for Endpoint registry events | 5 positive / 12 negative | `DeviceRegistryEvents` |
| [`MSEC-DET-0100`](catalog/detections/MSEC-DET-0100/manifest.json) | AppCert DLL registered from a staging or remote path | experimental | high | `T1546.009` | Microsoft Defender for Endpoint registry events | 5 positive / 10 negative | `DeviceRegistryEvents` |

## Records

### MSEC-DET-0001 — Windows service installation from a public or temporary path

Detects a new Windows service whose image path points into a public-user or temporary directory and therefore warrants investigation.

- Lifecycle: `experimental`; created 2026-08-27; review every 90 days
- Severity / confidence: `medium` / `low`
- ATT&CK: `T1543.003` (Persistence)
- Data sources: Windows service installation events (Windows service control manager)
- Synthetic evidence: 4 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0001/rule.yml](content/portable/sigma/MSEC-DET-0001/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Windows System Event 7045 telemetry is not bound to Sentinel in this repository. A staged service binary can be legitimate installation activity.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview: not bound
- Source: [catalog/detections/MSEC-DET-0001/manifest.json](catalog/detections/MSEC-DET-0001/manifest.json)

### MSEC-DET-0002 — Successful sign-in from a legacy client category

Detects successful Microsoft Entra sign-ins reported through selected legacy client categories. This is a policy-hygiene signal; the client label alone does not establish the authentication mechanism, bypass or compromise.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1078.004` (Initial Access)
- Data sources: Microsoft Entra sign-in logs (Identity authentication)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0002/rule.yml](content/portable/sigma/MSEC-DET-0002/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
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
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This forwards a vendor risk assessment; the sign-in risk level is not independent proof of account compromise.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `SigninLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0003.kql)
- Source: [catalog/detections/MSEC-DET-0003/manifest.json](catalog/detections/MSEC-DET-0003/manifest.json)

### MSEC-DET-0004 — Credential added to a Microsoft Entra service principal

Detects successful addition of credentials to a Microsoft Entra service principal. This broad change-monitoring signal includes normal provisioning and rotation and needs application and actor context.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `low`
- ATT&CK: `T1098.001` (Persistence)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0004/rule.yml](content/portable/sigma/MSEC-DET-0004/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0004.kql)
- Source: [catalog/detections/MSEC-DET-0004/manifest.json](catalog/detections/MSEC-DET-0004/manifest.json)

### MSEC-DET-0005 — Application role granted to a Microsoft Entra service principal

Detects successful app-role assignments to Microsoft Entra service principals. The operation alone does not reveal permission severity or malicious intent; use it for change monitoring and correlation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0005/rule.yml](content/portable/sigma/MSEC-DET-0005/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0005.kql)
- Source: [catalog/detections/MSEC-DET-0005/manifest.json](catalog/detections/MSEC-DET-0005/manifest.json)

### MSEC-DET-0006 — Office application starts a command or script interpreter

Detects a Microsoft Office application starting a selected command, script, or signed-binary interpreter in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1059` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0006/rule.yml](content/portable/sigma/MSEC-DET-0006/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0006.kql)
- Source: [catalog/detections/MSEC-DET-0006/manifest.json](catalog/detections/MSEC-DET-0006/manifest.json)

### MSEC-DET-0007 — PowerShell process uses an encoded-command flag

Detects PowerShell command lines containing a delimited encoded-command flag and Base64-shaped argument. Encoding is common in management tools; the argument is not decoded and the event alone does not establish malicious execution.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1059.001` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 6 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0007/rule.yml](content/portable/sigma/MSEC-DET-0007/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Encoded PowerShell is common in administration. This is a low-confidence hunt signal; payload decoding and contextual correlation are required.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0007.kql)
- Source: [catalog/detections/MSEC-DET-0007/manifest.json](catalog/detections/MSEC-DET-0007/manifest.json)

### MSEC-DET-0008 — Permanent Microsoft Entra role assignment outside PIM

Detects a successful permanent Microsoft Entra role assignment made outside Privileged Identity Management.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `low`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0008/rule.yml](content/portable/sigma/MSEC-DET-0008/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0008.kql)
- Source: [catalog/detections/MSEC-DET-0008/manifest.json](catalog/detections/MSEC-DET-0008/manifest.json)

### MSEC-DET-0009 — Security information registered for a Microsoft Entra account

Records successful administrator or user registration of Entra security information. Normal MFA enrollment dominates this change-monitoring signal; prioritize only after actor, account-risk or timing correlation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1098.001` (Persistence)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0009/rule.yml](content/portable/sigma/MSEC-DET-0009/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
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
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This forwards a vendor risk event and inherits the vendor's detection and licensing prerequisites.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AADUserRiskEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0010.kql)
- Source: [catalog/detections/MSEC-DET-0010/manifest.json](catalog/detections/MSEC-DET-0010/manifest.json)

### MSEC-DET-0011 — Potential LSASS memory dump through rundll32 and comsvcs

Detects rundll32 invoking the comsvcs MiniDump export or ordinal 24, a documented process-dump primitive that can target LSASS. The process event alone does not resolve the target PID.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1003.001` (Credential Access)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0011/rule.yml](content/portable/sigma/MSEC-DET-0011/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0011.kql)
- Source: [catalog/detections/MSEC-DET-0011/manifest.json](catalog/detections/MSEC-DET-0011/manifest.json)

### MSEC-DET-0012 — Mshta command references a remote resource

Detects mshta command lines referencing HTTP, HTTPS or FTP resources, including inline script download expressions. Process creation alone does not prove retrieval or execution.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1218.005` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0012/rule.yml](content/portable/sigma/MSEC-DET-0012/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0012.kql)
- Source: [catalog/detections/MSEC-DET-0012/manifest.json](catalog/detections/MSEC-DET-0012/manifest.json)

### MSEC-DET-0013 — Regsvr32 references a remote scriptlet or DLL

Detects regsvr32 command lines that combine the install flag with an HTTP, HTTPS or FTP resource in Microsoft Defender for Endpoint process telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.010` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0013/rule.yml](content/portable/sigma/MSEC-DET-0013/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
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
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
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
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0015.kql)
- Source: [catalog/detections/MSEC-DET-0015/manifest.json](catalog/detections/MSEC-DET-0015/manifest.json)

### MSEC-DET-0016 — Native Windows utility attempts to inhibit system recovery

Detects selected native Windows utilities attempting to delete shadow copies or backup catalogues, disable the Windows Recovery Environment, or weaken boot recovery. Process telemetry shows an attempt, not whether the change succeeded.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1490` (Impact)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 7 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0016/rule.yml](content/portable/sigma/MSEC-DET-0016/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0016.kql)
- Source: [catalog/detections/MSEC-DET-0016/manifest.json](catalog/detections/MSEC-DET-0016/manifest.json)

### MSEC-DET-0017 — Process attempts to clear a Windows event log

Detects wevtutil or PowerShell attempting to clear a Windows event log. Process telemetry shows the command attempt and does not prove that the log was cleared.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1685.005` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0017/rule.yml](content/portable/sigma/MSEC-DET-0017/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0017.kql)
- Source: [catalog/detections/MSEC-DET-0017/manifest.json](catalog/detections/MSEC-DET-0017/manifest.json)

### MSEC-DET-0018 — PowerShell attempts to weaken Microsoft Defender Antivirus

Detects literal PowerShell Defender cmdlets requesting selected disable switches with a true value or adding explicit non-empty exclusion values. Command-line evidence does not prove the configuration changed.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1685` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 6 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0018/rule.yml](content/portable/sigma/MSEC-DET-0018/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Only explicit command-line disable literals are covered. Variables, aliases, splatting, alternative APIs and actual resulting protection state are not evaluated.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0018.kql)
- Source: [catalog/detections/MSEC-DET-0018/manifest.json](catalog/detections/MSEC-DET-0018/manifest.json)

### MSEC-DET-0019 — Microsoft Entra federation trust configuration changed

Detects successful Microsoft Entra audit operations that change domain federation settings or domain authentication configuration.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1484.002` (Privilege Escalation), `T1484.002` (Defense Impairment)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0019/rule.yml](content/portable/sigma/MSEC-DET-0019/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0019.kql)
- Source: [catalog/detections/MSEC-DET-0019/manifest.json](catalog/detections/MSEC-DET-0019/manifest.json)

### MSEC-DET-0020 — Certutil forces retrieval of remote URL cache content

Detects certutil command lines combining a remote URL, a URL-cache command and the force-fetch switch. Cache display or deletion and a split option alone are outside the download-attempt claim.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1105` (Command and Control)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 8 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0020/rule.yml](content/portable/sigma/MSEC-DET-0020/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0020.kql)
- Source: [catalog/detections/MSEC-DET-0020/manifest.json](catalog/detections/MSEC-DET-0020/manifest.json)

### MSEC-DET-0021 — Highly privileged delegated permission granted for all users

Detects a successful delegated permission grant with the exact RoleManagement.ReadWrite.Directory scope and AllPrincipals consent in newValue properties from the same ServicePrincipal target. Requires the documented structural normalization.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1098.003` (Persistence), `T1098.003` (Privilege Escalation)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 5 positive and 11 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0021/rule.yml](content/portable/sigma/MSEC-DET-0021/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Only Scope and ConsentType newValue strings on the same ServicePrincipal target are supported. Missing, malformed, duplicate or differently structured properties are rejected; the adapter needs live KQL parity validation.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0021.kql)
- Source: [catalog/detections/MSEC-DET-0021/manifest.json](catalog/detections/MSEC-DET-0021/manifest.json)

### MSEC-DET-0022 — Microsoft Entra strong authentication disabled

Detects a successful Microsoft Entra audit operation that disables strong authentication for an account.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1556.006` (Defense Impairment), `T1556.006` (Persistence), `T1556.006` (Credential Access)
- Data sources: Microsoft Entra audit logs (Identity directory audit)
- Synthetic evidence: 3 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0022/rule.yml](content/portable/sigma/MSEC-DET-0022/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AuditLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0022.kql)
- Source: [catalog/detections/MSEC-DET-0022/manifest.json](catalog/detections/MSEC-DET-0022/manifest.json)

### MSEC-DET-0023 — Reg.exe exports the SAM or SECURITY registry hive

Detects reg.exe save or export commands targeting the SAM or SECURITY registry hive, a process-visible path toward offline credential extraction.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1003.002` (Credential Access)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0023/rule.yml](content/portable/sigma/MSEC-DET-0023/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0023.kql)
- Source: [catalog/detections/MSEC-DET-0023/manifest.json](catalog/detections/MSEC-DET-0023/manifest.json)

### MSEC-DET-0024 — WMI or CIM process creation with an explicit target selector

Detects Win32_Process creation with a WMIC node, PowerShell computer-name or CIM-session selector. These selectors may still resolve to the local computer; remote execution and successful creation require destination evidence.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1047` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0024/rule.yml](content/portable/sigma/MSEC-DET-0024/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0024.kql)
- Source: [catalog/detections/MSEC-DET-0024/manifest.json](catalog/detections/MSEC-DET-0024/manifest.json)

### MSEC-DET-0025 — BITSAdmin requests a remote transfer or adds a remote file

Detects BITSAdmin transfer requests and standalone addfile commands with an HTTP or HTTPS URL. Addfile configures an existing job; neither it nor process creation proves a successful transfer.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1197` (Stealth), `T1197` (Persistence), `T1197` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0025/rule.yml](content/portable/sigma/MSEC-DET-0025/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0025.kql)
- Source: [catalog/detections/MSEC-DET-0025/manifest.json](catalog/detections/MSEC-DET-0025/manifest.json)

### MSEC-DET-0026 — Successful Microsoft Entra ROPC sign-in

Detects a successful Microsoft Entra ROPC sign-in as a legacy-authentication hygiene signal; protocol use alone does not establish credential compromise.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1078.004` (Initial Access)
- Data sources: Microsoft Entra sign-in logs (Identity authentication)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0026/rule.yml](content/portable/sigma/MSEC-DET-0026/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `SigninLogs`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0026.kql)
- Source: [catalog/detections/MSEC-DET-0026/manifest.json](catalog/detections/MSEC-DET-0026/manifest.json)

### MSEC-DET-0027 — Rundll32 invokes inline script through MSHTML

Detects rundll32 command lines that invoke JavaScript or VBScript through the MSHTML RunHTMLApplication export.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1218.011` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0027/rule.yml](content/portable/sigma/MSEC-DET-0027/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0027.kql)
- Source: [catalog/detections/MSEC-DET-0027/manifest.json](catalog/detections/MSEC-DET-0027/manifest.json)

### MSEC-DET-0028 — Remote scheduled task creation command

Detects a Schtasks command requesting task creation with an explicit /s target. Process telemetry does not establish that the task was created successfully.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1053.005` (Execution), `T1053.005` (Persistence), `T1053.005` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0028/rule.yml](content/portable/sigma/MSEC-DET-0028/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0028.kql)
- Source: [catalog/detections/MSEC-DET-0028/manifest.json](catalog/detections/MSEC-DET-0028/manifest.json)

### MSEC-DET-0029 — Local Administrators membership addition command

Detects net or PowerShell commands requesting a member addition to the built-in local Administrators group using explicit English, German or SID forms. Confirm the actual membership change from account-management telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1098.007` (Persistence), `T1098.007` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 6 positive and 9 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0029/rule.yml](content/portable/sigma/MSEC-DET-0029/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0029.kql)
- Source: [catalog/detections/MSEC-DET-0029/manifest.json](catalog/detections/MSEC-DET-0029/manifest.json)

### MSEC-DET-0030 — NTDSutil installation-media creation command

Detects an NTDSutil command requesting Active Directory installation media through IFM after explicit NTDS instance activation. The process event does not confirm a database copy was produced.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1003.003` (Credential Access)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0030/rule.yml](content/portable/sigma/MSEC-DET-0030/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0030.kql)
- Source: [catalog/detections/MSEC-DET-0030/manifest.json](catalog/detections/MSEC-DET-0030/manifest.json)

### MSEC-DET-0031 — Suspicious process spawned by a web server

Detects command interpreters and administrative utilities spawned directly by common web-server processes.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1505.003` (Persistence)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0031/rule.yml](content/portable/sigma/MSEC-DET-0031/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0031.kql)
- Source: [catalog/detections/MSEC-DET-0031/manifest.json](catalog/detections/MSEC-DET-0031/manifest.json)

### MSEC-DET-0032 — Windows audit-policy clear command

Detects Auditpol commands requesting a system audit-policy clear or removal of all per-user audit policies. Verify the effective audit policy before concluding logging was impaired.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1685.001` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0032/rule.yml](content/portable/sigma/MSEC-DET-0032/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0032.kql)
- Source: [catalog/detections/MSEC-DET-0032/manifest.json](catalog/detections/MSEC-DET-0032/manifest.json)

### MSEC-DET-0033 — Windows Firewall profile disable command

Detects Netsh or PowerShell commands requesting Windows Firewall profile disablement. The false value must be the Enabled argument; process start alone does not establish a changed firewall state.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1686.003` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0033/rule.yml](content/portable/sigma/MSEC-DET-0033/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0033.kql)
- Source: [catalog/detections/MSEC-DET-0033/manifest.json](catalog/detections/MSEC-DET-0033/manifest.json)

### MSEC-DET-0034 — Remote Windows service creation command through SC

Detects SC commands requesting service creation on an explicit remote UNC host. Process creation does not establish that the remote operation succeeded.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1543.003` (Persistence), `T1543.003` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0034/rule.yml](content/portable/sigma/MSEC-DET-0034/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0034.kql)
- Source: [catalog/detections/MSEC-DET-0034/manifest.json](catalog/detections/MSEC-DET-0034/manifest.json)

### MSEC-DET-0035 — Certutil file decode command

Detects Certutil commands requesting Base64 or hexadecimal file decoding; approved certificate and support workflows can produce the same behavior.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1140` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0035/rule.yml](content/portable/sigma/MSEC-DET-0035/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0035.kql)
- Source: [catalog/detections/MSEC-DET-0035/manifest.json](catalog/detections/MSEC-DET-0035/manifest.json)

### MSEC-DET-0036 — ProcDump command targets LSASS by name

Detects ProcDump or a renamed ProcDump executable referencing LSASS as a command-line process-name token, including the default mini dump without a size switch. PID-only targeting requires separate process correlation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1003.001` (Credential Access)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0036/rule.yml](content/portable/sigma/MSEC-DET-0036/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0036.kql)
- Source: [catalog/detections/MSEC-DET-0036/manifest.json](catalog/detections/MSEC-DET-0036/manifest.json)

### MSEC-DET-0037 — Fodhelper spawns a suspicious child process

Detects fodhelper.exe spawning a command interpreter or administrative utility associated with UAC bypass activity.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1548.002` (Privilege Escalation), `T1548.002` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 3 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0037/rule.yml](content/portable/sigma/MSEC-DET-0037/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0037.kql)
- Source: [catalog/detections/MSEC-DET-0037/manifest.json](catalog/detections/MSEC-DET-0037/manifest.json)

### MSEC-DET-0038 — WinRM host spawns a command or administrative process

Detects selected command and administrative children of wsmprovhost.exe as remote-execution visibility. This relationship is common in legitimate PowerShell remoting and is not sufficient evidence of lateral movement.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `low` / `low`
- ATT&CK: `T1021.006` (Lateral Movement)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0038/rule.yml](content/portable/sigma/MSEC-DET-0038/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: WinRM worker child execution is routine management activity. Validate source host, identity and administrative change context before escalation.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0038.kql)
- Source: [catalog/detections/MSEC-DET-0038/manifest.json](catalog/detections/MSEC-DET-0038/manifest.json)

### MSEC-DET-0039 — PowerShell download-and-execute cradle

Detects visible PowerShell command lines containing both a selected download primitive and an expression-execution token. This is a co-occurrence heuristic; it does not prove that the downloaded content was executed.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1059.001` (Execution)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0039/rule.yml](content/portable/sigma/MSEC-DET-0039/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0039.kql)
- Source: [catalog/detections/MSEC-DET-0039/manifest.json](catalog/detections/MSEC-DET-0039/manifest.json)

### MSEC-DET-0040 — Accessibility feature IFEO debugger hijack

Detects a non-empty Debugger value written to the machine-wide IFEO path of a selected Windows accessibility or logon helper executable. Deletion and incomplete payload events are excluded.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `high`
- ATT&CK: `T1546.008` (Persistence), `T1546.008` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 3 positive and 8 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0040/rule.yml](content/portable/sigma/MSEC-DET-0040/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0040.kql)
- Source: [catalog/detections/MSEC-DET-0040/manifest.json](catalog/detections/MSEC-DET-0040/manifest.json)

### MSEC-DET-0041 — CMSTP spawns a child process

Detects a child process created by CMSTP. Legitimate profile installers can invoke helper programs, so the child and INF content require review before escalation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.003` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0041/rule.yml](content/portable/sigma/MSEC-DET-0041/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0041.kql)
- Source: [catalog/detections/MSEC-DET-0041/manifest.json](catalog/detections/MSEC-DET-0041/manifest.json)

### MSEC-DET-0042 — Odbcconf REGSVR registration command

Detects Odbcconf commands containing a braced REGSVR action and a payload argument, regardless of filename extension. Process start alone does not confirm successful registration.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.008` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0042/rule.yml](content/portable/sigma/MSEC-DET-0042/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0042.kql)
- Source: [catalog/detections/MSEC-DET-0042/manifest.json](catalog/detections/MSEC-DET-0042/manifest.json)

### MSEC-DET-0043 — Msiexec remote web package installation command

Detects Msiexec installation or administrative-install commands whose package argument is HTTP or HTTPS. URL properties on local packages are excluded and a .msi URL suffix is not required.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.007` (Stealth), `T1105` (Command and Control)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0043/rule.yml](content/portable/sigma/MSEC-DET-0043/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0043.kql)
- Source: [catalog/detections/MSEC-DET-0043/manifest.json](catalog/detections/MSEC-DET-0043/manifest.json)

### MSEC-DET-0044 — InstallUtil remote assembly argument

Detects an HTTP, HTTPS or FTP positional argument to InstallUtil. Remote strings confined to named installer options are excluded; successful retrieval or execution requires corroborating telemetry.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1218.004` (Stealth), `T1105` (Command and Control)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0044/rule.yml](content/portable/sigma/MSEC-DET-0044/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0044.kql)
- Source: [catalog/detections/MSEC-DET-0044/manifest.json](catalog/detections/MSEC-DET-0044/manifest.json)

### MSEC-DET-0045 — MSBuild spawns a suspicious child process

Detects MSBuild creating a selected command, script or signed proxy-execution process.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `low`
- ATT&CK: `T1127.001` (Execution), `T1127.001` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 4 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0045/rule.yml](content/portable/sigma/MSEC-DET-0045/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0045.kql)
- Source: [catalog/detections/MSEC-DET-0045/manifest.json](catalog/detections/MSEC-DET-0045/manifest.json)

### MSEC-DET-0046 — Suspicious script or LOLBin payload in a Run key

Detects a Run, RunOnce or Explorer policy Run value set to a selected script payload or suspicious signed Windows utility command.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1547.001` (Persistence), `T1547.001` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 3 positive and 6 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0046/rule.yml](content/portable/sigma/MSEC-DET-0046/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0046.kql)
- Source: [catalog/detections/MSEC-DET-0046/manifest.json](catalog/detections/MSEC-DET-0046/manifest.json)

### MSEC-DET-0047 — Winlogon Shell or Userinit value hijack

Detects a non-empty non-default Winlogon Shell or Userinit registry value set. Quoted and whitespace-normalized standard Explorer and Userinit values are excluded; missing payload data is not evidence of hijack.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1547.004` (Persistence), `T1547.004` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 4 positive and 8 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0047/rule.yml](content/portable/sigma/MSEC-DET-0047/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The recorded configuration event does not establish malicious intent, persistence effectiveness or the final security state. Verify the actor, value, approval and subsequent behavior.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0047.kql)
- Source: [catalog/detections/MSEC-DET-0047/manifest.json](catalog/detections/MSEC-DET-0047/manifest.json)

### MSEC-DET-0048 — Suspicious local scheduled task creation command

Detects local Schtasks creation requests whose explicit /tr argument contains a selected user-writable payload or suspicious script/proxy-execution behavior. Standard quoted actions and unquoted executable paths are covered; task names are not payload evidence.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1053.005` (Execution), `T1053.005` (Persistence), `T1053.005` (Privilege Escalation)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 8 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0048/rule.yml](content/portable/sigma/MSEC-DET-0048/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0048.kql)
- Source: [catalog/detections/MSEC-DET-0048/manifest.json](catalog/detections/MSEC-DET-0048/manifest.json)

### MSEC-DET-0049 — Mavinject process injection command

Detects Mavinject commands carrying a bounded INJECTRUNNING or HMODULE switch, including renamed executables identified by original-filename metadata. Successful injection and trustworthy binary identity require separate validation.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1218.013` (Stealth)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 4 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0049/rule.yml](content/portable/sigma/MSEC-DET-0049/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This single-event signal does not establish malicious intent or successful execution. Renamed binaries, alternate tools, obfuscation and unlogged activity can evade the bounded predicates.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0049.kql)
- Source: [catalog/detections/MSEC-DET-0049/manifest.json](catalog/detections/MSEC-DET-0049/manifest.json)

### MSEC-DET-0050 — Netsh PortProxy addition command

Detects a Netsh command requesting an interface PortProxy forwarding-rule addition, including explicit -c context syntax. Verify the resulting configuration and traffic before concluding that a proxy was established.

- Lifecycle: `experimental`; created 2026-09-03; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1090.001` (Command and Control)
- Data sources: Microsoft Defender for Endpoint process events (Endpoint process creation)
- Synthetic evidence: 5 positive and 5 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0050/rule.yml](content/portable/sigma/MSEC-DET-0050/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Authorized administration can produce this event. The rule does not independently establish compromise or completion of a command; assess identity, target and change approval.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceProcessEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0050.kql)
- Source: [catalog/detections/MSEC-DET-0050/manifest.json](catalog/detections/MSEC-DET-0050/manifest.json)

### MSEC-DET-0054 — Azure diagnostic or Activity Log export deleted

Detects a successful administrative deletion of an Azure diagnostic setting or legacy Activity Log export profile.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1685.002` (Defense Impairment)
- Data sources: Azure Activity administrative events (Azure control-plane administration)
- Synthetic evidence: 4 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0054/rule.yml](content/portable/sigma/MSEC-DET-0054/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Deleting one export configuration does not prove logging ceased elsewhere. Resource retirement and replacement can emit the same event.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AzureActivity`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0054.kql)
- Source: [catalog/detections/MSEC-DET-0054/manifest.json](catalog/detections/MSEC-DET-0054/manifest.json)

### MSEC-DET-0055 — SilentProcessExit monitor configured with an interpreter or staging path

Detects a machine-wide SilentProcessExit MonitorProcess value whose command starts with a selected interpreter or a rooted staging path.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1546.012` (Persistence)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 3 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0055/rule.yml](content/portable/sigma/MSEC-DET-0055/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The value is configuration evidence; GlobalFlag, ReportingMode, the monitored exit and actual process execution are not proven.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0055.kql)
- Source: [catalog/detections/MSEC-DET-0055/manifest.json](catalog/detections/MSEC-DET-0055/manifest.json)

### MSEC-DET-0056 — LSASS loads a DLL from a staging or remote location

Detects an ImageLoaded event for a DLL initiated by lsass.exe from a rooted profile, temporary, recycle-bin or UNC location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1547.005` (Persistence)
- Data sources: Microsoft Defender for Endpoint image-load events (Endpoint DLL loading)
- Synthetic evidence: 4 positive and 11 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0056/rule.yml](content/portable/sigma/MSEC-DET-0056/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: A selected filename and DLL load do not prove binary identity, malicious content, signature status or injection. Process reputation and effective filesystem permissions need separate verification.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceImageLoadEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0056.kql)
- Source: [catalog/detections/MSEC-DET-0056/manifest.json](catalog/detections/MSEC-DET-0056/manifest.json)

### MSEC-DET-0057 — System-named process connects publicly from a staging or remote location

Detects a successful public-IP connection by a selected Windows system-process name whose executable resides in a rooted profile, temporary, recycle-bin or UNC location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1036.005` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint network events (Endpoint network connection)
- Synthetic evidence: 4 positive and 9 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0057/rule.yml](content/portable/sigma/MSEC-DET-0057/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The predicate uses the source's Public classification, not independent IP reputation. A system filename suggests masquerading but does not prove identity or malicious intent.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceNetworkEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0057.kql)
- Source: [catalog/detections/MSEC-DET-0057/manifest.json](catalog/detections/MSEC-DET-0057/manifest.json)

### MSEC-DET-0060 — NTDS database filename created in a staging or remote location

Detects creation or rename of a file named ntds.dit in rooted profile, temporary, recycle-bin or UNC locations.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1003.003` (Credential Access)
- Data sources: Microsoft Defender for Endpoint file events (Endpoint file activity)
- Synthetic evidence: 4 positive and 8 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0060/rule.yml](content/portable/sigma/MSEC-DET-0060/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The filename is not proof of NTDS contents or credential extraction. Renamed/other-location copies, legitimate backups and incomplete file telemetry limit coverage.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceFileEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0060.kql)
- Source: [catalog/detections/MSEC-DET-0060/manifest.json](catalog/detections/MSEC-DET-0060/manifest.json)

### MSEC-DET-0063 — Defender Antivirus engine loads a DLL from a staging or remote location

Detects an ImageLoaded event for a DLL initiated by MsMpEng.exe from a rooted profile, temporary, recycle-bin or UNC location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1574.001` (Persistence)
- Data sources: Microsoft Defender for Endpoint image-load events (Endpoint DLL loading)
- Synthetic evidence: 4 positive and 11 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0063/rule.yml](content/portable/sigma/MSEC-DET-0063/rule.yml) — `active`; targets `sentinel`
- Signal class: `behavior`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: A selected filename and DLL load do not prove binary identity, malicious content, signature status or injection. Process reputation and effective filesystem permissions need separate verification.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceImageLoadEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0063.kql)
- Source: [catalog/detections/MSEC-DET-0063/manifest.json](catalog/detections/MSEC-DET-0063/manifest.json)

### MSEC-DET-0064 — RunAsPPL explicitly zeroed or removed

Detects RunAsPPL set to a decimal or hexadecimal zero, or deleted at its machine registry configuration location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1685` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 5 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0064/rule.yml](content/portable/sigma/MSEC-DET-0064/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Effective LSASS protection depends on operating-system defaults, policy, reboot state and UEFI lock; deleting a value does not prove protection was disabled.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0064.kql)
- Source: [catalog/detections/MSEC-DET-0064/manifest.json](catalog/detections/MSEC-DET-0064/manifest.json)

### MSEC-DET-0066 — Azure soft-deleted Key Vault purged

Detects a successful administrative purge of a previously soft-deleted Azure Key Vault.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1485` (Impact)
- Data sources: Azure Activity administrative events (Azure control-plane administration)
- Synthetic evidence: 3 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0066/rule.yml](content/portable/sigma/MSEC-DET-0066/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This control-plane event does not disclose the vault's prior contents or whether independent backups exist; approved retirement is possible.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AzureActivity`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0066.kql)
- Source: [catalog/detections/MSEC-DET-0066/manifest.json](catalog/detections/MSEC-DET-0066/manifest.json)

### MSEC-DET-0068 — Credential Guard registry configuration explicitly zeroed

Detects LsaCfgFlags set to a decimal or hexadecimal zero at its machine registry configuration location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1685` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 4 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0068/rule.yml](content/portable/sigma/MSEC-DET-0068/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This records a configured value, not a transition from enabled state or proof Credential Guard stopped; UEFI lock and effective policy may override it.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0068.kql)
- Source: [catalog/detections/MSEC-DET-0068/manifest.json](catalog/detections/MSEC-DET-0068/manifest.json)

### MSEC-DET-0073 — LSASS credential-theft ASR rule configured as disabled

Detects 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 set to a decimal or hexadecimal zero at its machine registry configuration location.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1685` (Defense Impairment)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 3 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0073/rule.yml](content/portable/sigma/MSEC-DET-0073/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Tamper protection and policy precedence may prevent the write from changing effective ASR behavior. Audit and warning states are outside this explicit-zero analytic.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0073.kql)
- Source: [catalog/detections/MSEC-DET-0073/manifest.json](catalog/detections/MSEC-DET-0073/manifest.json)

### MSEC-DET-0076 — AWS CloudTrail logging stopped or trail deleted

Detects successful AWS CloudTrail StopLogging or DeleteTrail management API writes with both error fields empty.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1685.002` (Defense Impairment)
- Data sources: AWS CloudTrail management events (AWS control-plane administration)
- Synthetic evidence: 3 positive and 14 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0076/rule.yml](content/portable/sigma/MSEC-DET-0076/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The operation affects one trail. Other trails, event history or independent exports may still retain visibility. The AWSCloudTrail source contract requires boolean management/read-only flags and string error fields; malformed or absent fixture values do not indicate success.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AWSCloudTrail`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0076.kql)
- Source: [catalog/detections/MSEC-DET-0076/manifest.json](catalog/detections/MSEC-DET-0076/manifest.json)

### MSEC-DET-0080 — Office 16 Trusted Location configured in a high-risk directory

Detects Office 16 per-user or user-policy Trusted Location paths directed to a drive root, selected download/temporary directories, profile variables or a UNC share.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `medium` / `medium`
- ATT&CK: `T1553` (Defense Evasion)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 4 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0080/rule.yml](content/portable/sigma/MSEC-DET-0080/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: Configuration alone does not establish effective trust or execution. Network locations can remain disabled by policy; other Office versions and custom paths are outside scope.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0080.kql)
- Source: [catalog/detections/MSEC-DET-0080/manifest.json](catalog/detections/MSEC-DET-0080/manifest.json)

### MSEC-DET-0081 — AWS GuardDuty detector deleted

Detects successful AWS GuardDuty DeleteDetector management API writes with both error fields empty.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1685` (Defense Impairment)
- Data sources: AWS CloudTrail management events (AWS control-plane administration)
- Synthetic evidence: 2 positive and 14 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0081/rule.yml](content/portable/sigma/MSEC-DET-0081/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: This covers successful detector deletion, not suspension, update or every region. Determine the effective account and regional coverage separately. The AWSCloudTrail source contract requires boolean management/read-only flags and string error fields; malformed or absent fixture values do not indicate success.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AWSCloudTrail`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0081.kql)
- Source: [catalog/detections/MSEC-DET-0081/manifest.json](catalog/detections/MSEC-DET-0081/manifest.json)

### MSEC-DET-0083 — Azure tenant-root access elevation succeeded

Detects successful use of the Azure administrative elevateAccess operation at tenant root.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1098.003` (Privilege Escalation)
- Data sources: Azure Activity administrative events (Azure control-plane administration)
- Synthetic evidence: 3 positive and 7 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0083/rule.yml](content/portable/sigma/MSEC-DET-0083/rule.yml) — `active`; targets `sentinel`
- Signal class: `administrative-activity`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The operation records an elevation workflow, not compromise. Global administrators may legitimately elevate for recovery and access management.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `AzureActivity`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0083.kql)
- Source: [catalog/detections/MSEC-DET-0083/manifest.json](catalog/detections/MSEC-DET-0083/manifest.json)

### MSEC-DET-0085 — Netsh helper DLL registered from a staging or remote path

Detects a machine registry DLL registration whose complete value names a DLL in selected profile, temporary, environment-variable or UNC locations.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1546.007` (Persistence)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 4 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0085/rule.yml](content/portable/sigma/MSEC-DET-0085/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The registry write does not prove the DLL exists, is malicious or was loaded. Relative DLL names and other locations are outside this deliberately bounded predicate.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0085.kql)
- Source: [catalog/detections/MSEC-DET-0085/manifest.json](catalog/detections/MSEC-DET-0085/manifest.json)

### MSEC-DET-0089 — Print port monitor DLL registered from a staging or remote path

Detects a machine registry DLL registration whose complete value names a DLL in selected profile, temporary, environment-variable or UNC locations.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1547.010` (Persistence)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 5 positive and 12 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0089/rule.yml](content/portable/sigma/MSEC-DET-0089/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The registry write does not prove the DLL exists, is malicious or was loaded. Relative DLL names and other locations are outside this deliberately bounded predicate.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0089.kql)
- Source: [catalog/detections/MSEC-DET-0089/manifest.json](catalog/detections/MSEC-DET-0089/manifest.json)

### MSEC-DET-0100 — AppCert DLL registered from a staging or remote path

Detects a machine registry DLL registration whose complete value names a DLL in selected profile, temporary, environment-variable or UNC locations.

- Lifecycle: `experimental`; created 2026-09-11; review every 90 days
- Severity / confidence: `high` / `medium`
- ATT&CK: `T1546.009` (Persistence)
- Data sources: Microsoft Defender for Endpoint registry events (Endpoint registry modification)
- Synthetic evidence: 5 positive and 10 negative cases
- Implementations:
  - [content/portable/sigma/MSEC-DET-0100/rule.yml](content/portable/sigma/MSEC-DET-0100/rule.yml) — `active`; targets `sentinel`
- Signal class: `configuration-change`; evidence: `synthetic-only`; reviewed 2026-09-11
- Limit: The registry write does not prove the DLL exists, is malicious or was loaded. Relative DLL names and other locations are outside this deliberately bounded predicate.
- Limit: Current-revision evidence is synthetic only. Validate full generated KQL, source fields, ingestion delay, alert volume and scoped exclusions in the target before enabling.
- Sentinel preview:
  - Table `DeviceRegistryEvents`; [reviewed Golden query](tests/golden/sentinel/MSEC-DET-0100.kql)
- Source: [catalog/detections/MSEC-DET-0100/manifest.json](catalog/detections/MSEC-DET-0100/manifest.json)
