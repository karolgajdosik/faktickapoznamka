"""Scrape votes of the current term.

Vote IDs are not contiguous, so we discover them from the per-session search
grid on nrsr.sk and download only the ones we don't have yet.
Usage: python scraper/run.py            # newest sessions only (hourly)
       python scraper/run.py --all      # every session of the term (backfill)
"""
import argparse, json, pathlib, sys, datetime, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse

DATA = pathlib.Path("data"); VOTES = DATA / "votes"; SPEECHES = DATA / "speeches"
TERM = 9

def save(mps: dict, meta: dict):
    (DATA / "mps.json").write_text(json.dumps(sorted(mps.values(), key=lambda m: m["sortName"]), ensure_ascii=False, indent=1))
    meta["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (DATA / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true"); ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--speech-minutes", type=float, default=25, help="time budget for the debate scrape")
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
                mps[pid] = {**mps.get(pid, {}), "id": pid, "name": display, "sortName": sn, "club": m["club"]}
            (VOTES / f"{vid}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
            known.add(vid); saved += 1
            print(f"{vid}: {v['title'][:70]}", flush=True)
            if saved % 50 == 0: save(mps, meta)
        if saved >= a.max: break
        if sess not in latest: done.add(sess)
        meta["sessionsDone"] = sorted(done)
    save(mps, meta)
    print(f"saved {saved} votes")

    # Older files saved before we stored per-vote club membership: refetch gradually.
    budget = min(300, a.max - saved)
    for f in sorted(VOTES.glob("*.json")):
        if budget <= 0: break
        old_v = json.loads(f.read_text())
        if "clubs" in old_v: continue
        r = nrsr.get({"sid": "schodze/hlasovanie/hlasklub", "ID": f.stem})
        v = parse.parse_vote(r.text, f.stem) if r.ok else None
        budget -= 1
        if v and v["datetime"]:
            v.pop("_mps"); f.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    save(mps, meta)

    scrape_speeches(sessions, meta, a.speech_minutes)
    save(mps, meta)

    # Profiles (birth date, residence, region, party on the ballot): refresh weekly.
    week_ago = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat()
    stale = [m for m in mps.values() if m.get("profileAt", "") < week_ago][:60]
    for m in stale:
        r = nrsr.get({"sid": "poslanci/poslanec", "PoslanecID": m["id"], "CisObdobia": TERM})
        prof = parse.parse_mp(r.text, m["id"]) if r.ok else None
        if prof:
            m.update({k: prof.get(k) for k in ("title", "party", "born", "city", "region")})
            m["profileAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if stale:
        save(mps, meta); print(f"profiles refreshed: {len(stale)}")

def scrape_speeches(sessions: list[int], meta: dict, minutes: float):
    """Debate transcripts per session. Texts appear days after the speech (authorisation),
    so the newest sessions are re-read on every run; older ones once."""
    SPEECHES.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + minutes * 60
    done = set(meta.get("speechSessionsDone", []))
    regular = [s for s in sessions if s < 1000]
    latest = regular[-2:]
    todo = latest[::-1] + [s for s in reversed(regular) if s not in done and s not in latest]
    for sess in todo:
        if time.time() > deadline: break
        f = SPEECHES / f"{sess}.json"
        old = {x["id"]: x for x in json.loads(f.read_text())} if f.exists() else {}
        items = nrsr.session_speeches(sess, TERM, deadline=deadline)
        complete = time.time() <= deadline
        for x in items:
            prev = old.get(x["id"])
            if prev and prev.get("text") and not x["text"]: x["text"] = prev["text"]  # never lose text
            old[x["id"]] = x
        data = sorted(old.values(), key=lambda x: (x["start"], x["id"]))
        f.write_text(json.dumps(data, ensure_ascii=False, indent=0))
        print(f"speeches {sess}: {len(items)} read, {len(data)} stored{'' if complete else ' (partial)'}", flush=True)
        if complete and sess not in latest: done.add(sess)
        meta["speechSessionsDone"] = sorted(done)

if __name__ == "__main__":
    main()
