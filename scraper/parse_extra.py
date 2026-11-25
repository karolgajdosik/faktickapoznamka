"""Parsers for MP activity pages, committees, changes, law process, calendar and
asset declarations on nrsr.sk. Tests: test_parse_extra.py (real pages in fixtures/)."""
import re, datetime
from bs4 import BeautifulSoup

def _soup(h): return BeautifulSoup(h, "lxml")
def _t(el): return " ".join(el.get_text(" ", strip=True).split()) if el else ""
def _rows(soup, min_cells):
    return [r for r in soup.find_all("tr") if len(r.find_all("td", recursive=False)) >= min_cells]

def dmy(s: str) -> str | None:
    m = re.search(r"(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})", s or "")
    return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else None

def date_range(s: str) -> list[str]:
    """'29. 11. 2023' | '22. - 23. 2. 2024' | '28. 6. - 3. 7. 2025' | '30. 12. 2024 - 2. 1. 2025' -> ISO days."""
    s = s.strip()
    m = re.match(r"(\d{1,2})\.\s*(?:(\d{1,2})\.\s*)?(?:(\d{4})\s*)?-\s*(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})", s)
    if m:
        d1, m1, y1, d2, m2, y2 = m.groups()
        a = datetime.date(int(y1 or y2), int(m1 or m2), int(d1)); b = datetime.date(int(y2), int(m2), int(d2))
        if a > b: return [b.isoformat()]
        return [(a + datetime.timedelta(days=i)).isoformat() for i in range((b - a).days + 1)][:60]
    d = dmy(s); return [d] if d else []

# ---------- MP activity ----------
def parse_excuses(html: str) -> list[dict]:
    out = []
    for r in _rows(_soup(html), 2):
        c = r.find_all("td", recursive=False)
        days = date_range(_t(c[0]))
        if days: out.append({"from": days[0], "to": days[-1], "days": days, "reason": _t(c[1])})
    return out

def parse_bills(html: str) -> list[dict]:
    out = []
    for r in _rows(_soup(html), 7):
        c = r.find_all("td", recursive=False)
        tl = re.search(r"(\d+)", _t(c[1]))   # the link text is the tlač number (the link's ID is internal)
        out.append({"title": _t(c[0]), "tlac": tl.group(1) if tl else None, "state": _t(c[2]),
                    "delivered": dmy(_t(c[3])), "approved": dmy(_t(c[4])), "sponsors": _t(c[5]), "category": _t(c[6])})
    return out

def parse_amendments(html: str) -> list[dict]:
    out = []
    for r in _rows(_soup(html), 6):
        c = r.find_all("td", recursive=False)
        if not dmy(_t(c[0])): continue
        vote = re.search(r"hlas\w*&(?:amp;)?ID=(\d+)", str(c[5]))
        did = re.search(r"nrepdn_detail&(?:amp;)?id=(\d+)", str(c[3]), re.I)
        out.append({"date": dmy(_t(c[0])), "by": _t(c[1]), "tlac": _t(c[2]) or None, "title": _t(c[3]),
                    "session": int(_t(c[4])) if _t(c[4]).isdigit() else None, "voteId": vote.group(1) if vote else None,
                    "id": did.group(1) if did else None})
    return out

def parse_interpellations(html: str) -> list[dict]:
    out = []
    for a in _soup(html).find_all("a", href=re.compile(r"interpelacia&(?:amp;)?ID=\d+")):
        tr = a.find_parent("tr")
        if not tr: continue
        c = [_t(td) for td in tr.find_all("td", recursive=False)]
        iid = re.search(r"ID=(\d+)", a["href"]).group(1)
        # columns: Popis, Stav, Dátum podania, Zadávateľ, Klub, Adresát
        out.append({"id": iid, "title": c[0] if c else _t(a), "state": c[1] if len(c) > 1 else "",
                    "date": dmy(c[2]) if len(c) > 2 else None, "to": c[5] if len(c) > 5 else ""})
    return out

def parse_trips(html: str) -> list[dict]:
    out = []
    for r in _rows(_soup(html), 2):
        c = r.find_all("td", recursive=False)
        days = date_range(_t(c[0]))
        if days: out.append({"from": days[0], "to": days[-1], "desc": _t(c[1])})
    return out

def parse_offices(html: str) -> list[str]:
    text = _soup(html).get_text("\n")
    m = re.search(r"\nKancelária\s*\n(.*?)\n\s*Informácie o refundovaných", text, re.S)
    if not m: return []
    return [" ".join(l.split()) for l in m.group(1).split("\n") if l.strip()]

# ---------- committees, changes, calendar ----------
def parse_committee(html: str) -> list[dict]:
    out = []
    for a in _soup(html).find_all("a", href=re.compile(r"PoslanecID=\d+")):
        pid = re.search(r"PoslanecID=(\d+)", a["href"]).group(1)
        tail = ""
        n = a.next_sibling
        for _ in range(4):
            if n is None: break
            tail += n.get_text(" ") if hasattr(n, "get_text") else str(n); n = n.next_sibling
        role = re.sub(r"\(.*?\)", "", " ".join(tail.split())).strip(" ,") or "člen"
        out.append({"mpId": pid, "role": role.split(" ")[0] if role else "člen"})
    seen, res = set(), []
    for x in out:
        if x["mpId"] not in seen: seen.add(x["mpId"]); res.append(x)
    return res

def parse_changes(html: str) -> list[dict]:
    out = []
    for r in _rows(_soup(html), 4):
        c = r.find_all("td", recursive=False)
        d = dmy(_t(c[0]))
        if not d: continue
        a = c[1].find("a", href=re.compile(r"PoslanecID=\d+"))
        out.append({"date": d, "mp": _t(c[1]), "mpId": re.search(r"PoslanecID=(\d+)", a["href"]).group(1) if a else None,
                    "status": re.sub(r"\s*\(.*$", "", _t(c[2])).strip("() -") or None, "reason": _t(c[3])})
    return out

def parse_program(html: str) -> list[dict]:
    text = _soup(html).get_text("\n")
    out = []
    for m in re.finditer(r"(\d+)\.\s*schôdza\s*\n\s*\(([^)]*)\)", text):
        out.append({"n": int(m.group(1)), "when": " ".join(m.group(2).split())})
    return out

# ---------- law process ----------
def parse_law(html: str) -> dict:
    text = re.sub(r"[ \t]+", " ", _soup(html).get_text("\n"))
    flat = " ".join(text.split())
    g = lambda pat: (re.search(pat, flat) or [None, None])[1]
    stages = []
    marks = [(m.start(), m.group(1)) for m in re.finditer(r"(?<![IV])(I{1,3}\. čítanie|Redakcia|Zbierka zákonov)\s", flat)][1:] if "Redakcia" in flat[:6000] else \
            [(m.start(), m.group(1)) for m in re.finditer(r"(?<![IV])(I{1,3}\. čítanie|Redakcia|Zbierka zákonov)\s", flat)]
    for i, (pos, st) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(flat)
        chunk = flat[pos + len(st):end]
        chunk = chunk.split("Priložené dokumenty")[0].split("Výsledok štádia")[0]
        res = re.search(r"Výsledok štádia procesu:\s*(.+?)(?: Priložené| Všetky dokumenty| Hlasovania poslancov| I{1,3}\. čítanie|$)", flat[pos:end])
        stages.append({"stage": st, "text": re.sub(r"\s+([.,])", r"\1", chunk.strip())[:320],
                       "result": re.sub(r"\s+([.,])", r"\1", res.group(1).strip())[:120] if res else None})
    zz = re.search(r"(\d{1,4}/\d{4})\s*Z\.\s*z\.", flat.split("Stav legislatívneho procesu")[-1]) if "Zbierka" in flat else None
    return {
        "state": (g(r"Stav legislatívneho procesu:\s*(.+?)\s*(?:\(|grafické)") or "").strip(),
        "stateNote": (g(r"Stav legislatívneho procesu:\s*[^(]+\((.+?)\)") or "").strip() or None,
        "delivered": dmy(g(r"Dátum doručenia:\s*([\d. ]+\d{4})") or ""),
        "submitter": (g(r"Navrhovateľ:\s*(.+?)\s*Priložené dokumenty") or "").strip() or None,
        "gestor": (g(r"gestorský výbor\s+(.+?)\s+s lehotou") or g(r"gestorskom výbore\s+(.+?)\s+s lehotou") or None),
        "returnedByPresident": bool(re.search(r"vrátil|vrátený prezident", flat, re.I)),
        "zbierka": zz.group(1) if zz else None,
        "stages": stages,
    }

# ---------- asset declarations (published part only; no property locations) ----------
def parse_declaration(html: str) -> dict | None:
    text = _soup(html).get_text("\n")
    k = text.find("Interné číslo:")
    if k < 0: return None
    lines = [" ".join(l.split()) for l in text[k:].split("\n") if l.strip()]
    def after(label, multi=False):
        for i, l in enumerate(lines):
            if l.lower().startswith(label.lower()):
                if not multi: return lines[i + 1] if i + 1 < len(lines) else None
                out = []
                for x in lines[i + 1:]:
                    if x.endswith(":") or re.match(r"^(vlastníctvo|užívanie|majetkové|vykonávam|počas výkonu|príjmy|spĺňam|späť|Vytlačiť)", x, re.I): break
                    out.append(x)
                return out
        return None
    def items(label):
        raw = [x for x in (after(label, multi=True) or []) if not x.lower().startswith("požitky") and not re.match(r"^(nevlastním|nemám|nevykonávam|nie)\b", x, re.I)]
        out = []
        for x in raw:                       # "(ORGANIZÁCIA)" belongs to the function above it
            if x.startswith("(") and out: out[-1] += " " + x
            else: out.append(x)
        return out
    inc = after("príjmy za rok") or ""
    pub = re.search(r"([\d\s]+)\s*€\s*\(z výkonu verejnej funkcie\)", inc)
    oth = re.search(r"([\d\s]+)\s*€\s*\(iné\)", inc)
    real = items("vlastníctvo nehnuteľnej veci")
    kinds: dict[str, int] = {}
    for r in real:
        kind = r.split(";")[0].strip().capitalize()   # keep only the kind, never the cadastral area or LV number
        if kind: kinds[kind] = kinds.get(kind, 0) + 1
    movables = items("vlastníctvo hnuteľnej veci")
    return {
        "year": int(after("oznámenie za rok") or 0) or None,
        "filed": after("oznámenie bolo podané"),
        "function": after("vykonávaná verejná funkcia"),
        "incomePublic": int(pub.group(1).replace(" ", "")) if pub else None,
        "incomeOther": int(oth.group(1).replace(" ", "")) if oth else None,
        "employment": after("vykonávam nasledovné zamestnanie"),
        "business": after("vykonávam nasledovnú podnikateľskú činnosť"),
        "roles": [x for x in items("počas výkonu verejnej funkcie mám tieto funkcie")][:40],
        "realEstateCount": len(real), "realEstateKinds": kinds,
        "movablesCount": len(movables),
        "movables": [re.split(r"[;,]", m)[0].strip().capitalize() for m in movables][:30],
        "rights": [re.split(r"[;,]", x)[0].strip().capitalize() for x in items("vlastníctvo majetkového práva alebo inej majetkovej hodnoty")][:30],
        "obligations": [re.split(r"[;,]", x)[0].strip().capitalize() for x in items("existencia záväzku")][:30],
    }

def parse_declaration_index(html: str) -> dict[str, str]:
    """'Priezvisko, Meno' -> UserId"""
    return {n.strip(): u for u, n in re.findall(r'vnf/oznamenie&(?:amp;)?UserId=([^"&]+)"[^>]*>([^<]+)<', html)}
