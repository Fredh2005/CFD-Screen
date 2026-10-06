# CFD Screen

A long/short swing screener for CFDs on Trading 212. It covers the four major
indices (S&P 500, Nasdaq 100, FTSE 100, DAX) and about 34 large-cap US and UK
shares, including the user's morning-brief watchlist. The horizon is a hold of
a few days. Each instrument is scored long and short, the stronger side gets a
card, and every card is sized for the user's account: margin, exposure, the £
at the stop, spread and overnight funding.

Same house style and split as `event-screen` and `morning-brief`. The live site
is https://fredh2005.github.io/cfd-screen/

## Files

- `data.js` — the universe (`names[]`), benchmarks, FX pairs and dated macro
  events (`macro[]`). Sets `window.__SCREEN__`. **This is the only file a
  refresh edits.**
- `index.html` — scoring, sizing, charts and rendering, all in the browser.
  Without a build it says "Not built yet", because it needs price history.
- `market.py` — Yahoo daily bars (one batch download, then retries), the
  indicators (SMA 20/50/200, Wilder ATR(14) and RSI(14), prior 20-day
  high/low, 5/21/63-day returns, 90-bar chart series) and next earnings dates.
- `build.py` — runs `market.py` over the universe and FX pairs and writes
  `site/data.js`. It refuses to publish with under 3/4 of instruments priced or
  without an FX rate.
- `.github/workflows/screen.yml` — builds four times each weekday and on every
  push, then deploys `site/` to Pages. `keepalive.yml` stops GitHub disabling
  the schedule.

Local build: `~/vwrp-screener/venv/bin/python build.py`, then serve `site/`
(`python3 -m http.server -d site`). It does not work from file://, because the
in-app browser snapshots file:// pages without loading `data.js`.

Do not move the scoring into Python. Keeping it in the page means the user's
settings (account, risk, ATR multiples, leverage, funding, spread) re-score and
re-size everything live.

## The rules that matter

- **The levels are mechanical, never forecasts.** *If it works* and *If it
  fails* are the price ± the user's ATR multiples (default 3 and 1.5), or the
  user's own override on the card. Never write a "target" from an opinion, and
  never present a level as a prediction.
- **No probabilities and no recommendations.** The score ranks rule-based
  setups. It is not a chance of success, and the page must never say "buy" or
  "sell". Labels stay as **Price now / If it works / If it fails** and
  **LONG / SHORT** (the side the rules favour).
- **Trend-following only.** The rules look for pullbacks within a trend and
  breakouts or breakdowns of the 20-day range. Do not add counter-trend
  "reversal" setups without the user asking.
- **Costs are always shown.** Every card shows spread and funding, and net R:R
  includes both. Funding and spread defaults are estimates, and the page tells
  the user to replace them with Trading 212's real figures.
- **Event risk is a penalty, not a filter.** Earnings inside the hold get a
  red flag, because a gap can go straight through the stop.

## Scoring (index.html → score())

```
score = (trend×0.30 + setup×0.30 + rs×0.15 + market×0.25) × 10 − stretch×3 − event×2.5
```
A card needs setup > 0 and score ≥ 55. Everything else goes in "No clear
trade" with both scores. The methodology panel on the page explains each input
in plain words. Keep it in step with the code.

## Refreshing (weekly, by hand or by routine)

1. Add the next dated macro events to `macro[]`, each verified against the
   primary calendar (federalreserve.gov, ecb.europa.eu, bankofengland.co.uk;
   BLS for CPI/payrolls if added). Drop past ones.
2. Earnings dates come from Yahoo on every build. Spot-check any that look
   wrong. Yahoo has none for some UK names (Unilever, Rio, Rolls-Royce, BAT,
   Glencore, RELX, BAE). Fill those in by adding `"earnings": "YYYY-MM-DD"`
   to the name; a hand-set date wins over Yahoo. Verify it against the company's
   own results calendar first.
3. Add or remove names only if they are liquid large caps that Trading 212
   offers as CFDs.

## Deployment

Pages source must be GitHub Actions. The Mac's git has no GitHub credential:
commit locally and the user pushes with GitHub Desktop. If the site freezes,
first look for an old deploy run stuck "queued" that is holding the `pages`
concurrency group (this happened to event-screen on 6 Oct 2026).
