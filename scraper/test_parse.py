"""Parser tests on real nrsr.sk pages saved by the probe workflow."""
import pathlib, sys
here = pathlib.Path(__file__).parent; sys.path.insert(0, str(here))
import parse

v = parse.parse_vote((here / "fixtures/hlasklub_52728.html").read_text(encoding="utf-8"), "52728")
assert v and len(v["votes"]) == 150, v and len(v["votes"])
assert v["counts"] == {"Z": 77, "P": 10, "?": 51, "N": 0, "0": 12}, v["counts"]
assert (v["session"], v["number"], v["tlac"], v["passed"]) == (3, 23, "29", True)
assert v["datetime"] == "2023-11-22T18:46:00+01:00"
assert v["title"].startswith("Vládny návrh zákona")
assert v["clubs"]["871"] == "SMER - SD"
assert {m["club"] for m in v["_mps"].values()} >= {"SMER - SD", "PS", "HLAS - SD", "KDH", "SaS", "SNS"}
assert parse.sort_name("Baláž, Vladimír") == ("Vladimír Baláž", "Baláž Vladimír")
assert "tlač 1448" in parse.parse_live((here / "fixtures/home.html").read_text(encoding="utf-8"))
print("ok")
p = parse.parse_mp((here / "fixtures/poslanec_1008.html").read_text(encoding="utf-8"), "1008")
assert p == {"id": "1008", "first": "Ján", "title": "PhDr. Mgr., MBA", "last": "Ferenčák", "party": "HLAS – sociálna demokracia",
             "born": "1974-06-30", "city": "Kežmarok", "region": "Prešovský"}, p
print("ok mp")
sp = parse.parse_speeches((here / "fixtures/rozprava_mp1008.html").read_text(encoding="utf-8"))
assert len(sp) == 20, len(sp)
f = [x for x in sp if x["id"] == "20260924114310-ferencak-jan"][0]
assert (f["start"], f["dur"], f["session"], f["day"], f["tlac"]) == ("2026-09-24T11:43:10+02:00", 120, 61, 7, "1316"), f
assert f["speaker"] == "Ferenčák, Ján" and f["role"] == "poslanec NR SR" and f["kind"] == "Vystúpenie s faktickou poznámkou"
assert f["text"].startswith("Ja vám to poviem celkom presne.") and f["video"] == "https://tv.nrsr.sk/archiv/schodza/9/61?id=375348"
s66 = parse.parse_speeches((here / "fixtures/rozprava_s66.html").read_text(encoding="utf-8"))
assert len(s66) == 20 and s66[0]["session"] == 66 and s66[0]["kind"] == ""
print("ok speeches")
