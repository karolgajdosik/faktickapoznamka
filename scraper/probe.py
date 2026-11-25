"""Downloads sample pages from nrsr.sk into probe/ so parsers can be calibrated
against the real HTML. Run manually via the 'Probe nrsr.sk' GitHub workflow."""
import pathlib, re, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr

out = pathlib.Path("probe"); out.mkdir(exist_ok=True)
term = 9
pages = {
    "home": ({}, "https://www.nrsr.sk/web/"),
    "poslanci_zoznam": ({"sid": "poslanci/zoznam_abc", "ListType": "0", "CisObdobia": term}, nrsr.BASE),
    "hlasovania_schodze": ({"sid": "schodze/hlasovanie/schodze"}, nrsr.BASE),
    "hlasovania_vyhladavanie": ({"sid": "schodze/hlasovanie/vyhladavanie_vysledok", "CisObdobia": term}, nrsr.BASE),
}
report = [f"# Probe {datetime.datetime.utcnow().isoformat()}Z\n"]
found_ids: set[str] = set(); mp_ids: set[str] = set()
for name, (params, url) in pages.items():
    try:
        r = nrsr.get(params, url)
        (out / f"{name}.html").write_text(r.text, encoding="utf-8")
        found_ids |= set(re.findall(r"hlasovanie/hlas(?:klub|ovanie)?&(?:amp;)?ID=(\d+)", r.text))
        mp_ids |= set(re.findall(r"PoslanecID=(\d+)", r.text))
        report.append(f"- {name}: HTTP {r.status_code}, ok={r.ok}, {len(r.text)} B, url {r.url}")
    except Exception as e:
        report.append(f"- {name}: ERROR {e!r}")

for i, vid in enumerate(sorted(found_ids, key=int, reverse=True)[:2]):
    for sid in ("schodze/hlasovanie/hlasklub", "schodze/hlasovanie/hlasovanie"):
        r = nrsr.get({"sid": sid, "ID": vid})
        fn = f"vote_{vid}_{sid.rsplit('/', 1)[1]}.html"
        (out / fn).write_text(r.text, encoding="utf-8")
        report.append(f"- {fn}: HTTP {r.status_code}, {len(r.text)} B")
for pid in sorted(mp_ids)[:1]:
    r = nrsr.get({"sid": "poslanci/poslanec", "PoslanecID": pid, "CisObdobia": term})
    (out / f"poslanec_{pid}.html").write_text(r.text, encoding="utf-8")
    report.append(f"- poslanec_{pid}: HTTP {r.status_code}, {len(r.text)} B")
report.append(f"\nVote IDs seen: {sorted(found_ids, key=int)[-10:]}\nMP IDs seen: {len(mp_ids)}")
(out / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
print("\n".join(report))
