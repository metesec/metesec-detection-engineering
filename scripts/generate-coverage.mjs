import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import {
  buildCoverageReport,
  renderCoverageJson,
  renderCoverageMarkdown,
} from "./lib/coverage.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const schemaPath = path.join(root, "governance", "schemas", "detection-coverage-report-v1.schema.json");
const outputs = [
  { path: path.join(root, "coverage", "index.json"), render: renderCoverageJson },
  { path: path.join(root, "COVERAGE.md"), render: renderCoverageMarkdown },
];

const args = process.argv.slice(2);
if (args.length > 1 || (args.length === 1 && args[0] !== "--check")) {
  throw new Error("Usage: node scripts/generate-coverage.mjs [--check]");
}

const report = buildCoverageReport(root);
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
if (!validate(report)) {
  const errors = (validate.errors || [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`Generated coverage report violates schema: ${errors}`);
}

if (args[0] === "--check") {
  const stale = outputs
    .filter((output) => !fs.existsSync(output.path) || fs.readFileSync(output.path, "utf8") !== output.render(report))
    .map((output) => path.relative(root, output.path).replaceAll("\\", "/"));
  if (stale.length > 0) {
    throw new Error(`Generated coverage report is stale: ${stale.join(", ")}. Run pnpm run build:coverage.`);
  }
  console.log(
    `Coverage validation passed: ${report.summary.attack_techniques} ATT&CK technique(s), `
      + `${report.summary.logical_data_sources} logical source(s), `
      + `${report.summary.sentinel_data_source_contracts} Sentinel contract(s).`,
  );
} else {
  for (const output of outputs) {
    fs.mkdirSync(path.dirname(output.path), { recursive: true });
    fs.writeFileSync(output.path, output.render(report), "utf8");
  }
  console.log("Generated coverage/index.json and COVERAGE.md from repository sources.");
}
