from __future__ import annotations

import pytest

from app.repositories import (
    alus as alus_repo,
)
from app.repositories import (
    bundles as bundles_repo,
)
from app.repositories import (
    evidence as evidence_repo,
)
from app.repositories import (
    listings as listings_repo,
)
from app.repositories import (
    orders as orders_repo,
)
from app.repositories import (
    parcels as parcels_repo,
)

BUYER = "0x2222222222222222222222222222222222222222"
SELLER = "0x3333333333333333333333333333333333333333"


def _insert_parcel(db, ulpin, attributes_ssl):
    db.execute(
        """
        INSERT INTO parcels (ulpin, geometry, geometry_source, geometry_status,
                             attributes)
        VALUES (%s, ST_GeomFromText(%s, 4326), 'DEMO_FIXTURE_NOT_OFFICIAL',
                'AVAILABLE', %s::jsonb)
        """,
        (
            ulpin,
            "MULTIPOLYGON(((0 0, 10 0, 10 10, 0 10, 0 0)))",
            attributes_ssl,
        ),
    )


@pytest.mark.integration
def test_parcel_and_alu_persistence(db):
    _insert_parcel(
        db,
        "INT-ULPIN-001",
        '{"owner_name": "Int Owner", "district": "Test", "zoning": "Residential"}',
    )
    db.execute(
        """
        INSERT INTO alus (alu_id, parent_id, level, geometry)
        VALUES ('INT-ALU-100m-000', NULL, '100m',
                ST_GeomFromText('POLYGON((2 2, 6 2, 6 6, 2 6, 2 2))', 4326)),
               ('INT-ALU-10m-001', 'INT-ALU-100m-000', '10m',
                ST_GeomFromText('POLYGON((2 2, 4 2, 4 4, 2 4, 2 2))', 4326))
        """,
    )
    db.execute(
        """
        INSERT INTO parcel_alus (ulpin, alu_id, relationship, overlap_percentage)
        VALUES ('INT-ULPIN-001', 'INT-ALU-10m-001', 'CONTAINS', 100)
        """,
    )
    db.commit()

    feature = parcels_repo.get_parcel("INT-ULPIN-001")
    assert feature is not None
    assert feature["id"] == "INT-ULPIN-001"
    assert feature["properties"]["demo"] is True
    assert feature["properties"]["attributes"]["zoning"] == "Residential"

    alu = alus_repo.get_alu("INT-ALU-10m-001")
    assert alu is not None
    assert alu["parent_id"] == "INT-ALU-100m-000"
    assert alus_repo.alus_present_in_parcel("INT-ULPIN-001", ["INT-ALU-10m-001"])


@pytest.mark.integration
def test_bundle_and_listing_flow(db):
    _insert_parcel(db, "INT-ULPIN-002", '{}')
    db.execute(
        """
        INSERT INTO bundles (ulpin, name, status, created_by)
        VALUES ('INT-ULPIN-002', 'Int bundle', 'ACTIVE', %s)
        """,
        (BUYER,),
    )
    bundle_row = db.execute(
        "SELECT id FROM bundles WHERE ulpin = 'INT-ULPIN-002'"
    ).fetchone()
    bundle_id = bundle_row[0]
    db.execute(
        "INSERT INTO bundle_alus (bundle_id, alu_id) VALUES (%s, 'INT-ALU-10m-001')",
        (bundle_id,),
    )
    db.execute(
        """
        INSERT INTO users (wallet_address, role, kyc_status)
        VALUES (%s, 'CITIZEN', 'VERIFIED')
        """,
        (BUYER,),
    )
    db.commit()

    bundle = bundles_repo.get_bundle(bundle_id)
    assert bundle is not None
    assert bundle["status"] == "ACTIVE"
    assert len(bundle["alus"]) == 1

    listing = listings_repo.create_listing(bundle_id, BUYER, "10000000000000000")
    assert listing["status"] == "DRAFT"
    assert listing["price_wei"] == "10000000000000000"

    updated = listings_repo.patch_listing_status(listing["id"], "LISTED")
    assert updated["status"] == "LISTED"

    listed = listings_repo.list_listings("LISTED")
    assert any(row["id"] == listing["id"] for row in listed)


@pytest.mark.integration
def test_order_and_evidence_persistence(db):
    db.execute(
        """
        INSERT INTO users (wallet_address, role, kyc_status)
        VALUES (%s, 'CITIZEN', 'VERIFIED'), (%s, 'CITIZEN', 'VERIFIED')
        """,
        (BUYER, SELLER),
    )
    _insert_parcel(db, "INT-ULPIN-003", '{}')
    db.execute(
        """
        INSERT INTO bundles (ulpin, name, status, created_by)
        VALUES ('INT-ULPIN-003', 'Int bundle 3', 'ACTIVE', %s)
        """,
        (BUYER,),
    )
    db.execute(
        """
        INSERT INTO listings (bundle_id, ulpin, seller_wallet, price_wei, status)
        SELECT id, 'INT-ULPIN-003', %s, '10000000000000000', 'LISTED'
        FROM bundles WHERE ulpin = 'INT-ULPIN-003'
        """,
        (SELLER,),
    )
    db.execute(
        """
        INSERT INTO orders (listing_id, buyer_wallet, seller_wallet, amount_wei,
                            state, chain_order)
        SELECT id, %s, seller_wallet, price_wei, 'FUNDED', %s
        FROM listings WHERE ulpin = 'INT-ULPIN-003'
        """,
        (
            BUYER,
            "0x1111111111111111111111111111111111111111111111111111111111111111",
        ),
    )
    db.commit()

    order_row = db.execute(
        """
        SELECT id FROM orders
        WHERE listing_id = (SELECT id FROM listings WHERE ulpin = 'INT-ULPIN-003')
        """
    ).fetchone()
    assert order_row is not None
    order = orders_repo.get_order(order_row[0])
    assert order is not None
    assert order["state"] == "FUNDED"

    evidence_id = evidence_repo.create_evidence_sheet(
        ulpin="INT-ULPIN-003",
        payload={"ulpin": "INT-ULPIN-003", "fields": {}, "sources": ["https://example.gov"]},
        source_refs=["https://example.gov"],
        tinyfish_run_id="run_int_001",
        evidence_hash="0xdeadbeef",
    )
    assert evidence_id is not None

    sheet = evidence_repo.get_evidence_sheet(evidence_id)
    assert sheet is not None
    assert sheet["ulpin"] == "INT-ULPIN-003"

    items = evidence_repo.list_evidence_sheets("INT-ULPIN-003")
    assert len(items) >= 1
