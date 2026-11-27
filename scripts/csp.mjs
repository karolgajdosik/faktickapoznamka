// Replaces 'unsafe-inline' in script-src of dist/_headers with SHA-256 hashes of every
// inline executable <script> in the built pages, so only our own inline code may run.
import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";
const hashes = new Set();
const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) walk(p); else if (p.endsWith(".html")) scan(readFileSync(p, "utf8")); } };
const scan = (s) => {
  for (const m of s.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)) {
    const [, attrs, body] = m;
    if (/\bsrc=/.test(attrs) || /type="application\/(ld\+)?json"/.test(attrs) || !body.trim()) continue;
    hashes.add(`'sha256-${createHash("sha256").update(body, "utf8").digest("base64")}'`);
  }
  if (/<[^>]+\son[a-z]+=/i.test(s)) throw new Error("inline event handler found; move it to a script");
};
walk("dist");
const file = "dist/_headers";
const h = readFileSync(file, "utf8");
const out = h.replaceAll(/script-src 'self' 'unsafe-inline'/g, `script-src 'self' ${[...hashes].sort().join(" ")}`);
if (out === h) throw new Error("script-src 'unsafe-inline' not found in dist/_headers");
writeFileSync(file, out);
console.log(`CSP: ${hashes.size} inline script hashes`);
