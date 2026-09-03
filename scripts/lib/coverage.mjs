import fs from "node:fs";
import path from "node:path";
import { buildDetectionCatalogue } from "./catalogue.mjs";

const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const compareText = (left, right) => left.localeCompare(right, "en");
const sorted = (values) => [...values].sort(compareText);
const toPosix = (value) => value.replaceAll("\\", "/");

const sameArray = (left, right) => JSON.stringify(left) === JSON.stringify(right);

export const buildCoverageReport = (root) => {
  const catalogue = buildDetectionCatalogue(root);
  const dataSourcePath = path.join(root, "targets", "sentinel", "data-sources.json");
  const contract = readJson(dataSourcePath);
  if (contract.schema_version !== 1 || contract.target !== "microsoft-sentinel" || !Array.isArray(contract.sources)) {
    throw new Error("targets/sentinel/data-sources.json: unsupported contract header");
  }

  const detectionsById = new Map(catalogue.detections.map((detection) => [detection.id, detection]));
  const boundByTable = new Map();
  const boundDetectionIds = new Set();
  for (const detection of catalogue.detections) {
    const sentinelBindings = detection.target_bindings.filter(
      (binding) => binding.target === "microsoft-sentinel",
    );
    if (sentinelBindings.length > 1) {
      throw new Error(`${detection.id}: multiple Sentinel preview bindings are not supported`);
    }
    for (const binding of sentinelBindings) {
      const consumers = boundByTable.get(binding.table) ?? [];
      consumers.push(detection.id);
      boundByTable.set(binding.table, consumers);
      boundDetectionIds.add(detection.id);
    }
  }

  const seenSourceIds = new Set();
  const seenTables = new Set();
  const sentinelContracts = [];
  for (const source of contract.sources) {
    if (seenSourceIds.has(source.id)) throw new Error(`duplicate data-source contract ID ${source.id}`);
    if (seenTables.has(source.table)) throw new Error(`duplicate data-source contract table ${source.table}`);
    seenSourceIds.add(source.id);
    seenTables.add(source.table);

    const expectedConsumers = boundByTable.get(source.table);
    if (!expectedConsumers) {
      throw new Error(`${source.id}: table ${source.table} has no Sentinel preview binding`);
    }
    if (!sameArray(source.consumers, expectedConsumers)) {
      throw new Error(`${source.id}: consumers do not match Sentinel preview bindings`);
    }
    for (const detectionId of source.consumers) {
      if (!detectionsById.has(detectionId)) {
        throw new Error(`${source.id}: unknown detection ${detectionId}`);
      }
    }

    sentinelContracts.push({
      source_id: source.id,
      table: source.table,
      display_name: source.display_name,
      detections: [...source.consumers],
      event_time_column: source.event_time_column,
      required_columns: source.required_columns.map((column) => ({ ...column })),
      freshness: { ...source.freshness },
    });
  }
  for (const table of boundByTable.keys()) {
    if (!seenTables.has(table)) {
      throw new Error(`Sentinel preview table ${table} has no data-source contract`);
    }
  }

  const techniques = new Map();
  const tactics = new Map();
  let attackMappings = 0;
  for (const detection of catalogue.detections) {
    for (const mapping of detection.attack) {
      attackMappings += 1;
      const technique = techniques.get(mapping.technique_id) ?? {
        technique_id: mapping.technique_id,
        tactics: new Set(),
        detections: new Set(),
      };
      technique.tactics.add(mapping.tactic);
      technique.detections.add(detection.id);
      techniques.set(mapping.technique_id, technique);

      const tactic = tactics.get(mapping.tactic) ?? {
        tactic: mapping.tactic,
        techniques: new Set(),
        detections: new Set(),
      };
      tactic.techniques.add(mapping.technique_id);
      tactic.detections.add(detection.id);
      tactics.set(mapping.tactic, tactic);
    }
  }

  const logicalSources = new Map();
  for (const detection of catalogue.detections) {
    for (const source of detection.data_sources) {
      const key = `${source.name}\u0000${source.category}`;
      const record = logicalSources.get(key) ?? {
        name: source.name,
        category: source.category,
        detections: new Set(),
        required_fields: new Set(),
      };
      record.detections.add(detection.id);
      for (const field of source.required_fields) record.required_fields.add(field);
      logicalSources.set(key, record);
    }
  }

  const attackTechniqueRecords = sorted(techniques.keys()).map((techniqueId) => {
    const record = techniques.get(techniqueId);
    return {
      technique_id: record.technique_id,
      tactics: sorted(record.tactics),
      detections: sorted(record.detections),
    };
  });
  const attackTacticRecords = sorted(tactics.keys()).map((tacticName) => {
    const record = tactics.get(tacticName);
    return {
      tactic: record.tactic,
      techniques: sorted(record.techniques),
      detections: sorted(record.detections),
    };
  });
  const logicalSourceRecords = [...logicalSources.values()]
    .sort((left, right) => compareText(left.name, right.name) || compareText(left.category, right.category))
    .map((record) => ({
      name: record.name,
      category: record.category,
      detections: sorted(record.detections),
      required_fields: sorted(record.required_fields),
    }));
  const unboundDetections = catalogue.detections
    .filter((detection) => !boundDetectionIds.has(detection.id))
    .map((detection) => ({
      id: detection.id,
      title: detection.title,
      data_sources: detection.data_sources.map((source) => source.name),
    }));

  return {
    schema_version: 1,
    source: {
      manifests: "catalog/detections/*/manifest.json",
      sentinel_preview: "targets/sentinel/preview.json",
      sentinel_data_sources: toPosix(path.relative(root, dataSourcePath)),
    },
    summary: {
      detections: catalogue.summary.detections,
      attack_mappings: attackMappings,
      attack_techniques: attackTechniqueRecords.length,
      attack_tactics: attackTacticRecords.length,
      logical_data_sources: logicalSourceRecords.length,
      sentinel_preview_bindings: boundDetectionIds.size,
      sentinel_data_source_contracts: sentinelContracts.length,
      detections_without_sentinel_binding: unboundDetections.length,
    },
    attack: {
      techniques: attackTechniqueRecords,
      tactics: attackTacticRecords,
    },
    data_sources: {
      logical: logicalSourceRecords,
      sentinel_contracts: sentinelContracts,
      detections_without_sentinel_binding: unboundDetections,
    },
  };
};

export const renderCoverageJson = (report) => `${JSON.stringify(report, null, 2)}\n`;

const escapeTable = (value) => String(value).replaceAll("|", "\\|");
const codeList = (values) => values.length > 0
  ? values.map((value) => `\`${value}\``).join(", ")
  : "—";
const detectionLinks = (ids) => ids.map(
  (id) => `[\`${id}\`](catalog/detections/${id}/manifest.json)`,
).join(", ");

export const renderCoverageMarkdown = (report) => {
  const lines = [
    "<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:coverage`. -->",
    "",
    "# Detection coverage",
    "",
    "This report is generated deterministically from the public detection manifests, Sentinel preview and Sentinel data-source contract.",
    "It inventories declared repository coverage only. It is not a claim of complete MITRE ATT&CK coverage, live telemetry health or production readiness.",
    "",
    "## Summary",
    "",
    `- Detection packages: **${report.summary.detections}**`,
    `- Declared ATT&CK mappings: **${report.summary.attack_mappings}** across **${report.summary.attack_techniques} techniques / ${report.summary.attack_tactics} tactics**`,
    `- Declared logical data sources: **${report.summary.logical_data_sources}**`,
    `- Sentinel preview bindings: **${report.summary.sentinel_preview_bindings}**`,
    `- Sentinel data-source contracts: **${report.summary.sentinel_data_source_contracts}**`,
    `- Detections without a Sentinel preview binding: **${report.summary.detections_without_sentinel_binding}**`,
    "",
    "## ATT&CK techniques",
    "",
    "| Technique | Tactic | Detection records |",
    "| --- | --- | --- |",
  ];

  for (const technique of report.attack.techniques) {
    lines.push(`| \`${technique.technique_id}\` | ${escapeTable(technique.tactics.join(", "))} | ${detectionLinks(technique.detections)} |`);
  }

  lines.push(
    "",
    "## ATT&CK tactics",
    "",
    "| Tactic | Techniques | Detection records |",
    "| --- | --- | --- |",
  );
  for (const tactic of report.attack.tactics) {
    lines.push(`| ${escapeTable(tactic.tactic)} | ${codeList(tactic.techniques)} | ${detectionLinks(tactic.detections)} |`);
  }

  lines.push(
    "",
    "## Declared logical data sources",
    "",
    "| Data source | Category | Detection records | Required fields |",
    "| --- | --- | --- | --- |",
  );
  for (const source of report.data_sources.logical) {
    lines.push(`| ${escapeTable(source.name)} | ${escapeTable(source.category)} | ${detectionLinks(source.detections)} | ${codeList(source.required_fields)} |`);
  }

  lines.push(
    "",
    "## Sentinel data-source contracts",
    "",
    "| Contract | Table | Detection records | Required columns | Freshness expectation |",
    "| --- | --- | --- | ---: | --- |",
  );
  for (const source of report.data_sources.sentinel_contracts) {
    lines.push(`| \`${source.source_id}\` | \`${source.table}\` | ${detectionLinks(source.detections)} | ${source.required_columns.length} | degraded after \`${source.freshness.degraded_after}\`; unavailable after \`${source.freshness.unavailable_after}\` |`);
  }

  lines.push("", "## Detections without a Sentinel preview binding", "");
  if (report.data_sources.detections_without_sentinel_binding.length === 0) {
    lines.push("None.");
  } else {
    for (const detection of report.data_sources.detections_without_sentinel_binding) {
      lines.push(`- ${detectionLinks([detection.id])} — ${detection.title}; declared source: ${detection.data_sources.join(", ")}`);
    }
  }
  lines.push(
    "",
    "A missing Sentinel binding is an explicit target gap, not a failing detection and not proof that the source is absent from a consumer environment.",
  );

  return `${lines.join("\n").trimEnd()}\n`;
};
