import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("machine lifecycle assessment satisfies its versioned schema", () => {
  const manifests = fs.readdirSync(path.join(root, "catalog/detections")).sort()
    .map((id) => JSON.parse(fs.readFileSync(path.join(root, "catalog/detections", id, "manifest.json"), "utf8")));
  const asOf = manifests.map((m) => m.lifecycle.modified).sort().at(-1);
  const nextDue = manifests.map((m) => {
    const due = new Date(`${m.lifecycle.modified}T00:00:00Z`);
    due.setUTCDate(due.getUTCDate() + m.lifecycle.review_interval_days);
    return due.toISOString().slice(0, 10);
  }).sort()[0];
  const result = spawnSync(
    "python",
    [
      "scripts/check_detection_lifecycle.py",
      "--as-of",
      asOf,
      "--baseline",
      "catalog/index.json",
      "--json",
    ],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);

  const assessment = JSON.parse(result.stdout);
  const schema = JSON.parse(
    fs.readFileSync(
      path.join(root, "governance", "schemas", "detection-lifecycle-assessment-v1.schema.json"),
      "utf8",
    ),
  );
  const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
  assert.equal(validate(assessment), true, JSON.stringify(validate.errors));
  assert.equal(assessment.baseline_checked, true);
  assert.equal(assessment.summary.next_review_due, nextDue);
});
