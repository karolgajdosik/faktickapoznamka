import pathlib, sys, json
here = pathlib.Path(__file__).parent; sys.path.insert(0, str(here))
import parse_extra as P
r = lambda n: (here / f"fixtures/x_{n}.html").read_text(encoding="utf-8")
print(json.dumps({
 "range": [P.date_range("22. - 23. 2. 2024"), P.date_range("28. 6. - 3. 7. 2025")[:2], P.date_range("29. 11. 2023")],
 "excuses": (lambda x: (len(x), x[0]))(P.parse_excuses(r("osp"))),
 "bills": (lambda x: (len(x), x[2]))(P.parse_bills(r("leg"))),
 "amend": (lambda x: (len(x), x[0]))(P.parse_amendments(r("pdn"))),
 "interp": P.parse_interpellations(r("interp")),
 "trips": (lambda x: (len(x), x[0]))(P.parse_trips(r("zpc"))),
 "offices": P.parse_offices(r("kanc")),
 "committee": (lambda x: (len(x), x[:3]))(P.parse_committee(r("vybor176"))),
 "changes": (lambda x: (len(x), x[:2]))(P.parse_changes(r("zmeny"))),
 "program": P.parse_program(r("program"))[:4],
 "law": P.parse_law(r("cpt_f0")),
 "decl": (lambda d: {k: d[k] for k in ["year","function","incomePublic","incomeOther","employment","business","realEstateCount","realEstateKinds","movablesCount"]})(P.parse_declaration(r("vnf_f0"))),
 "declIndex": len(P.parse_declaration_index(r("vnf"))),
}, ensure_ascii=False, indent=1))
