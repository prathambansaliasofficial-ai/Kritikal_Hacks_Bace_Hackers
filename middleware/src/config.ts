import "dotenv/config";

export const config = {
  port: Number(process.env.PORT ?? 8090),
  host: process.env.HOST ?? "127.0.0.1",
  tinyfishUrl: process.env.TINYFISH_URL ?? "",
  defaultSourceUrl:
    process.env.DEFAULT_SOURCE_URL ?? "https://bhunaksha.nic.in/bhunaksha/",
  tinyfishTimeoutMs: Number(process.env.TINYFISH_TIMEOUT_MS ?? 290_000),
};

export function requireEnv(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`${name} is not set. Add it to middleware/.env.`);
  }
  return value;
}

export function isConfigured(name: string): boolean {
  return Boolean(process.env[name]?.trim());
}
