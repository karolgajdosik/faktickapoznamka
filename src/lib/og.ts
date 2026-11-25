// Share images (1200×630 PNG) rendered at build time with resvg — no runtime cost.
import { Resvg } from "@resvg/resvg-js";
import sharp from "sharp";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync, utimesSync } from "node:fs";
import { createRequire } from "node:module";
import { clubs, mpById, clubHex as clubColor, type Code, type Mp } from "./data";

const require = createRequire(import.meta.url);
const font = (w: string) => require.resolve(`@expo-google-fonts/public-sans/${w}/PublicSans_${w}.ttf`);
const FONTS = [font("400Regular"), font("600SemiBold"), font("800ExtraBold")];

export const C = { bg: "#0c111d", panel: "#151d2e", line: "#243049", text: "#e7ecf5", muted: "#93a0b7", accent: "#8ab4ff",
  Z: "#3ccf91", P: "#f2616d", "?": "#f5b947", N: "#8a96ab", "0": "#3a4762" } as const;

export const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/** Greedy word wrap by approximate glyph width; ellipsis on the last line. */
export function wrap(text: string, size: number, width: number, maxLines: number): string[] {
  const per = Math.floor(width / (size * 0.53));
  const words = text.split(/\s+/); const lines: string[] = []; let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > per) { lines.push(cur.trim()); cur = w; if (lines.length === maxLines) break; }
    else cur = (cur + " " + w).trim();
  }
  if (lines.length < maxLines && cur) lines.push(cur);
  if (lines.length === maxLines && words.join(" ").length > lines.join(" ").length + 1) lines[maxLines - 1] = lines[maxLines - 1].replace(/\s*\S*$/, "") + "…";
  return lines;
}
export const textLines = (lines: string[], x: number, y: number, size: number, weight: number, fill: string, lh = 1.18) =>
  lines.map((l, i) => `<text x="${x}" y="${y + i * size * lh}" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(l)}</text>`).join("");

/** Mini hall: seats coloured by vote (or club), clubs by size from the left. */
export function hallSvg(opts: { ids: string[]; votes?: Record<string, Code>; clubsAt?: Record<string, string>; highlight?: string; x: number; y: number; w: number }) {
  const { ids, votes, clubsAt, highlight, x, y, w } = opts;
  const people = ids.map((i) => mpById.get(i)).filter((m): m is Mp => !!m);
  const clubOf = (m: Mp) => clubsAt?.[m.id] ?? m.club;
  const n = people.length, rows = 7, RI = 0.36, RO = w / 2, CX = x + w / 2, CY = y + RO;
  const radii = Array.from({ length: rows }, (_, i) => RI + ((1 - RI) * i) / (rows - 1));
  const sumR = radii.reduce((a, b) => a + b, 0);
  const per = radii.map((r) => Math.floor((n * r) / sumR)); let rest = n - per.reduce((a, b) => a + b, 0);
  for (let i = rows - 1; rest > 0; i = (i - 1 + rows) % rows, rest--) per[i]++;
  const seats: { x: number; y: number; a: number }[] = [];
  radii.forEach((r, i) => { for (let k = 0; k < per[i]; k++) { const a = per[i] === 1 ? Math.PI / 2 : Math.PI - (Math.PI * k) / (per[i] - 1); seats.push({ x: CX + RO * r * Math.cos(a), y: CY - RO * r * Math.sin(a), a }); } });
  seats.sort((p, q) => q.a - p.a || Math.hypot(p.x - CX, p.y - CY) - Math.hypot(q.x - CX, q.y - CY));
  const order: Code[] = ["Z", "?", "N", "P", "0"]; const ci = new Map(clubs.map((c, i) => [c.name, i]));
  const sorted = people.slice().sort((a, b) => ((ci.get(clubOf(a)) ?? 99) - (ci.get(clubOf(b)) ?? 99)) || (votes ? order.indexOf(votes[a.id]) - order.indexOf(votes[b.id]) : 0) || a.sortName.localeCompare(b.sortName, "sk"));
  const R = (RO * (1 - RI) / (rows - 1)) * 0.4;
  return sorted.map((m, i) => {
    const s = seats[i]; const club = clubColor(clubOf(m));
    if (votes) { const c = votes[m.id]; return c === "0"
      ? `<circle cx="${s.x.toFixed(1)}" cy="${s.y.toFixed(1)}" r="${(R * .8).toFixed(1)}" fill="none" stroke="${C["0"]}" stroke-width="2"/>`
      : `<circle cx="${s.x.toFixed(1)}" cy="${s.y.toFixed(1)}" r="${R.toFixed(1)}" fill="${C[c]}"/>`; }
    const hi = m.id === highlight;
    return `<circle cx="${s.x.toFixed(1)}" cy="${s.y.toFixed(1)}" r="${(hi ? R * 1.6 : R).toFixed(1)}" fill="${hi ? club : C.panel}" stroke="${hi ? C.text : club}" stroke-width="${hi ? 4 : 2.5}"/>`;
  }).join("");
}

export function frame(inner: string) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" font-family="Public Sans">
  <rect width="1200" height="630" fill="${C.bg}"/>
  <rect x="0" y="0" width="1200" height="8" fill="${C.accent}"/>
  <text x="64" y="84" font-size="26" font-weight="800" fill="${C.text}">faktická poznámka</text>
  <text x="1136" y="84" font-size="22" font-weight="600" fill="${C.muted}" text-anchor="end">faktickapoznamka.sk</text>
  ${inner}</svg>`;
}

const CACHE = ".og-cache"; // persisted between CI runs (actions/cache): unchanged images are not re-rendered
export async function png(svg: string) {
  const key = createHash("sha1").update(svg).digest("hex");
  const file = `${CACHE}/${key}.png`;
  if (existsSync(file)) { const now = new Date(); utimesSync(file, now, now); return new Response(new Uint8Array(readFileSync(file)), { headers: { "content-type": "image/png" } }); }
  const r = new Resvg(svg, { font: { fontFiles: FONTS, loadSystemFonts: false, defaultFontFamily: "Public Sans" }, fitTo: { mode: "width", value: 1200 } });
  // flat graphics compress far better as an indexed-colour PNG (~5× smaller)
  const out = await sharp(r.render().asPng()).png({ palette: true, colors: 48, effort: 1 }).toBuffer();
  mkdirSync(CACHE, { recursive: true }); writeFileSync(file, out);
  return new Response(new Uint8Array(out), { headers: { "content-type": "image/png" } });
}
