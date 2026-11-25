// Small per-MP activity file used by the "Sledujem" section on the home page.
import type { APIRoute } from "astro";
import { mps, formerMps, clubColor, initials, photo, type Mp } from "../../../lib/data";
import { mpActivity } from "../../../lib/feed";
export function getStaticPaths() { return [...mps, ...formerMps].map((m) => ({ params: { id: m.id }, props: { m } })); }
export const GET: APIRoute = ({ props }) => {
  const m = (props as { m: Mp }).m;
  return new Response(JSON.stringify({ id: m.id, name: m.name, club: m.club, color: clubColor(m.club), ini: initials(m), photo: photo(m.id),
    items: mpActivity(m, 4).map((i) => ({ t: i.title.replace(`${m.name}: `, "").replace(`${m.name} `, ""), u: i.url, d: i.date.slice(0, 10), x: i.text.slice(0, 160), k: i.type })) }),
    { headers: { "content-type": "application/json" } });
};
