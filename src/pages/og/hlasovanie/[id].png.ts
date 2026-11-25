import type { APIRoute } from "astro";
import { votes, voteWhat, lawTitle, resultText, fmtDate, type Vote } from "../../../lib/data";
import { C, frame, png, wrap, textLines, hallSvg } from "../../../lib/og";
export function getStaticPaths() { return votes.map((v) => ({ params: { id: v.id }, props: { v } })); }
export const GET: APIRoute = ({ props }) => {
  const v = (props as { v: Vote }).v;
  const head = wrap(voteWhat(v), 40, 600, 3), law = wrap(lawTitle(v.title), 22, 600, 2);
  const y0 = 150, yLaw = y0 + head.length * 47 + 14, yVer = Math.max(yLaw + law.length * 27 + 70, 420);
  const col = v.passed ? C.Z : v.passed === false ? C.P : C.muted;
  const counts = [["Za", v.counts.Z, C.Z], ["Proti", v.counts.P, C.P], ["Zdržal sa", v.counts["?"], C["?"]], ["Neprítomní", v.counts["0"], C.muted]] as const;
  return png(frame(`
    <text x="64" y="${y0 - 36}" font-size="22" font-weight="600" fill="${C.muted}">${fmtDate(v.datetime)}${v.tlac ? ` · tlač ${v.tlac}` : ""}</text>
    ${textLines(head, 64, y0 + 10, 40, 800, C.text)}
    ${textLines(law, 64, yLaw + 10, 22, 400, C.muted)}
    <text x="64" y="${yVer}" font-size="64" font-weight="800" fill="${col}">${resultText(v)}</text>
    ${counts.map(([l, n, c], i) => `<text x="${64 + i * 150}" y="${yVer + 62}" font-size="20" font-weight="600" fill="${C.muted}">${l}</text><text x="${64 + i * 150}" y="${yVer + 100}" font-size="34" font-weight="800" fill="${c}">${n}</text>`).join("")}
    ${hallSvg({ ids: Object.keys(v.votes), votes: v.votes, clubsAt: v.clubs, x: 712, y: 250, w: 440 })}
  `));
};
