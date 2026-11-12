#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");

const MODULES = ["frontend", "backend", "middleware"];
const REVIEW_FILES = {
  frontend: "frontend/review-f.md",
  backend: "backend/review-b.md",
  middleware: "middleware/review-m.md",
};
const LOGS = {
  frontend: "frontend/log-f.md",
  backend: "backend/log-b.md",
  middleware: "middleware/log-m.md",
};

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

const failures = [];
const warnings = [];

function fail(msg) {
  failures.push(msg);
  console.error(`FAIL: ${msg}`);
}

function warn(msg) {
  warnings.push(msg);
  console.error(`WARN: ${msg}`);
}

function stripCodeBlocks(text) {
  return text.replace(/```[\s\S]*?```/g, "");
}

async function read(p) {
  return readFile(path.join(ROOT, p), "utf8").catch(() => null);
}

// 1. Existing copy-sync check
const manifest = await loadManifest();
const stale = [];
for (const entry of manifest) {
  const rootBody = await read(entry.source);
  if (rootBody === null) {
    stale.push(`${entry.source} (root source is missing)`);
    continue;
  }
  const expected = notice(entry.source) + rootBody;
  const actual = await read(entry.dest);
  if (actual !== expected) {
    stale.push(entry.dest);
  }
}
if (stale.length > 0) {
  fail("Module copies are missing or stale. Run: npm run sync:docs");
  for (const file of stale) {
    fail(`  - ${file}`);
  }
}

// 2. Each module log must have a "NEEDS FROM OTHER MODULE" section
for (const moduleName of MODULES) {
  const logText = await read(LOGS[moduleName]);
  if (logText === null) {
    fail(`${LOGS[moduleName]} is missing`);
    continue;
  }
  if (!/^## NEEDS FROM OTHER MODULE$/m.test(logText)) {
    fail(`${LOGS[moduleName]} is missing the "## NEEDS FROM OTHER MODULE" section`);
  }
}

// 3-7. Review file checks
for (const moduleName of MODULES) {
  const reviewPath = REVIEW_FILES[moduleName];
  const reviewText = await read(reviewPath);
  if (reviewText === null) {
    fail(`${reviewPath} is missing`);
    continue;
  }

  // Template header present
  if (!/Last reviewed commit:/m.test(reviewText)) {
    fail(`${reviewPath} is missing the "Last reviewed commit:" pointer`);
  }
  if (!/^## Format spec$/m.test(reviewText)) {
    fail(`${reviewPath} is missing the "## Format spec" template header`);
  }

  // Split into entries on "## R-<n>"
  const clean = stripCodeBlocks(reviewText);
  const parts = clean.split(/\n(?=## R-)/);
  const entries = parts.slice(1); // first part is header
  if (entries.length === 0) {
    // No entries is fine (empty starting state), but header must exist (checked above).
  }

  for (const entry of entries) {
    // First line is the R-<n> title
    // Check Checked: line
    if (!/^Checked:/m.test(entry)) {
      fail(`${reviewPath}: entry "${entry.trim().split("\n")[0]}" is missing a "Checked:" line`);
    }
    // Check severity tag
    if (!/^-\s*\[(BLOCKER|MAJOR|NIT)\]\s/m.test(entry)) {
      fail(`${reviewPath}: entry "${entry.trim().split("\n")[0]}" is missing a severity tag [BLOCKER|MAJOR|NIT]`);
    }
    // Check Verdict and Status
    if (!/^Verdict:/m.test(entry)) {
      fail(`${reviewPath}: entry "${entry.trim().split("\n")[0]}" is missing a "Verdict:" line`);
    }
    if (!/^Status:/m.test(entry)) {
      fail(`${reviewPath}: entry "${entry.trim().split("\n")[0]}" is missing a "Status:" line`);
    }
    // Warn: open BLOCKER
    const hasBlocker = /^-\s*\[BLOCKER\]\s/m.test(entry);
    const statusMatch = entry.match(/^Status:\s*(\S+)/m);
    if (hasBlocker && statusMatch && statusMatch[1] === "OPEN") {
      warn(`${reviewPath}: entry "${entry.trim().split("\n")[0]}" has an open [BLOCKER]; no new task may start until resolved`);
    }
  }
}

if (failures.length > 0) {
  console.error(`\n${failures.length} check failure(s).`);
  process.exit(1);
}

if (warnings.length > 0) {
  console.error(`\n${warnings.length} warning(s).`);
}

console.log(`All ${manifest.length} module copies are in sync.`);
