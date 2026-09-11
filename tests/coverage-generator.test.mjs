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
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const manifests = fs.readdirSync(path.join(root, "catalog/detections"), { withFileTypes: true })
  .filter((entry) => entry.isDirectory()).map((entry) => readJson("catalog/detections/" + entry.name + "/manifest.json"))
  .sort((left, right) => left.id.localeCompare(right.id, "en"));
const preview = readJson("targets/sentinel/preview.json");
const contract = readJson("targets/sentinel/data-sources.json");
const uniqueSorted = (values) => [...new Set(values)].sort((a, b) => a.localeCompare(b, "en"));
const mappings = manifests.flatMap((item) => item.attack.map((mapping) => ({ id: item.id, ...mapping })));
const logicalSources = manifests.flatMap((item) => item.data_sources.map((source) => ({ id: item.id, ...source })));

test("builds exact aggregate coverage from authored sources without percentages", () => {
  assert.deepEqual(report.summary, {
    detections: manifests.length,
    attack_mappings: mappings.length,
    attack_techniques: new Set(mappings.map((item) => item.technique_id)).size,
    attack_tactics: new Set(mappings.map((item) => item.tactic)).size,
    logical_data_sources: new Set(logicalSources.map((item) => JSON.stringify([item.name, item.category]))).size,
    sentinel_preview_bindings: new Set(preview.detections.map((item) => item.id)).size,
    sentinel_data_source_contracts: contract.sources.length,
    detections_without_sentinel_binding: manifests.filter((item) => !preview.detections.some((binding) => binding.id === item.id)).length,
  });
  assert.equal(JSON.stringify(report).includes("percent"), false);
});

test("includes every ATT&CK relationship exactly once in ordered groups", () => {
  assert.deepEqual(report.attack.techniques.map((item) => item.technique_id), uniqueSorted(mappings.map((item) => item.technique_id)));
  for (const record of report.attack.techniques) {
    const selected = mappings.filter((item) => item.technique_id === record.technique_id);
    assert.deepEqual(record.detections, uniqueSorted(selected.map((item) => item.id)));
    assert.deepEqual(record.tactics, uniqueSorted(selected.map((item) => item.tactic)));
  }
  assert.deepEqual(report.attack.tactics.map((item) => item.tactic), uniqueSorted(mappings.map((item) => item.tactic)));
  for (const record of report.attack.tactics) {
    const selected = mappings.filter((item) => item.tactic === record.tactic);
    assert.deepEqual(record.detections, uniqueSorted(selected.map((item) => item.id)));
    assert.deepEqual(record.techniques, uniqueSorted(selected.map((item) => item.technique_id)));
  }
});

test("aggregates every logical source and exposes exact unbound detections", () => {
  const keys = uniqueSorted(logicalSources.map((item) => item.name + "\u0000" + item.category));
  assert.deepEqual(report.data_sources.logical.map((item) => item.name + "\u0000" + item.category), keys);
  for (const record of report.data_sources.logical) {
    const selected = logicalSources.filter((item) => item.name === record.name && item.category === record.category);
    assert.deepEqual(record.detections, uniqueSorted(selected.map((item) => item.id)));
    assert.deepEqual(record.required_fields, uniqueSorted(selected.flatMap((item) => item.required_fields)));
  }
  const expectedUnbound = manifests.filter((item) => !preview.detections.some((binding) => binding.id === item.id));
  assert.deepEqual(report.data_sources.detections_without_sentinel_binding, expectedUnbound.map((item) => ({
    id: item.id, title: item.title, data_sources: item.data_sources.map((source) => source.name),
  })));
  assert.ok(expectedUnbound.some((item) => item.id === "MSEC-DET-0001"));
});

test("retains exact Sentinel contracts and independently verifies their consumers", () => {
  assert.deepEqual(report.data_sources.sentinel_contracts.map((item) => item.source_id), contract.sources.map((item) => item.id));
  assert.deepEqual(uniqueSorted(contract.sources.map((item) => item.table)), uniqueSorted(preview.detections.map((item) => item.query_table)));
  for (const source of contract.sources) {
    const consumers = preview.detections.filter((item) => item.query_table === source.table).map((item) => item.id).sort();
    assert.deepEqual(source.consumers, consumers);
    assert.deepEqual(report.data_sources.sentinel_contracts.find((item) => item.source_id === source.id), {
      source_id: source.id,
      table: source.table,
      display_name: source.display_name,
      detections: consumers,
      event_time_column: source.event_time_column,
      required_columns: source.required_columns,
      freshness: source.freshness,
    });
  }
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
