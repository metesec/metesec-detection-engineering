import fs from "node:fs";
import path from "node:path";

const toPosix = (value) => value.replaceAll("\\", "/");
const isInside = (parent, candidate) => {
  const relative = path.relative(parent, candidate);
  return relative !== "" && !relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative);
};
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const schemaErrors = (validate) => (validate.errors || [])
  .map((error) => `${error.instancePath || "/"} ${error.message}`)
  .join("; ");

export const validateDetectionPackages = ({ root, validateManifest, validateFixtureSet }) => {
  const errors = [];
  const packages = [];
  const catalogRoot = path.join(root, "catalog", "detections");

  if (!fs.existsSync(catalogRoot)) {
    return { errors: ["catalog/detections: catalogue directory is missing"], packages };
  }

  const directories = fs.readdirSync(catalogRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .sort((left, right) => left.name.localeCompare(right.name));

  if (directories.length === 0) {
    return { errors: ["catalog/detections: expected at least one detection package"], packages };
  }

  const seenIds = new Set();
  for (const directory of directories) {
    const packageLabel = `catalog/detections/${directory.name}`;
    const manifestPath = path.join(catalogRoot, directory.name, "manifest.json");
    if (!fs.existsSync(manifestPath)) {
      errors.push(`${packageLabel}: manifest.json is missing`);
      continue;
    }

    let manifest;
    try {
      manifest = readJson(manifestPath);
    } catch (error) {
      errors.push(`${packageLabel}/manifest.json: invalid JSON (${error.message})`);
      continue;
    }

    if (!validateManifest(manifest)) {
      errors.push(`${packageLabel}/manifest.json: ${schemaErrors(validateManifest)}`);
      continue;
    }
    if (manifest.id !== directory.name) {
      errors.push(`${packageLabel}: directory must match manifest id ${manifest.id}`);
    }
    if (seenIds.has(manifest.id)) {
      errors.push(`${packageLabel}: duplicate detection id ${manifest.id}`);
    }
    seenIds.add(manifest.id);

    for (const implementation of manifest.implementations) {
      const relativeImplementation = toPosix(implementation.path);
      const implementationLabel = `${packageLabel}: ${relativeImplementation}`;
      if (path.isAbsolute(implementation.path) || relativeImplementation.split("/").includes("..")) {
        errors.push(`${implementationLabel}: implementation path must stay repository-relative`);
        continue;
      }

      const requiredPrefix = implementation.type === "sigma"
        ? "content/portable/sigma/"
        : "content/native/";
      if (!relativeImplementation.startsWith(requiredPrefix)) {
        errors.push(`${implementationLabel}: ${implementation.type} implementation must use ${requiredPrefix}`);
      }
      if (!relativeImplementation.split("/").includes(manifest.id)) {
        errors.push(`${implementationLabel}: path must contain detection id ${manifest.id}`);
      }

      const absoluteImplementation = path.resolve(root, ...relativeImplementation.split("/"));
      if (!isInside(root, absoluteImplementation)) {
        errors.push(`${implementationLabel}: implementation resolves outside the repository`);
        continue;
      }
      if (!fs.existsSync(absoluteImplementation) || !fs.statSync(absoluteImplementation).isFile()) {
        errors.push(`${implementationLabel}: declared implementation file does not exist`);
        continue;
      }

      const testsRoot = path.join(path.dirname(absoluteImplementation), "tests");
      const casesPath = path.join(testsRoot, "cases.json");
      const claimsEvidence = manifest.validation.positive_tests || manifest.validation.negative_tests;
      if (!fs.existsSync(casesPath)) {
        if (claimsEvidence) {
          errors.push(`${implementationLabel}: validation claims require tests/cases.json`);
        }
        continue;
      }

      let fixtureSet;
      try {
        fixtureSet = readJson(casesPath);
      } catch (error) {
        errors.push(`${implementationLabel}: tests/cases.json is invalid JSON (${error.message})`);
        continue;
      }
      if (!validateFixtureSet(fixtureSet)) {
        errors.push(`${implementationLabel}: tests/cases.json ${schemaErrors(validateFixtureSet)}`);
        continue;
      }
      if (fixtureSet.detection_id !== manifest.id) {
        errors.push(`${implementationLabel}: fixture detection_id must be ${manifest.id}`);
      }
      if (toPosix(fixtureSet.implementation) !== relativeImplementation) {
        errors.push(`${implementationLabel}: fixture implementation must reference the declared path`);
      }

      const caseIds = new Set();
      let positiveCases = 0;
      let negativeCases = 0;
      for (const testCase of fixtureSet.cases) {
        if (caseIds.has(testCase.id)) {
          errors.push(`${implementationLabel}: duplicate fixture case id ${testCase.id}`);
        }
        caseIds.add(testCase.id);
        if (testCase.expectation === "match") positiveCases += 1;
        if (testCase.expectation === "no_match") negativeCases += 1;

        const fixturePath = path.resolve(testsRoot, ...toPosix(testCase.fixture).split("/"));
        const fixturesRoot = path.join(testsRoot, "fixtures");
        if (!isInside(fixturesRoot, fixturePath)) {
          errors.push(`${implementationLabel}: fixture ${testCase.fixture} must stay inside tests/fixtures`);
        } else if (!fs.existsSync(fixturePath) || !fs.statSync(fixturePath).isFile()) {
          errors.push(`${implementationLabel}: fixture ${testCase.fixture} does not exist`);
        }
      }

      if (manifest.validation.positive_tests && positiveCases === 0) {
        errors.push(`${implementationLabel}: positive_tests requires at least one match case`);
      }
      if (manifest.validation.negative_tests && negativeCases === 0) {
        errors.push(`${implementationLabel}: negative_tests requires at least one no_match case`);
      }
    }

    packages.push({ id: manifest.id, status: manifest.lifecycle.status, implementations: manifest.implementations.length });
  }

  return { errors, packages };
};
