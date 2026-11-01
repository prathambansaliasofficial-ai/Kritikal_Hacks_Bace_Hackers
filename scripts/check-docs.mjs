#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");

async function loadManifest() {
  const mod = await import("./sync-docs.mjs");
  const files = await mod.sharedFiles();
  const manifest = [];
  for (const moduleName of mod.MODULES) {
    for (const source of files) {
      manifest.push({ source, dest: path.join(moduleName, source) });
    }
  }
  return manifest;
}

function notice(source) {
  return [
    "<!--",
    `  GENERATED FILE. Source: ${source}`,
    "  Do not edit this copy. Edit the root file, then run: npm run sync:docs",
    "-->",
    "",
  ].join("\n");
}

const manifest = await loadManifest();
const stale = [];

for (const entry of manifest) {
  const rootBody = await readFile(path.join(ROOT, entry.source), "utf8").catch(() => null);
  if (rootBody === null) {
    stale.push(`${entry.source} (root source is missing)`);
    continue;
  }

  const expected = notice(entry.source) + rootBody;
  const actual = await readFile(path.join(ROOT, entry.dest), "utf8").catch(() => null);
  if (actual !== expected) {
    stale.push(entry.dest);
  }
}

if (stale.length > 0) {
  console.error("Module copies are missing or stale. Run: npm run sync:docs");
  for (const file of stale) {
    console.error(`  - ${file}`);
  }
  process.exit(1);
}

console.log(`All ${manifest.length} module copies are in sync.`);
