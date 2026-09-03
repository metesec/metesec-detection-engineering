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
    detections: 5,
    attack_mappings: 5,
    attack_techniques: 4,
    attack_tactics: 3,
    logical_data_sources: 3,
    sentinel_preview_bindings: 4,
    sentinel_data_source_contracts: 2,
    detections_without_sentinel_binding: 1,
  });
  assert.equal(JSON.stringify(report).includes("percent"), false);
});

test("aggregates ATT&CK techniques and tactics deterministically", () => {
  assert.deepEqual(
    report.attack.techniques.map((item) => [item.technique_id, item.detections]),
    [
      ["T1078.004", ["MSEC-DET-0002", "MSEC-DET-0003"]],
      ["T1098.001", ["MSEC-DET-0004"]],
      ["T1098.003", ["MSEC-DET-0005"]],
      ["T1543.003", ["MSEC-DET-0001"]],
    ],
  );
  assert.deepEqual(
    report.attack.tactics.map((item) => item.tactic),
    ["Initial Access", "Persistence", "Privilege Escalation"],
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
        detections: ["MSEC-DET-0004", "MSEC-DET-0005"],
        required_columns: 7,
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
