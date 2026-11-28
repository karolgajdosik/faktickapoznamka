/// <reference types="@cloudflare/workers-types" />
// Static assets are served directly by Cloudflare (free, not counted as Worker requests).
// This Worker runs only for paths with no matching file: the www redirect and the newsletter API.
//
// Newsletter (double opt-in, GDPR):
//   POST /api/odber            {email, follows?, web?}  → stores a pending subscription, e-mails a confirmation link
//   GET  /api/odber/potvrdit?t=token                     → confirms (or applies a pending change of followed MPs)
//   GET  /api/odber/zrusit?t=token                       → deletes the subscription
// KV keys: e:<email> = Sub, t:<token> = <email>. Nothing else is stored; no IP addresses.
interface Env { ASSETS: Fetcher; ODBER?: KVNamespace; BREVO_API_KEY?: string; MAIL_FROM?: string }
interface Sub { s: "pending" | "ok"; t: string; f: string[]; pf?: string[]; c: string; ok?: string }

const SITE = "https://faktickapoznamka.sk";
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const back = (stav: string) => Response.redirect(`${SITE}/odber/?stav=${stav}`, 303);
const EMAIL = /^[^\s@<>"']{1,64}@[^\s@<>"']{1,190}\.[a-z]{2,24}$/i;

async function limited(req: Request): Promise<boolean> {
  // a few attempts per IP and 10 minutes, kept in the edge cache (no storage, nothing personal persisted)
  const ip = req.headers.get("cf-connecting-ip") ?? "x";
  const key = new Request(`${SITE}/__rl/${encodeURIComponent(ip)}/${Math.floor(Date.now() / 600000)}`);
  const cache = caches.default, hit = await cache.match(key);
  const n = hit ? Number(await hit.text()) : 0;
  if (n >= 5) return true;
  await cache.put(key, new Response(String(n + 1), { headers: { "cache-control": "max-age=600" } }));
  return false;
}

async function mail(env: Env, to: string, subject: string, html: string) {
  if (!env.BREVO_API_KEY) throw new Error("BREVO_API_KEY missing");
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST", headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify({ sender: { name: "faktickapoznamka.sk", email: env.MAIL_FROM || "upozornenia@mestovcislach.sk" }, to: [{ email: to }], subject, htmlContent: html, tags: ["odber-potvrdenie"] }),
  });
  if (!r.ok) throw new Error(`Brevo ${r.status}`);
}

const confirmHtml = (token: string, change: boolean) => `<!doctype html><html lang="sk"><body style="font-family:Arial,sans-serif;color:#1a2233;max-width:560px;margin:0 auto;padding:16px">
<h2 style="margin:0 0 12px">${change ? "Potvrďte zmenu odberu" : "Potvrďte odber"}</h2>
<p>Niekto (pravdepodobne vy) ${change ? "chce zmeniť sledovaných poslancov v" : "zadal túto adresu pre"} týždenný e-mail stránky <b>faktickapoznamka.sk</b>: zhrnutie týždňa v parlamente a novinky o poslancoch, ktorých sledujete.</p>
<p style="margin:24px 0"><a href="${SITE}/api/odber/potvrdit?t=${token}" style="background:#2f6fed;color:#fff;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:bold">${change ? "Potvrdiť zmenu" : "Potvrdiť odber"}</a></p>
<p style="color:#5b6577;font-size:13px">Ak ste o odber nežiadali, tento e-mail ignorujte; bez potvrdenia vám nič ďalšie nepošleme a adresu do 7 dní vymažeme.<br>Prevádzkovateľ: IT Future s. r. o., IČO 52 966 593 · <a href="${SITE}/ochrana-sukromia/#odber">Ochrana súkromia</a></p>
</body></html>`;

async function subscribe(req: Request, env: Env) {
  const kv = env.ODBER; if (!kv) return json({ ok: false, error: "Odber zatiaľ nie je zapnutý." }, 503);
  let b: { email?: string; follows?: unknown; web?: string };
  try { b = await req.json(); } catch { return json({ ok: false, error: "Neplatná požiadavka." }, 400); }
  if (b.web) return json({ ok: true }); // honeypot field filled by bots
  const email = String(b.email ?? "").trim().toLowerCase();
  if (!EMAIL.test(email)) return json({ ok: false, error: "Skontrolujte e-mailovú adresu." }, 400);
  if (await limited(req)) return json({ ok: false, error: "Príliš veľa pokusov, skúste to o pár minút." }, 429);
  const follows = (Array.isArray(b.follows) ? b.follows : []).map(String).filter((x) => /^\d{1,6}$/.test(x)).slice(0, 50);
  const old = await kv.get<Sub>(`e:${email}`, "json");
  const token = old?.t ?? crypto.randomUUID().replace(/-/g, "");
  let sub: Sub;
  if (old?.s === "ok") {
    if (follows.join() === old.f.join()) return json({ ok: true, already: true });
    sub = { ...old, pf: follows };                    // change of followed MPs waits for confirmation from the inbox
  } else sub = { s: "pending", t: token, f: follows, c: new Date().toISOString() };
  // pending entries expire after 7 days unless confirmed
  const ttl = sub.s === "pending" ? { expirationTtl: 7 * 86400 } : {};
  await kv.put(`e:${email}`, JSON.stringify(sub), ttl);
  await kv.put(`t:${token}`, email, ttl);
  try { await mail(env, email, sub.s === "ok" ? "Potvrďte zmenu odberu – faktickapoznamka.sk" : "Potvrďte odber – faktickapoznamka.sk", confirmHtml(token, sub.s === "ok")); }
  catch { return json({ ok: false, error: "E-mail sa nepodarilo odoslať, skúste to neskôr." }, 502); }
  return json({ ok: true, change: sub.s === "ok" });
}

async function confirm(url: URL, env: Env) {
  const kv = env.ODBER; const t = url.searchParams.get("t") ?? "";
  if (!kv || !/^[a-f0-9]{32}$/.test(t)) return back("neplatny");
  const email = await kv.get(`t:${t}`); if (!email) return back("neplatny");
  const sub = await kv.get<Sub>(`e:${email}`, "json"); if (!sub) return back("neplatny");
  if (sub.pf) { sub.f = sub.pf; delete sub.pf; }
  sub.s = "ok"; sub.ok ??= new Date().toISOString();
  await kv.put(`e:${email}`, JSON.stringify(sub));      // confirmed: no expiry
  await kv.put(`t:${t}`, email);
  return back("potvrdene");
}

async function unsubscribe(url: URL, env: Env) {
  const kv = env.ODBER; const t = url.searchParams.get("t") ?? "";
  if (!kv || !/^[a-f0-9]{32}$/.test(t)) return back("neplatny");
  const email = await kv.get(`t:${t}`);
  if (email) await Promise.all([kv.delete(`e:${email}`), kv.delete(`t:${t}`)]);
  return back("zrusene");
}

export default {
  async fetch(req: Request, env: Env) {
    const url = new URL(req.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/odber" && req.method === "POST") return subscribe(req, env);
    if (url.pathname === "/api/odber/potvrdit") return confirm(url, env);
    if (url.pathname === "/api/odber/zrusit") {
      // one-click unsubscribe (RFC 8058) posts here; a GET from the e-mail link works too
      return unsubscribe(url, env);
    }
    return env.ASSETS.fetch(req);
  },
} satisfies ExportedHandler<Env>;
