// Data for /porovnanie/: per-MP figures plus the voting-agreement triangle for every pair.
import type { APIRoute } from "astro";
import { mps, clubColor, mpStats, talk, photo, initials } from "../../lib/data";
import { absence, mpExtra, isApproved, committeesOf, agreementTriangle } from "../../lib/extra";

export const GET: APIRoute = () => {
  const { ids, tri } = agreementTriangle();
  const byId = new Map(mps.map((m) => [m.id, m]));
  const people = ids.map((id) => {
    const m = byId.get(id)!, s = mpStats(id), t = talk.get(id), x = mpExtra.get(id), a = absence.get(id), d = x?.declaration;
    return {
      id, n: m.name, s: m.sortName, c: m.club, col: clubColor(m.club), p: photo(id), i: initials(m), r: m.region ?? null,
      att: s.attendance, loy: s.loyalty, reb: s.rebels.length, unex: a?.unexcused ?? null,
      talk: t?.seconds ?? 0, spk: t?.count ?? 0, fact: t?.factual ?? 0, words: t?.words ?? 0,
      bills: x?.bills.length ?? null, billsOk: x ? x.bills.filter(isApproved).length : null,
      amend: x?.amendments.length ?? null, interp: x?.interpellations.length ?? null, trips: x?.trips.length ?? null,
      incP: d?.incomePublic ?? null, incO: d?.incomeOther ?? null, re: d ? d.realEstateCount : null, mov: d ? d.movablesCount : null,
      obl: d ? d.obligations.length : null, com: committeesOf(id).map((c) => [c.id, c.short.replace(/ NR SR$/, ""), c.label]),
    };
  });
  return new Response(JSON.stringify({ people, tri }), { headers: { "content-type": "application/json" } });
};
