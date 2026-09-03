import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const contractPath = path.join(root, "targets", "sentinel", "data-sources.json");
const previewPath = path.join(root, "targets", "sentinel", "preview.json");
const contractSchemaPath = path.join(
  root,
  "governance",
  "schemas",
  "sentinel-data-source-contract-v1.schema.json",
);
const observationSchemaPath = path.join(
  root,
  "governance",
  "schemas",
  "sentinel-data-source-observation-v1.schema.json",
);
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const formatErrors = (errors = []) => errors
  .map((error) => `${error.instancePath || "/"} ${error.message}`)
  .join("; ");

const ajv = new Ajv2020({ allErrors: true, strict: true });
const validateContract = ajv.compile(readJson(contractSchemaPath));
ajv.compile(readJson(observationSchemaPath));
const contract = readJson(contractPath);

if (!validateContract(contract)) {
  console.error(
    `FAIL ${path.relative(root, contractPath)}: ${formatErrors(validateContract.errors)}`,
  );
  process.exit(1);
}

const preview = readJson(previewPath);
const expectedByTable = new Map();
for (const binding of preview.detections) {
  const consumers = expectedByTable.get(binding.query_table) ?? [];
  consumers.push(binding.id);
  expectedByTable.set(binding.query_table, consumers);
}

const errors = [];
const sourceIds = new Set();
const sourceTables = new Set();
for (const source of contract.sources) {
  if (sourceIds.has(source.id)) errors.push(`duplicate source ID ${source.id}`);
  if (sourceTables.has(source.table)) errors.push(`duplicate source table ${source.table}`);
  sourceIds.add(source.id);
  sourceTables.add(source.table);

  const columnNames = source.required_columns.map((column) => column.name);
  if (new Set(columnNames).size !== columnNames.length) {
    errors.push(`${source.id} contains duplicate required columns`);
  }
  const eventTime = source.required_columns.find(
    (column) => column.name === source.event_time_column,
  );
  if (!eventTime || eventTime.type !== "datetime") {
    errors.push(`${source.id} event_time_column must be a required datetime column`);
  }

  const expected = expectedByTable.get(source.table);
  if (!expected) {
    errors.push(`${source.id} has no binding in the Sentinel preview`);
  } else if (JSON.stringify(source.consumers) !== JSON.stringify(expected)) {
    errors.push(
      `${source.id} consumers must exactly match preview bindings: ${expected.join(", ")}`,
    );
  }
}

for (const table of expectedByTable.keys()) {
  if (!sourceTables.has(table)) errors.push(`preview table ${table} has no data-source contract`);
}

if (errors.length > 0) {
  for (const error of errors) console.error(`FAIL ${error}`);
  process.exit(1);
}

console.log(
  `Sentinel data-source contract verified: ${contract.sources.length} source(s), `
    + `${preview.detections.length} bound detection(s).`,
);
