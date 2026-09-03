import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import {
  buildDetectionCatalogue,
  renderCatalogueJson,
  renderCatalogueMarkdown
} from "../scripts/lib/catalogue.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalogue = buildDetectionCatalogue(root);

test("builds the expected ordered catalogue and aggregate evidence", () => {
  assert.deepEqual(
    catalogue.detections.map((detection) => detection.id),
    ["MSEC-DET-0001", "MSEC-DET-0002", "MSEC-DET-0003", "MSEC-DET-0004", "MSEC-DET-0005"]
  );
  assert.deepEqual(catalogue.summary, {
    detections: 5,
    implementations: 5,
    positive_cases: 15,
    negative_cases: 20,
    sentinel_preview_bindings: 4
  });
  assert.deepEqual(catalogue.detections[0].target_bindings, []);
  assert.deepEqual(
    catalogue.detections.slice(1).map((detection) => detection.target_bindings[0].table),
    ["SigninLogs", "SigninLogs", "AuditLogs", "AuditLogs"]
  );
});

test("generated machine catalogue satisfies its versioned schema", () => {
  const schema = JSON.parse(fs.readFileSync(path.join(root, "governance", "schemas", "detection-catalogue-v1.schema.json"), "utf8"));
  const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
  assert.equal(validate(catalogue), true, JSON.stringify(validate.errors));
});

test("tracked machine and human catalogues match deterministic rendering", () => {
  assert.equal(
    fs.readFileSync(path.join(root, "catalog", "index.json"), "utf8"),
    renderCatalogueJson(catalogue)
  );
  assert.equal(
    fs.readFileSync(path.join(root, "CATALOGUE.md"), "utf8"),
    renderCatalogueMarkdown(catalogue)
  );
});
