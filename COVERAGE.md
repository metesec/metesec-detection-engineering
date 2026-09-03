<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:coverage`. -->

# Detection coverage

This report is generated deterministically from the public detection manifests, Sentinel preview and Sentinel data-source contract.
It inventories declared repository coverage only. It is not a claim of complete MITRE ATT&CK coverage, live telemetry health or production readiness.

## Summary

- Detection packages: **15**
- Declared ATT&CK mappings: **15** across **10 techniques / 6 tactics**
- Declared logical data sources: **5**
- Sentinel preview bindings: **14**
- Sentinel data-source contracts: **4**
- Detections without a Sentinel preview binding: **1**

## ATT&CK techniques

| Technique | Tactic | Detection records |
| --- | --- | --- |
| `T1003.001` | Credential Access | [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json) |
| `T1059` | Execution | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json) |
| `T1059.001` | Execution | [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json) |
| `T1078.004` | Initial Access | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) |
| `T1098.001` | Persistence | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json) |
| `T1098.003` | Privilege Escalation | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) |
| `T1218.005` | Defense Evasion | [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json) |
| `T1218.010` | Defense Evasion | [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) |
| `T1543.003` | Persistence | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) |
| `T1556.009` | Defense Evasion | [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json) |

## ATT&CK tactics

| Tactic | Techniques | Detection records |
| --- | --- | --- |
| Credential Access | `T1003.001` | [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json) |
| Defense Evasion | `T1218.005`, `T1218.010`, `T1556.009` | [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json) |
| Execution | `T1059`, `T1059.001` | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json) |
| Initial Access | `T1078.004` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) |
| Persistence | `T1098.001`, `T1543.003` | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json), [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json) |
| Privilege Escalation | `T1098.003` | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) |

## Declared logical data sources

| Data source | Category | Detection records | Required fields |
| --- | --- | --- | --- |
| Microsoft Defender for Endpoint process events | Endpoint process creation | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) | `AccountName`, `DeviceId`, `DeviceName`, `FileName`, `FolderPath`, `InitiatingProcessFileName`, `ProcessCommandLine`, `ReportId`, `TimeGenerated`, `Timestamp` |
| Microsoft Entra audit logs | Identity directory audit | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) | `CorrelationId`, `InitiatedBy`, `LoggedByService`, `OperationName`, `Result`, `TargetResources`, `TimeGenerated` |
| Microsoft Entra sign-in logs | Identity authentication | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | `AppDisplayName`, `ClientAppUsed`, `IPAddress`, `ResultType`, `RiskLevelDuringSignIn`, `TimeGenerated`, `UserPrincipalName` |
| Microsoft Entra user risk events | Identity risk | [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | `OperationName`, `RiskEventType`, `RiskLevel`, `RiskState`, `TimeGenerated`, `UserId`, `UserPrincipalName` |
| Windows service installation events | Windows service control manager | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | `Computer`, `EventID`, `ImagePath`, `Provider_Name`, `ServiceName` |

## Sentinel data-source contracts

| Contract | Table | Detection records | Required columns | Freshness expectation |
| --- | --- | --- | ---: | --- |
| `MSEC-SDS-0001` | `SigninLogs` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | 15 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0002` | `AuditLogs` | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json) | 7 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0003` | `DeviceProcessEvents` | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) | 12 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0004` | `AADUserRiskEvents` | [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | 10 | degraded after `PT6H`; unavailable after `P1D` |

## Detections without a Sentinel preview binding

- [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) — Windows service installation from a public or temporary path; declared source: Windows service installation events

A missing Sentinel binding is an explicit target gap, not a failing detection and not proof that the source is absent from a consumer environment.
