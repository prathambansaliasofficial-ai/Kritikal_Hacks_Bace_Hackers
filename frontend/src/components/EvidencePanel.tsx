import { useCallback, useEffect, useRef, useState } from "react";
import {
  fetchEvidenceByUlpin,
  type EvidenceField,
  type EvidenceSheet,
  type EvidenceStatus,
} from "../lib/api";

const EVIDENCE_STATUS_CHIPS: Record<EvidenceStatus, string> = {
  AVAILABLE: "chip good",
  PARTIAL: "chip wait",
  "N/A": "chip muted",
  "N/D": "chip bad",
};

const EVIDENCE_FIELDS: string[] = [
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
];

export type EvidencePanelProps = {
  ulpin: string;
  onEvidenceLoaded?: (sheet: EvidenceSheet) => void;
};

export function EvidencePanel({ ulpin, onEvidenceLoaded }: EvidencePanelProps) {
  const [sheet, setSheet] = useState<EvidenceSheet | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const copiedRef = useRef<HTMLButtonElement | null>(null);

  const loadEvidence = useCallback(async () => {
    if (!ulpin.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchEvidenceByUlpin(ulpin.trim());
      const s = data.items[0] ?? null;
      setSheet(s);
      if (s) onEvidenceLoaded?.(s);
      if (!s) setError("No evidence found for this ULPIN.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load evidence. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  }, [ulpin, onEvidenceLoaded]);

  useEffect(() => {
    void loadEvidence();
  }, [loadEvidence]);

  function copyHash() {
    if (!sheet?.evidence_hash) return;
    navigator.clipboard.writeText(sheet.evidence_hash);
    const el = copiedRef.current;
    if (el) {
      const prev = el.textContent;
      el.textContent = "Copied!";
      setTimeout(() => {
        el.textContent = prev;
      }, 1200);
    }
  }

  function fieldValue(f: EvidenceField | undefined): string {
    if (!f) return "—";
    if (f.value === null || f.value === "") return "—";
    return String(f.value);
  }

  if (loading) {
    return (
      <div className="panel evidence-loading">
        <p className="muted">Loading evidence…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel evidence-error">
        <p className="error">Evidence error: {error}</p>
        <p className="muted">
          Causes: middleware down, missing API key, or no evidence sheet for this
          ULPIN.
        </p>
      </div>
    );
  }

  if (!sheet) {
    return (
      <div className="panel evidence-empty">
        <p className="muted">Submit a ULPIN to request the 21-field evidence sheet.</p>
      </div>
    );
  }

  return (
    <div className="panel evidence-panel">
      <div className="evidence-header">
        <h3>Evidence Sheet</h3>
        <div className="evidence-meta">
          <span className="meta-item">
            <strong>Hash:</strong>
            <span className="hash">{sheet.evidence_hash}</span>
            <button
              className="copy-btn"
              onClick={copyHash}
              ref={copiedRef}
              title="Copy evidence hash"
            >
              Copy
            </button>
          </span>
          <span className="meta-item">
            <strong>Run ID:</strong> {sheet.tinyfish_run_id}
          </span>
          <span className="meta-item">
            <strong>Status:</strong>
            <span className={`chip ${sheet.status}`}>{sheet.status}</span>
          </span>
        </div>
      </div>

      {sheet.sources.length > 0 && (
        <div className="evidence-sources">
          <h4>Sources</h4>
          <ul>
            {sheet.sources.map((src, i) => (
              <li key={i}>
                <a href={src} target="_blank" rel="noopener noreferrer">
                  {src}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <table className="evidence-table">
        <thead>
          <tr>
            <th>Field</th>
            <th>Value</th>
            <th>Status</th>
            <th>Source</th>
            <th>Retrieved</th>
          </tr>
        </thead>
        <tbody>
          {EVIDENCE_FIELDS.map((key) => {
            const f = sheet.fields[key];
            return (
              <tr key={key}>
                <td className="field-name">{key}</td>
                <td className="field-value">{fieldValue(f)}</td>
                <td>
                  <span className={EVIDENCE_STATUS_CHIPS[f?.status ?? "N/D"]}>
                    {f?.status ?? "N/D"}
                  </span>
                </td>
                <td>
                  {f?.source ? (
                    <a
                      href={f.source}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="source-link"
                    >
                      view
                    </a>
                  ) : (
                    <span className="muted">—</span>
                  )}
                </td>
                <td>{f?.retrieved_at ?? "—"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
