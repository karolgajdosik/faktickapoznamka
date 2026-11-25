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
