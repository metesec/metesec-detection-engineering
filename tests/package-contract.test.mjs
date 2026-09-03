import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { validateDetectionPackages } from "../scripts/lib/package-contract.mjs";

const alwaysValid = Object.assign(() => true, { errors: [] });
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
};
const createRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "metesec-package-v1-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};
const manifest = (id = "MSEC-DET-0001", overrides = {}) => ({
  id,
  lifecycle: { status: "draft" },
  validation: { positive_tests: false, negative_tests: false },
  implementations: [],
  ...overrides
});
const validate = (root) => validateDetectionPackages({
  root,
  validateManifest: alwaysValid,
  validateFixtureSet: alwaysValid,
  validateEventFixture: alwaysValid
});

test("accepts a compact draft package without speculative implementation files", (t) => {
  const root = createRoot(t);
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest());
  assert.deepEqual(validate(root).errors, []);
});

test("rejects a catalogue directory that differs from the manifest identity", (t) => {
  const root = createRoot(t);
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-9999", "manifest.json"), manifest());
  assert.match(validate(root).errors.join("\n"), /directory must match manifest id MSEC-DET-0001/);
});

test("rejects a declared implementation that does not exist", (t) => {
  const root = createRoot(t);
  const implementation = "content/portable/sigma/MSEC-DET-0001/rule.yml";
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    implementations: [{ type: "sigma", path: implementation, targets: ["sentinel"], status: "planned" }]
  }));
  assert.match(validate(root).errors.join("\n"), /declared implementation file does not exist/);
});

test("rejects implementation paths that escape the repository", (t) => {
  const root = createRoot(t);
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    implementations: [{ type: "sigma", path: "../MSEC-DET-0001/rule.yml", targets: ["sentinel"], status: "planned" }]
  }));
  assert.match(validate(root).errors.join("\n"), /implementation path must stay repository-relative/);
});

test("rejects behavioral claims without a fixture-set index", (t) => {
  const root = createRoot(t);
  const implementation = "content/portable/sigma/MSEC-DET-0001/rule.yml";
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    validation: { positive_tests: true, negative_tests: false },
    implementations: [{ type: "sigma", path: implementation, targets: ["sentinel"], status: "active" }]
  }));
  fs.mkdirSync(path.join(root, "content", "portable", "sigma", "MSEC-DET-0001"), { recursive: true });
  fs.writeFileSync(path.join(root, ...implementation.split("/")), "title: Synthetic test rule\n");
  assert.match(validate(root).errors.join("\n"), /validation claims require tests\/cases.json/);
});

test("accepts linked implementation and synthetic positive and negative fixtures", (t) => {
  const root = createRoot(t);
  const implementation = "content/portable/sigma/MSEC-DET-0001/rule.yml";
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    validation: { positive_tests: true, negative_tests: true },
    implementations: [{ type: "sigma", path: implementation, targets: ["sentinel"], status: "active" }]
  }));
  fs.mkdirSync(path.join(root, "content", "portable", "sigma", "MSEC-DET-0001"), { recursive: true });
  fs.writeFileSync(path.join(root, ...implementation.split("/")), "title: Synthetic test rule\n");
  const testsRoot = path.join(root, "content", "portable", "sigma", "MSEC-DET-0001", "tests");
  writeJson(path.join(testsRoot, "cases.json"), {
    schema_version: 1,
    detection_id: "MSEC-DET-0001",
    implementation,
    cases: [
      { id: "suspicious-service", expectation: "match", fixture: "fixtures/suspicious.json", description: "Synthetic suspicious service creation." },
      { id: "approved-installer", expectation: "no_match", fixture: "fixtures/approved.json", description: "Synthetic approved software installation." }
    ]
  });
  writeJson(path.join(testsRoot, "fixtures", "suspicious.json"), { synthetic: true });
  writeJson(path.join(testsRoot, "fixtures", "approved.json"), { synthetic: true });
  assert.deepEqual(validate(root).errors, []);
});

test("rejects fixture paths that escape the implementation-local fixture directory", (t) => {
  const root = createRoot(t);
  const implementation = "content/portable/sigma/MSEC-DET-0001/rule.yml";
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    implementations: [{ type: "sigma", path: implementation, targets: ["sentinel"], status: "active" }]
  }));
  fs.mkdirSync(path.join(root, "content", "portable", "sigma", "MSEC-DET-0001"), { recursive: true });
  fs.writeFileSync(path.join(root, ...implementation.split("/")), "title: Synthetic test rule\n");
  const testsRoot = path.join(root, "content", "portable", "sigma", "MSEC-DET-0001", "tests");
  writeJson(path.join(testsRoot, "cases.json"), {
    schema_version: 1,
    detection_id: "MSEC-DET-0001",
    implementation,
    cases: [
      { id: "escaped-fixture", expectation: "match", fixture: "fixtures/../../outside.json", description: "Fixture path attempts to leave its owned directory." }
    ]
  });
  assert.match(validate(root).errors.join("\n"), /must stay inside tests\/fixtures/);
});

test("rejects an event fixture that violates its schema", (t) => {
  const root = createRoot(t);
  const implementation = "content/portable/sigma/MSEC-DET-0001/rule.yml";
  writeJson(path.join(root, "catalog", "detections", "MSEC-DET-0001", "manifest.json"), manifest("MSEC-DET-0001", {
    implementations: [{ type: "sigma", path: implementation, targets: ["sentinel"], status: "active" }]
  }));
  fs.mkdirSync(path.join(root, "content", "portable", "sigma", "MSEC-DET-0001"), { recursive: true });
  fs.writeFileSync(path.join(root, ...implementation.split("/")), "title: Synthetic test rule\n");
  const testsRoot = path.join(root, "content", "portable", "sigma", "MSEC-DET-0001", "tests");
  writeJson(path.join(testsRoot, "cases.json"), {
    schema_version: 1,
    detection_id: "MSEC-DET-0001",
    implementation,
    cases: [
      { id: "not-synthetic", expectation: "match", fixture: "fixtures/not-synthetic.json", description: "Fixture deliberately fails the synthetic-event contract." }
    ]
  });
  writeJson(path.join(testsRoot, "fixtures", "not-synthetic.json"), { synthetic: false });
  const rejectNonSynthetic = Object.assign((fixture) => fixture.synthetic === true, {
    errors: [{ instancePath: "/synthetic", message: "must be equal to constant" }]
  });

  const result = validateDetectionPackages({
    root,
    validateManifest: alwaysValid,
    validateFixtureSet: alwaysValid,
    validateEventFixture: rejectNonSynthetic
  });

  assert.match(result.errors.join("\n"), /fixture fixtures\/not-synthetic\.json \/synthetic must be equal to constant/);
});
