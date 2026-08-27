import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const schemaPath = path.join(root, "governance", "schemas", "logical-detection-manifest-v1.schema.json");
const validDirectory = path.join(root, "examples", "manifests", "valid");
const invalidDirectory = path.join(root, "examples", "manifests", "invalid");

const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const jsonFiles = (directory) => fs.readdirSync(directory)
  .filter((name) => name.endsWith(".json"))
  .sort()
  .map((name) => path.join(directory, name));
const formatErrors = (errors = []) => errors
  .map((error) => `${error.instancePath || "/"} ${error.message}`)
  .join("; ");

const ajv = new Ajv2020({ allErrors: true, strict: true });
const validate = ajv.compile(readJson(schemaPath));
const validExamples = jsonFiles(validDirectory);
const invalidExamples = jsonFiles(invalidDirectory);

if (validExamples.length === 0 || invalidExamples.length === 0) {
  throw new Error("Expected at least one valid and one invalid manifest example.");
}

let failed = false;
for (const file of validExamples) {
  if (!validate(readJson(file))) {
    failed = true;
    console.error(`FAIL valid/${path.basename(file)}: ${formatErrors(validate.errors)}`);
  } else {
    console.log(`PASS valid/${path.basename(file)}`);
  }
}

for (const file of invalidExamples) {
  if (validate(readJson(file))) {
    failed = true;
    console.error(`FAIL invalid/${path.basename(file)}: unexpectedly accepted`);
  } else {
    console.log(`PASS invalid/${path.basename(file)} rejected: ${formatErrors(validate.errors)}`);
  }
}

if (failed) {
  process.exitCode = 1;
} else {
  console.log(`Manifest contract verified: ${validExamples.length} valid accepted, ${invalidExamples.length} invalid rejected.`);
}
