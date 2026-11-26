// Local quick-search data (MPs, prints, committees) for the header palette and /hladat/.
import type { APIRoute } from "astro";
import { mps, laws, clubColor, photo, initials } from "../../lib/data";
import { committees } from "../../lib/extra";
export const GET: APIRoute = () => new Response(JSON.stringify({
  mps: mps.map((m) => ({ id: m.id, n: m.name, c: m.club, col: clubColor(m.club), p: photo(m.id), i: initials(m) })),
  laws: laws.map((l) => [l.tlac, l.title.slice(0, 110), l.status]),
  com: committees.map((c) => [c.id, c.short.replace(/ NR SR$/, "")]),
}), { headers: { "content-type": "application/json" } });
