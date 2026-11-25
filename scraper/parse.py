"""Parsers for nrsr.sk HTML. Written defensively (text patterns + link IDs rather
than brittle CSS paths). Calibrate against probe/*.html; tests in test_parse.py."""
import re, unicodedata
from bs4 import BeautifulSoup

CODE_RE = re.compile(r"\[(Z|P|\?|N|0)\]")
CLUB_RE = re.compile(r"^\s*(Klub\s.+?|Poslanci,?\s+ktorí\s+nie\s+sú\s+členmi.+?)\s*(\(\d+\))?\s*$", re.I)

def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")

def _label(text: str, label: str) -> str | None:
    m = re.search(label + r"\s*:?\s*\n?\s*([^\n]+)", text, re.I)
    return m.group(1).strip() if m else None

def _int(s: str | None) -> int | None:
    m = re.search(r"\d+", s or ""); return int(m.group()) if m else None

def club_name(raw: str) -> str:
    raw = re.sub(r"\s*\(\d+\)\s*$", "", raw.strip())
    if raw.lower().startswith("poslanci, ktorí nie sú") or raw.lower().startswith("poslanci ktorí nie sú"):
        return "Nezaradení"
    return re.sub(r"^Klub\s+", "", raw, flags=re.I).strip()

def parse_vote(html: str, vote_id: str) -> dict | None:
    """Parse a 'hlasklub' page: header metadata + per-MP votes grouped by club."""
    soup = _soup(html)
    text = soup.get_text("\n")
    k = text.find("hlasovanie poslancov")  # skip site menu; metadata follows this heading
    if k >= 0: text = text[k:]
    anchors = [a for a in soup.find_all("a", href=True) if "PoslanecID=" in a["href"]]
    if len(anchors) < 20:  # not a vote page (or empty / non-existent ID)
        return None
    votes, mps = {}, {}
    for a in anchors:
        pid = re.search(r"PoslanecID=(\d+)", a["href"]).group(1)
        name = " ".join(a.get_text(" ", strip=True).split())
        code = None
        node = a.previous_sibling
        for _ in range(4):
            if node is None: break
            m = CODE_RE.search(node.get_text() if hasattr(node, "get_text") else str(node))
            if m: code = m.group(1); break
            node = node.previous_sibling
        if code is None:
            m = CODE_RE.search(a.parent.get_text(" ")); code = m.group(1) if m else None
        if code is None: continue
        club_node = a.find_previous(string=CLUB_RE)
        votes[pid] = code
        mps[pid] = {"id": pid, "rawName": name, "club": club_name(club_node) if club_node else "Neznámy"}
    counts = {c: 0 for c in ["Z", "P", "?", "N", "0"]}
    for c in votes.values(): counts[c] += 1
    title = _label(text, r"Názov hlasovania") or _label(text, r"Názov") or f"Hlasovanie {vote_id}"
    # Lines between the title and "Výsledok hlasovania" say what exactly was voted on
    # (e.g. "Hlasovanie o pozmeňujúcom návrhu zo spoločnej správy výborov - 1 bod").
    detail = None
    dm = re.search(r"Názov hlasovania\s*\n\s*[^\n]+\n(.*?)\n\s*Výsledok hlasovania", text, re.S)
    if dm:
        detail = " ".join(l.strip() for l in dm.group(1).split("\n") if l.strip()) or None
    res = (_label(text, r"Výsledok hlasovania") or "").lower()
    dt = _label(text, r"Dátum a čas") or _label(text, r"Dátum")
    tlac = re.search(r"tla[čc]\s*(\d+)", title, re.I)
    return {
        "id": str(vote_id),
        "session": _int(_label(text, r"Schôdza\s*\n")),
        "number": _int(_label(text, r"Číslo hlasovania")),
        "datetime": parse_dt(dt),
        "title": title,
        "detail": detail,
        "tlac": tlac.group(1) if tlac else None,
        "passed": True if "návrh prešiel" in res or "schválen" in res and "neschválen" not in res
                  else False if res else None,
        "counts": counts,
        "votes": votes,
        "clubs": {pid: m["club"] for pid, m in mps.items()},
        "_mps": mps,
    }

def parse_dt(s: str | None) -> str | None:
    """'12. 11. 2026 11:05' -> ISO with Bratislava offset (approximate DST rule)."""
    if not s: return None
    m = re.search(r"(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})\s*(\d{1,2}):(\d{2})", s)
    if not m: return None
    d, mo, y, h, mi = map(int, m.groups())
    off = "+02:00" if 4 <= mo <= 9 or (mo == 3 and d >= 25) or (mo == 10 and d < 25) else "+01:00"
    return f"{y:04d}-{mo:02d}-{d:02d}T{h:02d}:{mi:02d}:00{off}"

def sort_name(name: str) -> tuple[str, str]:
    """nrsr usually writes 'Priezvisko, Meno' — return (display, sortName)."""
    name = re.sub(r"\s+", " ", name).strip()
    if "," in name:
        last, first = [p.strip() for p in name.split(",", 1)]
        return f"{first} {last}", f"{last} {first}"
    parts = name.split(" ")
    return name, " ".join(parts[1:] + parts[:1])

def parse_live(html: str) -> str | None:
    """Current agenda item from the homepage box 'Priebeh rokovania NR SR'."""
    soup = _soup(html)
    for h3 in soup.find_all("h3"):
        if "Priebeh rokovania" in h3.get_text():
            div = h3.find_next_sibling("div")
            txt = " ".join(div.get_text(" ", strip=True).split()) if div else ""
            return txt or None
    return None

def parse_mp(html: str, mp_id: str) -> dict | None:
    """Profile fields from 'Detaily poslanca'. Labels and values alternate as lines."""
    text = _soup(html).get_text("\n")
    k = text.find("Detaily poslanca")
    if k < 0: return None
    lines = [l.strip() for l in text[k:].split("\n") if l.strip()]
    labels = {"Meno": "first", "Titul": "title", "Priezvisko": "last", "Kandidoval(a) za": "party",
              "Narodený(á)": "born", "Národnosť": None, "Bydlisko": "city", "Kraj": "region", "E-mail": None}
    out: dict = {"id": mp_id}
    for i, l in enumerate(lines[:-1]):
        if l in labels and labels[l] and lines[i + 1] not in labels:
            out[labels[l]] = lines[i + 1]
    m = re.search(r"(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})", out.get("born", ""))
    out["born"] = f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else None
    if out.get("title"): out["title"] = re.sub(r"\s*,\s*", ", ", out["title"]).strip(" ,")
    return out if out.get("last") else None

SPEECH_TIME_RE = re.compile(r"(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2}):(\d{2})")

def _iso(y, mo, d, h, mi, s):
    off = "+02:00" if 4 <= mo <= 9 or (mo == 3 and d >= 25) or (mo == 10 and d < 25) else "+01:00"
    return f"{y:04d}-{mo:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}{off}"

def parse_speeches(html: str) -> list[dict]:
    """Items of the debate search ('Vyhľadávanie v prepise rozpravy')."""
    out = []
    for it in _soup(html).find_all("div", class_="daily_info_item"):
        heads = it.find_all("div", class_="daily_info_speech_header")
        if len(heads) < 2: continue
        spans = heads[0].find_all("span", recursive=False)
        m = SPEECH_TIME_RE.search(spans[0].get_text(" ", strip=True)) if spans else None
        if not m: continue
        d, mo, y, h1, m1, s1, h2, m2, s2 = map(int, m.groups())
        start, end = _iso(y, mo, d, h1, m1, s1), _iso(y, mo, d, h2, m2, s2)
        dur = (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)
        place = spans[1].get_text(" ", strip=True) if len(spans) > 1 else ""
        pm = re.search(r"(\d+)\.\s*schôdza.*?(\d+)\.\s*deň", place)
        tl = re.search(r"Tlač\s*(\d+)", heads[0].get_text(" ", strip=True))
        video = heads[0].find("a", href=re.compile(r"tv\.nrsr\.sk/archiv/schodza/\d+/\d+\?id=\d+"))
        vid = re.search(r"\?id=(\d+)", video["href"]).group(1) if video else None
        s2_ = heads[1].find_all("span", recursive=False)
        name = " ".join(s2_[0].get_text(" ", strip=True).split()) if s2_ else ""
        role = s2_[2].get_text(" ", strip=True).lstrip("- ").strip() if len(s2_) > 2 else ""
        em = heads[1].find("em")
        kind = em.get_text(" ", strip=True) if em else ""
        body = it.find("div", class_="grid_12")
        text = ""
        if body:
            parts = [p.strip() for p in body.get_text("\n").split("\n")]
            parts = [p for p in parts if p]
            if parts and re.fullmatch(r"\d+\.", parts[0]): parts = parts[1:]  # running number
            text = "\n".join(parts)
        slug = re.sub(r"[^a-z]+", "-", unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()).strip("-")
        out.append({
            "id": f"{y:04d}{mo:02d}{d:02d}{h1:02d}{m1:02d}{s1:02d}-{slug}", "start": start, "end": end, "dur": max(dur, 0),
            "session": int(pm.group(1)) if pm else None, "day": int(pm.group(2)) if pm else None,
            "tlac": tl.group(1) if tl else None, "speaker": name, "role": role,
            "kind": "" if kind == "-" else kind, "video": video["href"].replace("http://", "https://") if video else None,
            "text": text,
        })
    return out
