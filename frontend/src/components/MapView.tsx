import { useEffect, useRef } from "react";
import { Map as MapLibreMap, NavigationControl } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

const PILOT_CENTER: [number, number] = [73.8077, 18.5074]; // Kothrud, Pune

export function MapView() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const map = new MapLibreMap({
      container: containerRef.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: PILOT_CENTER,
      zoom: 12,
    });

    map.addControl(new NavigationControl(), "top-right");

    return () => {
      map.remove();
    };
  }, []);

  return <div className="map" ref={containerRef} />;
}
