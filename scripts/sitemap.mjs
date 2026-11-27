// Writes dist/sitemap.xml from the built pages (one URL per index.html; 404 excluded).
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const SITE = "https://faktickapoznamka.sk";
const urls = [];
const walk = (d) => {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f === "index.html") urls.push("/" + p.slice(5, -10).replace(/\\/g, "/"));
  }
};
walk("dist");
const prio = (u) => (u === "/" ? "1.0" : /^\/(poslanci|zakony|hlasovania|schodze|statistiky)\/$/.test(u) ? "0.9" : /^\/poslanci\/\d+\/$/.test(u) ? "0.8" : "0.5");
urls.sort((a, b) => a.split("/").length - b.split("/").length || a.localeCompare(b, "sk", { numeric: true }));
const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
  .map((u) => `<url><loc>${SITE}${encodeURI(u)}</loc><priority>${prio(u)}</priority></url>`)
  .join("\n")}\n</urlset>\n`;
if (urls.length > 50000) throw new Error("sitemap over 50k URLs; split it");
writeFileSync("dist/sitemap.xml", xml);
console.log(`sitemap: ${urls.length} URLs`);
