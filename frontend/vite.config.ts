import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // 0.0.0.0 so the dev server is reachable from a phone on the same Wi-Fi and
    // from a cloud preview tunnel. Override the port with: npm run dev -- --port 3001
    host: "0.0.0.0",
    port: 5173,
    // Same-origin API: proxy backend routes so the app also works behind a
    // single exposed dev-server hostname (cloud preview / tunnel).
    proxy: {
      "/api": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/health": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/docs": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/openapi.json": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
});
