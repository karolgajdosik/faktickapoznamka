import type { APIRoute } from "astro";
import { versionInfo } from "../lib/build";
export const GET: APIRoute = () => new Response(JSON.stringify(versionInfo), { headers: { "content-type": "application/json" } });
