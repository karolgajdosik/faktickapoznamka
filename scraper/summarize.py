"""AI summaries (bills from their explanatory memorandum, longer debate speeches) via Cloudflare Workers AI.

GitHub Models, used before, was retired on 30 July 2026. Workers AI on the free plan gives 10,000 neurons
a day at no charge and refuses further requests (no billing), so a run simply stops at the limit.
Needs CF_API_TOKEN with the permission Account > Workers AI > Read and CLOUDFLARE_ACCOUNT_ID.
Newest items first. Summaries are labelled as AI on the site and always link to the full source."""
import json, re, os, pathlib, sys, time, datetime, urllib.request, urllib.error

DATA = pathlib.Path("data"); OUT = DATA / "summaries.json"
MODEL = os.environ.get("SUMMARY_MODEL", "@cf/meta/llama-3.3-70b-instruct-fp8-fast")
PER_RUN = int(os.environ.get("SUMMARY_PER_RUN", "12"))
PER_DAY = int(os.environ.get("SUMMARY_PER_DAY", "60"))  # ~120 neurons each, under the free 10,000/day
MIN_CHARS = 1500  # roughly 2–3 minutes of speech
CHAIR = "Vstup predsedajúceho"
PROMPT = ("Si nestranný slovenský redaktor. Zhrň vystúpenie poslanca v Národnej rade SR v 2 až 3 krátkych vetách spisovnou slovenčinou (nie češtinou). "
          "Začni slovom „Rečník“ alebo „Rečníčka“ podľa toho, kto hovorí, bez mena. Používaj slovesá tvrdí, navrhuje (navrhuje, aby…), kritizuje, pýta sa. "
          "Uveď len hlavné body, ktoré rečník skutočne povedal, v tretej osobe (napr. „Rečník tvrdí…“, „Navrhuje…“). "
          "Nehodnoť, nepridávaj fakty ani kontext, ktoré v texte nie sú, nepoužívaj citácie dlhšie ako päť slov. Expresívne alebo urážlivé výrazy rečníka nepreberaj, opíš ich neutrálne. Píš spisovnou slovenčinou s diakritikou. "
          "Ak je text procedurálny alebo príliš krátky na zhrnutie, odpovedz iba slovom PROCEDURÁLNE.")

LAW_PROMPT = ("Si nestranný redaktor. Z dôvodovej správy k návrhu zákona v Národnej rade SR napíš po slovensky 3 až 4 krátke vety "
              "jednoduchou rečou pre bežného čitateľa: čo návrh mení a koho sa týka; dátum účinnosti uveď len vtedy, ak je v texte presne uvedený, inak o ňom nepíš vôbec. Píš spisovnou slovenčinou (nie češtinou). "
              "Nehodnoť, nepreberaj argumenty navrhovateľa ako fakty (píš „návrh má…“, „podľa navrhovateľa…“), nepridávaj nič, čo v texte nie je, "
              "a nepoužívaj citácie dlhšie ako päť slov. Ak text nestačí na zhrnutie, odpovedz iba slovom NEDOSTATOČNÉ.")


# Frequent slips of the free model in Slovak (Czech forms, typos); applied to every summary before saving.
FIXES = [(r"\bministera\b", "ministra"), (r"\bMinistera\b", "Ministra"), (r"\bRečníkk([ay])\b", r"Rečníčk\1"), (r"\bnávrhům\b", "návrhom"),
         (r"\bpriznat\b", "priznať"), (r"\btieto poslanci\b", "títo poslanci"), (r"\bTieto poslanci\b", "Títo poslanci"),
         (r"\bkterý\b", "ktorý"), (r"\bkterá\b", "ktorá"), (r"\bkteré\b", "ktoré"), (r"\bjejich\b", "ich"), (r"\bbude moci\b", "bude môcť"),
         (r"\bnavrhuje, že\b", "navrhuje, aby"), (r"\bv rámci\s+rámca\b", "v rámci"), (r"\s+([,.])", r"\1")]

def fix_sk(t: str | None) -> str | None:
    if not t: return t
    for a, b in FIXES: t = re.sub(a, b, t)
    return t

class Stop(Exception):
    pass

def call(text: str, prompt: str = PROMPT, max_tokens: int = 220) -> str | None:
    acc, tok = os.environ["CLOUDFLARE_ACCOUNT_ID"].strip(), os.environ["CF_API_TOKEN"].strip()
    body = json.dumps({"model": MODEL, "temperature": 0.2, "max_tokens": max_tokens, "messages": [
        {"role": "system", "content": prompt}, {"role": "user", "content": text[:9000]}]}).encode()
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/v1/chat/completions", data=body, headers={
        "Authorization": f"Bearer {tok}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "faktickapoznamka-summaries"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read(); status = r.status; ctype = r.headers.get("content-type", "")
    except urllib.error.HTTPError as e:
        raise Stop(f"HTTP {e.code} from Workers AI: {e.read()[:300]!r}")
    try:
        d = json.loads(raw)
    except ValueError:
        raise Stop(f"non-JSON answer (HTTP {status}, {ctype}, {len(raw)} bytes): {raw[:300]!r}")
    if "choices" not in d:
        raise Stop(f"unexpected answer: {str(d)[:300]}")
    return fix_sk((d["choices"][0]["message"].get("content") or "").strip())

def laws(meta, today, budget):
    """Plain-language summaries of bills from their explanatory memorandum (data/extra/lawtext)."""
    out_f = DATA / "lawsummaries.json"
    out = json.loads(out_f.read_text()) if out_f.exists() else {}
    done = 0
    files = sorted((DATA / "extra" / "lawtext").glob("*.txt"), key=lambda f: int(f.stem), reverse=True)
    for f in files:
        if done >= budget or meta["daily"][today] >= PER_DAY: break
        t = f.stem; txt = f.read_text(encoding="utf-8")
        if t in out or len(txt) < 400: continue
        try:
            s = call(txt, LAW_PROMPT, 260)
        except Stop as e:
            print(e); break
        meta["daily"][today] += 1; done += 1
        out[t] = {"s": None if not s or s.upper().startswith("NEDOSTAT") else s, "src": txt.split("\n", 1)[0].lstrip("# ").strip(), "at": today}
        time.sleep(1)
    out_f.write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print(f"law summaries: {done} new, {sum(1 for v in out.values() if v.get('s'))} total")
    return done

def main():
    if not (os.environ.get("CF_API_TOKEN") and os.environ.get("CLOUDFLARE_ACCOUNT_ID")): print("no CF_API_TOKEN / CLOUDFLARE_ACCOUNT_ID, skipping"); return
    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    meta = out.setdefault("_meta", {"model": MODEL, "daily": {}})
    today = datetime.date.today().isoformat()
    meta["daily"] = {today: meta.get("daily", {}).get(today, 0)}
    laws(meta, today, max(PER_RUN // 2, 10))
    todo = []
    for f in DATA.glob("speeches/*.json"):
        for x in json.loads(f.read_text()):
            if x.get("text") and len(x["text"]) >= MIN_CHARS and x.get("kind") != CHAIR and x["id"] not in out:
                todo.append(x)
    todo.sort(key=lambda x: x["start"], reverse=True)
    done = 0
    for x in todo:
        if done >= PER_RUN or meta["daily"][today] >= PER_DAY: break
        try:
            s = call(f"Rečník: {x['speaker']} ({x.get('role','')})\nTyp: {x.get('kind') or 'vystúpenie'}\n\n{x['text']}")
        except Stop as e:
            print(e); break
        except Exception as e:
            print(f"error {e!r}, stopping"); break
        meta["daily"][today] += 1; done += 1
        out[x["id"]] = {"s": None if not s or s.upper().startswith("PROCEDUR") else s, "at": today}
        time.sleep(1)
    meta["model"] = MODEL
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print(f"summaries: {done} new, {len(todo) - done} waiting, today {meta['daily'][today]}")

if __name__ == "__main__":
    main()
