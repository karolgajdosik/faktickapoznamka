"""Parsers for nrsr.sk HTML. Written defensively (text patterns + link IDs rather
than brittle CSS paths). Calibrate against probe/*.html; tests in test_parse.py."""
import re
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
    res = (_label(text, r"Výsledok hlasovania") or "").lower()
    dt = _label(text, r"Dátum a čas") or _label(text, r"Dátum")
    tlac = re.search(r"tla[čc]\s*(\d+)", title, re.I)
    return {
        "id": str(vote_id),
        "session": _int(_label(text, r"Schôdza")),
        "number": _int(_label(text, r"Číslo hlasovania")),
        "datetime": parse_dt(dt),
        "title": title,
        "tlac": tlac.group(1) if tlac else None,
        "passed": True if "návrh prešiel" in res or "schválen" in res and "neschválen" not in res
                  else False if res else None,
        "counts": counts,
        "votes": votes,
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
