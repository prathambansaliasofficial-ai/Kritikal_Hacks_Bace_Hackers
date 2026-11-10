from __future__ import annotations

from typing import Any

from app.repositories.base import fetch_all, fetch_one

ACTIVE_STATUSES = ("DRAFT", "LISTED", "PAUSED")

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "DRAFT": {"LISTED", "CANCELLED"},
    "LISTED": {"PAUSED", "CANCELLED"},
    "PAUSED": {"LISTED", "CANCELLED"},
    "SOLD": set(),
    "CANCELLED": set(),
}


class ListingError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _row_dict(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return dict(row)


def get_bundle(bundle_id: int) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, ulpin, name, status, created_by, created_at, updated_at
        FROM bundles
        WHERE id = %s
        """,
        (bundle_id,),
    )


def get_seller(wallet_address: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, wallet_address, role, kyc_status, created_at, updated_at
        FROM users
        WHERE wallet_address = %s
        """,
        (wallet_address,),
    )


def count_active_listings_for_bundle(
    bundle_id: int, exclude_listing_id: int | None = None
) -> int:
    if exclude_listing_id is None:
        row = fetch_one(
            """
            SELECT count(*) AS c FROM listings
            WHERE bundle_id = %s AND status = ANY(%s)
            """,
            (bundle_id, list(ACTIVE_STATUSES)),
        )
    else:
        row = fetch_one(
            """
            SELECT count(*) AS c FROM listings
            WHERE bundle_id = %s AND status = ANY(%s) AND id <> %s
            """,
            (bundle_id, list(ACTIVE_STATUSES), exclude_listing_id),
        )
    return int(row["c"])


def alu_has_sold_listing(
    alu_id: str, exclude_listing_id: int | None = None
) -> bool:
    """True iff a SOLD listing already exists for this ALU (sold lock)."""
    if exclude_listing_id is None:
        row = fetch_one(
            """
            SELECT 1 FROM listings
            WHERE alu_id = %s AND status = 'SOLD'
            LIMIT 1
            """,
            (alu_id,),
        )
    else:
        row = fetch_one(
            """
            SELECT 1 FROM listings
            WHERE alu_id = %s AND status = 'SOLD' AND id <> %s
            LIMIT 1
            """,
            (alu_id, exclude_listing_id),
        )
    return row is not None


def alu_has_active_listing(
    alu_id: str, exclude_listing_id: int | None = None
) -> bool:
    """True iff another ACTIVE listing already exists for this ALU."""
    if exclude_listing_id is None:
        row = fetch_one(
            """
            SELECT 1 FROM listings
            WHERE alu_id = %s AND status = ANY(%s)
            LIMIT 1
            """,
            (alu_id, list(ACTIVE_STATUSES)),
        )
    else:
        row = fetch_one(
            """
            SELECT 1 FROM listings
            WHERE alu_id = %s AND status = ANY(%s) AND id <> %s
            LIMIT 1
            """,
            (alu_id, list(ACTIVE_STATUSES), exclude_listing_id),
        )
    return row is not None


def create_listing(
    bundle_id: int,
    seller_wallet: str,
    price_wei: str,
    alu_id: str | None = None,
) -> dict[str, Any]:
    bundle = get_bundle(bundle_id)
    if bundle is None:
        raise ListingError(404, "Bundle not found")
    if bundle["status"] != "ACTIVE":
        raise ListingError(409, "Bundle is not ACTIVE")

    seller = get_seller(seller_wallet)
    if seller is None:
        raise ListingError(404, "Seller not found")
    if seller["kyc_status"] != "VERIFIED":
        raise ListingError(409, "Seller KYC not VERIFIED")

    try:
        price = int(price_wei)
    except (TypeError, ValueError) as error:
        raise ListingError(422, "price_wei must be a positive integer") from error
    if price <= 0:
        raise ListingError(422, "price_wei must be greater than 0")

    if count_active_listings_for_bundle(bundle_id) > 0:
        raise ListingError(409, "Bundle already has an active listing")

    if alu_id is not None:
        if alu_has_sold_listing(alu_id):
            raise ListingError(409, "ALU is sold and cannot be re-listed")
        if alu_has_active_listing(alu_id):
            raise ListingError(409, "ALU already has an active listing")

    row = fetch_one(
        """
        INSERT INTO listings (bundle_id, ulpin, seller_wallet, price_wei, status, alu_id)
        VALUES (%s, %s, %s, %s, 'DRAFT', %s)
        RETURNING id, bundle_id, ulpin, seller_wallet, price_wei, status, alu_id, created_at
        """,
        (bundle_id, bundle["ulpin"], seller_wallet, price_wei, alu_id),
    )
    return _row_dict(row)


def list_listings(status: str | None = None) -> list[dict[str, Any]]:
    if status is None:
        status = "LISTED"
    rows = fetch_all(
        """
        SELECT id, bundle_id, ulpin, seller_wallet, price_wei, status, alu_id,
               created_at
        FROM listings
        WHERE status = %s
        ORDER BY id DESC
        """,
        (status,),
    )
    return [_row_dict(row) for row in rows]


def get_listing(listing_id: int) -> dict[str, Any] | None:
    return _row_dict(
        fetch_one(
            """
            SELECT id, bundle_id, ulpin, seller_wallet, price_wei, status, alu_id,
                   created_at
            FROM listings
            WHERE id = %s
            """,
            (listing_id,),
        )
    )


def patch_listing_status(listing_id: int, status: str) -> dict[str, Any] | None:
    listing = get_listing(listing_id)
    if listing is None:
        return None
    current = listing["status"]
    if status not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ListingError(409, f"invalid transition {current} -> {status}")

    if status in ACTIVE_STATUSES:
        if count_active_listings_for_bundle(
            int(listing["bundle_id"]), exclude_listing_id=listing_id
        ) > 0:
            raise ListingError(409, "Bundle already has an active listing")
        listing_alu_id = listing["alu_id"]
        if listing_alu_id is not None:
            if alu_has_sold_listing(
                listing_alu_id, exclude_listing_id=listing_id
            ):
                raise ListingError(409, "ALU is sold and cannot be re-listed")
            if alu_has_active_listing(
                listing_alu_id, exclude_listing_id=listing_id
            ):
                raise ListingError(409, "ALU already has an active listing")

    return _row_dict(
        fetch_one(
            """
            UPDATE listings
            SET status = %s, updated_at = now()
            WHERE id = %s
            RETURNING id, bundle_id, ulpin, seller_wallet, price_wei, status,
                      alu_id, created_at
            """,
            (status, listing_id),
        )
    )
