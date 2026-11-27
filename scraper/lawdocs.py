"""Explanatory memorandum (dôvodová správa) for each bill, as plain text for the AI summary.

For every print with votes, open its page in the parliamentary press (zakony/cpt), pick the
"Dôvodová správa – Všeobecná časť" document (or the whole memorandum), download it and keep the
first part of its text in data/extra/lawtext/<tlač>.txt. Official documents are not protected by
copyright (§ 5 of Act 185/2015). Time-budgeted; newest prints first; each print is read once.
"""
import io, re, sys, time, zipfile, json, argparse, pathlib, html as H
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr

DATA = pathlib.Path("data"); OUT = DATA / "extra" / "lawtext"; KEEP = 9000

def docs(page: str) -> list[tuple[str, str]]:
    """(DocID, name) pairs. The name is the visible text next to the document's links."""
    hits = [(m.start(), m.group(1)) for m in re.finditer(r"Download\.aspx\?DocID=(\d+)", page)]
    out, seen = [], set()
    for k, (pos, i) in enumerate(hits):
        if i in seen: continue
        seen.add(i)
        nxt = next((p for p, j in hits[k + 1:] if j != i), pos + 1500)
        chunk = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<img[^>]*alt=\"([^\"]*)\"[^>]*>", " ", page[pos:nxt])))
        name = " ".join(chunk.split()).split("' target=")[-1].replace('" target="_blank">', "").strip(" '\">")
        name = re.sub(r"^.*?>\s*", "", name) if ">" in name[:20] else name
        name = re.sub(r"^[^A-Za-zÁ-ž]*", "", name)
        out.append((i, re.sub(r"\s*\(\d+\s*[KM]B\).*$", "", name)))
    return out

def pick(ds):
    for pat in (r"Dôvodová správa\s*[-–]\s*[Vv]šeobecná", r"^Dôvodová správa(?!.*[Oo]sobitná)", r"Dôvodová správa", r"Návrh (zákona|ústavného zákona|novely)"):
        for i, n in ds:
            if re.search(pat, n): return i, n
    return None

def text_of(b: bytes) -> str:
    if b[:2] == b"PK":                                    # .docx
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            x = z.read("word/document.xml").decode("utf-8", "ignore")
        x = re.sub(r"</w:p>", "\n", x)
        return H.unescape(re.sub(r"<[^>]+>", "", x))
    if b[:4] == b"%PDF":
        from pypdf import PdfReader
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(b)).pages[:12])
    if b[:4] == b"\xd0\xcf\x11\xe0":                      # legacy .doc: keep readable runs of text
        t = b.decode("utf-16-le", "ignore")
        return "\n".join(r for r in re.findall(r"[\w\s.,;:§()%–\-„“\"/]{40,}", t))
    return ""

def clean(t: str) -> str:
    t = re.sub(r"[ \t ]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t).strip()
    return t[:KEEP]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--minutes", type=float, default=10); ap.add_argument("--max", type=int, default=60)
    a = ap.parse_args(); end = time.time() + a.minutes * 60
    OUT.mkdir(parents=True, exist_ok=True)
    tl = set()
    for f in (DATA / "votes").glob("*.json"):
        t = json.loads(f.read_text()).get("tlac")
        if t and str(t).isdigit(): tl.add(str(t))
    todo = [t for t in sorted(tl, key=int, reverse=True) if not (OUT / f"{t}.txt").exists()]
    n = miss = 0
    for t in todo[: a.max]:
        if time.time() > end: break
        r = nrsr.get({"sid": "zakony/cpt", "ZakZborID": 13, "CisObdobia": 9, "ID": t})
        if not r.ok: continue
        p = pick(docs(r.text))
        body = nrsr.get_bytes(f"https://www.nrsr.sk/web/Dynamic/Download.aspx?DocID={p[0]}") if p else None
        txt = clean(text_of(body)) if body else ""
        # an empty marker file means "looked, nothing usable" so the print is not fetched every run
        (OUT / f"{t}.txt").write_text(f"# {p[1] if p else 'bez dôvodovej správy'}\n{txt}" if len(txt) > 400 else "", encoding="utf-8")
        n += 1; miss += len(txt) <= 400
    print(f"lawtext: {n} read ({miss} without usable text), {max(len(todo) - n, 0)} waiting", flush=True)

if __name__ == "__main__":
    main()
