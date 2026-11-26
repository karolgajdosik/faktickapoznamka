// Compact list of every parliamentary print for the filterable /zakony/ page.
import type { APIRoute } from "astro";
import { laws, shortTitle } from "../../lib/data";
import { lawProcess, committees } from "../../lib/extra";
const shortC = new Map(committees.map((c) => [c.name, c.short.replace(/ NR SR$/, "")]));
export const GET: APIRoute = () => {
  const rows = laws.map((l) => {
    const p = lawProcess.get(l.tlac);
    return [l.tlac, shortTitle(l.title, 220), l.kind, l.status, l.first, l.last, l.votes.length, l.speeches.length,
      p?.gestor ? shortC.get(p.gestor) ?? p.gestor.replace(/^Výbor NR SR pre /, "") : "", p?.zbierka ?? "", p?.returnedByPresident ? 1 : 0,
      p?.submitter ? shortTitle(p.submitter.replace(/^Vláda SR\s*-?\s*/i, "Vláda: "), 90) : "", p?.state ?? ""];
  });
  return new Response(JSON.stringify(rows), { headers: { "content-type": "application/json" } });
};
