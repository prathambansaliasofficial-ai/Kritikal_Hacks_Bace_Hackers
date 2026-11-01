import { expect } from "chai";
import { EVIDENCE_FIELDS, type EvidenceField } from "../src/tinyfish/evidence.js";

describe("Mock TinyFish evidence (no API key needed)", function () {
  it("has exactly 21 evidence fields", function () {
    expect(EVIDENCE_FIELDS).to.have.lengthOf(21);
  });

  it("includes all required field names from api-contract §2.3", function () {
    const required = [
      "ulpin", "cadastral_map", "satellite_imagery", "record_of_rights",
      "registration_deeds", "master_plan", "building_permissions",
      "completion_occupancy", "encumbrances", "mortgages_liens",
      "land_use_zoning", "utility_infrastructure", "property_tax_arrears",
      "valuation_circle_rate", "infrastructure_row", "environmental_buffers",
      "restriction_zones", "service_linkages", "litigation_stays",
      "change_detection", "workflow_tracking",
    ];
    for (const field of required) {
      expect(EVIDENCE_FIELDS).to.include(field);
    }
  });

  it("EvidenceField type has correct shape", function () {
    const field: EvidenceField = {
      value: "Residential",
      status: "AVAILABLE",
      source: "https://example.gov/parcel/DEMO-ULPIN-001",
      retrieved_at: "2026-10-29T16:40:00Z",
    };
    expect(field.status).to.be.oneOf(["AVAILABLE", "PARTIAL", "N/A", "N/D"]);
    expect(field.value).to.equal("Residential");
  });

  it("N/D field shape for missing data", function () {
    const ndField: EvidenceField = {
      value: null,
      status: "N/D",
      source: null,
      retrieved_at: null,
    };
    expect(ndField.status).to.equal("N/D");
    expect(ndField.value).to.be.null;
  });
});
