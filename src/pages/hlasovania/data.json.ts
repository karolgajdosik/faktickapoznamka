// Compact list of every vote for the filterable /hlasovania/ page (fetched once, cached by the service worker).
import type { APIRoute } from "astro";
import { votes, clubs, NEZ, mpById, voteHeadline, voteContext, isFinal, shortTitle } from "../../lib/data";
import { temaOfVote, TEMY } from "../../lib/temy";

export const clubOrder = clubs.filter((c) => c.name !== NEZ).map((c) => c.name);
const PROC = /prezentáci|program(u)? schôdze|zmen[ay] programu|procedur|skrátené legislatívne|presunutie|prerušenie|hlasovanie bez rozpravy/i;
const PERSON = /voľb|zvolen|odvolan|vyslovenie nedôvery|dôvery vláde|nedôvery/i;
const AMEND = /pozmeňujúc|doplňujúc|návrh poslanc|návrh výboru|spoločnej správy|z (?:bodu|bodov) spoločnej/i;

export const GET: APIRoute = () => {
  const rows = votes.map((v) => {
    const t: Record<string, Record<string, number>> = {};
    for (const [id, c] of Object.entries(v.votes)) {
      if (c !== "Z" && c !== "P" && c !== "?") continue;
      const cl = v.clubs?.[id] ?? mpById.get(id)?.club ?? ""; (t[cl] ??= {})[c] = (t[cl][c] ?? 0) + 1;
    }
    const maj = clubOrder.map((cl) => { const r = Object.entries(t[cl] ?? {}).sort((a, b) => b[1] - a[1]); return r[0] && (!r[1] || r[0][1] > r[1][1]) ? r[0][0] : "-"; }).join("");
    const text = `${v.title} ${v.detail ?? ""}`;
    const kind = isFinal(v) ? "f" : PERSON.test(text) ? "o" : PROC.test(text) ? "p" : AMEND.test(v.detail ?? "") ? "a" : "x";
    const ctx = voteContext(v);
    return [v.id, v.datetime, shortTitle(voteHeadline(v), 170), ctx ? shortTitle(ctx, 130) : "", v.tlac ?? "", v.session ?? 0,
      v.passed === null ? -1 : v.passed ? 1 : 0, v.counts.Z, v.counts.P, v.counts["?"], v.counts.N, v.counts["0"], kind, maj, (temaOfVote.get(v.id) ?? []).join(",")];
  });
  return new Response(JSON.stringify({ clubs: clubOrder, temy: TEMY.map((t) => [t.slug, t.name]), rows }), { headers: { "content-type": "application/json" } });
};
