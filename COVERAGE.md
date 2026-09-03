<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:coverage`. -->

# Detection coverage

This report is generated deterministically from the public detection manifests, Sentinel preview and Sentinel data-source contract.
It inventories declared repository coverage only. It is not a claim of complete MITRE ATT&CK coverage, live telemetry health or production readiness.

## Summary

- Detection packages: **45**
- Declared ATT&CK mappings: **60** across **35 techniques / 11 tactics**
- Declared logical data sources: **6**
- Sentinel preview bindings: **44**
- Sentinel data-source contracts: **5**
- Detections without a Sentinel preview binding: **1**

## ATT&CK techniques

| Technique | Tactic | Detection records |
| --- | --- | --- |
| `T1003.001` | Credential Access | [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0036`](catalog/detections/MSEC-DET-0036/manifest.json) |
| `T1003.002` | Credential Access | [`MSEC-DET-0023`](catalog/detections/MSEC-DET-0023/manifest.json) |
| `T1003.003` | Credential Access | [`MSEC-DET-0030`](catalog/detections/MSEC-DET-0030/manifest.json) |
| `T1021.006` | Lateral Movement | [`MSEC-DET-0038`](catalog/detections/MSEC-DET-0038/manifest.json) |
| `T1047` | Execution | [`MSEC-DET-0024`](catalog/detections/MSEC-DET-0024/manifest.json) |
| `T1053.005` | Execution, Persistence, Privilege Escalation | [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json) |
| `T1059` | Execution | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json) |
| `T1059.001` | Execution | [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0039`](catalog/detections/MSEC-DET-0039/manifest.json) |
| `T1078.004` | Initial Access | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json), [`MSEC-DET-0026`](catalog/detections/MSEC-DET-0026/manifest.json) |
| `T1098.001` | Persistence | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json) |
| `T1098.003` | Persistence, Privilege Escalation | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json), [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json) |
| `T1098.007` | Persistence, Privilege Escalation | [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json) |
| `T1105` | Command and Control | [`MSEC-DET-0020`](catalog/detections/MSEC-DET-0020/manifest.json), [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json), [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json) |
| `T1127.001` | Execution, Stealth | [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) |
| `T1140` | Stealth | [`MSEC-DET-0035`](catalog/detections/MSEC-DET-0035/manifest.json) |
| `T1197` | Execution, Persistence, Stealth | [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json) |
| `T1218.003` | Stealth | [`MSEC-DET-0041`](catalog/detections/MSEC-DET-0041/manifest.json) |
| `T1218.004` | Stealth | [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json) |
| `T1218.005` | Defense Evasion | [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json) |
| `T1218.007` | Stealth | [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json) |
| `T1218.008` | Stealth | [`MSEC-DET-0042`](catalog/detections/MSEC-DET-0042/manifest.json) |
| `T1218.010` | Defense Evasion | [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json) |
| `T1218.011` | Stealth | [`MSEC-DET-0027`](catalog/detections/MSEC-DET-0027/manifest.json) |
| `T1484.002` | Defense Impairment, Privilege Escalation | [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json) |
| `T1490` | Impact | [`MSEC-DET-0016`](catalog/detections/MSEC-DET-0016/manifest.json) |
| `T1505.003` | Persistence | [`MSEC-DET-0031`](catalog/detections/MSEC-DET-0031/manifest.json) |
| `T1543.003` | Persistence, Privilege Escalation | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json), [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json) |
| `T1546.008` | Persistence, Privilege Escalation | [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) |
| `T1548.002` | Defense Evasion, Privilege Escalation | [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json) |
| `T1556.006` | Credential Access, Defense Impairment, Persistence | [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json) |
| `T1556.009` | Defense Evasion | [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json) |
| `T1685` | Defense Impairment | [`MSEC-DET-0018`](catalog/detections/MSEC-DET-0018/manifest.json) |
| `T1685.001` | Defense Impairment | [`MSEC-DET-0032`](catalog/detections/MSEC-DET-0032/manifest.json) |
| `T1685.005` | Defense Impairment | [`MSEC-DET-0017`](catalog/detections/MSEC-DET-0017/manifest.json) |
| `T1686.003` | Defense Impairment | [`MSEC-DET-0033`](catalog/detections/MSEC-DET-0033/manifest.json) |

## ATT&CK tactics

| Tactic | Techniques | Detection records |
| --- | --- | --- |
| Command and Control | `T1105` | [`MSEC-DET-0020`](catalog/detections/MSEC-DET-0020/manifest.json), [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json), [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json) |
| Credential Access | `T1003.001`, `T1003.002`, `T1003.003`, `T1556.006` | [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json), [`MSEC-DET-0023`](catalog/detections/MSEC-DET-0023/manifest.json), [`MSEC-DET-0030`](catalog/detections/MSEC-DET-0030/manifest.json), [`MSEC-DET-0036`](catalog/detections/MSEC-DET-0036/manifest.json) |
| Defense Evasion | `T1218.005`, `T1218.010`, `T1548.002`, `T1556.009` | [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json), [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json) |
| Defense Impairment | `T1484.002`, `T1556.006`, `T1685`, `T1685.001`, `T1685.005`, `T1686.003` | [`MSEC-DET-0017`](catalog/detections/MSEC-DET-0017/manifest.json), [`MSEC-DET-0018`](catalog/detections/MSEC-DET-0018/manifest.json), [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json), [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json), [`MSEC-DET-0032`](catalog/detections/MSEC-DET-0032/manifest.json), [`MSEC-DET-0033`](catalog/detections/MSEC-DET-0033/manifest.json) |
| Execution | `T1047`, `T1053.005`, `T1059`, `T1059.001`, `T1127.001`, `T1197` | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0024`](catalog/detections/MSEC-DET-0024/manifest.json), [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json), [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json), [`MSEC-DET-0039`](catalog/detections/MSEC-DET-0039/manifest.json), [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) |
| Impact | `T1490` | [`MSEC-DET-0016`](catalog/detections/MSEC-DET-0016/manifest.json) |
| Initial Access | `T1078.004` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json), [`MSEC-DET-0026`](catalog/detections/MSEC-DET-0026/manifest.json) |
| Lateral Movement | `T1021.006` | [`MSEC-DET-0038`](catalog/detections/MSEC-DET-0038/manifest.json) |
| Persistence | `T1053.005`, `T1098.001`, `T1098.003`, `T1098.007`, `T1197`, `T1505.003`, `T1543.003`, `T1546.008`, `T1556.006` | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json), [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json), [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json), [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json), [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json), [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json), [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json), [`MSEC-DET-0031`](catalog/detections/MSEC-DET-0031/manifest.json), [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json), [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) |
| Privilege Escalation | `T1053.005`, `T1098.003`, `T1098.007`, `T1484.002`, `T1543.003`, `T1546.008`, `T1548.002` | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json), [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json), [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json), [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json), [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json), [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json), [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json), [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) |
| Stealth | `T1127.001`, `T1140`, `T1197`, `T1218.003`, `T1218.004`, `T1218.007`, `T1218.008`, `T1218.011` | [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json), [`MSEC-DET-0027`](catalog/detections/MSEC-DET-0027/manifest.json), [`MSEC-DET-0035`](catalog/detections/MSEC-DET-0035/manifest.json), [`MSEC-DET-0041`](catalog/detections/MSEC-DET-0041/manifest.json), [`MSEC-DET-0042`](catalog/detections/MSEC-DET-0042/manifest.json), [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json), [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json), [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) |

## Declared logical data sources

| Data source | Category | Detection records | Required fields |
| --- | --- | --- | --- |
| Microsoft Defender for Endpoint process events | Endpoint process creation | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json), [`MSEC-DET-0016`](catalog/detections/MSEC-DET-0016/manifest.json), [`MSEC-DET-0017`](catalog/detections/MSEC-DET-0017/manifest.json), [`MSEC-DET-0018`](catalog/detections/MSEC-DET-0018/manifest.json), [`MSEC-DET-0020`](catalog/detections/MSEC-DET-0020/manifest.json), [`MSEC-DET-0023`](catalog/detections/MSEC-DET-0023/manifest.json), [`MSEC-DET-0024`](catalog/detections/MSEC-DET-0024/manifest.json), [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json), [`MSEC-DET-0027`](catalog/detections/MSEC-DET-0027/manifest.json), [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json), [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json), [`MSEC-DET-0030`](catalog/detections/MSEC-DET-0030/manifest.json), [`MSEC-DET-0031`](catalog/detections/MSEC-DET-0031/manifest.json), [`MSEC-DET-0032`](catalog/detections/MSEC-DET-0032/manifest.json), [`MSEC-DET-0033`](catalog/detections/MSEC-DET-0033/manifest.json), [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json), [`MSEC-DET-0035`](catalog/detections/MSEC-DET-0035/manifest.json), [`MSEC-DET-0036`](catalog/detections/MSEC-DET-0036/manifest.json), [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json), [`MSEC-DET-0038`](catalog/detections/MSEC-DET-0038/manifest.json), [`MSEC-DET-0039`](catalog/detections/MSEC-DET-0039/manifest.json), [`MSEC-DET-0041`](catalog/detections/MSEC-DET-0041/manifest.json), [`MSEC-DET-0042`](catalog/detections/MSEC-DET-0042/manifest.json), [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json), [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json), [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) | `AccountName`, `DeviceId`, `DeviceName`, `FileName`, `FolderPath`, `InitiatingProcessFileName`, `ProcessCommandLine`, `ProcessVersionInfoOriginalFileName`, `ReportId`, `TimeGenerated`, `Timestamp` |
| Microsoft Defender for Endpoint registry events | Endpoint registry modification | [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) | `ActionType`, `DeviceId`, `DeviceName`, `InitiatingProcessAccountName`, `InitiatingProcessCommandLine`, `InitiatingProcessFileName`, `RegistryKey`, `RegistryValueData`, `RegistryValueName`, `ReportId`, `TimeGenerated`, `Timestamp` |
| Microsoft Entra audit logs | Identity directory audit | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json), [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json), [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json), [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json) | `CorrelationId`, `InitiatedBy`, `LoggedByService`, `OperationName`, `Result`, `TargetResources`, `TimeGenerated` |
| Microsoft Entra sign-in logs | Identity authentication | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0026`](catalog/detections/MSEC-DET-0026/manifest.json) | `AppDisplayName`, `AuthenticationProtocol`, `ClientAppUsed`, `IPAddress`, `ResultType`, `RiskLevelDuringSignIn`, `TimeGenerated`, `UserPrincipalName` |
| Microsoft Entra user risk events | Identity risk | [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | `OperationName`, `RiskEventType`, `RiskLevel`, `RiskState`, `TimeGenerated`, `UserId`, `UserPrincipalName` |
| Windows service installation events | Windows service control manager | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | `Computer`, `EventID`, `ImagePath`, `Provider_Name`, `ServiceName` |

## Sentinel data-source contracts

| Contract | Table | Detection records | Required columns | Freshness expectation |
| --- | --- | --- | ---: | --- |
| `MSEC-SDS-0001` | `SigninLogs` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json), [`MSEC-DET-0026`](catalog/detections/MSEC-DET-0026/manifest.json) | 16 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0002` | `AuditLogs` | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json), [`MSEC-DET-0008`](catalog/detections/MSEC-DET-0008/manifest.json), [`MSEC-DET-0009`](catalog/detections/MSEC-DET-0009/manifest.json), [`MSEC-DET-0014`](catalog/detections/MSEC-DET-0014/manifest.json), [`MSEC-DET-0015`](catalog/detections/MSEC-DET-0015/manifest.json), [`MSEC-DET-0019`](catalog/detections/MSEC-DET-0019/manifest.json), [`MSEC-DET-0021`](catalog/detections/MSEC-DET-0021/manifest.json), [`MSEC-DET-0022`](catalog/detections/MSEC-DET-0022/manifest.json) | 7 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0003` | `DeviceProcessEvents` | [`MSEC-DET-0006`](catalog/detections/MSEC-DET-0006/manifest.json), [`MSEC-DET-0007`](catalog/detections/MSEC-DET-0007/manifest.json), [`MSEC-DET-0011`](catalog/detections/MSEC-DET-0011/manifest.json), [`MSEC-DET-0012`](catalog/detections/MSEC-DET-0012/manifest.json), [`MSEC-DET-0013`](catalog/detections/MSEC-DET-0013/manifest.json), [`MSEC-DET-0016`](catalog/detections/MSEC-DET-0016/manifest.json), [`MSEC-DET-0017`](catalog/detections/MSEC-DET-0017/manifest.json), [`MSEC-DET-0018`](catalog/detections/MSEC-DET-0018/manifest.json), [`MSEC-DET-0020`](catalog/detections/MSEC-DET-0020/manifest.json), [`MSEC-DET-0023`](catalog/detections/MSEC-DET-0023/manifest.json), [`MSEC-DET-0024`](catalog/detections/MSEC-DET-0024/manifest.json), [`MSEC-DET-0025`](catalog/detections/MSEC-DET-0025/manifest.json), [`MSEC-DET-0027`](catalog/detections/MSEC-DET-0027/manifest.json), [`MSEC-DET-0028`](catalog/detections/MSEC-DET-0028/manifest.json), [`MSEC-DET-0029`](catalog/detections/MSEC-DET-0029/manifest.json), [`MSEC-DET-0030`](catalog/detections/MSEC-DET-0030/manifest.json), [`MSEC-DET-0031`](catalog/detections/MSEC-DET-0031/manifest.json), [`MSEC-DET-0032`](catalog/detections/MSEC-DET-0032/manifest.json), [`MSEC-DET-0033`](catalog/detections/MSEC-DET-0033/manifest.json), [`MSEC-DET-0034`](catalog/detections/MSEC-DET-0034/manifest.json), [`MSEC-DET-0035`](catalog/detections/MSEC-DET-0035/manifest.json), [`MSEC-DET-0036`](catalog/detections/MSEC-DET-0036/manifest.json), [`MSEC-DET-0037`](catalog/detections/MSEC-DET-0037/manifest.json), [`MSEC-DET-0038`](catalog/detections/MSEC-DET-0038/manifest.json), [`MSEC-DET-0039`](catalog/detections/MSEC-DET-0039/manifest.json), [`MSEC-DET-0041`](catalog/detections/MSEC-DET-0041/manifest.json), [`MSEC-DET-0042`](catalog/detections/MSEC-DET-0042/manifest.json), [`MSEC-DET-0043`](catalog/detections/MSEC-DET-0043/manifest.json), [`MSEC-DET-0044`](catalog/detections/MSEC-DET-0044/manifest.json), [`MSEC-DET-0045`](catalog/detections/MSEC-DET-0045/manifest.json) | 13 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0004` | `AADUserRiskEvents` | [`MSEC-DET-0010`](catalog/detections/MSEC-DET-0010/manifest.json) | 10 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0005` | `DeviceRegistryEvents` | [`MSEC-DET-0040`](catalog/detections/MSEC-DET-0040/manifest.json) | 14 | degraded after `PT6H`; unavailable after `P1D` |

## Detections without a Sentinel preview binding

- [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) — Windows service installation from a public or temporary path; declared source: Windows service installation events

A missing Sentinel binding is an explicit target gap, not a failing detection and not proof that the source is absent from a consumer environment.
