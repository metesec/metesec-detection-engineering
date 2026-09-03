import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const policyPath = path.join(root, "governance", "policies", "detection-lifecycle-v1.json");
const policySchemaPath = path.join(root, "governance", "schemas", "detection-lifecycle-policy-v1.schema.json");
const manifestSchemaPath = path.join(root, "governance", "schemas", "logical-detection-manifest-v1.schema.json");
const assessmentSchemaPath = path.join(root, "governance", "schemas", "detection-lifecycle-assessment-v1.schema.json");

const policy = readJson(policyPath);
const schema = readJson(policySchemaPath);
const ajv = new Ajv2020({ allErrors: true, strict: true });
const validate = ajv.compile(schema);
ajv.compile(readJson(assessmentSchemaPath));
if (!validate(policy)) {
  const errors = (validate.errors || [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`Lifecycle policy violates schema: ${errors}`);
}

const manifestSchema = readJson(manifestSchemaPath);
const manifestStatuses = manifestSchema.$defs.lifecycle.properties.status.enum;
const transitionStatuses = policy.transitions.map((entry) => entry.from);
if (JSON.stringify(transitionStatuses) !== JSON.stringify(manifestStatuses)) {
  throw new Error("Lifecycle policy must define each manifest status once in schema order");
}
for (const transition of policy.transitions) {
  if (!transition.to.includes(transition.from)) {
    throw new Error(`Lifecycle policy must allow unchanged status ${transition.from}`);
  }
}

console.log(
  `Lifecycle policy verified: ${policy.transitions.length} status transition set(s), `
    + `${policy.review_states.length} review state(s).`,
);
