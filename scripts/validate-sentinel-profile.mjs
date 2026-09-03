import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const schemaPath = path.join(
  root,
  "governance",
  "schemas",
  "sentinel-analytics-rule-profile-v1.schema.json",
);
const profilePath = path.join(root, "targets", "sentinel", "analytics-rules.json");
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const formatErrors = (errors = []) => errors
  .map((error) => `${error.instancePath || "/"} ${error.message}`)
  .join("; ");

const ajv = new Ajv2020({ allErrors: true, strict: true });
const validate = ajv.compile(readJson(schemaPath));
const profile = readJson(profilePath);

if (!validate(profile)) {
  console.error(`FAIL ${path.relative(root, profilePath)}: ${formatErrors(validate.errors)}`);
  process.exitCode = 1;
} else {
  console.log(
    `Sentinel analytics-rule profile verified: ${profile.rules.length} disabled rule configuration(s).`,
  );
}
