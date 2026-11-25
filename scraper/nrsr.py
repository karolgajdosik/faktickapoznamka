"""Polite HTTP client for nrsr.sk: identifies itself, rate-limits, retries."""
import time, requests

BASE = "https://www.nrsr.sk/web/Default.aspx"
UA = "faktickapoznamka.sk-bot/0.1 (+https://faktickapoznamka.sk/o-projekte/; kontakt@faktickapoznamka.sk)"
DELAY = 1.5  # seconds between requests — be gentle with a public institution's server

_s = requests.Session()
_s.headers.update({"User-Agent": UA, "Accept-Language": "sk,en;q=0.5"})
_last = 0.0

def get(params: dict | None = None, url: str = BASE, tries: int = 3) -> requests.Response:
    global _last
    for attempt in range(tries):
        wait = DELAY - (time.time() - _last)
        if wait > 0: time.sleep(wait)
        _last = time.time()
        try:
            r = _s.get(url, params=params, timeout=30)
            if r.status_code < 500 and r.status_code != 429:
                r.encoding = r.apparent_encoding if r.encoding in (None, "ISO-8859-1") else r.encoding
                return r
        except requests.RequestException:
            if attempt == tries - 1: raise
        time.sleep(5 * (attempt + 1))
    return r
