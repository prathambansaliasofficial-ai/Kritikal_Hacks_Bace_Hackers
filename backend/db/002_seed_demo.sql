-- Demo seed data (T1.3). Every row is a DEMO_FIXTURE_NOT_OFFICIAL fixture;
-- no government record and no official claim. Exact IDs/geometries:
-- docs/decisions.md section 2.
-- Idempotent: safe to re-run (ON CONFLICT DO NOTHING). The seed script also
-- deletes the demo rows first, then inserts.

INSERT INTO parcels (ulpin, geometry, geometry_source, geometry_status, attributes)
VALUES (
    'DEMO-ULPIN-001',
    ST_GeomFromText(
        'MULTIPOLYGON(((73.8055 18.5055, 73.8095 18.5055, 73.8095 18.5095, 73.8055 18.5095, 73.8055 18.5055)))',
        4326,
    ),
    'DEMO_FIXTURE_NOT_OFFICIAL',
    'AVAILABLE',
    '{"owner_name": "Demo Owner", "district": "Pune", "zoning": "Residential"}'::jsonb
)
ON CONFLICT (ulpin) DO NOTHING;

INSERT INTO alus (alu_id, parent_id, level, geometry) VALUES
    (
        'ALU-100m-DEMO-000', NULL, '100m',
        ST_GeomFromText('POLYGON((73.8060 18.5060, 73.8080 18.5060, 73.8080 18.5080, 73.8060 18.5080, 73.8060 18.5060))', 4326)
    ),
    (
        'ALU-10m-DEMO-001', 'ALU-100m-DEMO-000', '10m',
        ST_GeomFromText('POLYGON((73.8060 18.5060, 73.8070 18.5060, 73.8070 18.5070, 73.8060 18.5070, 73.8060 18.5060))', 4326)
    ),
    (
        'ALU-10m-DEMO-002', 'ALU-100m-DEMO-000', '10m',
        ST_GeomFromText('POLYGON((73.8070 18.5060, 73.8080 18.5060, 73.8080 18.5070, 73.8070 18.5070, 73.8070 18.5060))', 4326)
    ),
    (
        'ALU-10m-DEMO-003', 'ALU-100m-DEMO-000', '10m',
        ST_GeomFromText('POLYGON((73.8060 18.5070, 73.8070 18.5070, 73.8070 18.5080, 73.8060 18.5080, 73.8060 18.5070))', 4326)
    ),
    (
        'ALU-10m-DEMO-004', 'ALU-100m-DEMO-000', '10m',
        ST_GeomFromText('POLYGON((73.8070 18.5070, 73.8080 18.5070, 73.8080 18.5080, 73.8070 18.5080, 73.8070 18.5070))', 4326)
    )
ON CONFLICT (alu_id) DO NOTHING;

INSERT INTO parcel_alus (ulpin, alu_id, relationship, overlap_percentage) VALUES
    ('DEMO-ULPIN-001', 'ALU-10m-DEMO-001', 'CONTAINS', 100),
    ('DEMO-ULPIN-001', 'ALU-10m-DEMO-002', 'CONTAINS', 100),
    ('DEMO-ULPIN-001', 'ALU-10m-DEMO-003', 'CONTAINS', 100),
    ('DEMO-ULPIN-001', 'ALU-10m-DEMO-004', 'CONTAINS', 100)
ON CONFLICT (ulpin, alu_id) DO NOTHING;
