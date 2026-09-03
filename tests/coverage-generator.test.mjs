import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import {
  buildCoverageReport,
  renderCoverageJson,
  renderCoverageMarkdown,
} from "../scripts/lib/coverage.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const report = buildCoverageReport(root);

test("builds exact aggregate coverage without percentages", () => {
  assert.deepEqual(report.summary, {
    detections: 45,
    attack_mappings: 60,
    attack_techniques: 35,
    attack_tactics: 11,
    logical_data_sources: 6,
    sentinel_preview_bindings: 44,
    sentinel_data_source_contracts: 5,
    detections_without_sentinel_binding: 1,
  });
  assert.equal(JSON.stringify(report).includes("percent"), false);
});

test("aggregates ATT&CK techniques and tactics deterministically", () => {
  assert.deepEqual(
    report.attack.techniques.map((item) => [item.technique_id, item.detections]),
    [
      ["T1003.001", ["MSEC-DET-0011", "MSEC-DET-0036"]],
      ["T1003.002", ["MSEC-DET-0023"]],
      ["T1003.003", ["MSEC-DET-0030"]],
      ["T1021.006", ["MSEC-DET-0038"]],
      ["T1047", ["MSEC-DET-0024"]],
      ["T1053.005", ["MSEC-DET-0028"]],
      ["T1059", ["MSEC-DET-0006"]],
      ["T1059.001", ["MSEC-DET-0007", "MSEC-DET-0039"]],
      ["T1078.004", ["MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0010", "MSEC-DET-0026"]],
      ["T1098.001", ["MSEC-DET-0004", "MSEC-DET-0009"]],
      ["T1098.003", ["MSEC-DET-0005", "MSEC-DET-0008", "MSEC-DET-0015", "MSEC-DET-0021"]],
      ["T1098.007", ["MSEC-DET-0029"]],
      ["T1105", ["MSEC-DET-0020", "MSEC-DET-0043", "MSEC-DET-0044"]],
      ["T1127.001", ["MSEC-DET-0045"]],
      ["T1140", ["MSEC-DET-0035"]],
      ["T1197", ["MSEC-DET-0025"]],
      ["T1218.003", ["MSEC-DET-0041"]],
      ["T1218.004", ["MSEC-DET-0044"]],
      ["T1218.005", ["MSEC-DET-0012"]],
      ["T1218.007", ["MSEC-DET-0043"]],
      ["T1218.008", ["MSEC-DET-0042"]],
      ["T1218.010", ["MSEC-DET-0013"]],
      ["T1218.011", ["MSEC-DET-0027"]],
      ["T1484.002", ["MSEC-DET-0019"]],
      ["T1490", ["MSEC-DET-0016"]],
      ["T1505.003", ["MSEC-DET-0031"]],
      ["T1543.003", ["MSEC-DET-0001", "MSEC-DET-0034"]],
      ["T1546.008", ["MSEC-DET-0040"]],
      ["T1548.002", ["MSEC-DET-0037"]],
      ["T1556.006", ["MSEC-DET-0022"]],
      ["T1556.009", ["MSEC-DET-0014"]],
      ["T1685", ["MSEC-DET-0018"]],
      ["T1685.001", ["MSEC-DET-0032"]],
      ["T1685.005", ["MSEC-DET-0017"]],
      ["T1686.003", ["MSEC-DET-0033"]],
    ],
  );
  assert.deepEqual(
    report.attack.tactics.map((item) => item.tactic),
    ["Command and Control", "Credential Access", "Defense Evasion", "Defense Impairment", "Execution", "Impact", "Initial Access", "Lateral Movement", "Persistence", "Privilege Escalation", "Stealth"],
  );
});

test("aggregates logical sources and exposes the explicit Sentinel gap", () => {
  const signIns = report.data_sources.logical.find(
    (item) => item.name === "Microsoft Entra sign-in logs",
  );
  assert.deepEqual(signIns.detections, ["MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0026"]);
  assert.deepEqual(
    signIns.required_fields,
    [
      "AppDisplayName",
      "AuthenticationProtocol",
      "ClientAppUsed",
      "IPAddress",
      "ResultType",
      "RiskLevelDuringSignIn",
      "TimeGenerated",
      "UserPrincipalName",
    ],
  );
  assert.deepEqual(report.data_sources.detections_without_sentinel_binding, [
    {
      id: "MSEC-DET-0001",
      title: "Windows service installation from a public or temporary path",
      data_sources: ["Windows service installation events"],
    },
  ]);
});

test("retains exact Sentinel contract relationships", () => {
  assert.deepEqual(
    report.data_sources.sentinel_contracts.map((item) => ({
      source_id: item.source_id,
      table: item.table,
      detections: item.detections,
      required_columns: item.required_columns.length,
    })),
    [
      {
        source_id: "MSEC-SDS-0001",
        table: "SigninLogs",
        detections: ["MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0026"],
        required_columns: 16,
      },
      {
        source_id: "MSEC-SDS-0002",
        table: "AuditLogs",
        detections: ["MSEC-DET-0004", "MSEC-DET-0005", "MSEC-DET-0008", "MSEC-DET-0009", "MSEC-DET-0014", "MSEC-DET-0015", "MSEC-DET-0019", "MSEC-DET-0021", "MSEC-DET-0022"],
        required_columns: 7,
      },
      {
        source_id: "MSEC-SDS-0003",
        table: "DeviceProcessEvents",
        detections: ["MSEC-DET-0006", "MSEC-DET-0007", "MSEC-DET-0011", "MSEC-DET-0012", "MSEC-DET-0013", "MSEC-DET-0016", "MSEC-DET-0017", "MSEC-DET-0018", "MSEC-DET-0020", "MSEC-DET-0023", "MSEC-DET-0024", "MSEC-DET-0025", "MSEC-DET-0027", "MSEC-DET-0028", "MSEC-DET-0029", "MSEC-DET-0030", "MSEC-DET-0031", "MSEC-DET-0032", "MSEC-DET-0033", "MSEC-DET-0034", "MSEC-DET-0035", "MSEC-DET-0036", "MSEC-DET-0037", "MSEC-DET-0038", "MSEC-DET-0039", "MSEC-DET-0041", "MSEC-DET-0042", "MSEC-DET-0043", "MSEC-DET-0044", "MSEC-DET-0045"],
        required_columns: 13,
      },
      {
        source_id: "MSEC-SDS-0004",
        table: "AADUserRiskEvents",
        detections: ["MSEC-DET-0010"],
        required_columns: 10,
      },
      {
        source_id: "MSEC-SDS-0005",
        table: "DeviceRegistryEvents",
        detections: ["MSEC-DET-0040"],
        required_columns: 14,
      },
    ],
  );
});

test("generated machine report satisfies its versioned schema", () => {
  const schema = JSON.parse(
    fs.readFileSync(
      path.join(root, "governance", "schemas", "detection-coverage-report-v1.schema.json"),
      "utf8",
    ),
  );
  const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
  assert.equal(validate(report), true, JSON.stringify(validate.errors));
});

test("tracked machine and human reports match deterministic rendering", () => {
  assert.equal(
    fs.readFileSync(path.join(root, "coverage", "index.json"), "utf8"),
    renderCoverageJson(report),
  );
  assert.equal(
    fs.readFileSync(path.join(root, "COVERAGE.md"), "utf8"),
    renderCoverageMarkdown(report),
  );
});
