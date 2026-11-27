import type { APIRoute } from "astro";
import { existsSync, readFileSync } from "node:fs";
import { mps, formerMps, mpStats, mpTalk, pct, fmtDur, clubHex as clubColor, currentIds, type Mp } from "../../../lib/data";
import { C, frame, png, esc, hallSvg } from "../../../lib/og";
export function getStaticPaths() { return [...mps, ...formerMps].map((m) => ({ params: { id: m.id }, props: { m } })); }
export const GET: APIRoute = ({ props }) => {
  const m = (props as { m: Mp }).m; const s = mpStats(m.id), t = mpTalk(m.id);
  const tiles = [["Účasť", pct(s.attendance)], ["Súlad s klubom", pct(s.loyalty)], ["Pri rečníckom pulte", fmtDur(t.seconds)]];
  const foto = `public/foto/${m.id}.jpg`;
  const photo = currentIds.has(m.id) && existsSync(foto)
    ? `<clipPath id="ph"><circle cx="932" cy="418" r="62"/></clipPath><circle cx="932" cy="418" r="66" fill="${clubColor(m.club)}"/>
       <image href="data:image/jpeg;base64,${readFileSync(foto).toString("base64")}" x="870" y="356" width="124" height="124" clip-path="url(#ph)" preserveAspectRatio="xMidYMid slice"/>` : "";
  return png(frame(`
    <text x="64" y="160" font-size="24" font-weight="600" fill="${C.muted}">Poslanec NR SR</text>
    <text x="64" y="232" font-size="60" font-weight="800" fill="${C.text}">${esc(m.name)}</text>
    <circle cx="76" cy="282" r="9" fill="${clubColor(m.club)}"/><text x="96" y="291" font-size="28" font-weight="600" fill="${C.text}">${esc(m.club)}</text>
    ${tiles.map(([k, v], i) => `<rect x="${64 + i * 200}" y="360" width="184" height="120" rx="14" fill="${C.panel}" stroke="${C.line}"/>
      <text x="${82 + i * 200}" y="398" font-size="17" font-weight="600" fill="${C.muted}">${k}</text>
      <text x="${82 + i * 200}" y="452" font-size="${v.length > 9 ? 28 : 38}" font-weight="800" fill="${i === 0 ? C.accent : C.text}">${esc(v)}</text>`).join("")}
    ${currentIds.has(m.id) ? hallSvg({ ids: [...currentIds], highlight: m.id, x: 712, y: 250, w: 440 }) : ""}
    ${photo}
  `));
};
