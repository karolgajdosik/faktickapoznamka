"""Scrape votes of the current term.

Vote IDs are not contiguous, so we discover them from the per-session search
grid on nrsr.sk and download only the ones we don't have yet.
Usage: python scraper/run.py            # newest sessions only (hourly)
       python scraper/run.py --all      # every session of the term (backfill)
"""
import argparse, json, pathlib, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse

DATA = pathlib.Path("data"); VOTES = DATA / "votes"
TERM = 9

def save(mps: dict, meta: dict):
    (DATA / "mps.json").write_text(json.dumps(sorted(mps.values(), key=lambda m: m["sortName"]), ensure_ascii=False, indent=1))
    meta["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (DATA / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true"); ap.add_argument("--max", type=int, default=400)
    a = ap.parse_args()
    VOTES.mkdir(parents=True, exist_ok=True)
    meta = json.loads((DATA / "meta.json").read_text())
    if meta.get("demo"):
        print("Removing demo data"); [p.unlink() for p in VOTES.glob("*.json")]
        meta = {"demo": False, "term": TERM}; (DATA / "mps.json").write_text("[]")
    meta.pop("lastVoteId", None)
    mps = {m["id"]: m for m in json.loads((DATA / "mps.json").read_text())}

    home = nrsr.get(url=nrsr.HOME)
    if not home.ok: sys.exit("Blocked by nrsr.sk bot check, stopping")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    item = parse.parse_live(home.text)
    old = json.loads((DATA / "live.json").read_text()) if (DATA / "live.json").exists() else {}
    if item != old.get("item"):  # write only on change to keep commits (and deploys) rare
        (DATA / "live.json").write_text(json.dumps({"item": item, "since": now}, ensure_ascii=False, indent=1))

    sessions = nrsr.session_numbers(TERM)
    if not sessions: sys.exit("No sessions found (page layout changed?)")
    known = {p.stem for p in VOTES.glob("*.json")}
    done = set(meta.get("sessionsDone", []))
    regular = [s for s in sessions if s < 1000]
    latest = regular[-2:]  # an ongoing session + the previous one
    todo = [s for s in sessions if a.all and s not in done or s in latest or s not in done and s > max(done or {0})]
    print(f"sessions: {len(sessions)}, scanning {todo}", flush=True)

    saved = 0
    for sess in todo:
        ids = nrsr.session_vote_ids(sess, TERM)
        new = [i for i in ids if i not in known]
        print(f"session {sess}: {len(ids)} votes, {len(new)} new", flush=True)
        for vid in new:
            if saved >= a.max: break
            r = nrsr.get({"sid": "schodze/hlasovanie/hlasklub", "ID": vid})
            if not r.ok and nrsr.is_challenge(r.url, r.text): sys.exit("Blocked by nrsr.sk bot check, stopping")
            v = parse.parse_vote(r.text, vid) if r.ok else None
            if not v or not v["datetime"]:
                print(f"{vid}: no per-MP data (secret or non-electronic vote?)", flush=True); continue
            for pid, m in v.pop("_mps").items():
                display, sn = parse.sort_name(m["rawName"])
                mps[pid] = {"id": pid, "name": display, "sortName": sn, "club": m["club"]}
            (VOTES / f"{vid}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
            known.add(vid); saved += 1
            print(f"{vid}: {v['title'][:70]}", flush=True)
            if saved % 50 == 0: save(mps, meta)
        if saved >= a.max: break
        if sess not in latest: done.add(sess)
        meta["sessionsDone"] = sorted(done)
    save(mps, meta)
    print(f"saved {saved} votes")

if __name__ == "__main__":
    main()
