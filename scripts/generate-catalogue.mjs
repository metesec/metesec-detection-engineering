import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import {
  buildDetectionCatalogue,
  renderCatalogueJson,
  renderCatalogueMarkdown
} from "./lib/catalogue.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const schemaPath = path.join(root, "governance", "schemas", "detection-catalogue-v1.schema.json");
const outputs = [
  {
    path: path.join(root, "catalog", "index.json"),
    render: renderCatalogueJson
  },
  {
    path: path.join(root, "CATALOGUE.md"),
    render: renderCatalogueMarkdown
  }
];

const args = process.argv.slice(2);
if (args.length > 1 || (args.length === 1 && args[0] !== "--check")) {
  throw new Error("Usage: node scripts/generate-catalogue.mjs [--check]");
}

const catalogue = buildDetectionCatalogue(root);
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const validate = new Ajv2020({ allErrors: true, strict: true }).compile(schema);
if (!validate(catalogue)) {
  const errors = (validate.errors || [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`Generated catalogue violates schema: ${errors}`);
}

if (args[0] === "--check") {
  const stale = [];
  for (const output of outputs) {
    const expected = output.render(catalogue);
    if (!fs.existsSync(output.path) || fs.readFileSync(output.path, "utf8") !== expected) {
      stale.push(path.relative(root, output.path).replaceAll("\\", "/"));
    }
  }
  if (stale.length > 0) {
    throw new Error(`Generated catalogue is stale: ${stale.join(", ")}. Run pnpm run build:catalogue.`);
  }
  console.log(`Catalogue validation passed: ${catalogue.summary.detections} detections, ${catalogue.summary.positive_cases + catalogue.summary.negative_cases} synthetic cases, ${catalogue.summary.sentinel_preview_bindings} Sentinel preview bindings.`);
} else {
  for (const output of outputs) {
    fs.mkdirSync(path.dirname(output.path), { recursive: true });
    fs.writeFileSync(output.path, output.render(catalogue), "utf8");
  }
  console.log("Generated catalog/index.json and CATALOGUE.md from repository sources.");
}
