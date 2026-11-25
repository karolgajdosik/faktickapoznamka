"""Extra data beyond votes and debates, refreshed gradually within a time budget:
per-MP activity (excuses, bills, amendments, interpellations, trips, offices, asset
declaration), committees, changes in the house, session programme, official law process,
and debate keywords. Usage: python scraper/extra.py --minutes 12
"""
import argparse, json, pathlib, sys, datetime, time, re, math, unicodedata, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse_extra as P

DATA = pathlib.Path("data"); X = DATA / "extra"; TERM = 9
NOW = lambda: datetime.datetime.now(datetime.timezone.utc)
iso = lambda d: d.isoformat(timespec="seconds")
COMMITTEES = range(172, 191)

def rd(p, default):
    try: return json.loads(p.read_text())
    except Exception: return default
def wr(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    new = json.dumps(obj, ensure_ascii=False, indent=1)
    if not p.exists() or p.read_text() != new: p.write_text(new)
def ascii_tokens(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return frozenset(t for t in re.split(r"[^a-z]+", s) if t)
def page(params):
    r = nrsr.get({**params})
    if not r.ok and nrsr.is_challenge(r.url, r.text): sys.exit("Blocked by nrsr.sk bot check")
    return r.text if r.ok else None
def url(sid, **kw): return nrsr.BASE + "?sid=" + sid + "".join(f"&{k}={v}" for k, v in kw.items())

def older(ts, **delta): return not ts or ts < iso(NOW() - datetime.timedelta(**delta))

def mp_activity(mp, vnf_index):
    pid = mp["id"]; out = {"id": pid}
    h = page({"sid": "poslanci/ospravedlnenia", "PoslanecID": pid, "CisObdobia": TERM}); out["excuses"] = P.parse_excuses(h) if h else []
    out["bills"] = nrsr.paginate(url("zakony/sslp", PredkladatelID=0, PredkladatelPoslanecId=pid, CisObdobia=TERM), P.parse_bills, max_pages=10)
    out["amendments"] = nrsr.paginate(url("schodze/nrepdn", CisObdobia=TERM, PoslanecMasterID=pid), P.parse_amendments, max_pages=15)
    out["interpellations"] = nrsr.paginate(url("schodze/interpelacie_result", ZadavatelId=pid, CisObdobia=TERM), P.parse_interpellations, max_pages=10)
    h = page({"sid": "poslanci/zpc", "PoslanecID": pid, "CisObdobia": TERM}); out["trips"] = P.parse_trips(h) if h else []
    h = page({"sid": "poslanci/kancelarie", "PoslanecID": pid, "CisObdobia": TERM}); out["offices"] = P.parse_offices(h) if h else []
    uid = vnf_index.get(ascii_tokens(mp["name"]))
    out["declaration"] = None
    if uid:
        h = page({"sid": "vnf/oznamenie", "UserId": uid})
        d = P.parse_declaration(h) if h else None
        if d: out["declaration"] = {**d, "userId": uid}
    for k in ("bills", "amendments", "interpellations"):   # pages may repeat rows
        seen, uniq = set(), []
        for x in out[k]:
            key = json.dumps(x, sort_keys=True)
            if key not in seen: seen.add(key); uniq.append(x)
        out[k] = uniq
    out["at"] = iso(NOW())
    return out

def laws_todo(meta):
    tl = set()
    for f in (DATA / "votes").glob("*.json"):
        t = rd(f, {}).get("tlac")
        if t and str(t).isdigit(): tl.add(str(t))
    todo = []
    for t in sorted(tl, key=int, reverse=True):
        cur = rd(X / "law" / f"{t}.json", None)
        if cur is None: todo.append((0, t)); continue
        final = cur.get("zbierka") or re.search(r"Uzavretá|vzatý späť|nebol schválený|Zamietnutý|Stiahnutý", cur.get("state", "") + (cur.get("stateNote") or ""), re.I)
        if older(cur.get("at"), days=30 if final else 2): todo.append((1, t))
    return [t for _, t in sorted(todo, key=lambda x: x[0])]

STOP = set("""ako alebo ale aby aj až ani asi bez bol bola boli bolo bude budem budeme budete budú by byť cez čo či ďakujem dnes do ešte ho iba ich ja je jeho jej len lebo ma mal mala mali malo mám máme máte medzi mi mňa mne môže môžeme my na nad nám nás náš naša naše ne nech nie nič niečo no o od on ona oni ono po pod podľa pre pred pri sa si sme ste sú so svoj ta tak takže tam teda ten tento tie tiež to toho tom tomu toto tu tým už v vám vás váš ve veď vo však vy z za že keď kde ktorá ktoré ktorý ktorí ktorú ktorého ktorej ktorým ktorých pretože preto alebo naozaj vlastne ešte jednoducho samozrejme proste práve teraz potom potrebné chcem chceme hovoriť povedať hovorím hovoril poviem treba skutočne určite
pán pani páni dámy kolegovia kolegyne kolega kolegyňa predseda predsedajúci predsedajúca podpredseda poslanec poslankyňa poslanci poslancov poslankyne vážený vážená vážení ctené ctení minister ministerka ministra návrh návrhu návrhom zákon zákona zákonov zákone zákonom národná národnej rady rada slovenskej republiky republika vláda vlády vláde výbor výboru bod bodu schôdze schôdza hlasovanie hlasovať faktická poznámka faktickú poznámku poznámky reakcia reagovať vystúpenie vystúpení rozprava rozpravy rokovanie rokovania slovo slova ďakujem prosím dobre takto takéto takej takú tejto tohto tieto týchto týmto tento ktorom nejaké nejaký niektorí niekto niekoľko všetci všetky všetko každý veľmi viac menej celé celý stále vôbec napríklad jedna jeden jedno dva dve prvé druhé hlavne milí milé milý ďalej tomto tieto také táto nášho našej našich vašej vašich dneska vyjadriť povedal povedala""".split())

GENERIC = {w[:7] for w in "každopádne prerušujem vravím fantastické reakciami poradie zaujať písomnú popoludňajšom nedostupné sústavne citeľne ilustračne finále vlaňajší tohtoročný vybrané absolutne absolútne totiž dokonca jednoznačne zásadne ohromne nehovoriac konkrétne konečne otázka otázku odpoveď odpovede priestor problém problémy situácia situácii pravda vlastne postupne požiadať zoberte zobrať pozrite pozrieť chcela chceli myslím myslíte rozumiem uvidíme hovorí hovoria hovorili spomínal spomínali pripomenúť".split()}

def topics(mps):
    by_name = {}
    for m in mps:
        parts = m["sortName"].split(" ")
        for i in range(1, len(parts)):
            by_name[ascii_tokens(" ".join(parts[:i]) + " " + " ".join(parts[i:]))] = m["id"]
    tf = collections.defaultdict(collections.Counter); surface = collections.defaultdict(collections.Counter)
    for f in sorted((DATA / "speeches").glob("*.json")):
        for s in rd(f, []):
            pid = by_name.get(ascii_tokens(s.get("speaker", "")))
            if not pid or not s.get("text") or "predseda" in s.get("role", "").lower(): continue  # chairing the sitting isn't a topic
            for w in re.findall(r"(?<![\w])[a-záäčďéíĺľňóôŕšťúýž]{6,}", s["text"]):   # lowercase only: skips names
                lw = w
                if lw in STOP: continue
                stem = lw[:7]; tf[pid][stem] += 1; surface[stem][lw] += 1
    n = len(tf) or 1; df = collections.Counter()
    for c in tf.values(): df.update(c.keys())
    out = {}
    for pid, c in tf.items():
        total = sum(c.values()) or 1
        sc = [(math.sqrt(v) * math.log(n / df[s]) ** 1.5, s) for s, v in c.items() if v >= 12 and 6 <= df[s] <= n * 0.4 and s not in GENERIC]
        out[pid] = [surface[s].most_common(1)[0][0] for _, s in sorted(sc, reverse=True)[:12]]
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--minutes", type=float, default=12); a = ap.parse_args()
    deadline = time.time() + a.minutes * 60
    meta = rd(X / "meta.json", {}); mps = rd(DATA / "mps.json", [])
    left = lambda: deadline - time.time()

    # small global pages: daily
    if older(meta.get("globalAt"), hours=20):
        h = page({"sid": "schodze/zoznam"})
        if h: wr(X / "program.json", P.parse_program(h))
        comms = []
        for cid in COMMITTEES:
            h = page({"sid": "vybory/vybor", "ID": cid})
            if not h: continue
            from bs4 import BeautifulSoup
            name = (BeautifulSoup(h, "lxml").find("h1") or BeautifulSoup("<h1/>", "lxml").h1).get_text(" ", strip=True)
            if name: comms.append({"id": cid, "name": name, "members": P.parse_committee(h)})
        if comms: wr(X / "committees.json", comms)
        ch = nrsr.paginate(url("poslanci/zmeny"), P.parse_changes, max_pages=20)
        if ch:
            uniq = list({json.dumps(c, sort_keys=True): c for c in ch}.values())
            wr(X / "changes.json", sorted(uniq, key=lambda c: c["date"], reverse=True))
        meta["globalAt"] = iso(NOW()); wr(X / "meta.json", meta)
        print(f"global: {len(comms)} committees, {len(ch)} changes", flush=True)

    # declarations index: weekly
    idx_p = X / "vnf_index.json"
    if older(meta.get("vnfAt"), days=7) or not idx_p.exists():
        h = page({"sid": "vnf/zoznam", "ViewType": 1})
        if h: wr(idx_p, P.parse_declaration_index(h)); meta["vnfAt"] = iso(NOW())
    vnf_index = {ascii_tokens(k): v for k, v in rd(idx_p, {}).items()}

    # per-MP pages: weekly, stalest first (≈7 pages each)
    stale = sorted(mps, key=lambda m: rd(X / "mp" / f"{m['id']}.json", {}).get("at", ""))
    done = 0
    for m in stale:
        if left() < 120: break
        if not older(rd(X / "mp" / f"{m['id']}.json", {}).get("at"), days=7): break
        try: wr(X / "mp" / f"{m['id']}.json", mp_activity(m, vnf_index)); done += 1
        except SystemExit: raise
        except Exception as e: print(f"mp {m['id']}: {e!r}", flush=True)
    print(f"mp activity: {done} refreshed", flush=True)

    # law process for every tlač we have votes on
    n = 0
    for t in laws_todo(meta):
        if left() < 30: break
        h = page({"sid": "zakony/zakon", "ZakZborID": 13, "CisObdobia": TERM, "CPT": t})
        if not h: continue
        d = P.parse_law(h)
        if d.get("state") or d.get("submitter"): wr(X / "law" / f"{t}.json", {**d, "at": iso(NOW())}); n += 1
    print(f"laws: {n} refreshed", flush=True)

    if older(meta.get("topicsAt"), days=1):
        wr(X / "topics.json", topics(mps)); meta["topicsAt"] = iso(NOW())
    wr(X / "meta.json", meta)

if __name__ == "__main__":
    try: main()
    finally: nrsr.close()
