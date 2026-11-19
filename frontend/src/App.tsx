import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import { MapView } from "./components/MapView";
import { EvidencePanel } from "./components/EvidencePanel";
import { ReviewQueue } from "./components/ReviewQueue";
import { ListingCard } from "./components/ListingCard";
import { TradeStatus } from "./components/TradeStatus";
import {
  API_BASE_URL,
  fetchHealth,
  fetchListings,
  createOrderApi,
  fundOrderApi,
  evaluateOrderApi,
  fetchOrderApi,
  requestVerification,
  type HealthResponse,
  type Listing,
  type Order,
} from "./lib/api";
import { isChainConfigured, chainWarning, chainConfig } from "./lib/chain";
import {
  connectWallet,
  switchToConfiguredChain,
  onAccountsChanged,
  shortenAddress,
  type WalletState,
} from "./lib/wallet";
import { chainOrderId, createOrder } from "./lib/web3";

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
const DEMO_BANNER = "Testnet only, not a legal title transfer.";

type BuyStatus = "idle" | "creating" | "funding" | "evaluating" | "polling" | "settled" | "failed";

export default function App() {
  const [health, setHealth] = useState<HealthState>({ phase: "loading" });
  const [ulpin, setUlpin] = useState("");
  const [verify, setVerify] = useState<VerifyState>({ phase: "idle" });
  const [wallet, setWallet] = useState<WalletState>({ phase: "no-wallet" });
  const [listings, setListings] = useState<Listing[] | null>(null);
  const [listingsLoading, setListingsLoading] = useState(false);
  const [listingsError, setListingsError] = useState<string | null>(null);
  const [buyStatus, setBuyStatus] = useState<BuyStatus>("idle");
  const [buyError, setBuyError] = useState<string | null>(null);
  const [tradeOrder, setTradeOrder] = useState<Order | null>(null);
  const [tradeStartedAt, setTradeStartedAt] = useState<number | null>(null);
  const accountListenerRef = useRef<(() => void) | null>(null);
  const cancelPollRef = useRef(false);

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

  const loadListings = useCallback(async () => {
    setListingsLoading(true);
    setListingsError(null);
    try {
      const { items } = await fetchListings("LISTED");
      setListings(items);
    } catch (error) {
      setListingsError(error instanceof Error ? error.message : "Failed to load listings");
      setListings([]);
    } finally {
      setListingsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadHealth();
    void loadListings();

    accountListenerRef.current = onAccountsChanged((account) => {
      if (account) {
        setWallet({ phase: "connected", account, chainId: chainConfig.chainId });
      } else {
        setWallet({ phase: "no-wallet" });
      }
    });

    return () => {
      accountListenerRef.current?.();
    };
  }, []);

  const disconnectWallet = useCallback(() => {
    setWallet({ phase: "no-wallet" });
  }, []);

  async function handleConnectWallet() {
    try {
      setWallet({ phase: "connecting" });
      const account = await connectWallet();
      setWallet({ phase: "connected", account, chainId: chainConfig.chainId });
    } catch (err) {
      setWallet({
        phase: "error",
        message: err instanceof Error ? err.message : "Wallet connect failed",
      });
    }
  }

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

  async function handleBuy(listing: Listing) {
    if (wallet.phase !== "connected") {
      setBuyError("Connect your wallet first.");
      return;
    }
    if (!isChainConfigured) {
      setBuyError("Escrow contract not configured.");
      return;
    }

    setBuyError(null);
    setTradeOrder(null);

    try {
      setBuyStatus("creating");
      const order = await createOrderApi(listing.id, wallet.account);
      if (!order.evidence_hash) {
        setBuyStatus("failed");
        setBuyError("Evidence hash not set on order. Verify the parcel first.");
        return;
      }

      setBuyStatus("funding");
      const orderIdHex = chainOrderId(order.id);
      const txHash = await createOrder({
        orderId: orderIdHex,
        seller: order.seller_wallet,
        evidenceHash: order.evidence_hash,
        valueWei: order.amount_wei,
      });

      await fundOrderApi(order.id, orderIdHex, txHash);

      setBuyStatus("evaluating");
      const evaluated = await evaluateOrderApi(order.id);
      setTradeOrder(evaluated);
      setBuyStatus("polling");
      setTradeStartedAt(Date.now());
    } catch (error) {
      setBuyStatus("failed");
      setBuyError(error instanceof Error ? error.message : "Buy failed");
    }
  }

  useEffect(() => {
    const polling =
      tradeOrder &&
      (buyStatus === "polling") &&
      tradeOrder.state !== "SETTLED" &&
      tradeOrder.state !== "REFUNDED" &&
      tradeOrder.state !== "FAILED";

    if (!polling) {
      cancelPollRef.current = false;
      return;
    }

    cancelPollRef.current = false;

    const loop = async () => {
      if (cancelPollRef.current) return;
      try {
        const current = await fetchOrderApi(tradeOrder!.id);
        setTradeOrder(current);
        if (
          current.state === "SETTLED" ||
          current.state === "REFUNDED" ||
          current.state === "FAILED"
        ) {
          setBuyStatus(
            current.state === "SETTLED" ? "settled" : "failed",
          );
          cancelPollRef.current = true;
          return;
        }
      } catch {
        // Retry on next tick.
      }
      if (!cancelPollRef.current) {
        setTimeout(loop, 3000);
      }
    };

    void loop();

    return () => {
      cancelPollRef.current = true;
    };
  }, [tradeOrder, buyStatus]);

  const refreshTrade = useCallback(async () => {
    if (!tradeOrder) return;
    try {
      const current = await fetchOrderApi(tradeOrder.id);
      setTradeOrder(current);
      setTradeStartedAt(Date.now());
    } catch {
      // Swallowed; user can retry with Refresh button.
    }
  }, [tradeOrder]);

  const dbStatus =
    health.phase === "ready" ? health.data.database.status : "unknown";

  return (
    <div className="shell">
      <div className="demo-banner" role="status" aria-live="polite">
        {DEMO_BANNER}
      </div>
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
          <WalletPill wallet={wallet} onConnect={handleConnectWallet} onDisconnect={disconnectWallet} />
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

          {/* ---- Listings browse ---- */}
          <section className="panel listings-section">
            <div className="panel-heading">
              <h2>Listings</h2>
              <span className="muted">Demo parcels · buy on local chain</span>
            </div>

            {listingsLoading && (
              <p className="listing-empty">Loading listings…</p>
            )}
            {listingsError && !listingsLoading && (
              <p className="error">Listings unavailable: {listingsError}</p>
            )}
            {!listingsLoading && !listingsError && listings === null && (
              <p className="listing-empty">No listings.</p>
            )}
            {!listingsLoading && !listingsError && listings && listings.length === 0 && (
              <p className="listing-empty">No active listings.</p>
            )}
            {!listingsLoading && !listingsError && listings && listings.length > 0 && (
              <ul className="listings-grid">
                {listings.map((listing) => (
                  <li key={listing.id}>
                    <ListingCard
                      listing={listing}
                      onBuy={handleBuy}
                      buying={buyStatus !== "idle"}
                    />
                  </li>
                ))}
              </ul>
            )}

            {buyError && (
              <p className="error" role="status" aria-live="polite">
                Buy error: {buyError}
              </p>
            )}
          </section>

          {/* ---- Trade status ---- */}
          {tradeOrder && (
            <TradeStatus
              order={tradeOrder}
              polling={buyStatus === "polling"}
              startedAt={tradeStartedAt}
              onRefresh={refreshTrade}
              explorerUrl={chainConfig.explorerUrl}
            />
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

function WalletPill({
  wallet,
  onConnect,
  onDisconnect,
}: {
  wallet: WalletState;
  onConnect: () => void;
  onDisconnect: () => void;
}) {
  if (wallet.phase === "no-wallet") {
    return (
      <span className="pill bad" role="status" aria-live="polite">
        <span className="dot" /> Wallet: not connected{" "}
        <button className="wallet-btn" onClick={onConnect}>
          Connect
        </button>
      </span>
    );
  }

  if (wallet.phase === "connecting") {
    return (
      <span className="pill wait" role="status" aria-live="polite">
        <span className="dot" /> Wallet: connecting…
      </span>
    );
  }

  if (wallet.phase === "error") {
    return (
      <span className="pill bad" role="status" aria-live="polite">
        <span className="dot" /> Wallet error: {wallet.message}{" "}
        <button className="wallet-btn" onClick={onConnect}>
          Retry
        </button>
      </span>
    );
  }

  return (
    <span className="pill good" role="status" aria-live="polite">
      <span className="dot" />
      Wallet: {shortenAddress(wallet.account)} (chain {wallet.chainId}){" "}
      <button className="wallet-btn" onClick={switchChain}>
        Switch chain
      </button>{" "}
      <button className="wallet-btn" onClick={onDisconnect}>
        Disconnect
      </button>
    </span>
  );

  async function switchChain() {
    try {
      await switchToConfiguredChain();
    } catch {
      // Switched handled by error state in caller via accountsChanged
    }
  }
}
