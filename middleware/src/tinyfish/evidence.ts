import { TinyFish } from "@tiny-fish/sdk";
import { config, requireEnv } from "../config.js";

/**
 * The 21 evidence categories defined for the prototype. TinyFish must return one
 * entry per field, or N/D when the source does not expose it. Values are never
 * invented by the UI or backend.
 */
export const EVIDENCE_FIELDS = [
  "ulpin",
  "cadastral_map",
  "satellite_imagery",
  "record_of_rights",
  "registration_deeds",
  "master_plan",
  "building_permissions",
  "completion_occupancy",
  "encumbrances",
  "mortgages_liens",
  "land_use_zoning",
  "utility_infrastructure",
  "property_tax_arrears",
  "valuation_circle_rate",
  "infrastructure_row",
  "environmental_buffers",
  "restriction_zones",
  "service_linkages",
  "litigation_stays",
  "change_detection",
  "workflow_tracking",
] as const;

export type EvidenceField = {
  value: string | null;
  status: "AVAILABLE" | "PARTIAL" | "N/A" | "N/D";
  source: string | null;
  retrieved_at: string | null;
};

export type EvidenceSheet = {
  ulpin: string;
  sourceUrl: string;
  status: string;
  tinyfish_run_id: string | null;
  fields: Record<string, EvidenceField>;
  sources: string[];
  rawResult: unknown;
};

export type EvidenceRequest = {
  ulpin: string;
  sourceUrl?: string;
  goal?: string;
};

function buildGoal(ulpin: string): string {
  return [
    `You are verifying land parcel ${ulpin} for a government land-market prototype.`,
    "Navigate the page, open the relevant parcel/search result if available, and collect evidence.",
    "Return JSON with exactly these keys:",
    `"ulpin" (string), "fields" (object), "sources" (array of URLs you actually used).`,
    "Inside fields return one entry for every one of these 21 categories:",
    EVIDENCE_FIELDS.join(", "),
    "Each field must be shaped as:",
    '{"value": string|null, "status": "AVAILABLE"|"PARTIAL"|"N/A"|"N/D", "source": string|null, "retrieved_at": ISO-8601 string|null}.',
    "Rules: never guess or fabricate values. If a category is missing use status N/D and value null.",
    "If the page blocks access, shows a CAPTCHA, or the parcel is not found, return the fields you could",
    "verify with statuses and add a top-level \"blocked\" boolean plus \"reason\" string.",
    "Do not submit forms that change ownership, payments, or government records.",
  ].join("\n");
}

function normalizeFields(result: unknown): Record<string, EvidenceField> {
  if (!result || typeof result !== "object") {
    return {};
  }
  const candidate = (result as { fields?: unknown }).fields;
  if (!candidate || typeof candidate !== "object") {
    return {};
  }
  return candidate as Record<string, EvidenceField>;
}

function normalizeSources(result: unknown): string[] {
  if (!result || typeof result !== "object") {
    return [];
  }
  const sources = (result as { sources?: unknown }).sources;
  if (!Array.isArray(sources)) {
    return [];
  }
  return sources.filter((entry): entry is string => typeof entry === "string");
}

/**
 * Runs a TinyFish Web Agent and returns the structured 21-field evidence sheet.
 * Only gathers evidence: trade decisions stay in the backend's fixed rules.
 */
export async function collectEvidence(
  request: EvidenceRequest,
): Promise<EvidenceSheet> {
  const apiKey = requireEnv("TINYFISH_API_KEY");
  process.env.TINYFISH_API_KEY = apiKey;

  const client = new TinyFish();
  const sourceUrl = request.sourceUrl ?? config.tinyfishUrl ?? config.defaultSourceUrl;
  const goal = request.goal ?? buildGoal(request.ulpin);

  const work = (async () => {
    const stream = await client.agent.stream({ url: sourceUrl, goal });

    let complete: { status?: string; result?: unknown; runId?: string } | null =
      null;

    for await (const rawEvent of stream) {
      const event = rawEvent as unknown as {
        type?: string;
        status?: string;
        result?: unknown;
        result_json?: unknown;
        run_id?: string;
      };
      if (event.type === "COMPLETE") {
        complete = {
          status: event.status ?? "COMPLETED",
          result: event.result ?? event.result_json,
          runId: event.run_id,
        };
      }
    }

    if (!complete) {
      throw new Error("TinyFish stream ended without a COMPLETE event.");
    }

    const result = complete.result;
    return {
      ulpin: request.ulpin,
      sourceUrl,
      status: complete.status ?? "COMPLETED",
      tinyfish_run_id: complete.runId ?? null,
      fields: normalizeFields(result),
      sources: normalizeSources(result),
      rawResult: result,
    } satisfies EvidenceSheet;
  })();

  let timer: NodeJS.Timeout | undefined;
  const timeout = new Promise<never>((_, reject) => {
    timer = setTimeout(
      () => reject(new Error(`TinyFish run timed out after ${config.tinyfishTimeoutMs}ms.`)),
      config.tinyfishTimeoutMs,
    );
  });

  try {
    return await Promise.race([work, timeout]);
  } finally {
    if (timer) {
      clearTimeout(timer);
    }
  }
}
