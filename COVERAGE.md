<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:coverage`. -->

# Detection coverage

This report is generated deterministically from the public detection manifests, Sentinel preview and Sentinel data-source contract.
It inventories declared repository coverage only. It is not a claim of complete MITRE ATT&CK coverage, live telemetry health or production readiness.

## Summary

- Detection packages: **5**
- Declared ATT&CK mappings: **5** across **4 techniques / 3 tactics**
- Declared logical data sources: **3**
- Sentinel preview bindings: **4**
- Sentinel data-source contracts: **2**
- Detections without a Sentinel preview binding: **1**

## ATT&CK techniques

| Technique | Tactic | Detection records |
| --- | --- | --- |
| `T1078.004` | Initial Access | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) |
| `T1098.001` | Persistence | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json) |
| `T1098.003` | Privilege Escalation | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) |
| `T1543.003` | Persistence | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) |

## ATT&CK tactics

| Tactic | Techniques | Detection records |
| --- | --- | --- |
| Initial Access | `T1078.004` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) |
| Persistence | `T1098.001`, `T1543.003` | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json), [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json) |
| Privilege Escalation | `T1098.003` | [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) |

## Declared logical data sources

| Data source | Category | Detection records | Required fields |
| --- | --- | --- | --- |
| Microsoft Entra audit logs | Identity directory audit | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) | `CorrelationId`, `InitiatedBy`, `OperationName`, `Result`, `TargetResources`, `TimeGenerated` |
| Microsoft Entra sign-in logs | Identity authentication | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | `AppDisplayName`, `ClientAppUsed`, `IPAddress`, `ResultType`, `RiskLevelDuringSignIn`, `TimeGenerated`, `UserPrincipalName` |
| Windows service installation events | Windows service control manager | [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) | `Computer`, `EventID`, `ImagePath`, `Provider_Name`, `ServiceName` |

## Sentinel data-source contracts

| Contract | Table | Detection records | Required columns | Freshness expectation |
| --- | --- | --- | ---: | --- |
| `MSEC-SDS-0001` | `SigninLogs` | [`MSEC-DET-0002`](catalog/detections/MSEC-DET-0002/manifest.json), [`MSEC-DET-0003`](catalog/detections/MSEC-DET-0003/manifest.json) | 15 | degraded after `PT6H`; unavailable after `P1D` |
| `MSEC-SDS-0002` | `AuditLogs` | [`MSEC-DET-0004`](catalog/detections/MSEC-DET-0004/manifest.json), [`MSEC-DET-0005`](catalog/detections/MSEC-DET-0005/manifest.json) | 7 | degraded after `PT6H`; unavailable after `P1D` |

## Detections without a Sentinel preview binding

- [`MSEC-DET-0001`](catalog/detections/MSEC-DET-0001/manifest.json) — Windows service installation from a public or temporary path; declared source: Windows service installation events

A missing Sentinel binding is an explicit target gap, not a failing detection and not proof that the source is absent from a consumer environment.
