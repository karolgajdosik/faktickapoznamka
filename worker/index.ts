/// <reference types="@cloudflare/workers-types" />
// Serves the static site (ASSETS) and /api/live: what is being debated right now.
// /api/live fetches nrsr.sk on demand and caches it ~60 s at the edge, so nrsr.sk
// sees roughly one request per minute per Cloudflare location, no matter the traffic.

interface Env { ASSETS: Fetcher }

const NRSR_HOME = "https://www.nrsr.sk/web/";
const UA = "faktickapoznamka.sk-bot/0.1 (+https://faktickapoznamka.sk/o-projekte/)";

function inSessionHours(d = new Date()) {
  const p = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Bratislava", weekday: "short", hour: "numeric", hour12: false }).formatToParts(d);
  const wd = p.find((x) => x.type === "weekday")!.value, h = Number(p.find((x) => x.type === "hour")!.value);
  return !["Sat", "Sun"].includes(wd) && h >= 8 && h < 21;
}

async function live(ctx: ExecutionContext): Promise<Response> {
  const cache = caches.default;
  const key = new Request("https://faktickapoznamka.sk/__live-v1");
  const hit = await cache.match(key);
  if (hit) return hit;

  let body: Record<string, unknown> = { live: false };
  if (inSessionHours()) {
    try {
      const r = await fetch(NRSR_HOME, { headers: { "user-agent": UA }, cf: { cacheTtl: 0 } });
      const text = (await r.text()).replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<[^>]+>/g, "\n")
        .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/[ \t]+/g, " ");
      // TODO calibrate against probe/home.html — section headed "Priebeh rokovania NR SR".
      const m = text.match(/Priebeh rokovania NR SR\s*\n[\s\n]*([^\n]{10,400})/);
      if (m) body = { live: true, item: m[1].trim(), url: "https://tv.nrsr.sk/" };
    } catch { body = { live: false, error: "nrsr_unreachable" }; }
  }
  body.checkedAt = new Date().toISOString();
  const res = new Response(JSON.stringify(body), {
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=60" },
  });
  ctx.waitUntil(cache.put(key, res.clone()));
  return res;
}

export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(req.url);
    if (url.hostname === "www.faktickapoznamka.sk") {
      url.hostname = "faktickapoznamka.sk"; return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/live") return live(ctx);
    return env.ASSETS.fetch(req);
  },
} satisfies ExportedHandler<Env>;
