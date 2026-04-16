import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/",
  build: {
    outDir: "docs",
    assetsDir: "assets",
    emptyOutDir: true,
    // Raise the chunk warning threshold slightly
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        // Split vendor libs into separate cacheable chunks
        manualChunks: {
          "vendor-react": ["react", "react-dom", "react-router-dom"],
          "vendor-motion": ["framer-motion"],
          "vendor-icons": ["lucide-react"],
        },
      },
    },
  },
});
