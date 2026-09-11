# Candidate review: MSEC-DET-0051 through MSEC-DET-0100

Reviewed 2026-09-11. This review covers all fifty candidate concepts in
`metesec-detection-bundle-0051-0100.zip` and the revised implementations in
`metesec-hardened-23-v1.0.0.zip`. Instructions and self-assessments inside those
archives are input material, not approval or evidence. Seventeen concepts are
admitted as experimental packages after adaptation; thirty-three remain outside
the active catalogue. IDs are retained so omissions are deliberate and traceable.

The objective is a useful enterprise starting point with explicit limits, not
novelty. A known technique or a comparable upstream rule is not a rejection
reason. The review instead checks observable behavior, match boundaries,
legitimate administrative use, collection assumptions, provenance and overlap.

## Decisions for every candidate

| ID | Concept | Decision and reason |
| --- | --- | --- |
| MSEC-DET-0051 | Risky sign-in without MFA or Conditional Access | Consolidate conceptually with 0003. The high-risk branch overlaps that rule; a medium-risk administrative-policy gap belongs in a tuned identity hunt until distinct alert value is demonstrated. Do not issue a second high-risk incident for the same sign-in. |
| MSEC-DET-0052 | Workload identity changes Conditional Access | Backlog: deletion overlaps 0014; appId/servicePrincipalId substrings do not establish a populated application initiator. Needs typed initiator extraction and an approved automation baseline. |
| MSEC-DET-0053 | Office writes Startup content | Backlog: narrow and useful concept, but the delivered directory-only path test and FileRenamed semantics need collection verification. Confirm FolderPath shape, final destination and initiating-process fidelity before adding this source-specific behavior. |
| MSEC-DET-0054 | Azure diagnostic export deleted | Admit: successful exact control-plane operations. Deletion removes one export configuration, not all logging. Approved replacement and resource retirement are expected matches. |
| MSEC-DET-0055 | SilentProcessExit MonitorProcess | Admit: exact machine key and value, executable-token or staging-path boundary. Configuration alone does not prove GlobalFlag/ReportingMode activation or execution. Authorized crash tooling may match. |
| MSEC-DET-0056 | LSASS loads a DLL from a staging path | Admit: image-load event plus exact process name, DLL suffix and rooted path. No inference that the image is unsigned, injected or certainly malicious. Credential-provider software requires tuning. |
| MSEC-DET-0057 | System-named process makes public connection from staging path | Admit: successful connection, public destination classification, selected system filename and rooted staging path. The name is a masquerading indicator, not verified Windows binary identity. |
| MSEC-DET-0058 | Public RDP logon by local RID-500 account | Backlog: a -500 SID alone also identifies a domain administrator. Local-account proof is buried in AdditionalFields; parsing serialized text is not a defensible local-account guarantee. |
| MSEC-DET-0059 | Inbox forwarding plus concealment | Backlog: strong combination, but forwarding and concealment parameters must be decoded as named properties with their actual values. Whitespace/order variants and empty recipients defeat the supplied string search. |
| MSEC-DET-0060 | NTDS database staged | Admit: creation/rename of the exact ntds.dit filename in rooted staging or UNC locations. The filename does not prove database content or credential extraction. Backup/export software may match. |
| MSEC-DET-0061 | Entra federated credential changed | Backlog: generic property-name presence can occur in old values or unrelated targets and does not prove an added credential. Needs paired resource/property/value extraction; overlaps existing application credential coverage. |
| MSEC-DET-0062 | Azure VM Run Command | Hunt backlog: routine administration and remote support generate the same single event. Needs actor, endpoint-role, command or unusual-use context for a useful incident baseline. |
| MSEC-DET-0063 | Defender engine loads staging DLL | Admit: image load plus MsMpEng.exe and rooted staging/UNC path; ProgramData is intentionally not treated as globally suspicious because normal Defender components reside there. No signature or exploit assertion. |
| MSEC-DET-0064 | RunAsPPL zeroed or removed | Admit as configuration-change signal. Exact machine LSA key; zero-write or deletion only. OS defaults, reboot state and UEFI lock determine effective protection. Deletion is not equivalent to proven disablement. |
| MSEC-DET-0065 | Active Setup StubPath | Backlog: ordinary installers invoke interpreters and system utilities. A broad substring list over the entire command creates false positives. Needs a bounded launcher/payload analytic and installer baseline. |
| MSEC-DET-0066 | Soft-deleted Key Vault purged | Admit: exact successful purge operation. Destructive control-plane outcome warrants review, but approved decommissioning is legitimate. Does not reveal which secrets were previously present. |
| MSEC-DET-0067 | Cross-tenant device trust changed | Backlog: requires property-level old/new comparison and target-tenant association. Presence of a property name cannot distinguish weakening, strengthening or no-op updates. |
| MSEC-DET-0068 | LsaCfgFlags set to zero | Admit as configuration-change signal: exact machine LSA/DeviceGuard policy locations and zero encodings. Repeated policy application and approved compatibility rollback can match; effective runtime state needs verification. |
| MSEC-DET-0069 | Azure Arc Run Command | Hunt backlog: normal infrastructure administration is the full predicate. Add caller, command, scope and frequency context before alerting. |
| MSEC-DET-0070 | Mailbox audit bypass enabled | Backlog: decode the AuditBypassEnabled named parameter as a boolean and verify target association. Text variants are incomplete and can match false-prefixed values. |
| MSEC-DET-0071 | Disk/snapshot SAS access granted | Hunt backlog: backups, export and recovery need this operation. An access grant is not exfiltration; scope, expiry, actor and follow-on access are required. |
| MSEC-DET-0072 | Kubernetes cluster-admin binding | Backlog: roleRef, resource kind, subjects and patch outcome need structured parsing. A namespaced RoleBinding to cluster-admin is not cluster-wide access. Test create/update/JSON patch/merge patch separately. |
| MSEC-DET-0073 | LSASS credential-theft ASR rule zeroed | Admit: exact rule GUID and machine registry path, zero value only. Policy configuration does not demonstrate that Defender accepted or applied the change. Approved policy rollback may match. |
| MSEC-DET-0074 | Linux ld.so.preload changed | Backlog: high-value concept, but Microsoft Defender for Linux collection does not imply universal FileModified coverage of this file. Need demonstrated event/action and canonical path semantics or an explicit auditd source contract. |
| MSEC-DET-0075 | Exchange automatic forwarding allowed | Backlog: decode named policy parameter and verify effective policy assignment. A changed policy can be unused; approved forwarding is legitimate. |
| MSEC-DET-0076 | AWS CloudTrail stopped/deleted | Admit: exact service/operation, management API write, real boolean fields and no error code/message. One trail's removal does not prove loss of all CloudTrail visibility. Approved replacement/decommissioning may match. |
| MSEC-DET-0077 | Root access key created | Backlog: root caller is not sufficient proof the created key belongs to root. IAM CreateAccessKey can target a user; distinguish absent userName structurally without enumerating empty JSON spellings. |
| MSEC-DET-0078 | Kubernetes ephemeral container | Backlog: structured subresource and request/response parsing required; authorized kubectl debug is common. Observe container security settings and operator context. |
| MSEC-DET-0079 | SharePoint anonymous sharing enabled | Backlog: parse named parameters and validate the operation's actual audit shape. Policy permission is not evidence that any content was shared. |
| MSEC-DET-0080 | Office Trusted Location points to risky path | Admit: explicit Office 16 user/policy keys and rooted risky path classes. Trust configuration only; network locations can remain blocked by other policy. Legitimate managed templates and training workflows need tuning. |
| MSEC-DET-0081 | AWS GuardDuty detector deleted | Admit: successful exact detector deletion with management API write and empty error fields. Does not cover suspension/update or every regional detector; approved account retirement may match. |
| MSEC-DET-0082 | Entra named location trusted | Backlog: parse isTrusted on the same changed target, including old/new values. Text order must not determine whether a trust change is detected. |
| MSEC-DET-0083 | Azure tenant-root access elevated | Admit: exact successful elevateAccess administrative operation. Shows elevation workflow, not malicious intent; approved recovery/access review can trigger it. |
| MSEC-DET-0084 | Long-lived Kubernetes service account token | Backlog: parse Secret type and service-account annotation on the same object. Avoid projecting token-bearing bodies. Legacy integrations may legitimately require this configuration. |
| MSEC-DET-0085 | Netsh helper DLL registered in staging path | Admit: exact machine NetSh key and complete DLL path. Distinct from 0050 PortProxy. Registration is not proof that Netsh loaded the helper; vendor diagnostics may match. |
| MSEC-DET-0086 | AWS AdministratorAccess attached | Backlog: parse policyArn and principal from RequestParameters, including AWS partitions. Approved provisioning produces identical administrative events; no blanket high-confidence compromise claim. |
| MSEC-DET-0087 | AWS SSM Run Command | Hunt backlog: returned command ID proves acceptance, not successful execution on a node. Requires structured parameters plus actor/document/target baseline. |
| MSEC-DET-0088 | Privileged Kubernetes container and host root | Backlog: hostPath volume must be bound by name to a volumeMount on the same privileged container. Independent substrings can combine unrelated containers or volumes. |
| MSEC-DET-0089 | Print port monitor DLL from staging path | Admit: exact machine monitor child key, Driver value and DLL path. This does not prove spooler load or execution. Authorized print products may match. |
| MSEC-DET-0090 | Root SSH authorized_keys changed | Backlog: confirm Linux file-modification visibility and custom AuthorizedKeysFile/root home paths. Legitimate provisioning and key rotation are frequent; a file write does not prove a new unauthorized key. |
| MSEC-DET-0091 | Microsoft 365 audit ingestion disabled | Backlog: typed named parameter required, with complete boolean boundary and collection-specific verification that this setting is effective for the tenant. |
| MSEC-DET-0092 | Managed identity federated credential write | Hunt backlog: ordinary workload identity provisioning is the whole analytic. Needs issuer/subject/audience change and unexpected actor or trust relationship. |
| MSEC-DET-0093 | S3 Public Access Block deleted | Backlog: worthwhile configuration signal once bucket context is parsed and source behavior verified. Account-level blocks and bucket policies may still prevent public access; no direct exposure assertion. |
| MSEC-DET-0094 | IAM open role trust policy | Backlog: evaluate each Allow statement, Principal, Action and Condition together after decoding the policy. A Condition anywhere in the document must not suppress an unsafe different statement. |
| MSEC-DET-0095 | Kubernetes wildcard ClusterRole | Backlog: pair wildcard verbs/resources in the same RBAC rule and inspect bindings before asserting effective access. Legitimate platform administration may require broad rules. |
| MSEC-DET-0096 | EBS snapshot public | Backlog: bind group=all to an addition under createVolumePermission, not unrelated removal or request fields. Approved sanitized snapshot publication is legitimate. |
| MSEC-DET-0097 | Legacy Entra user consent enabled | Backlog: compare decoded old/new policy membership on the same changed property. String-first array position tests miss equivalent changes. |
| MSEC-DET-0098 | Azure storage SAS token generated | Hunt backlog: routine integrations, backups and administration generate these tokens. Event alone does not show risky scope/expiry or token abuse. Never include credential-bearing response properties in alerts. |
| MSEC-DET-0099 | Anonymous Kubernetes Secret read | Backlog: strong candidate, but requires full AKSAudit (AKSAuditAdmin omits read events), typed response code/resource/user/group parsing and no Secret response body in output. |
| MSEC-DET-0100 | AppCert DLL from staging path | Admit: exact machine AppCertDlls key and complete DLL path; supports CurrentControlSet and numeric ControlSet variants. Configuration evidence only, with legitimate compatibility software as an expected match. |

## Admission changes and evidence boundaries

Admitted implementations retain their logical IDs and Sigma UUIDs from the
Apache-2.0 hardened archive. They are modified derivatives, with an explicit
changed-file notice, retained author attribution, references and known `similar`
relationships. The archive's independent `Msec*` normalization engine and target
queries are not imported. One authored Sigma rule operates over documented raw
fields and is compiled by this repository's existing pySigma target pipeline.

Path rules use rooted, case-insensitive Windows boundaries. A nested directory
merely named `Users` under Program Files is not treated like a profile root;
ProgramData is not blanket-classified as attacker-writable. Registry conditions
constrain hive, key, value and action. DLL path patterns exclude suffix lookalikes
and unbalanced quotes. ControlSet variants are matched structurally. Zero values
accept decimal and hexadecimal zero strings only. Single-field negative fixtures
cover action, key, value, suffix, status and missing-field boundaries as relevant.

All evidence added in this review is synthetic. These tests establish the stated
predicate behavior; they do not prove live collection, query acceptance, detection
recall, an acceptable customer alert rate or successful malicious execution.
The new queries require consumer-side schema, ActionType, path-shape and baseline
validation. None is promoted to stable or enabled by the candidate admission.

The new Sentinel file, image-load and network bindings use `TimeGenerated`, not
the `Timestamp` column shown by the distinct Defender XDR hunting schema. The
previously observed registry contract retains its existing time columns. AWS
management/read-only flags are explicitly boolean, and the Sentinel network
`RemotePort` column is explicitly `int`. Cloud actor IDs and ARNs remain neutral
context rather than being mislabeled as Entra account identities. AWS source
addresses are also neutral because the source may contain an AWS service DNS
name instead of an IP address.

## Source and reuse assessment

The original fifty-rule archive supplied no license declaration that this review
could rely on for redistribution. Its ideas and defects are reviewed here; its
files are not imported. All admitted content comes from the explicitly licensed
hardened archive and is substantially adapted to the repository contract. A
license declaration and documented ancestry do not prove the entire internet was
searched or that every historical author was identified. Known related upstream
rules remain disclosed rather than erased to create an appearance of originality.

Primary specifications consulted for the implementation include the Microsoft
[registry](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceregistryevents-table),
[image-load](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceimageloadevents-table),
[network](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table),
[AzureActivity](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/azureactivity)
and [AWSCloudTrail](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/awscloudtrail)
table references. Behavioral boundaries follow Microsoft's
[SilentProcessExit](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/registry-entries-for-silent-process-exit),
[LSA protection](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection),
[Credential Guard](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/configure),
[ASR reference](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference)
and [Trusted Locations](https://learn.microsoft.com/en-us/microsoft-365-apps/security/trusted-locations)
documentation and the AWS [StopLogging](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_StopLogging.html)
and [DeleteDetector](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DeleteDetector.html)
API definitions. Per-rule references retain further mechanism-specific sources.
