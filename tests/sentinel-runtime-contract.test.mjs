import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("machine Sentinel runtime assessment satisfies its versioned schema", (context) => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "metesec-runtime-health-"));
  context.after(() => fs.rmSync(temporary, { recursive: true, force: true }));
  const observationPath = path.join(temporary, "observation.json");
  const observedAt = "2026-09-03T12:00:00Z";
  const rule = (id, lastExecutionAt) => ({
    id,
    rule_exists: true,
    enabled: true,
    last_execution_at: lastExecutionAt,
    last_execution_status: "succeeded",
    alert_outcome: {
      window_start: "2026-09-03T11:00:00Z",
      window_end: observedAt,
      alerts_created: 0,
      incidents_created: 0,
    },
  });
  const observation = {
    schema_version: 1,
    target: "microsoft-sentinel",
    observed_at: observedAt,
    rules: [
      rule("MSEC-DET-0002", "2026-09-03T11:30:00Z"),
      rule("MSEC-DET-0003", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0004", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0005", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0006", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0007", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0008", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0009", "2026-09-03T11:59:00Z"),
      rule("MSEC-DET-0010", "2026-09-03T11:59:00Z"),
    ],
  };
  const observationSchema = JSON.parse(
    fs.readFileSync(
      path.join(root, "governance", "schemas", "sentinel-runtime-observation-v1.schema.json"),
      "utf8",
    ),
  );
  const validateObservation = new Ajv2020({ allErrors: true, strict: true })
    .compile(observationSchema);
  assert.equal(
    validateObservation(observation),
    true,
    JSON.stringify(validateObservation.errors),
  );
  fs.writeFileSync(observationPath, `${JSON.stringify(observation, null, 2)}\n`, "utf8");

  const result = spawnSync(
    "python",
    [
      "scripts/check_sentinel_runtime_health.py",
      "--observation",
      observationPath,
      "--json",
    ],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);

  const assessment = JSON.parse(result.stdout);
  const schema = JSON.parse(
    fs.readFileSync(
      path.join(root, "governance", "schemas", "sentinel-runtime-assessment-v1.schema.json"),
      "utf8",
    ),
  );
  const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
  assert.equal(validate(assessment), true, JSON.stringify(validate.errors));
  assert.deepEqual(assessment.summary, {
    rules: 9,
    healthy: 9,
    degraded: 0,
    failed: 0,
    unknown: 0,
  });
  assert.ok(assessment.rules.every((item) => item.alert_outcome.alerts_created === 0));
});
