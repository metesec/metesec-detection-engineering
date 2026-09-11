"""Explicit, versioned raw-event adapters; never infer normalization from an ID."""
from __future__ import annotations

import json

NAME = "entra-delegated-grant-v1"
FIELDS = ("MsecDelegatedPermissionScope", "MsecConsentType")
PROPERTIES = ("DelegatedPermissionGrant.Scope", "DelegatedPermissionGrant.ConsentType")


def normalization_name(rule):
    name = rule.custom_attributes.get("metesec_normalization")
    if name not in (None, NAME):
        raise ValueError(f"unsupported event normalization: {name}")
    if name and (rule.logsource.product != "azure" or rule.logsource.service != "auditlogs"):
        raise ValueError("delegated-grant normalization requires azure/auditlogs")
    return name


def _string_value(value):
    if not isinstance(value, str):
        return None
    # Audit records use either a scalar string or a JSON-encoded string.
    try:
        parsed = json.loads(value)
    except (ValueError, TypeError):
        return value
    return parsed if isinstance(parsed, str) else None


def normalize_event(rule, event):
    if normalization_name(rule) is None:
        return [event]
    raw = event.get("TargetResources")
    try:
        targets = json.loads(raw) if isinstance(raw, str) else raw
    except ValueError:
        return []
    if not isinstance(targets, list):
        return []
    result = []
    for target in targets:
        if not isinstance(target, dict) or target.get("type") != "ServicePrincipal":
            continue
        properties = target.get("modifiedProperties")
        if not isinstance(properties, list):
            continue
        row = {key: value for key, value in event.items() if key not in FIELDS}
        row["MsecTarget"] = target
        for field, name in zip(FIELDS, PROPERTIES):
            values = [p.get("newValue") for p in properties if isinstance(p, dict) and p.get("displayName") == name]
            # Duplicate property names are ambiguous, even if values are equal.
            if len(values) != 1 or (value := _string_value(values[0])) is None:
                break
            row[field] = value
        else:
            result.append(row)
    return result


def kql_prefix(rule, table):
    if normalization_name(rule) is None:
        return table
    if table != "AuditLogs":
        raise ValueError("delegated-grant normalization requires AuditLogs")
    # mv-apply preserves the original event and keeps property pairs inside one
    # target object. countif rejects duplicates; no oldValue or text search.
    return table + r'''
| mv-apply MsecTarget = TargetResources on (
    where tostring(MsecTarget.type) == "ServicePrincipal"
    | mv-apply MsecProperty = MsecTarget.modifiedProperties on (
        summarize MsecScopes = make_list_if(MsecProperty.newValue, tostring(MsecProperty.displayName) == "DelegatedPermissionGrant.Scope"),
                  MsecConsentTypes = make_list_if(MsecProperty.newValue, tostring(MsecProperty.displayName) == "DelegatedPermissionGrant.ConsentType"),
                  MsecScopeCount = countif(tostring(MsecProperty.displayName) == "DelegatedPermissionGrant.Scope"),
                  MsecConsentCount = countif(tostring(MsecProperty.displayName) == "DelegatedPermissionGrant.ConsentType")
    )
    | where MsecScopeCount == 1 and MsecConsentCount == 1
    | where gettype(MsecScopes[0]) == "string" and gettype(MsecConsentTypes[0]) == "string"
    | extend MsecScopeParsed = parse_json(tostring(MsecScopes[0])), MsecConsentParsed = parse_json(tostring(MsecConsentTypes[0]))
    | where gettype(MsecScopeParsed) == "string" and gettype(MsecConsentParsed) == "string"
    | extend MsecDelegatedPermissionScope = tostring(MsecScopeParsed), MsecConsentType = tostring(MsecConsentParsed)
)'''
