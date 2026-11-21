#!/usr/bin/env node
// Checks the three .env files for a given mode. Never prints secret values.
// Usage: npm run check:env            (local Hardhat chain)
//        npm run check:env -- sepolia (Sepolia testnet)
//        npm run check:env -- demo    (simulated demo payment, no chain)
import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.CHECK_ENV_ROOT ?? path.resolve(HERE, "..");
const mode = (process.argv[2] ?? "local").toLowerCase();
if (!["local", "sepolia", "demo"].includes(mode)) {
  console.error(`Unknown mode "${mode}". Use: local | sepolia | demo`);
  process.exit(2);
}

function parseEnv(file) {
  const full = path.join(ROOT, file);
  if (!existsSync(full)) return null;
  const out = {};
  for (const raw of readFileSync(full, "utf8").split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const i = line.indexOf("=");
    if (i < 1) continue;
    let v = line.slice(i + 1).trim();
    if (/^(["']).*\1$/.test(v)) v = v.slice(1, -1);
    out[line.slice(0, i).trim()] = v;
  }
  return out;
}

const be = parseEnv("backend/.env");
const mw = parseEnv("middleware/.env");
const fe = parseEnv("frontend/.env");

let fails = 0;
let warns = 0;
const pass = (m) => console.log(`PASS  ${m}`);
const warn = (m) => { warns++; console.log(`WARN  ${m}`); };
const fail = (m) => { fails++; console.log(`FAIL  ${m}`); };

const isAddr = (v) => /^0x[0-9a-fA-F]{40}$/.test(v ?? "");
const isKey = (v) => /^0x[0-9a-fA-F]{64}$/.test(v ?? "");
const HARDHAT_ACCOUNT_0 =
  "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";

for (const [name, env, file] of [
  ["backend", be, "backend/.env"],
  ["middleware", mw, "middleware/.env"],
  ["frontend", fe, "frontend/.env"],
]) {
  if (env) pass(`${file} exists`);
  else fail(`${file} is missing. Create it: cp ${file}.example ${file}`);
}
if (!be || !mw || !fe) {
  console.log(`\n${fails} FAIL, ${warns} WARN. See docs/api-keys-setup.md`);
  process.exit(1);
}

// TinyFish
if (mw.TINYFISH_API_KEY) {
  pass("TINYFISH_API_KEY is set");
  if (!mw.TINYFISH_API_KEY.startsWith("sk-tinyfish-"))
    warn("TINYFISH_API_KEY does not start with the usual prefix. Check you copied the whole key.");
  if (/\s/.test(mw.TINYFISH_API_KEY)) fail("TINYFISH_API_KEY contains whitespace");
} else {
  warn("TINYFISH_API_KEY is empty: live evidence disabled, trades cannot reach APPROVED. See docs/keys-tinyfish.md");
}

// Officer token
if (!be.DEV_OFFICER_TOKEN) fail("backend DEV_OFFICER_TOKEN is empty (officer actions need it)");
else {
  pass("backend DEV_OFFICER_TOKEN is set");
  if (be.DEV_OFFICER_TOKEN === "dev-officer-token")
    warn("DEV_OFFICER_TOKEN is still the example value. Change it before sharing any URL.");
}
if (fe.VITE_OFFICER_TOKEN) {
  if (fe.VITE_OFFICER_TOKEN === be.DEV_OFFICER_TOKEN) pass("VITE_OFFICER_TOKEN matches DEV_OFFICER_TOKEN");
  else fail("VITE_OFFICER_TOKEN differs from DEV_OFFICER_TOKEN, review screen calls will get 401");
  warn("VITE_OFFICER_TOKEN is set: it is public in the built frontend. Leave it empty on any public deployment.");
}

if (mode === "demo") {
  (mw.DEMO_PAYMENT === "true" ? pass : fail)("middleware DEMO_PAYMENT=true");
  (fe.VITE_DEMO_PAYMENT === "true" ? pass : fail)("frontend VITE_DEMO_PAYMENT=true");
  if (isAddr(fe.VITE_DEMO_BUYER_WALLET)) pass("VITE_DEMO_BUYER_WALLET looks valid");
  else fail("VITE_DEMO_BUYER_WALLET must be a 0x address of a KYC-VERIFIED buyer");
} else {
// Chain
const wantChain = mode === "sepolia" ? "11155111" : "31337";
(mw.CHAIN_ID === wantChain ? pass : fail)(`middleware CHAIN_ID is ${wantChain}`);
(fe.VITE_CHAIN_ID === wantChain || (!fe.VITE_CHAIN_ID && wantChain === "31337") ? pass : fail)(
  `frontend VITE_CHAIN_ID matches ${wantChain}`,
);

if (isAddr(mw.ESCROW_CONTRACT_ADDRESS)) pass("middleware ESCROW_CONTRACT_ADDRESS looks valid");
else fail("middleware ESCROW_CONTRACT_ADDRESS is empty or not a 0x address (deploy first)");
if (isAddr(fe.VITE_ESCROW_ADDRESS)) {
  if (fe.VITE_ESCROW_ADDRESS.toLowerCase() === (mw.ESCROW_CONTRACT_ADDRESS ?? "").toLowerCase())
    pass("VITE_ESCROW_ADDRESS matches the middleware address");
  else fail("VITE_ESCROW_ADDRESS differs from ESCROW_CONTRACT_ADDRESS");
} else fail("frontend VITE_ESCROW_ADDRESS is empty or not a 0x address");

(isKey(mw.OPERATOR_PRIVATE_KEY) ? pass : fail)("OPERATOR_PRIVATE_KEY is a 0x + 64 hex key");

if (mode === "sepolia") {
  if (/^https:\/\//.test(mw.SEPOLIA_RPC_URL ?? "")) pass("SEPOLIA_RPC_URL is an https URL");
  else fail("SEPOLIA_RPC_URL is empty or not https (see docs/keys-sepolia.md Step 2)");
  if ((mw.CHAIN_RPC_URL ?? "") === (mw.SEPOLIA_RPC_URL ?? "x")) pass("CHAIN_RPC_URL equals SEPOLIA_RPC_URL");
  else fail("CHAIN_RPC_URL must equal SEPOLIA_RPC_URL, or settlement will talk to the wrong chain");
  (isKey(mw.DEPLOYER_PRIVATE_KEY) ? pass : fail)("DEPLOYER_PRIVATE_KEY is a 0x + 64 hex key");
  if (isKey(mw.DEPLOYER_PRIVATE_KEY) && isKey(mw.OPERATOR_PRIVATE_KEY)) {
    if (mw.DEPLOYER_PRIVATE_KEY.toLowerCase() === mw.OPERATOR_PRIVATE_KEY.toLowerCase())
      pass("OPERATOR_PRIVATE_KEY equals DEPLOYER_PRIVATE_KEY");
    else fail("OPERATOR_PRIVATE_KEY must equal DEPLOYER_PRIVATE_KEY (the deployer is the contract operator)");
  }
  if ((mw.OPERATOR_PRIVATE_KEY ?? "").toLowerCase() === HARDHAT_ACCOUNT_0)
    fail("OPERATOR_PRIVATE_KEY is the public Hardhat test key. Use a fresh Sepolia wallet.");
  if (fe.VITE_EXPLORER_URL) pass("VITE_EXPLORER_URL is set");
  else warn("VITE_EXPLORER_URL is empty: no explorer links in the UI (use https://sepolia.etherscan.io)");
  if (!(be.CORS_ORIGINS ?? "").trim()) warn("backend CORS_ORIGINS is empty");
}

}

console.log(`\n${fails} FAIL, ${warns} WARN. Values are never printed. Guide: docs/api-keys-setup.md`);
process.exit(fails > 0 ? 1 : 0);
