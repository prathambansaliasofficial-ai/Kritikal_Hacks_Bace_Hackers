import { useEffect, useRef, useState } from "react";
import {
  Map as MapLibreMap,
  NavigationControl,
  Popup,
  type GeoJSONSource,
} from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import {
  fetchAlus,
  fetchParcel,
  type AluLevel,
  type BBox,
  type FeatureCollection,
} from "../lib/api";

const PILOT_CENTER: [number, number] = [73.8077, 18.5074];
const DEMO_ULPIN = "DEMO-ULPIN-001";

const SOURCE_PARCEL = "lm-parcels";
const SOURCE_ALU = "lm-alus";
const LAYER_PARCEL_FILL = "lm-parcel-fill";
const LAYER_PARCEL_OUTLINE = "lm-parcel-outline";
const LAYER_ALU_LINES = "lm-alu-lines";

function levelForZoom(zoom: number): AluLevel | null {
  if (zoom >= 20) return "1m";
  if (zoom >= 17) return "10m";
  if (zoom >= 14) return "100m";
  if (zoom >= 10) return "1km";
  return null;
}

export function MapView() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const currentLevelRef = useRef<AluLevel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const map = new MapLibreMap({
      container: containerRef.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: PILOT_CENTER,
      zoom: 12,
    });

    mapRef.current = map;
    map.addControl(new NavigationControl(), "top-right");

    map.on("load", () => {
      map.addSource(SOURCE_PARCEL, {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addSource(SOURCE_ALU, {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });

      map.addLayer({
        id: LAYER_PARCEL_FILL,
        type: "fill",
        source: SOURCE_PARCEL,
        paint: { "fill-color": "#4cc38a", "fill-opacity": 0.35 },
      });

      map.addLayer({
        id: LAYER_PARCEL_OUTLINE,
        type: "line",
        source: SOURCE_PARCEL,
        paint: { "line-color": "#4cc38a", "line-width": 2, "line-opacity": 0.9 },
      });

      map.addLayer({
        id: LAYER_ALU_LINES,
        type: "line",
        source: SOURCE_ALU,
        paint: { "line-color": "#7fb3d5", "line-width": 1, "line-opacity": 0.6 },
      });

      setLoading(false);
      void loadParcel(DEMO_ULPIN);
    });

    map.on("zoom", () => {
      const level = levelForZoom(map.getZoom());
      if (level === currentLevelRef.current) return;
      currentLevelRef.current = level;
      if (!level) {
        (map.getSource(SOURCE_ALU) as GeoJSONSource).setData({ type: "FeatureCollection", features: [] });
        return;
      }
      const bounds = map.getBounds();
      const bbox: BBox = [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()];
      void loadAlus(bbox, level);
    });

    map.on("moveend", () => {
      const level = currentLevelRef.current;
      if (!level) return;
      const bounds = map.getBounds();
      const bbox: BBox = [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()];
      void loadAlus(bbox, level);
    });

    map.on("click", (event) => {
      const features = map.queryRenderedFeatures(event.point, {
        layers: [LAYER_PARCEL_FILL, LAYER_ALU_LINES],
      });
      if (features.length === 0) {
        new Popup().remove();
        return;
      }
      const f = features[0];
      const props = f.properties as Record<string, unknown>;
      const ulpin = props["ulpin"] as string | undefined;
      const aluId = props["alu_id"] as string | undefined;
      const level = props["level"] as string | undefined;

      if (ulpin) {
        new Popup({ offset: 25 })
          .setLngLat(event.lngLat)
          .setHTML(`<strong>ULPIN:</strong> ${ulpin}<br/><em>Parcel</em>`)
          .addTo(map);
      } else if (aluId) {
        new Popup({ offset: 25 })
          .setLngLat(event.lngLat)
          .setHTML(`<strong>ALU ID:</strong> ${aluId}<br/><em>Level: ${level ?? "?"}</em>`)
          .addTo(map);
      }
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  async function loadParcel(ulpin: string) {
    setError(null);
    try {
      const parcel = await fetchParcel(ulpin);
      const source = mapRef.current?.getSource(SOURCE_PARCEL);
      if (source) {
        (source as GeoJSONSource).setData({ type: "FeatureCollection", features: [parcel] } as FeatureCollection<unknown>);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load parcel");
    }
  }

  async function loadAlus(bbox: BBox, level: AluLevel) {
    try {
      const collection = await fetchAlus(bbox, level);
      const source = mapRef.current?.getSource(SOURCE_ALU);
      if (source) {
        (source as GeoJSONSource).setData(collection);
      }
    } catch {
      // ALU fetch failures are non-fatal; parcels still show.
    }
  }

  if (loading) {
    return (
      <div className="map" ref={containerRef}>
        <div className="map-loading">Loading map…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="map" ref={containerRef}>
        <div className="map-error">Map error: {error}</div>
      </div>
    );
  }

  return <div className="map" ref={containerRef} />;
}
