import fs from "node:fs";
import path from "node:path";

const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const toPosix = (value) => value.replaceAll("\\", "/");
const compareText = (left, right) => left.localeCompare(right, "en");

const fixtureEvidenceFor = (root, detectionId, implementations) => {
  let positiveCases = 0;
  let negativeCases = 0;

  for (const implementation of implementations) {
    const implementationPath = path.resolve(root, ...toPosix(implementation.path).split("/"));
    const casesPath = path.join(path.dirname(implementationPath), "tests", "cases.json");
    if (!fs.existsSync(casesPath)) continue;

    const fixtureSet = readJson(casesPath);
    if (fixtureSet.detection_id !== detectionId) {
      throw new Error(`${toPosix(path.relative(root, casesPath))}: detection_id must be ${detectionId}`);
    }
    if (toPosix(fixtureSet.implementation) !== toPosix(implementation.path)) {
      throw new Error(`${toPosix(path.relative(root, casesPath))}: implementation does not match the manifest`);
    }

    for (const testCase of fixtureSet.cases) {
      if (testCase.expectation === "match") positiveCases += 1;
      if (testCase.expectation === "no_match") negativeCases += 1;
    }
  }

  return { positive_cases: positiveCases, negative_cases: negativeCases };
};

const sentinelBindings = (root) => {
  const profilePath = path.join(root, "targets", "sentinel", "preview.json");
  if (!fs.existsSync(profilePath)) return new Map();

  const profile = readJson(profilePath);
  const bindings = new Map();
  for (const entry of profile.detections) {
    if (bindings.has(entry.id)) {
      throw new Error(`${toPosix(path.relative(root, profilePath))}: duplicate target binding for ${entry.id}`);
    }
    bindings.set(entry.id, [{
      target: profile.target,
      table: entry.query_table,
      golden: toPosix(entry.golden)
    }]);
  }
  return bindings;
};

export const buildDetectionCatalogue = (root) => {
  const catalogRoot = path.join(root, "catalog", "detections");
  const directories = fs.readdirSync(catalogRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .sort((left, right) => compareText(left.name, right.name));
  const bindings = sentinelBindings(root);
  const detections = [];
  const seenIds = new Set();

  for (const directory of directories) {
    const manifestRelative = `catalog/detections/${directory.name}/manifest.json`;
    const manifest = readJson(path.join(root, ...manifestRelative.split("/")));
    if (manifest.id !== directory.name) {
      throw new Error(`${manifestRelative}: manifest id must match its directory`);
    }
    if (seenIds.has(manifest.id)) {
      throw new Error(`${manifestRelative}: duplicate detection id ${manifest.id}`);
    }
    seenIds.add(manifest.id);

    const validation = fixtureEvidenceFor(root, manifest.id, manifest.implementations);
    detections.push({
      id: manifest.id,
      title: manifest.title,
      description: manifest.description,
      lifecycle: {
        status: manifest.lifecycle.status,
        created: manifest.lifecycle.created,
        modified: manifest.lifecycle.modified,
        review_interval_days: manifest.lifecycle.review_interval_days
      },
      severity: manifest.severity,
      confidence: manifest.confidence,
      attack: manifest.attack,
      data_sources: manifest.data_sources,
      validation,
      implementations: manifest.implementations,
      target_bindings: bindings.get(manifest.id) || [],
      manifest: manifestRelative
    });
  }

  for (const detectionId of bindings.keys()) {
    if (!seenIds.has(detectionId)) {
      throw new Error(`targets/sentinel/preview.json: binding references unknown detection ${detectionId}`);
    }
  }

  const summary = detections.reduce((totals, detection) => ({
    detections: totals.detections + 1,
    implementations: totals.implementations + detection.implementations.length,
    positive_cases: totals.positive_cases + detection.validation.positive_cases,
    negative_cases: totals.negative_cases + detection.validation.negative_cases,
    sentinel_preview_bindings: totals.sentinel_preview_bindings
      + detection.target_bindings.filter((binding) => binding.target === "microsoft-sentinel").length
  }), {
    detections: 0,
    implementations: 0,
    positive_cases: 0,
    negative_cases: 0,
    sentinel_preview_bindings: 0
  });

  return {
    schema_version: 1,
    source: "catalog/detections/*/manifest.json",
    summary,
    detections
  };
};

export const renderCatalogueJson = (catalogue) => `${JSON.stringify(catalogue, null, 2)}\n`;

const escapeTable = (value) => String(value).replaceAll("|", "\\|");
const codeList = (values) => values.length > 0
  ? values.map((value) => `\`${value}\``).join(", ")
  : "—";
const link = (label, target) => `[${label}](${toPosix(target)})`;

export const renderCatalogueMarkdown = (catalogue) => {
  const lines = [
    "<!-- GENERATED FILE. DO NOT EDIT. Run `pnpm run build:catalogue`. -->",
    "",
    "# Detection catalogue",
    "",
    "This index is generated deterministically from the versioned detection manifests, implementation-local fixture indexes, and explicit Sentinel preview profile.",
    "",
    "## Summary",
    "",
    `- Detection packages: **${catalogue.summary.detections}**`,
    `- Implementations: **${catalogue.summary.implementations}**`,
    `- Synthetic evidence: **${catalogue.summary.positive_cases} positive / ${catalogue.summary.negative_cases} negative cases**`,
    `- Sentinel preview bindings: **${catalogue.summary.sentinel_preview_bindings}**`,
    "",
    "## Coverage",
    "",
    "| ID | Detection | Status | Severity | ATT&CK | Data source | Synthetic evidence | Sentinel preview |",
    "| --- | --- | --- | --- | --- | --- | --- | --- |"
  ];

  for (const detection of catalogue.detections) {
    const attack = detection.attack.map((mapping) => mapping.technique_id);
    const dataSources = detection.data_sources.map((source) => source.name);
    const sentinel = detection.target_bindings.map((binding) => binding.table);
    lines.push(`| ${link(`\`${detection.id}\``, detection.manifest)} | ${escapeTable(detection.title)} | ${detection.lifecycle.status} | ${detection.severity} | ${codeList(attack)} | ${escapeTable(dataSources.join(", "))} | ${detection.validation.positive_cases} positive / ${detection.validation.negative_cases} negative | ${codeList(sentinel)} |`);
  }

  lines.push("", "## Records", "");
  for (const detection of catalogue.detections) {
    lines.push(
      `### ${detection.id} — ${detection.title}`,
      "",
      detection.description,
      "",
      `- Lifecycle: \`${detection.lifecycle.status}\`; created ${detection.lifecycle.created}; review every ${detection.lifecycle.review_interval_days} days`,
      `- Severity / confidence: \`${detection.severity}\` / \`${detection.confidence}\``,
      `- ATT&CK: ${detection.attack.length > 0 ? detection.attack.map((mapping) => `\`${mapping.technique_id}\` (${mapping.tactic})`).join(", ") : "—"}`,
      `- Data sources: ${detection.data_sources.map((source) => `${source.name} (${source.category})`).join(", ")}`,
      `- Synthetic evidence: ${detection.validation.positive_cases} positive and ${detection.validation.negative_cases} negative cases`,
      "- Implementations:"
    );
    for (const implementation of detection.implementations) {
      lines.push(`  - ${link(implementation.path, implementation.path)} — \`${implementation.status}\`; targets ${codeList(implementation.targets)}`);
    }
    if (detection.target_bindings.length === 0) {
      lines.push("- Sentinel preview: not bound");
    } else {
      lines.push("- Sentinel preview:");
      for (const binding of detection.target_bindings) {
        lines.push(`  - Table \`${binding.table}\`; ${link("reviewed Golden query", binding.golden)}`);
      }
    }
    lines.push(`- Source: ${link(detection.manifest, detection.manifest)}`, "");
  }

  return `${lines.join("\n").trimEnd()}\n`;
};
