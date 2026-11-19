from __future__ import annotations

import hashlib
import json
from typing import Any

EVIDENCE_FIELDS: list[str] = [
    "ulpin", "cadastral_map", "satellite_imagery", "record_of_rights",
    "registration_deeds", "master_plan", "building_permissions",
    "completion_occupancy", "encumbrances", "mortgages_liens",
    "land_use_zoning", "utility_infrastructure", "property_tax_arrears",
    "valuation_circle_rate", "infrastructure_row", "environmental_buffers",
    "restriction_zones", "service_linkages", "litigation_stays",
    "change_detection", "workflow_tracking",
]

ND_FIELD: dict[str, Any] = {
    "value": None,
    "status": "N/D",
    "source": None,
    "retrieved_at": None,
}


def normalize_sheet(fields: Any) -> dict[str, dict[str, Any]]:
    """Return exactly the 21 evidence keys; missing/invalid -> N/D object."""
    if not isinstance(fields, dict):
        return {key: dict(ND_FIELD) for key in EVIDENCE_FIELDS}
    result: dict[str, dict[str, Any]] = {}
    for key in EVIDENCE_FIELDS:
        value = fields.get(key)
        if isinstance(value, dict):
            result[key] = value
        else:
            result[key] = dict(ND_FIELD)
    return result


def canonical_hash(
    ulpin: str, fields: dict[str, dict[str, Any]], sources: list[str]
) -> str:
    """SHA-256 with 0x prefix, per docs/decisions.md section 4."""
    payload = {
        "ulpin": ulpin,
        "fields": fields,
        "sources": sorted(set(sources)),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
