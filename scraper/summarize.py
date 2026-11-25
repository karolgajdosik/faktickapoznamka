"""AI summaries of longer debate speeches via GitHub Models (free, rate-limited).
Runs in GitHub Actions with the built-in GITHUB_TOKEN (permission models: read).
Newest speeches first; stops at the daily budget or on the first rate-limit answer.
Summaries are labelled as AI on the site and always link to the full transcript."""
import json, os, pathlib, sys, time, datetime, urllib.request, urllib.error

DATA = pathlib.Path("data"); OUT = DATA / "summaries.json"
MODEL = os.environ.get("SUMMARY_MODEL", "openai/gpt-4.1-mini")
PER_RUN = int(os.environ.get("SUMMARY_PER_RUN", "40"))
PER_DAY = int(os.environ.get("SUMMARY_PER_DAY", "120"))
MIN_CHARS = 1500  # roughly 2–3 minutes of speech
CHAIR = "Vstup predsedajúceho"
PROMPT = ("Si nestranný redaktor. Zhrň vystúpenie poslanca v Národnej rade SR v 2 až 3 vetách po slovensky. "
          "Uveď len hlavné body, ktoré rečník skutočne povedal, v tretej osobe (napr. „Rečník tvrdí…“, „Navrhuje…“). "
          "Nehodnoť, nepridávaj fakty ani kontext, ktoré v texte nie sú, nepoužívaj citácie dlhšie ako päť slov. "
          "Ak je text procedurálny alebo príliš krátky na zhrnutie, odpovedz iba slovom PROCEDURÁLNE.")

def call(text: str) -> str | None:
    body = json.dumps({"model": MODEL, "temperature": 0.2, "max_tokens": 220, "messages": [
        {"role": "system", "content": PROMPT}, {"role": "user", "content": text[:12000]}]}).encode()
    req = urllib.request.Request("https://models.github.ai/inference/chat/completions", data=body, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()

def main():
    if not os.environ.get("GITHUB_TOKEN"): print("no GITHUB_TOKEN, skipping"); return
    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    meta = out.setdefault("_meta", {"model": MODEL, "daily": {}})
    today = datetime.date.today().isoformat()
    meta["daily"] = {today: meta.get("daily", {}).get(today, 0)}
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
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} from GitHub Models, stopping ({e.read()[:200]!r})"); break
        except Exception as e:
            print(f"error {e!r}, stopping"); break
        meta["daily"][today] += 1; done += 1
        out[x["id"]] = {"s": None if not s or s.upper().startswith("PROCEDUR") else s, "at": today}
        time.sleep(4)  # stay well under the per-minute limit
    meta["model"] = MODEL
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print(f"summaries: {done} new, {len(todo) - done} waiting, today {meta['daily'][today]}")

if __name__ == "__main__":
    main()
