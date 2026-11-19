import { useCallback, useEffect, useState } from "react";
import {
  fetchReviews,
  submitReviewDecision,
  type ReviewItem,
  type ReviewDecision,
} from "../lib/api";

export type ReviewQueueProps = {
  officer: string;
  onDecision?: (evidenceId: number, decision: ReviewDecision) => void;
};

export function ReviewQueue({ officer, onDecision }: ReviewQueueProps) {
  const [items, setItems] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingId, setPendingId] = useState<number | null>(null);
  const [deciding, setDeciding] = useState<number | null>(null);
  const [reason, setReason] = useState("");
  const [decisionType, setDecisionType] = useState<ReviewDecision>("APPROVE");

  const loadReviews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchReviews("PENDING");
      setItems(data.items);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load review queue. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadReviews();
  }, [loadReviews]);

  function openDecision(item: ReviewItem, decision: ReviewDecision) {
    setPendingId(item.evidence_id);
    setDecisionType(decision);
    setReason(decision === "REJECT" ? "" : "");
  }

  function closeDecision() {
    setPendingId(null);
    setReason("");
    setDecisionType("APPROVE");
  }

  const handleSubmit = useCallback(async () => {
    if (!pendingId) return;
    if (decisionType === "REJECT" && !reason.trim()) {
      setError("Reason is required for rejection.");
      return;
    }
    setDeciding(pendingId);
    try {
      await submitReviewDecision(pendingId, decisionType, reason.trim(), officer);
      setItems((prev) => prev.filter((i) => i.evidence_id !== pendingId));
      onDecision?.(pendingId, decisionType);
      closeDecision();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to submit decision. Check officer token.",
      );
    } finally {
      setDeciding(null);
    }
  }, [pendingId, decisionType, reason, officer, onDecision]);

  if (loading) {
    return (
      <div className="panel review-loading">
        <p className="muted">Loading review queue…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel review-error">
        <p className="error">Review error: {error}</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="panel review-empty">
        <p className="muted">No pending evidence reviews.</p>
      </div>
    );
  }

  return (
    <div className="panel review-panel">
      <h3>Review Queue</h3>
      <p className="muted">
        Officer token: <code>{officer.slice(0, 8)}…</code>
      </p>

      <table className="review-table">
        <thead>
          <tr>
            <th>ULPIN</th>
            <th>Status</th>
            <th>Evidence Hash</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.evidence_id}>
              <td>{item.ulpin}</td>
              <td>
                <span className="chip pending">{item.status}</span>
              </td>
              <td className="hash-cell">{item.evidence_hash}</td>
              <td className="actions">
                <button
                  className="btn approve"
                  onClick={() => openDecision(item, "APPROVE")}
                  disabled={deciding === item.evidence_id}
                >
                  Approve
                </button>
                <button
                  className="btn reject"
                  onClick={() => openDecision(item, "REJECT")}
                  disabled={deciding === item.evidence_id}
                >
                  Reject
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {pendingId && (
        <div className="review-decision">
          <h4>
            {decisionType === "APPROVE" ? "Approve" : "Reject"} evidence
            #{pendingId}
          </h4>
          {decisionType === "REJECT" && (
            <div className="form-row">
              <label>Reason (required)</label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Enter rejection reason"
              />
              {reason.trim() === "" && (
                <p className="error">Reason is required to reject.</p>
              )}
            </div>
          )}
          <div className="form-row actions">
            <button
              className="btn confirm"
              onClick={handleSubmit}
              disabled={deciding === pendingId}
            >
              {deciding === pendingId ? "Submitting…" : "Confirm"}
            </button>
            <button className="btn cancel" onClick={closeDecision}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
