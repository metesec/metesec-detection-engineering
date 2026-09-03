import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import { validateDetectionPackages } from "./lib/package-contract.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const ajv = new Ajv2020({ allErrors: true, strict: true });
const validateManifest = ajv.compile(readJson(path.join(root, "governance", "schemas", "logical-detection-manifest-v1.schema.json")));
const validateFixtureSet = ajv.compile(readJson(path.join(root, "governance", "schemas", "detection-fixture-set-v1.schema.json")));
const result = validateDetectionPackages({ root, validateManifest, validateFixtureSet });

if (result.errors.length > 0) {
  result.errors.forEach((error) => console.error(`FAIL ${error}`));
  process.exitCode = 1;
} else {
  result.packages.forEach((entry) => console.log(`PASS ${entry.id}: ${entry.status}, ${entry.implementations} implementation(s)`));
  console.log(`Detection package contract verified: ${result.packages.length} package(s).`);
}
