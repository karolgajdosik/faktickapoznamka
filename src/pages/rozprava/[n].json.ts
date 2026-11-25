// Full transcripts per session, fetched on demand by the session page ("Celý prepis").
import type { APIRoute } from "astro";
import { speechesBySession } from "../../lib/data";
export function getStaticPaths() { return [...speechesBySession.keys()].map((n) => ({ params: { n: String(n) } })); }
export const GET: APIRoute = ({ params }) => {
  const list = speechesBySession.get(Number(params.n)) ?? [];
  return new Response(JSON.stringify(Object.fromEntries(list.map((x) => [x.id, x.text]))), { headers: { "content-type": "application/json" } });
};
