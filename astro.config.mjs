import { defineConfig } from "astro/config";
export default defineConfig({
  site: "https://faktickapoznamka.sk", trailingSlash: "always", build: { format: "directory" },
  vite: { ssr: { external: ["@resvg/resvg-js", "sharp"] } },
});
