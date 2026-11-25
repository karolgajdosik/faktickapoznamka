"""Diagnostics: how the debate grid of one session paginates. Prints per page:
navigation y/n, item count, first item id, pager links present."""
import re, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nrsr, parse

sess = int(sys.argv[1]) if len(sys.argv) > 1 else 61
nrsr._start()
url = nrsr.BASE + f"?sid=schodze/rozprava/vyhladavanie&CisObdobia=9&CisSchodze={sess}"
page = nrsr._ctx.new_page()
page.goto(url, wait_until="domcontentloaded", timeout=60000)
for _ in range(60):
    if "nrsr-challenge" not in page.url: break
    page.wait_for_timeout(1000)
page.select_option("select[name$='_meetingNrCombo']", str(sess))
with page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
    page.click("input[name$='_searchButton']")
html = page.content()
pathlib.Path("probe").mkdir(exist_ok=True); pathlib.Path(f"probe/dbg_{sess}_p1.html").write_text(html, encoding="utf-8")
def info(h):
    it = parse.parse_speeches(h)
    pager = sorted(set(re.findall(r"'(Page\$[^']+)'", h)), key=lambda x: (len(x), x))
    count = re.findall(r"(?:Počet|Nájden|Záznam)[^<]{0,80}", h)[:2]
    return len(it), (it[0]["id"], it[0]["start"]) if it else None, pager, count
print("p1", info(html), flush=True)
grid = re.search(r"__doPostBack\('([^']+)','Page\$\d+'\)", html).group(1)
print("grid", grid)
for k in range(2, 16):
    time.sleep(2.5)
    t = time.time(); nav = True
    try:
        with page.expect_navigation(wait_until="domcontentloaded", timeout=30000):
            loc = page.locator(f"a[href*=\"'Page${k}'\"]")
            if loc.count(): loc.first.click()
            else: page.evaluate("([t, a]) => __doPostBack(t, a)", [grid, f"Page${k}"])
    except Exception as e:
        nav = f"no ({type(e).__name__})"
    page.wait_for_timeout(500)
    h = page.content()
    if k in (5, 6, 7): pathlib.Path(f"probe/dbg_{sess}_p{k}.html").write_text(h, encoding="utf-8")
    print(f"p{k} nav={nav} {time.time()-t:.1f}s", info(h), "url:", page.url[-60:], flush=True)
