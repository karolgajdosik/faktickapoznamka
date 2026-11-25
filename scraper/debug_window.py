"""Diagnostics: walk one session's debate backwards in time with GET requests (DatumDo)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse
from urllib.parse import quote
sess = int(sys.argv[1]) if len(sys.argv) > 1 else 61
until = "2100-1-1 0:0:0"; seen = set()
for i in range(8):
    url = (nrsr.BASE + f"?sid=schodze%2frozprava%2fvyhladavanie&CisObdobia=9&CPT=&CisSchodze={sess}&PoslanecID=0"
           f"&DatumOd={quote('1900-1-1 0:0:0')}&DatumDo={quote(until)}&TypVystupenia=")
    r = nrsr.get(url=url)
    items = parse.parse_speeches(r.text)
    new = [x for x in items if x["id"] not in seen]; seen.update(x["id"] for x in items)
    print(f"#{i} HTTP {r.status_code} ok={r.ok} items={len(items)} new={len(new)}",
          items[0]["start"] if items else None, "→", items[-1]["start"] if items else None, "sessions", sorted({x["session"] for x in items}), flush=True)
    if not items: break
    s = items[-1]["start"]  # 2026-11-20T15:31:23+01:00 → local "2026-11-20 15:31:23"
    until = f"{int(s[0:4])}-{int(s[5:7])}-{int(s[8:10])} {int(s[11:13])}:{int(s[14:16])}:{int(s[17:19])}"
print("total unique", len(seen))
