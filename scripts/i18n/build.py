"""Builds public/i18n/{en,de,hu,pl}.json from the dictionary parts. Run: python scripts/i18n/build.py"""
import json, pathlib, re, sys
here = pathlib.Path(__file__).parent; sys.path.insert(0, str(here))
import dict1, dict2, dict3, dict4, dict5, dict6  # noqa: E401  (parts register rows in dict1.R)
NUM = re.compile(r"\d+(?:[   ]\d{3})*(?:[,.]\d+)?")
SKIP = {"Posledné hlasovanie, {n}. novembra {n} o {n}:{n}"}
out = {l: {} for l in ("en", "de", "hu", "pl")}
seen = {}
for keys, *vals in dict1.R:
    for k in keys:
        k = " ".join(k.split())
        k = NUM.sub("{n}", k)
        if k in SKIP: continue
        if k in seen and seen[k] != vals: print("conflict:", k, file=sys.stderr)
        seen[k] = vals
        for l, v in zip(out, vals): out[l][k] = v
root = here.parent.parent / "public" / "i18n"
for l, d in out.items():
    (root / f"{l}.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
print(len(seen), "keys")
