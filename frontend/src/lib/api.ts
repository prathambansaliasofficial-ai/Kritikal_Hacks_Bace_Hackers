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

export function requestVerification(ulpin: string): Promise<VerificationResponse> {
  return request<VerificationResponse>("/api/v1/verifications", {
    method: "POST",
    body: JSON.stringify({ ulpin }),
  });
}

export { API_BASE_URL };
