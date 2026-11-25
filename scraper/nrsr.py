"""HTTP client for nrsr.sk.

nrsr.sk sits behind BunkerWeb with a JavaScript proof-of-work check, so plain
HTTP requests only ever see the challenge page. We open the site once in a
headless Chromium (which completes the check like any visitor's browser), then
reuse that browser context's cookies for ordinary requests. Rate-limited and
self-identifying; if the check reappears we pass it again in the browser.
"""
import time, atexit
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

BASE = "https://www.nrsr.sk/web/Default.aspx"
HOME = "https://www.nrsr.sk/web/"
CONTACT = "faktickapoznamka.sk-bot (+https://faktickapoznamka.sk/o-projekte/; kontakt@faktickapoznamka.sk)"
DELAY = 2.0  # seconds between requests

_pw = _browser = _ctx = None
_last = 0.0

class Resp:
    def __init__(self, status: int, url: str, text: str):
        self.status_code, self.url, self.text = status, url, text
        self.ok = 200 <= status < 300 and not is_challenge(url, text)

def is_challenge(url: str, text: str) -> bool:
    return "nrsr-challenge" in url or ("BUNKERWEB" in text.upper() and "PROOF" in text.upper())

def _start():
    global _pw, _browser, _ctx
    if _ctx: return
    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch()
    ua = _browser.new_page().evaluate("navigator.userAgent").replace("HeadlessChrome", "Chrome")
    _ctx = _browser.new_context(user_agent=f"{ua} {CONTACT}", locale="sk-SK")
    atexit.register(close)
    _solve(HOME)

def _solve(url: str) -> Resp:
    page = _ctx.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        for _ in range(60):  # proof-of-work usually takes a second or two
            if "nrsr-challenge" not in page.url: break
            page.wait_for_timeout(1000)
        page.wait_for_load_state("domcontentloaded")
        return Resp(200, page.url, page.content())
    finally:
        page.close()

def _wait():
    global _last
    d = DELAY - (time.time() - _last)
    if d > 0: time.sleep(d)
    _last = time.time()

def get(params: dict | None = None, url: str = BASE, tries: int = 3) -> Resp:
    _start()
    full = url + ("?" + urlencode(params) if params else "")
    r = Resp(0, full, "")
    for attempt in range(tries):
        _wait()
        try:
            res = _ctx.request.get(full, timeout=60_000)
            r = Resp(res.status, res.url, res.text())
            if is_challenge(r.url, r.text):
                r = _solve(full)          # check reappeared: pass it in the browser
            if r.ok or r.status_code in (404, 410): return r
        except Exception as e:
            r = Resp(0, full, f"ERROR {e!r}")
        time.sleep(5 * (attempt + 1))
    return r

def close():
    global _pw, _browser, _ctx
    try:
        if _browser: _browser.close()
        if _pw: _pw.stop()
    finally:
        _pw = _browser = _ctx = None
