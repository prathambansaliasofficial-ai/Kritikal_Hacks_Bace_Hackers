import { useCallback, useEffect, useState, type FormEvent } from "react";
import { MapView } from "./components/MapView";
import { EvidencePanel } from "./components/EvidencePanel";
import { ReviewQueue } from "./components/ReviewQueue";
import {
  API_BASE_URL,
  fetchHealth,
  requestVerification,
  type HealthResponse,
} from "./lib/api";
import { isChainConfigured, chainWarning } from "./lib/chain";

type HealthState =
  | { phase: "loading" }
  | { phase: "ready"; data: HealthResponse }
  | { phase: "error"; message: string };

type VerifyState =
  | { phase: "idle" }
  | { phase: "loading" }
  | { phase: "done"; sheetId: number }
  | { phase: "error"; message: string };

const OFFICER_TOKEN = import.meta.env.VITE_OFFICER_TOKEN ?? "";

export default function App() {
  const [health, setHealth] = useState<HealthState>({ phase: "loading" });
  const [ulpin, setUlpin] = useState("");
  const [verify, setVerify] = useState<VerifyState>({ phase: "idle" });

  const loadHealth = useCallback(async () => {
    setHealth({ phase: "loading" });
    try {
      setHealth({ phase: "ready", data: await fetchHealth() });
    } catch (error) {
      setHealth({
        phase: "error",
        message: error instanceof Error ? error.message : "Unknown error",
      });
    }
  }, []);

  useEffect(() => {
    void loadHealth();
  }, [loadHealth]);

  async function handleVerify(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = ulpin.trim();
    if (!value) {
      return;
    }

    setVerify({ phase: "loading" });
    try {
      const sheet = await requestVerification(value);
      setVerify({ phase: "done", sheetId: sheet.id });
    } catch (error) {
      setVerify({
        phase: "error",
        message: error instanceof Error ? error.message : "Unknown error",
      });
    }
  }

  const dbStatus =
    health.phase === "ready" ? health.data.database.status : "unknown";

  return (
    <div className="shell">
      {!isChainConfigured && (
        <div className="warn-banner" role="status" aria-live="polite">
          {chainWarning}
        </div>
      )}
      <header className="topbar">
        <div>
          <p className="eyebrow">Kritical Hacks 2026 · Prototype</p>
          <h1>Land Market</h1>
        </div>
        <div className="status-row">
          <StatusPill label="API" value={health.phase} />
          <StatusPill label="PostGIS" value={dbStatus} />
        </div>
      </header>

      <main className="layout">
        <section className="panel map-panel">
          <div className="panel-heading">
            <h2>Pilot map</h2>
            <span className="muted">Kothrud, Pune</span>
          </div>
          <MapView />
        </section>

        <aside className="panel">
          <div className="panel-heading">
            <h2>Officer verification</h2>
            <span className="muted">TinyFish evidence</span>
          </div>

          <form className="form" onSubmit={handleVerify}>
            <label htmlFor="ulpin">ULPIN</label>
            <input
              id="ulpin"
              value={ulpin}
              onChange={(event) => setUlpin(event.target.value)}
              placeholder="Enter a demo ULPIN"
              autoComplete="off"
            />
            <button type="submit" disabled={verify.phase === "loading"}>
              {verify.phase === "loading" ? "Verifying…" : "Start verification"}
            </button>
          </form>

          <div className="output">
            {health.phase === "error" && (
              <p className="error">API unreachable: {health.message}</p>
            )}
            {verify.phase === "idle" && (
              <p className="muted">
                Submit a ULPIN to request the 21-field evidence sheet from the
                middleware.
              </p>
            )}
            {verify.phase === "error" && (
              <p className="error">{verify.message}</p>
            )}
            {verify.phase === "done" && (
              <div className="evidence-loaded">
                <p className="muted">
                  Evidence sheet #{verify.sheetId} loaded. Review it below.
                </p>
              </div>
            )}
          </div>

          {verify.phase === "done" && (
            <EvidencePanel ulpin={ulpin} />
          )}

          <footer className="footnote">
            Backend: <code>{API_BASE_URL}</code>
          </footer>
        </aside>

        {OFFICER_TOKEN && (
          <section className="panel review-panel-wrapper">
            <div className="panel-heading">
              <h2>Review Queue</h2>
              <span className="muted">Officer review</span>
            </div>
            <ReviewQueue officer={OFFICER_TOKEN} />
          </section>
        )}
      </main>
    </div>
  );
}

function StatusPill({ label, value }: { label: string; value: string }) {
  const tone = value === "ready" || value === "ok" ? "good" : value === "loading" ? "wait" : "bad";
  return (
    <span className={`pill ${tone}`}>
      <span className="dot" />
      {label}: {value}
    </span>
  );
}
