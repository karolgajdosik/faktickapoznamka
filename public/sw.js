// faktická poznámka – service worker
// • Hashed build assets (/_astro/…), fonts and photos: cache-first (immutable; a new build has new URLs).
// • Pages (HTML) and data (JSON): network-first with a 4 s timeout; on timeout/offline serve the
//   last stored copy and tell the page {type:"stale"} so it can show a notice.
// • Never store redirects or error responses, never touch /api/ or /version.json.
const ASSETS = "fp-assets-v1";
const PAGES = "fp-pages-v1";
const MAX_ASSETS = 150;

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== ASSETS && k !== PAGES) await caches.delete(k);
    await self.clients.claim();
  })());
});

const storable = (res) => res && res.ok && res.type === "basic" && !res.redirected;
const isAsset = (p) => p.startsWith("/_astro/") || p.startsWith("/foto/") || /\.(woff2?|svg|png|ico)$/.test(p);

async function prune(cache) {
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_ASSETS; i++) await cache.delete(keys[i]); // oldest first
}

async function cacheFirst(req) {
  const cache = await caches.open(ASSETS);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (storable(res)) { await cache.put(req, res.clone()); prune(cache); }
  return res;
}

async function notifyStale(clientId) {
  const ids = clientId ? [await self.clients.get(clientId)] : await self.clients.matchAll({ type: "window" });
  for (const c of ids) if (c) c.postMessage({ type: "stale" });
}

async function networkFirst(e) {
  const req = e.request;
  const cache = await caches.open(PAGES);
  const net = fetch(req).then(async (res) => {
    if (storable(res)) await cache.put(req, res.clone());
    return res;
  });
  e.waitUntil(net.catch(() => {})); // let a slow response still refresh the cache
  const timeout = new Promise((resolve) => setTimeout(() => resolve(null), 4000));
  try {
    const res = await Promise.race([net, timeout]);
    if (res) return res;
  } catch { /* offline */ }
  const hit = await cache.match(req);
  if (hit) { notifyStale(e.resultingClientId || e.clientId); return hit; }
  try { return await net; } catch {
    return new Response("<!doctype html><meta charset=utf-8><title>Offline</title><p style='font-family:system-ui;padding:2rem'>Ste offline a táto stránka ešte nie je uložená. Skúste to znova po pripojení.</p>",
      { status: 503, headers: { "content-type": "text/html; charset=utf-8" } });
  }
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/") || url.pathname === "/version.json" || url.pathname === "/sw.js") return;
  if (isAsset(url.pathname)) { e.respondWith(cacheFirst(req)); return; }
  const html = req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html");
  if (html || url.pathname.endsWith(".json")) e.respondWith(networkFirst(e));
});
