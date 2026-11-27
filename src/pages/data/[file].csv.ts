import type { APIRoute } from "astro";
import { tables, toCsv, type Table } from "../../lib/opendata";
export function getStaticPaths() { return tables().map((t) => ({ params: { file: t.file }, props: { t } })); }
export const GET: APIRoute = ({ props }) => new Response(toCsv((props as { t: Table }).t), { headers: { "content-type": "text/csv; charset=utf-8" } });
