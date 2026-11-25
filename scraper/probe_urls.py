"""Download arbitrary nrsr.sk pages into probe/ (for exploring new sections).
Usage: python scraper/probe_urls.py name=URL [name=URL ...]
Also follows up to 3 links per page whose URL matches FOLLOW (regex) if set."""
import os, pathlib, re, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr

out = pathlib.Path("probe"); out.mkdir(exist_ok=True)
follow = os.environ.get("FOLLOW")
report = []
for arg in (sys.argv[1:] or os.environ.get("URLS", "").split()):
    name, url = arg.split("=", 1)
    r = nrsr.get(url=url)
    (out / f"{name}.html").write_text(r.text, encoding="utf-8")
    report.append(f"- {name}: HTTP {r.status_code}, ok={r.ok}, {len(r.text)} B, {r.url}")
    if follow:
        links = []
        for l in re.findall(r'href="([^"]+)"', r.text):
            l = html.unescape(l)
            if re.search(follow, l) and l not in links: links.append(l)
        for i, l in enumerate(links[:3]):
            u = l if l.startswith("http") else "https://www.nrsr.sk/web/" + l.lstrip("/").removeprefix("web/")
            rr = nrsr.get(url=u)
            (out / f"{name}_f{i}.html").write_text(rr.text, encoding="utf-8")
            report.append(f"  - {name}_f{i}: HTTP {rr.status_code}, {len(rr.text)} B, {u}")
(out / "REPORT2.md").write_text("\n".join(report) + "\n", encoding="utf-8")
print("\n".join(report))
