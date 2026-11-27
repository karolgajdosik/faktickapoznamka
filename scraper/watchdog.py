"""Data watchdog: detects a silently broken scraper.

Prints a Markdown report and exits 1 when something looks wrong:
- a session from the NR SR programme started 3+ days ago and has no votes,
- the newest vote is older than the newest session start by more than 4 days,
- the extra data (committees, declarations, laws) has not refreshed for 3 days,
- the MP list is unexpectedly short or a vote file is malformed.
"""
import json, re, sys, glob, datetime as dt
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
now = dt.datetime.now(dt.timezone.utc)
today = now.date()
problems = []


def load(p):
    return json.loads((D / p).read_text(encoding="utf-8"))


votes = []
for f in glob.glob(str(D / "votes" / "*.json")):
    try:
        v = json.loads(Path(f).read_text(encoding="utf-8"))
        votes.append((v["session"], dt.datetime.fromisoformat(v["datetime"])))
    except Exception as e:  # noqa: BLE001
        problems.append(f"Poškodený súbor hlasovania `{Path(f).name}`: {e}")

sessions_with_votes = {s for s, _ in votes}
newest_vote = max((t for _, t in votes), default=None)

# programme: [{"n": 66, "when": "24. 11. 2026 -"}, ...]
for s in load("extra/program.json")[:6]:
    when = s.get("when", "")
    if re.search(r"SPÄŤ|ZRUŠ|PRESUN", when, re.I):
        continue
    m = re.match(r"\s*(\d{1,2})\.\s*(?:-\s*\d{1,2}\.\s*)?(\d{1,2})\.\s*(\d{4})", when)
    if not m:
        continue
    d, mo, y = map(int, m.groups())
    try:
        start = dt.date(y, mo, d)
    except ValueError:
        continue
    if start <= today - dt.timedelta(days=3) and s["n"] not in sessions_with_votes:
        problems.append(f"{s['n']}. schôdza sa začala {start:%d. %m. %Y}, ale nemáme z nej ani jedno hlasovanie.")
    if newest_vote and start <= today - dt.timedelta(days=4) and newest_vote.date() < start:
        problems.append(f"Posledné hlasovanie je z {newest_vote:%d. %m. %Y}, hoci {s['n']}. schôdza začala {start:%d. %m. %Y}.")

extra = load("extra/meta.json")
g = extra.get("globalAt")
if g and now - dt.datetime.fromisoformat(g) > dt.timedelta(days=3):
    problems.append(f"Doplnkové dáta (výbory, zmeny, program) sa neobnovili od {g[:10]}.")

mps = load("mps.json")
if len(mps) < 140:
    problems.append(f"Zoznam poslancov má iba {len(mps)} záznamov.")

problems = list(dict.fromkeys(problems))
if problems:
    print("Strážca dát našiel problém, scraper pravdepodobne prestal fungovať (napr. zmena webu nrsr.sk):\n")
    print("\n".join(f"- {p}" for p in problems))
    print(f"\nPosledné hlasovanie v dátach: {newest_vote:%d. %m. %Y %H:%M}" if newest_vote else "")
    sys.exit(1)
print(f"OK: {len(votes)} hlasovaní, posledné {newest_vote:%d. %m. %Y %H:%M}, {len(mps)} poslancov.")
