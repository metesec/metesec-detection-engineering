import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const schema = (name) => readJson(path.join(root, "governance", "schemas", name));
const policyPath = path.join(root, "governance", "policies", "sentinel-runtime-health-v1.json");
const policy = readJson(policyPath);
const ajv = new Ajv2020({ allErrors: true, strict: true });
const validatePolicy = ajv.compile(schema("sentinel-runtime-health-policy-v1.schema.json"));
ajv.compile(schema("sentinel-runtime-observation-v1.schema.json"));
ajv.compile(schema("sentinel-runtime-assessment-v1.schema.json"));

if (!validatePolicy(policy)) {
  const errors = (validatePolicy.errors || [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`Sentinel runtime-health policy violates schema: ${errors}`);
}
if (policy.degraded_after_missed_runs >= policy.failed_after_missed_runs) {
  throw new Error("Sentinel runtime-health degraded threshold must be below failed threshold");
}

const profile = readJson(path.join(root, ...policy.source_profile.split("/")));
if (profile.schema_version !== 1 || profile.target !== policy.target || !Array.isArray(profile.rules)) {
  throw new Error("Sentinel runtime-health source profile is invalid");
}
const ids = profile.rules.map((rule) => rule.id);
if (new Set(ids).size !== ids.length) {
  throw new Error("Sentinel runtime-health source profile contains duplicate rule IDs");
}

console.log(
  `Sentinel runtime-health contract verified: ${ids.length} rule(s), `
    + `${policy.degraded_after_missed_runs}/${policy.failed_after_missed_runs} missed-run thresholds.`,
);
