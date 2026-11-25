"""Smoke test on a synthetic page shaped like nrsr 'hlasklub'. Replace/extend
with real fixtures from probe/ once available."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import parse

rows = "".join(f'<td>[{"ZP?N0"[i % 5]}] <a href="Default.aspx?sid=poslanci/poslanec&PoslanecID={i}">Priezvisko{i}, Meno</a></td>' for i in range(30))
html = f"""<html><body><span>Schôdza:</span><span>61</span><span>Dátum a čas:</span><span>12. 11. 2026 11:05</span>
<span>Číslo hlasovania:</span><span>12</span><span>Názov hlasovania:</span><span>Návrh zákona (tlač 1422) - tretie čítanie</span>
<span>Výsledok hlasovania:</span><span>Návrh prešiel</span><h2>Klub SAMPLE (30)</h2><table><tr>{rows}</tr></table></body></html>"""
v = parse.parse_vote(html, "777")
assert v and len(v["votes"]) == 30, v
assert v["counts"]["Z"] == 6 and v["session"] == 61 and v["number"] == 12
assert v["passed"] is True and v["tlac"] == "1422" and v["datetime"] == "2026-11-12T11:05:00+01:00"
assert v["_mps"]["3"]["club"] == "SAMPLE"
assert parse.sort_name("Priezvisko, Meno") == ("Meno Priezvisko", "Priezvisko Meno")
print("ok")
