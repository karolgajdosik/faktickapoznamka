"""Incremental scrape: walks vote IDs upward from the last known one and stores
each vote as data/votes/<id>.json. MPs and clubs are derived from vote pages.
Usage: python scraper/run.py [--start ID] [--max N]"""
import argparse, json, pathlib, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse

DATA = pathlib.Path("data"); VOTES = DATA / "votes"
MISS_LIMIT = 40  # IDs are global and can have gaps (secret votes, other bodies)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int); ap.add_argument("--max", type=int, default=400)
    a = ap.parse_args()
    meta = json.loads((DATA / "meta.json").read_text())
    if meta.get("demo"):
        print("Removing demo data"); [p.unlink() for p in VOTES.glob("*.json")]
        meta = {"demo": False, "term": 9, "lastVoteId": None}; (DATA / "mps.json").write_text("[]")
    mps = {m["id"]: m for m in json.loads((DATA / "mps.json").read_text())}
    start = a.start or (int(meta["lastVoteId"]) + 1 if meta.get("lastVoteId") else None)
    if not start: sys.exit("No start ID: run with --start <vote id> (see probe/REPORT.md)")
    vid, misses, saved = start, 0, 0
    while misses < MISS_LIMIT and saved < a.max:
        r = nrsr.get({"sid": "schodze/hlasovanie/hlasklub", "ID": vid})
        v = parse.parse_vote(r.text, str(vid)) if r.ok else None
        if not r.ok and nrsr.is_challenge(r.url, r.text): sys.exit("Blocked by nrsr.sk bot check, stopping")
        if v and v["datetime"]:
            for pid, m in v.pop("_mps").items():
                display, sn = parse.sort_name(m["rawName"])
                mps[pid] = {"id": pid, "name": display, "sortName": sn, "club": m["club"]}
            (VOTES / f"{vid}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
            meta["lastVoteId"] = str(vid); saved += 1; misses = 0
            print(f"{vid}: {v['title'][:70]}")
        else:
            misses += 1
        vid += 1
    (DATA / "mps.json").write_text(json.dumps(sorted(mps.values(), key=lambda m: m["sortName"]), ensure_ascii=False, indent=1))
    if saved: meta["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    meta.setdefault("updatedAt", datetime.datetime.now(datetime.timezone.utc).isoformat())
    (DATA / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"saved {saved} votes, last {meta.get('lastVoteId')}")

if __name__ == "__main__":
    main()
