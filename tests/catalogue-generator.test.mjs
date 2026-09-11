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
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const manifestDirectories = fs.readdirSync(path.join(root, "catalog/detections"), { withFileTypes: true })
  .filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
const manifests = manifestDirectories.map((id) => readJson("catalog/detections/" + id + "/manifest.json"));
const preview = readJson("targets/sentinel/preview.json");

test("builds every authored detection and counts its independent fixture evidence", () => {
  assert.ok(manifests.length > 0);
  assert.deepEqual(manifests.map((item) => item.id), manifestDirectories);
  assert.deepEqual(catalogue.detections.map((item) => item.id), manifestDirectories);
  assert.equal(new Set(catalogue.detections.map((item) => item.id)).size, manifests.length);
  const fixtureCases = manifests.flatMap((manifest) => manifest.implementations.flatMap(
    (implementation) => readJson(path.posix.join(path.posix.dirname(implementation.path), "tests/cases.json")).cases,
  ));
  assert.deepEqual(catalogue.summary, {
    detections: manifests.length,
    implementations: manifests.flatMap((manifest) => manifest.implementations).length,
    positive_cases: fixtureCases.filter((item) => item.expectation === "match").length,
    negative_cases: fixtureCases.filter((item) => item.expectation === "no_match").length,
    sentinel_preview_bindings: preview.detections.length,
  });
  for (const manifest of manifests) {
    const actual = catalogue.detections.find((item) => item.id === manifest.id);
    for (const field of ["title", "description", "lifecycle", "severity", "confidence", "attack", "data_sources", "implementations"]) {
      assert.deepEqual(actual[field], manifest[field], manifest.id + " " + field);
    }
    const cases = manifest.implementations.flatMap(
      (implementation) => readJson(path.posix.join(path.posix.dirname(implementation.path), "tests/cases.json")).cases,
    );
    assert.deepEqual(actual.validation, {
      positive_cases: cases.filter((item) => item.expectation === "match").length,
      negative_cases: cases.filter((item) => item.expectation === "no_match").length,
    });
    assert.deepEqual(actual.target_bindings, preview.detections.filter((entry) => entry.id === manifest.id).map(
      (entry) => ({ target: preview.target, table: entry.query_table, golden: entry.golden }),
    ));
  }
  assert.deepEqual(catalogue.detections.find((item) => item.id === "MSEC-DET-0001").target_bindings, []);
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
