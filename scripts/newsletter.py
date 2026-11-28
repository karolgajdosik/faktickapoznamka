"""Monday newsletter for confirmed subscribers: last week in parliament + news about the MPs each reader follows.

Subscribers live in Cloudflare Workers KV (written by worker/index.ts after double opt-in). This script runs in
GitHub Actions, reads them through the Cloudflare API, builds one e-mail per reader from the repository data and
sends them in one Brevo call (messageVersions). Sent only after a week with votes.

Environment:
  CF_API_TOKEN, CLOUDFLARE_ACCOUNT_ID – token needs Account > Workers KV Storage > Read
  ODBER_KV_ID                          – (optional) KV namespace id; read from wrangler.jsonc otherwise
  BREVO_API_KEY                        – transactional e-mail
  NEWSLETTER_FROM                      – (optional) verified sender address
  DRY_RUN=1                            – build and print, send nothing
"""
import datetime as dt, html, json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import requests

D = Path(__file__).resolve().parent.parent / "data"
SITE = "https://faktickapoznamka.sk"
TZ = dt.timezone(dt.timedelta(hours=1))
FROM = {"name": "faktickapoznamka.sk", "email": os.environ.get("NEWSLETTER_FROM", "").strip() or "upozornenia@mestovcislach.sk"}
BREVO_DAILY = 280  # free plan: 300 e-mails a day, keep a margin for confirmations

def load(p): return json.loads((D / p).read_text(encoding="utf-8"))
def esc(s): return html.escape(str(s), quote=True)
def pl(n, a, b, c): return a if n == 1 else b if 2 <= n <= 4 else c
def is_presence(t): return re.match(r"^prezentácia(\s+č\.\s*\d+)?\.?$", t.strip(), re.I)
def day(iso): return dt.datetime.fromisoformat(iso).astimezone(TZ).date()

def week_range(today: dt.date):
    mon = today - dt.timedelta(days=today.weekday() + 7)
    return mon, mon + dt.timedelta(days=6)

def iso_key(d: dt.date):
    y, w, _ = d.isocalendar(); return f"{y}-W{w:02d}"

def build_week(today: dt.date):
    mon, sun = week_range(today)
    mps = {m["id"]: m for m in load("mps.json")}
    votes = []
    for f in (D / "votes").glob("*.json"):
        v = json.loads(f.read_text(encoding="utf-8"))
        if is_presence(v["title"]): continue
        if mon <= day(v["datetime"]) <= sun: votes.append(v)
    votes.sort(key=lambda v: v["datetime"])
    speeches = []
    for f in (D / "speeches").glob("*.json"):
        for s in json.loads(f.read_text(encoding="utf-8")):
            if s.get("start") and mon <= day(s["start"]) <= sun and s.get("kind") != "Vstup predsedajúceho": speeches.append(s)
    return mon, sun, mps, votes, speeches

def club_majority(v, mps):
    t = defaultdict(Counter)
    for i, c in v["votes"].items():
        if c in "ZP?":
            cl = (v.get("clubs") or {}).get(i) or mps.get(i, {}).get("club")
            if cl and cl != "Nezaradení": t[cl][c] += 1
    out = {}
    for cl, cnt in t.items():
        top = cnt.most_common(2)
        if len(top) == 1 or top[0][1] > top[1][1]: out[cl] = top[0][0]
    return out

def is_final(v): return bool(re.search(r"ako celku|tretie čítanie|3\. čítanie", (v.get("detail") or "") + " " + v["title"], re.I))
def law_title(t):
    t = re.sub(r"\s*\(tl\.?\s*\d+\)\s*", " ", re.sub(r"^.*?(Vládny návrh|Návrh)", r"\1", t))
    return re.sub(r"\s*[-–]\s*(prvé|druhé|tretie) čítanie.*$", "", t, flags=re.I).strip()

def cut(t, n):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"

def margin(v):
    present = 150 - v["counts"]["0"]; need = present // 2 + 1
    return v["counts"]["Z"] - need + 1 if v["passed"] else need - v["counts"]["Z"]

def fmt_dur(s): h, m = divmod(round(s / 60), 60); return f"{h} h {m:02d} min" if h else f"{m} min"

def summary_html(mon, sun, votes, speeches, mps):
    passed = [v for v in votes if v["passed"]]
    finals = [v for v in votes if is_final(v)]
    close = sorted([v for v in votes if v["passed"] is not None and margin(v) > 0], key=margin)[:3]
    absent, rebels = Counter(), Counter()
    for v in votes:
        mj = club_majority(v, mps)
        for i, c in v["votes"].items():
            if c == "0": absent[i] += 1
            cl = (v.get("clubs") or {}).get(i) or mps.get(i, {}).get("club")
            if cl in mj and c in "ZP?" and c != mj[cl]: rebels[i] += 1
    key = iso_key(mon)
    li = lambda xs: "".join(f'<li style="margin:4px 0">{x}</li>' for x in xs)
    def vote_link(v, text): return f'<a href="{SITE}/hlasovania/{v["id"]}/" style="color:#2f6fed">{esc(text)}</a>'
    parts = [
        f'<p style="font-size:15px">{len(votes)} {pl(len(votes), "hlasovanie", "hlasovania", "hlasovaní")} · {len(passed)} schválených · '
        f'{sum(1 for v in finals if v["passed"])} prijatých zákonov · {len(speeches)} vystúpení</p>'
    ]
    if finals:
        parts.append('<h3 style="margin:20px 0 6px">Záverečné hlasovania o zákonoch</h3><ul style="padding-left:18px">' + li(
            f'{"✅" if v["passed"] else "❌"} {vote_link(v, cut(law_title(v["title"]), 150))} <span style="color:#5b6577">({v["counts"]["Z"]} za, {v["counts"]["P"]} proti)</span>' for v in finals[:12]) + "</ul>")
    if close:
        parts.append('<h3 style="margin:20px 0 6px">Najtesnejšie hlasovania</h3><ul style="padding-left:18px">' + li(
            f'{vote_link(v, cut(law_title(v["title"]), 130))} <span style="color:#5b6577">· rozhodlo {margin(v)} {pl(margin(v), "hlas", "hlasy", "hlasov")}</span>' for v in close) + "</ul>")
    top_abs = [(mps[i], n) for i, n in absent.most_common(5) if i in mps]
    if top_abs:
        parts.append('<h3 style="margin:20px 0 6px">Najviac chýbali</h3><p>' + " · ".join(f'<a href="{SITE}/poslanci/{m["id"]}/" style="color:#2f6fed">{esc(m["name"])}</a> ({n}×)' for m, n in top_abs) + "</p>")
    top_reb = [(mps[i], n) for i, n in rebels.most_common(5) if i in mps]
    if top_reb:
        parts.append('<h3 style="margin:20px 0 6px">Hlasovali proti svojmu klubu</h3><p>' + " · ".join(f'<a href="{SITE}/poslanci/{m["id"]}/" style="color:#2f6fed">{esc(m["name"])}</a> ({n}×)' for m, n in top_reb) + "</p>")
    parts.append(f'<p style="margin:20px 0"><a href="{SITE}/tyzden/{key}/" style="background:#2f6fed;color:#fff;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:bold">Celé zhrnutie týždňa</a></p>')
    return "".join(parts), absent, rebels

def follow_html(ids, votes, speeches, mps, absent, rebels):
    rows = []
    talk = defaultdict(lambda: [0, 0])
    for s in speeches:
        if s.get("mpId"): t = talk[s["mpId"]]; t[0] += s.get("dur", 0); t[1] += 1
    for i in ids:
        m = mps.get(i)
        if not m: continue
        n_votes = sum(1 for v in votes if i in v["votes"])
        here = sum(1 for v in votes if v["votes"].get(i) not in (None, "0"))
        bits = [f"hlasoval v {here} z {n_votes}" if n_votes else "tento týždeň nehlasoval"]
        if rebels.get(i): bits.append(f'{rebels[i]}× proti klubu')
        if talk[i][1]: bits.append(f'{talk[i][1]} {pl(talk[i][1], "vystúpenie", "vystúpenia", "vystúpení")} ({fmt_dur(talk[i][0])})')
        rows.append(f'<li style="margin:6px 0"><a href="{SITE}/poslanci/{i}/" style="color:#2f6fed;font-weight:bold">{esc(m["name"])}</a> <span style="color:#5b6577">({esc(m["club"])})</span>: {", ".join(bits)}</li>')
    return ('<h3 style="margin:24px 0 6px">Poslanci, ktorých sledujete</h3><ul style="padding-left:18px">' + "".join(rows) + "</ul>") if rows else ""

def wrap(mon, sun, body, token):
    unsub = f"{SITE}/api/odber/zrusit?t={token}"
    return (f'<!doctype html><html lang="sk"><body style="font-family:Arial,sans-serif;color:#1a2233;max-width:600px;margin:0 auto;padding:16px">'
            f'<p style="color:#5b6577;margin:0">faktickapoznamka.sk · Týždeň v parlamente</p>'
            f'<h2 style="margin:4px 0 12px">{mon.day}. {mon.month}. – {sun.day}. {sun.month}. {sun.year}</h2>{body}'
            f'<hr style="border:0;border-top:1px solid #e3e7ef;margin:24px 0"><p style="color:#5b6577;font-size:12px">Údaje z oficiálnych záznamov NR SR; počty sú štatistický výpočet, nie hodnotenie. '
            f'Tento e-mail dostávate, lebo ste si potvrdili odber na faktickapoznamka.sk. <a href="{unsub}">Odhlásiť sa</a> · '
            f'<a href="{SITE}/ochrana-sukromia/#odber">Ochrana súkromia</a><br>Prevádzkovateľ: IT Future s. r. o., IČO 52 966 593</p></body></html>'), unsub

def subscribers():
    acc, tok = os.environ["CLOUDFLARE_ACCOUNT_ID"].strip(), os.environ["CF_API_TOKEN"].strip()
    ns = os.environ.get("ODBER_KV_ID", "").strip() or re.search(r'"binding":\s*"ODBER",\s*"id":\s*"([0-9a-f]{32})"', (D.parent / "wrangler.jsonc").read_text()).group(1)
    h = {"Authorization": f"Bearer {tok}"}
    base = f"https://api.cloudflare.com/client/v4/accounts/{acc}/storage/kv/namespaces/{ns}"
    keys, cursor = [], None
    while True:
        r = requests.get(f"{base}/keys", headers=h, params={"prefix": "e:", "limit": 1000, **({"cursor": cursor} if cursor else {})}, timeout=30)
        r.raise_for_status(); d = r.json()
        keys += [k["name"] for k in d["result"]]
        cursor = (d.get("result_info") or {}).get("cursor")
        if not cursor: break
    out = []
    for i in range(0, len(keys), 100):
        r = requests.post(f"{base}/bulk/get", headers=h, json={"keys": keys[i:i + 100], "type": "json"}, timeout=30)
        r.raise_for_status()
        for k, v in (r.json()["result"]["values"] or {}).items():
            if v and v.get("s") == "ok": out.append((k[2:], v))
    return out

def main():
    today = dt.datetime.now(TZ).date()
    mon, sun, mps, votes, speeches = build_week(today)
    if not votes:
        print(f"no votes {mon}–{sun}, nothing to send"); return 0
    body, absent, rebels = summary_html(mon, sun, votes, speeches, mps)
    subs = subscribers()
    print(f"{len(votes)} votes, {len(subs)} confirmed subscribers")
    if not subs: return 0
    subject = f"Týždeň v parlamente {mon.day}. – {sun.day}. {sun.month}.: {sum(1 for v in votes if v['passed'])} schválených, {sum(1 for v in votes if is_final(v) and v['passed'])} zákonov"
    versions = []
    for email, s in subs[:BREVO_DAILY]:
        html_body, unsub = wrap(mon, sun, body + follow_html(s.get("f") or [], votes, speeches, mps, absent, rebels), s["t"])
        versions.append({"to": [{"email": email}], "htmlContent": html_body,
                         "headers": {"List-Unsubscribe": f"<{unsub}>", "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"}})
    if len(subs) > BREVO_DAILY: print(f"::warning::{len(subs)} subscribers, only {BREVO_DAILY} sent (Brevo free daily limit)")
    if os.environ.get("DRY_RUN"):
        print(versions[0]["htmlContent"][:2000]); return 0
    key = os.environ["BREVO_API_KEY"].strip()
    for i in range(0, len(versions), 900):
        r = requests.post("https://api.brevo.com/v3/smtp/email", headers={"api-key": key, "content-type": "application/json", "accept": "application/json"}, timeout=60,
                          json={"sender": FROM, "subject": subject, "htmlContent": versions[i]["htmlContent"], "messageVersions": versions[i:i + 900], "tags": ["tyzden"]})
        if r.status_code >= 300: print(r.status_code, r.text[:300]); return 1
    print(f"sent {len(versions)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
