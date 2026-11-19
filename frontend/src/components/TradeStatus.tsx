import { type Order } from "../lib/api";

const CHECK_ORDER = [
  "LISTED",
  "BUNDLE_INTACT",
  "KYC_WALLET",
  "ZONING_OK",
  "FUNDS_IN_ESCROW",
  "TRADE_MATCH",
] as const;

const TIMEOUT_MS = 30000;

type TradeStatusProps = {
  order: Order | null;
  polling: boolean;
  startedAt: number | null;
  onRefresh: () => void;
  explorerUrl?: string;
};

export function TradeStatus({
  order,
  polling,
  startedAt,
  onRefresh,
  explorerUrl,
}: TradeStatusProps) {
  const terminal =
    order?.state === "SETTLED" ||
    order?.state === "REFUNDED" ||
    order?.state === "FAILED";

  const elapsed = startedAt ? Date.now() - startedAt : 0;
  const timedOut = !terminal && polling && elapsed > TIMEOUT_MS;

  const decisionLabel =
    order?.decision === "APPROVED"
      ? "Approved"
      : order?.decision === "REJECTED"
      ? "Rejected"
      : order?.decision === "NEEDS_REVIEW"
      ? "Officer review"
      : "Pending";

  const chainStateLabel =
    order?.state === "FUNDED" ? "Funded (1)" :
    order?.state === "SETTLED" ? "Settled (2)" :
    order?.state === "REFUNDED" ? "Refunded (3)" :
    order?.state === "CREATED" ? "None (0)" :
    order?.state === "FAILED" ? "Failed" :
    "—";

  return (
    <section className="panel trade-status">
      <div className="panel-heading">
        <h2>Trade status</h2>
        <span className={`chip ${order?.state === "SETTLED" ? "good" : order?.state === "FAILED" || order?.state === "REFUNDED" ? "bad" : "wait"}`}>
          {order?.state ?? "—"}
        </span>
      </div>

      {!order ? (
        <p className="trade-empty">No active trade. Buy a listing to start.</p>
      ) : (
        <>
          <div className="trade-meta">
            <div className="meta-item">
              <span className="meta-label">Order</span>
              <span className="meta-value">#{order.id}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Listing</span>
              <span className="meta-value">#{order.listing_id}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Amount</span>
              <span className="meta-value">{order.amount_wei} wei</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Chain state</span>
              <span className="meta-value">{chainStateLabel}</span>
            </div>
          </div>

          <div className="trade-section">
            <h3>Six checks</h3>
            <table className="check-table">
              <thead>
                <tr>
                  <th>Check</th>
                  <th>Result</th>
                  <th>Reason</th>
                  <th>Blocking</th>
                </tr>
              </thead>
              <tbody>
                {CHECK_ORDER.map((name) => {
                  const result = order.checks.find((c) => c.name === name);
                  return (
                    <tr key={name}>
                      <td className="check-name">{name}</td>
                      <td>
                        <span
                          className={`check-result ${result?.passed ? "pass" : "fail"}`}>
                          {result ? (result.passed ? "Pass" : "Fail") : "—"}
                        </span>
                      </td>
                      <td className="check-reason">{result?.reason ?? "—"}</td>
                      <td>
                        {result?.blocking ? (
                          <span className="chip bad">Yes</span>
                        ) : result ? (
                          <span className="chip muted">No</span>
                        ) : (
                          <span className="chip muted">—</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="trade-section decision-box">
            <h3>Decision</h3>
            <p className={`decision ${order?.decision ?? "pending"}`}>
              {decisionLabel}
            </p>
            {order?.decision === "NEEDS_REVIEW" && (
              <p className="needs-review">
                Officer review required — do not claim settle.
              </p>
            )}
            {order?.decision === null && order.checks.length > 0 && (
              <p className="muted" style={{ fontSize: 11 }}>
                Awaiting evaluation result…
              </p>
            )}
          </div>

          {order.tx_hash && (
            <div className="trade-section tx-row">
              <h3>Transaction</h3>
              <span className="tx-hash">{order.tx_hash}</span>
              {explorerUrl && (
                <a href={`${explorerUrl}/tx/${order.tx_hash}`} target="_blank" rel="noopener noreferrer" className="explorer-link">
                  Explorer
                </a>
              )}
            </div>
          )}

          <div className="trade-actions">
            <button
              className="btn refresh-btn"
              onClick={onRefresh}
              disabled={terminal || polling}
              aria-label={terminal ? "Trade is terminal" : "Refresh status"}
            >
              {terminal ? "Terminal" : polling ? "Polling…" : "Refresh"}
            </button>
            {timedOut && (
              <p className="timeout-msg">
                Taking longer than expected. Refresh to check again.
              </p>
            )}
          </div>
        </>
      )}
    </section>
  );
}
