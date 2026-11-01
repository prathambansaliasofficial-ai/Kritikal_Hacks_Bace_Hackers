import { collectEvidence } from "../src/tinyfish/evidence.js";

// Proves the TinyFish integration end-to-end before wiring government portals.
// Usage: npm run smoke:tinyfish -- [url]
const url = process.argv[2] ?? "https://scrapeme.live/shop";

const sheet = await collectEvidence({
  ulpin: "SMOKE-TEST-001",
  sourceUrl: url,
  goal: [
    "Extract the first 2 product names and prices from this page.",
    'Return JSON: {"ulpin":"SMOKE-TEST-001","fields":{"ulpin":{"value":"SMOKE-TEST-001","status":"AVAILABLE","source":"<page url>","retrieved_at":"<ISO time>"},"land_use_zoning":{"value":<first product name>,"status":"PARTIAL","source":"<page url>","retrieved_at":"<ISO time>"}},"sources":["<page url>"]}',
  ].join("\n"),
});

console.log(JSON.stringify(sheet, null, 2));
