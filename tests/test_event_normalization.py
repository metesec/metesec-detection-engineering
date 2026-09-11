import json
import unittest
from types import SimpleNamespace
from scripts.event_normalization import NAME, normalize_event, kql_prefix


class EventNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.rule = SimpleNamespace(custom_attributes={"metesec_normalization": NAME}, logsource=SimpleNamespace(product="azure", service="auditlogs"))
        self.properties = [
            {"displayName": "DelegatedPermissionGrant.Scope", "newValue": '"RoleManagement.ReadWrite.Directory"'},
            {"displayName": "DelegatedPermissionGrant.ConsentType", "newValue": "AllPrincipals"},
        ]

    def event(self, targets):
        return {"TargetResources": json.dumps(targets), "MsecConsentType": "spoof"}

    def test_same_target_new_values_only(self):
        rows = normalize_event(self.rule, self.event([{"type": "ServicePrincipal", "modifiedProperties": self.properties}]))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["MsecConsentType"], "AllPrincipals")
        self.assertEqual(rows[0]["MsecDelegatedPermissionScope"], "RoleManagement.ReadWrite.Directory")

    def test_cross_target_cannot_join(self):
        targets = [{"type": "ServicePrincipal", "modifiedProperties": [p]} for p in self.properties]
        self.assertEqual(normalize_event(self.rule, self.event(targets)), [])

    def test_matching_target_identity_and_multiple_rows_are_preserved(self):
        targets = [{"id": "unmatched", "type": "ServicePrincipal", "modifiedProperties": []},
                   {"id": "matched", "type": "ServicePrincipal", "modifiedProperties": self.properties}]
        rows = normalize_event(self.rule, self.event(targets))
        self.assertEqual([r["MsecTarget"]["id"] for r in rows], ["matched"])
        targets.append(dict(targets[1], id="second-match"))
        rows = normalize_event(self.rule, self.event(targets))
        self.assertEqual([r["MsecTarget"]["id"] for r in rows], ["matched", "second-match"])

    def test_ambiguous_duplicate_nonstring_and_old_values_rejected(self):
        variants = [self.properties + [self.properties[0]],
                    [dict(self.properties[0], newValue=["scope"]), self.properties[1]],
                    [{"displayName": self.properties[0]["displayName"], "oldValue": "scope"}, self.properties[1]],
                    [dict(self.properties[0], newValue='["scope"]'), self.properties[1]]]
        for properties in variants:
            self.assertEqual(normalize_event(self.rule, self.event([{"type": "ServicePrincipal", "modifiedProperties": properties}])), [])
        for raw in ("broken", "{}", "null", "[]"):
            self.assertEqual(normalize_event(self.rule, {"TargetResources": raw}), [])

    def test_unknown_normalization_and_wrong_table_fail_closed(self):
        self.assertIn("mv-apply", kql_prefix(self.rule, "AuditLogs"))
        with self.assertRaises(ValueError):
            kql_prefix(self.rule, "SigninLogs")
        self.rule.custom_attributes["metesec_normalization"] = "typo"
        with self.assertRaises(ValueError):
            normalize_event(self.rule, {})
