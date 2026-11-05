const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"
).replace(/\/+$/, "");

export type DatabaseHealth = {
  status: string;
  postgis_version?: string | null;
  error?: string | null;
};

export type HealthResponse = {
  status: "ok" | "degraded" | string;
  service: string;
  environment: string;
  database: DatabaseHealth;
};

export type VerificationResponse = {
  ulpin: string;
  status: string;
  evidence: unknown;
};

/* ---- Parcel / ALU / Listing types (docs/api-contract.md §2) ---- */

export type AluLevel = "1km" | "100m" | "10m" | "1m" | "0.1m2";
export type ListingStatus = "DRAFT" | "LISTED" | "PAUSED" | "SOLD" | "CANCELLED";
export type GeometryStatus = "AVAILABLE" | "N/D";

export type BBox = [number, number, number, number];

export type GeoJSONGeometry = {
  type:
    | "Point"
    | "MultiPoint"
    | "LineString"
    | "MultiLineString"
    | "Polygon"
    | "MultiPolygon";
  coordinates: unknown;
};

export type FeatureProperties = Record<string, unknown> & { demo?: boolean };

export type GeoJSONFeature<P = FeatureProperties> = {
  type: "Feature";
  id: string | number;
  geometry: GeoJSONGeometry;
  properties: P;
};

export type FeatureCollection<P = FeatureProperties> = {
  type: "FeatureCollection";
  features: GeoJSONFeature<P>[];
};

export type ParcelProperties = {
  ulpin: string;
  geometry_status: GeometryStatus;
  attributes: { owner_name: string; district: string; zoning: string };
  demo: boolean;
};

export type ParcelFeature = GeoJSONFeature<ParcelProperties>;

export type AluProperties = {
  alu_id: string;
  parent_id: string | null;
  level: AluLevel;
  area_sqm: number;
  demo: boolean;
};

export type AluFeature = GeoJSONFeature<AluProperties>;

export type Listing = {
  id: number;
  bundle_id: number;
  ulpin: string;
  seller_wallet: string;
  price_wei: string;
  status: ListingStatus;
  created_at: string;
  demo: boolean;
};

/* ---- Order types (docs/api-contract.md §2.4, §3) ---- */

export type OrderState = "CREATED" | "FUNDED" | "SETTLED" | "REFUNDED" | "FAILED";
export type TradeDecision = "APPROVED" | "NEEDS_REVIEW" | "REJECTED";

export type CheckResult = {
  name: "LISTED" | "BUNDLE_INTACT" | "KYC_WALLET" | "ZONING_OK" | "FUNDS_IN_ESCROW" | "TRADE_MATCH";
  passed: boolean;
  reason: string;
  blocking: boolean;
};

export type Order = {
  id: number;
  listing_id: number;
  buyer_wallet: string;
  seller_wallet: string;
  amount_wei: string;
  state: OrderState;
  chain_order_id: string | null;
  tx_hash: string | null;
  evidence_hash: string | null;
  checks: CheckResult[];
  decision: TradeDecision | null;
  decided_at: string | null;
  created_at: string;
  updated_at: string;
};

export type CreateOrderRequest = {
  listing_id: number;
  buyer_wallet: string;
};

export type FundOrderRequest = {
  chain_order_id: string;
  tx_hash: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      body || `Request failed with status ${response.status}`,
    );
  }

  return (await response.json()) as T;
}

export function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function fetchParcel(ulpin: string): Promise<ParcelFeature> {
  return request<ParcelFeature>(`/api/v1/parcels/${encodeURIComponent(ulpin)}`);
}

export function fetchAlus(
  bbox: BBox,
  level: AluLevel,
): Promise<FeatureCollection<AluProperties>> {
  const bboxStr = bbox.join(",");
  return request<FeatureCollection<AluProperties>>(
    `/api/v1/alus?bbox=${encodeURIComponent(bboxStr)}&level=${encodeURIComponent(level)}`,
  );
}

export function fetchListings(
  status?: ListingStatus,
): Promise<{ items: Listing[] }> {
  const qs = status ? `?status=${encodeURIComponent(status)}` : "";
  return request<{ items: Listing[] }>(`/api/v1/listings${qs}`);
}

/* ---- Evidence / review types (docs/api-contract.md §2.3, §3) ---- */

export type EvidenceStatus = "AVAILABLE" | "PARTIAL" | "N/A" | "N/D";

export type EvidenceField = {
  value: string | null;
  status: EvidenceStatus;
  source: string | null;
  retrieved_at: string | null;
};

export type EvidenceSheet = {
  id: number;
  ulpin: string;
  status: "PENDING" | "CLEAN" | "NEEDS_REVIEW" | "REJECTED";
  evidence_hash: string;
  tinyfish_run_id: string;
  fields: Record<string, EvidenceField>;
  sources: string[];
  created_at: string;
};

export type ReviewItem = {
  evidence_id: number;
  ulpin: string;
  status: "PENDING" | "NEEDS_REVIEW";
  evidence_hash: string;
  created_at: string;
};

export type ReviewDecision = "APPROVE" | "REJECT";

export function requestVerification(
  ulpin: string,
  sourceUrl?: string,
  goal?: string,
): Promise<EvidenceSheet> {
  return request<EvidenceSheet>("/api/v1/verifications", {
    method: "POST",
    body: JSON.stringify({ ulpin, source_url: sourceUrl, goal }),
  });
}

export function fetchEvidence(id: number): Promise<EvidenceSheet> {
  return request<EvidenceSheet>(`/api/v1/evidence/${id}`);
}

export function fetchEvidenceByUlpin(
  ulpin: string,
): Promise<{ items: EvidenceSheet[] }> {
  return request<{ items: EvidenceSheet[] }>(
    `/api/v1/evidence?ulpin=${encodeURIComponent(ulpin)}`,
  );
}

export function fetchReviews(
  status: "PENDING" | "NEEDS_REVIEW" = "PENDING",
): Promise<{ items: ReviewItem[] }> {
  return request<{ items: ReviewItem[] }>(
    `/api/v1/reviews?status=${encodeURIComponent(status)}`,
  );
}

export function submitReviewDecision(
  evidenceId: number,
  decision: ReviewDecision,
  reason: string,
  officer: string,
): Promise<EvidenceSheet> {
  return request<EvidenceSheet>(`/api/v1/reviews/${evidenceId}/decision`, {
    method: "POST",
    headers: { "X-Officer-Token": officer },
    body: JSON.stringify({ decision, reason, officer }),
  });
}

/* ---- Order API (docs/api-contract.md §3) ---- */

export function createOrderApi(
  listingId: number,
  buyerWallet: string,
): Promise<Order> {
  return request<Order>("/api/v1/orders", {
    method: "POST",
    body: JSON.stringify({ listing_id: listingId, buyer_wallet: buyerWallet }),
  });
}

export function fundOrderApi(
  orderId: number,
  chainOrderId: string,
  txHash: string,
): Promise<Order> {
  return request<Order>(`/api/v1/orders/${orderId}/funded`, {
    method: "POST",
    body: JSON.stringify({ chain_order_id: chainOrderId, tx_hash: txHash }),
  });
}

export function evaluateOrderApi(orderId: number): Promise<Order> {
  return request<Order>(`/api/v1/orders/${orderId}/evaluate`, {
    method: "POST",
  });
}

export function fetchOrderApi(orderId: number): Promise<Order> {
  return request<Order>(`/api/v1/orders/${orderId}`);
}

export { API_BASE_URL };
