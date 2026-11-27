import type { APIRoute } from "astro";
import { weeks, weekLabel, type Week } from "../../../lib/weeks";
import { pct } from "../../../lib/data";
import { C, frame, png, esc, wrap, textLines } from "../../../lib/og";
export function getStaticPaths() { return weeks.map((w) => ({ params: { key: w.key }, props: { w } })); }
export const GET: APIRoute = ({ props }) => {
  const w = (props as { w: Week }).w;
  const laws = w.finals.filter((v) => v.passed).length;
  const tiles = [["Hlasovaní", String(w.votes.length), C.text], ["Schválené", String(w.passed), C.Z], ["Neschválené", String(w.failed), C.P], ["Prijaté zákony", String(laws), C.accent], ["Účasť", pct(w.attendance), C.text]] as const;
  const close = w.close[0];
  const closeLines = close ? wrap(close.title.replace(/\s*\(tl\.?\s*\d+\)/i, ""), 22, 1060, 2) : [];
  return png(frame(`
    <text x="64" y="150" font-size="26" font-weight="600" fill="${C.muted}">Týždeň v parlamente</text>
    <text x="64" y="215" font-size="56" font-weight="800" fill="${C.text}">${esc(weekLabel(w))}</text>
    ${tiles.map(([k, v, c], i) => `<rect x="${64 + i * 216}" y="262" width="200" height="118" rx="14" fill="${C.panel}" stroke="${C.line}"/>
      <text x="${84 + i * 216}" y="300" font-size="18" font-weight="600" fill="${C.muted}">${k}</text>
      <text x="${84 + i * 216}" y="355" font-size="40" font-weight="800" fill="${c}">${esc(v)}</text>`).join("")}
    ${close ? `<text x="64" y="440" font-size="20" font-weight="600" fill="${C.muted}">Najtesnejšie hlasovanie · ${close.counts.Z} za, ${close.counts.P} proti</text>${textLines(closeLines, 64, 478, 22, 600, C.text)}` : ""}
  `));
};
