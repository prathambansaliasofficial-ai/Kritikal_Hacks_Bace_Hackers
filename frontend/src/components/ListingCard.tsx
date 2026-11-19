import { type Listing } from "../lib/api";
import { formatWeiToEth } from "../lib/web3";

type ListingCardProps = {
  listing: Listing;
  aluCount?: number;
  sellerKyc?: string;
  onBuy: (listing: Listing) => void;
  buying: boolean;
};

export function ListingCard({
  listing,
  aluCount,
  sellerKyc,
  onBuy,
  buying,
}: ListingCardProps) {
  const priceEth = formatWeiToEth(listing.price_wei);
  const isDemo = Boolean(listing.demo);
  const disabled = buying || listing.status !== "LISTED";

  const kycTone =
    sellerKyc === "VERIFIED" ? "good" : sellerKyc === "REJECTED" ? "bad" : "muted";

  return (
    <article className="panel listing-card">
      <div className="panel-heading">
        <h2>Listing #{listing.id}</h2>
        <span className={`chip ${isDemo ? "muted" : "good"}`}>
          {isDemo ? "DEMO_FIXTURE_NOT_OFFICIAL" : "LIVE"}
        </span>
      </div>

      <dl className="listing-meta">
        <dt>Bundle</dt>
        <dd>#{listing.bundle_id}</dd>

        <dt>ULPIN</dt>
        <dd>{listing.ulpin}</dd>

        <dt>Price</dt>
        <dd>
          {priceEth} ETH{" "}
          <span className="muted">({listing.price_wei} wei)</span>
        </dd>

        <dt>ALU count</dt>
        <dd>{aluCount ?? "—"}</dd>

        <dt>Seller KYC</dt>
        <dd>
          <span className={`chip ${kycTone}`}>{sellerKyc ?? "—"}</span>
        </dd>

        <dt>Status</dt>
        <dd>
          <span className={`chip ${listing.status === "LISTED" ? "good" : "muted"}`}>
            {listing.status}
          </span>
        </dd>
      </dl>

      <button
        className="buy-btn"
        onClick={() => onBuy(listing)}
        disabled={disabled}
        aria-label={disabled ? "Buy disabled" : `Buy listing #${listing.id}`}
      >
        {disabled ? (listing.status !== "LISTED" ? "Not listed" : "Buying…") : "Buy"}
      </button>

      {isDemo && (
        <p className="muted" style={{ fontSize: 11, marginTop: 8 }}>
          Testnet demo only — not a legal title transfer.
        </p>
      )}
    </article>
  );
}
