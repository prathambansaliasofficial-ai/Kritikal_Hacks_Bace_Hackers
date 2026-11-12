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
const LOGS = {
  frontend: "frontend/log-f.md",
  backend: "backend/log-b.md",
  middleware: "middleware/log-m.md",
};

function notice(source) {
  return [
    "<!--",
    `  GENERATED FILE. Source: ${source}`,
    "  Do not edit this copy. Edit the root file, then run: npm run sync:docs",
    "-->",
    "",
  ].join("\n");
}

// Parses "NEEDS FROM OTHER MODULE" lines from a module log.
// Line format:
//   - [.] needs: backend | what: GET /escrow/status/{orderId} | contract ref: §4 | requested by: session-F2
const NEEDS_RE = /^-\s*\[([^\]]*)\]\s*needs:\s*([^|]+)\s*\|\s*what:\s*([^|]+)\s*\|\s*contract ref:\s*([^|]+)\s*\|\s*requested by:\s*(.+)$/;

function parseNeeds(logText) {
  const needs = [];
  for (const line of logText.split("\n")) {
    const m = line.match(NEEDS_RE);
    if (!m) continue;
    needs.push({
      done: m[1].trim() === ".",
      target: m[2].trim(),
      what: m[3].trim(),
      contractRef: m[4].trim(),
      requestedBy: m[5].trim(),
    });
  }
  return needs;
}

function needsNotice() {
  return [
    "<!--",
    `  GENERATED FILE. Source: module logs (frontend/log-f.md, backend/log-b.md, middleware/log-m.md)`,
    "  Do not edit this copy. Edit the source logs, then run: npm run sync:docs",
    "-->",
    "",
  ].join("\n");
}

async function syncCrossModuleNeeds() {
  // Collect needs per module log (raised by) and per target module.
  const raisedBy = {}; // module -> needs[] found in its log
  const targetedAt = {}; // target module -> needs[] directed at it
  for (const moduleName of MODULES) {
    raisedBy[moduleName] = [];
    targetedAt[moduleName] = [];
  }
  for (const moduleName of MODULES) {
    const logPath = path.join(ROOT, LOGS[moduleName]);
    let text;
    try {
      text = await readFile(logPath, "utf8");
    } catch {
      continue;
    }
    const sectionStart = text.indexOf("## NEEDS FROM OTHER MODULE");
    const sectionText =
      sectionStart === -1 ? "" : text.slice(sectionStart);
    const needs = parseNeeds(sectionText);
    raisedBy[moduleName] = needs;
    for (const n of needs) {
      if (targetedAt[n.target] !== undefined) {
        targetedAt[n.target].push({ ...n, raisedBy: moduleName });
      }
    }
  }

  for (const moduleName of MODULES) {
    const targeted = targetedAt[moduleName];
    const raised = raisedBy[moduleName];
    const lines = [];
    lines.push("## Cross-module needs for " + moduleName);
    lines.push("");
    lines.push("Items TARGETED at this module (other modules need this from " + moduleName + "):");
    if (targeted.length === 0) lines.push("(none)");
    for (const n of targeted) {
      const status = n.done ? "[.]" : "[]";
      lines.push(
        `- ${status} needs: ${n.target} | what: ${n.what} | contract ref: ${n.contractRef} | requested by: ${n.raisedBy}`
      );
    }
    lines.push("");
    lines.push("Items RAISED by this module (needs this module placed on others):");
    if (raised.length === 0) lines.push("(none)");
    for (const n of raised) {
      const status = n.done ? "[.]" : "[]";
      lines.push(
        `- ${status} needs: ${n.target} | what: ${n.what} | contract ref: ${n.contractRef} | requested by: ${moduleName}`
      );
    }
    lines.push("");
    const body = lines.join("\n") + "\n";
    const destPath = path.join(ROOT, moduleName, "docs", "cross-module-needs.md");
    await mkdir(path.dirname(destPath), { recursive: true });
    await writeFile(destPath, needsNotice() + body, "utf8");
    console.log(`synced cross-module needs -> ${moduleName}/docs/cross-module-needs.md`);
  }
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
  await syncCrossModuleNeeds();
  console.log(`\n${manifest.length} module copies refreshed.`);
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

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await sync();
}
