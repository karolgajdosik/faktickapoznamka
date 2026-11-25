import type { APIRoute } from "astro";
import { laws, type Law } from "../../../lib/data";
import { C, frame, png, wrap, textLines, hallSvg } from "../../../lib/og";
export function getStaticPaths() { return laws.map((l) => ({ params: { tlac: l.tlac }, props: { l } })); }
export const GET: APIRoute = ({ props }) => {
  const l = (props as { l: Law }).l; const fv = l.finalVote;
  const title = wrap(l.title, 38, fv ? 600 : 1060, 5);
  const col = l.status === "schválený" ? C.Z : l.status === "neschválený" ? C.P : C.accent;
  return png(frame(`
    <text x="64" y="138" font-size="22" font-weight="600" fill="${C.muted}">Tlač ${l.tlac} · ${l.kind}</text>
    ${textLines(title, 64, 196, 38, 800, C.text)}
    <text x="64" y="${Math.max(196 + title.length * 45 + 80, 470)}" font-size="${l.status.length > 12 ? 40 : 56}" font-weight="800" fill="${col}">${l.status === "v procese" ? "V procese" : l.status === "schválený" ? "Schválený" : l.status === "neschválený" ? "Neschválený" : "Bez záverečného hlasovania"}</text>
    ${fv ? `<text x="64" y="${Math.max(196 + title.length * 45 + 124, 514)}" font-size="24" font-weight="600" fill="${C.muted}">za ${fv.counts.Z} · proti ${fv.counts.P} · zdržalo sa ${fv.counts["?"]}</text>
      ${hallSvg({ ids: Object.keys(fv.votes), votes: fv.votes, clubsAt: fv.clubs, x: 712, y: 250, w: 440 })}` : ""}
  `));
};
