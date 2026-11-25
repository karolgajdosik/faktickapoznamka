// Cloudflare Workers static assets: max 20,000 files per deployment (free plan).
import { readdirSync, statSync, existsSync, rmSync } from "node:fs";
import { join } from "node:path";
let n = 0;
const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? walk(p) : n++; } };
walk("dist");
const LIMIT = 20000;
console.log(`dist: ${n} files (limit ${LIMIT})`);
if (n > LIMIT) { console.error("Too many files for Cloudflare static assets"); process.exit(1); }
if (n > LIMIT * 0.85) console.log("::warning::dist is close to the Cloudflare file limit");

// Drop cached share images that this build did not use (touched on every hit).
if (existsSync(".og-cache")) {
  const cutoff = Date.now() - 6 * 3600e3; let removed = 0;
  for (const f of readdirSync(".og-cache")) { const p = join(".og-cache", f); if (statSync(p).mtimeMs < cutoff) { rmSync(p); removed++; } }
  if (removed) console.log(`og-cache: removed ${removed} unused images`);
}
