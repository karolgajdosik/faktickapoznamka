# faktická poznámka

Nezávislá, neoficiálna stránka o tom, ako hlasujú poslanci Národnej rady SR. Inšpirované projektom [skupstina.live](https://skupstina.live/).

**Náklady: 0 €** (okrem domény): GitHub Actions (scraper) + Cloudflare Workers (statická stránka + `/api/live`).

## Ako to funguje

```
GitHub Actions (cron) ── scraper/run.py ──> data/*.json (commit) ──> astro build ──> wrangler deploy
Cloudflare Worker: statické súbory z dist/ + /api/live (čo sa práve rokuje, cache 60 s)
```

| Priečinok | Obsah |
|---|---|
| `src/` | stránka (Astro, statický výstup) |
| `data/` | dáta: `mps.json`, `meta.json`, `votes/<id>.json` |
| `scraper/` | Python scraper nrsr.sk (`probe.py`, `parse.py`, `run.py`) |
| `worker/` | Cloudflare Worker |
| `.github/workflows/` | `probe.yml` (ručne), `update.yml` (cron + deploy) |

## Formát dát

`data/votes/<id>.json`: `id`, `session`, `number`, `datetime`, `title`, `tlac`, `passed`, `counts`, `votes` (`{ PoslanecID: "Z"|"P"|"?"|"N"|"0" }`).
Kódy: Z = za, P = proti, ? = zdržal sa, N = nehlasoval, 0 = neprítomný. Dáta môžete voľne použiť, uveďte zdroj nrsr.sk.

## Lokálne

```sh
npm install
npm run demo-data   # vymyslené ukážkové dáta
npm run dev
```

## Nasadenie (jednorazovo)

1. Doména v Cloudflare (nameservery u registrátora).
2. Cloudflare → *My Profile → API Tokens → Create Token* → šablóna **Edit Cloudflare Workers**, zóna `faktickapoznamka.sk`.
3. GitHub → *Settings → Secrets and variables → Actions*: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
4. *Actions → Probe nrsr.sk → Run workflow* (overí prístup na nrsr.sk, uloží vzorky do `probe/`).
5. Po kalibrácii parserov: *Actions → Update data and deploy → Run workflow* s počiatočným ID hlasovania.

## Zásady

- Neoficiálna stránka, žiadne logá ani znak NR SR.
- Scraper sa identifikuje (User-Agent s kontaktom) a robí max. 1 požiadavku za 1,5 s.
- Video sa iba odkazuje na oficiálny prenos, neprevysiela sa.
- Kluby sú v grafoch zoradené podľa veľkosti, nie podľa politickej orientácie.
