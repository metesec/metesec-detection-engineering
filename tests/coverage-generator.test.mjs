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
    detections: 15,
    attack_mappings: 15,
    attack_techniques: 10,
    attack_tactics: 6,
    logical_data_sources: 5,
    sentinel_preview_bindings: 14,
    sentinel_data_source_contracts: 4,
    detections_without_sentinel_binding: 1,
  });
  assert.equal(JSON.stringify(report).includes("percent"), false);
});

test("aggregates ATT&CK techniques and tactics deterministically", () => {
  assert.deepEqual(
    report.attack.techniques.map((item) => [item.technique_id, item.detections]),
    [
      ["T1003.001", ["MSEC-DET-0011"]],
      ["T1059", ["MSEC-DET-0006"]],
      ["T1059.001", ["MSEC-DET-0007"]],
      ["T1078.004", ["MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0010"]],
      ["T1098.001", ["MSEC-DET-0004", "MSEC-DET-0009"]],
      ["T1098.003", ["MSEC-DET-0005", "MSEC-DET-0008", "MSEC-DET-0015"]],
      ["T1218.005", ["MSEC-DET-0012"]],
      ["T1218.010", ["MSEC-DET-0013"]],
      ["T1543.003", ["MSEC-DET-0001"]],
      ["T1556.009", ["MSEC-DET-0014"]],
    ],
  );
  assert.deepEqual(
    report.attack.tactics.map((item) => item.tactic),
    ["Credential Access", "Defense Evasion", "Execution", "Initial Access", "Persistence", "Privilege Escalation"],
  );
});

test("aggregates logical sources and exposes the explicit Sentinel gap", () => {
  const signIns = report.data_sources.logical.find(
    (item) => item.name === "Microsoft Entra sign-in logs",
  );
  assert.deepEqual(signIns.detections, ["MSEC-DET-0002", "MSEC-DET-0003"]);
  assert.deepEqual(
    signIns.required_fields,
    [
      "AppDisplayName",
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
        detections: ["MSEC-DET-0002", "MSEC-DET-0003"],
        required_columns: 15,
      },
      {
        source_id: "MSEC-SDS-0002",
        table: "AuditLogs",
        detections: ["MSEC-DET-0004", "MSEC-DET-0005", "MSEC-DET-0008", "MSEC-DET-0009", "MSEC-DET-0014", "MSEC-DET-0015"],
        required_columns: 7,
      },
      {
        source_id: "MSEC-SDS-0003",
        table: "DeviceProcessEvents",
        detections: ["MSEC-DET-0006", "MSEC-DET-0007", "MSEC-DET-0011", "MSEC-DET-0012", "MSEC-DET-0013"],
        required_columns: 12,
      },
      {
        source_id: "MSEC-SDS-0004",
        table: "AADUserRiskEvents",
        detections: ["MSEC-DET-0010"],
        required_columns: 10,
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
