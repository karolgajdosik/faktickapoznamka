import type { APIRoute } from "astro";
import { mps, formerMps, type Mp } from "../../../lib/data";
import { rss, mpActivity } from "../../../lib/feed";
export function getStaticPaths() { return [...mps, ...formerMps].map((m) => ({ params: { id: m.id }, props: { m } })); }
export const GET: APIRoute = ({ props }) => {
  const m = (props as { m: Mp }).m;
  return new Response(rss(`${m.name} – faktická poznámka`, `/poslanci/${m.id}/`, `Vystúpenia a hlasovania proti klubu: ${m.name} (${m.club})`, mpActivity(m)),
    { headers: { "content-type": "application/rss+xml; charset=utf-8" } });
};
