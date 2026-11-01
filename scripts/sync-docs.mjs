#!/usr/bin/env node
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");

export const MODULES = ["frontend", "backend", "middleware"];

// "Boss order" files: every module branch gets a read-only copy.
export const SHARED_FILES = [
  "whole_plan.md",
  "docs/api-contract.md",
  "docs/decisions.md",
  "docs/checks.md",
  "docs/team-workflow.md",
  "docs/task-ownership.md",
];

const CONTEXT_DIR = "docs/context";

function notice(source) {
  return [
    "<!--",
    `  GENERATED FILE. Source: ${source}`,
    "  Do not edit this copy. Edit the root file, then run: npm run sync:docs",
    "-->",
    "",
  ].join("\n");
}

async function contextFiles() {
  const entries = await readdir(path.join(ROOT, CONTEXT_DIR));
  return entries
    .filter((name) => name.endsWith(".md"))
    .sort()
    .map((name) => `${CONTEXT_DIR}/${name}`);
}

export async function sharedFiles() {
  return [...SHARED_FILES, ...(await contextFiles())];
}

async function buildManifest() {
  const files = await sharedFiles();
  const manifest = [];
  for (const moduleName of MODULES) {
    for (const source of files) {
      manifest.push({
        source,
        dest: path.join(moduleName, source),
      });
    }
  }
  return manifest;
}

async function sync() {
  const manifest = await buildManifest();
  for (const entry of manifest) {
    const sourcePath = path.join(ROOT, entry.source);
    const destPath = path.join(ROOT, entry.dest);
    const body = await readFile(sourcePath, "utf8");
    await mkdir(path.dirname(destPath), { recursive: true });
    await writeFile(destPath, notice(entry.source) + body, "utf8");
    console.log(`synced ${entry.source} -> ${entry.dest}`);
  }
  console.log(`\n${manifest.length} module copies refreshed.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await sync();
}
