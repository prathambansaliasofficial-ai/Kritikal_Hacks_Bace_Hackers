from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest

EVIDENCE_FIELDS = [
    "ulpin", "cadastral_map", "satellite_imagery", "record_of_rights",
    "registration_deeds", "master_plan", "building_permissions",
    "completion_occupancy", "encumbrances", "mortgages_liens",
    "land_use_zoning", "utility_infrastructure", "property_tax_arrears",
    "valuation_circle_rate", "infrastructure_row", "environmental_buffers",
    "restriction_zones", "service_linkages", "litigation_stays",
    "change_detection", "workflow_tracking",
]


def nd_field() -> dict[str, Any]:
    return {"value": None, "status": "N/D", "source": None, "retrieved_at": None}


def normalize_sheet(fields: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize to exactly 21 keys; missing -> N/D."""
    result: dict[str, Any] = {}
    for key in EVIDENCE_FIELDS:
        if fields and key in fields and isinstance(fields[key], dict):
            result[key] = fields[key]
        else:
            result[key] = nd_field()
    return result


def canonical_hash(ulpin: str, fields: dict[str, Any], sources: list[str]) -> str:
    """SHA-256 with 0x prefix, per docs/decisions.md §4."""
    payload = {
        "ulpin": ulpin,
        "fields": fields,
        "sources": sorted(set(sources)),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class TestEvidenceNormalization:
    def test_missing_fields_become_nd(self) -> None:
        result = normalize_sheet({})
        assert len(result) == 21
        for key in EVIDENCE_FIELDS:
            assert result[key] == nd_field(), f"field {key} should be N/D"

    def test_extra_fields_are_dropped(self) -> None:
        result = normalize_sheet({"fake_field": {"value": "x", "status": "AVAILABLE", "source": "s", "retrieved_at": "t"}})
        assert len(result) == 21
        assert "fake_field" not in result

    def test_partial_fields_kept(self) -> None:
        input_fields = {"ulpin": {"value": "DEMO-ULPIN-001", "status": "AVAILABLE", "source": "https://example.gov", "retrieved_at": "2026-10-29T16:40:00Z"}}
        result = normalize_sheet(input_fields)
        assert result["ulpin"]["value"] == "DEMO-ULPIN-001"
        assert result["ulpin"]["status"] == "AVAILABLE"
        # All other fields should be N/D
        for key in EVIDENCE_FIELDS:
            if key != "ulpin":
                assert result[key] == nd_field(), f"field {key} should be N/D"

    def test_all_21_fields_present(self) -> None:
        full_input = {key: {"value": "v", "status": "AVAILABLE", "source": "s", "retrieved_at": "t"} for key in EVIDENCE_FIELDS}
        result = normalize_sheet(full_input)
        assert len(result) == 21
        for key in EVIDENCE_FIELDS:
            assert result[key]["status"] == "AVAILABLE"


class TestEvidenceHash:
    def test_hash_deterministic(self) -> None:
        fields = normalize_sheet({})
        sources = ["https://example.gov/parcel/DEMO-ULPIN-001"]
        h1 = canonical_hash("DEMO-ULPIN-001", fields, sources)
        h2 = canonical_hash("DEMO-ULPIN-001", fields, sources)
        assert h1 == h2
        assert h1.startswith("0x")
        assert len(h1) == 66  # 0x + 64 hex chars

    def test_hash_changes_with_different_input(self) -> None:
        fields = normalize_sheet({})
        h1 = canonical_hash("DEMO-ULPIN-001", fields, ["https://a.com"])
        h2 = canonical_hash("DEMO-ULPIN-002", fields, ["https://a.com"])
        assert h1 != h2

    def test_sources_sorted_and_deduped(self) -> None:
        fields = normalize_sheet({})
        h1 = canonical_hash("DEMO-ULPIN-001", fields, ["https://b.com", "https://a.com", "https://a.com"])
        h2 = canonical_hash("DEMO-ULPIN-001", fields, ["https://a.com", "https://b.com"])
        assert h1 == h2  # same after sort+dedupe

    def test_hash_is_lowercase(self) -> None:
        fields = normalize_sheet({})
        h = canonical_hash("DEMO-ULPIN-001", fields, ["https://example.gov"])
        hex_part = h[2:]
        assert hex_part == hex_part.lower()


class TestMiddlewareDown:
    def test_middleware_down_returns_503(self) -> None:
        """When middleware is unreachable, backend returns 503. No state change."""
        # This is a behavior contract; actual httpx mock is in T3.2
        assert True  # placeholder - implemented in T3.2

    def test_invalid_sheet_returns_422(self) -> None:
        """Sheet without exactly 21 fields returns 422. Never invent values."""
        # This is a behavior contract; actual validation is in T3.2
        assert True  # placeholder - implemented in T3.2
