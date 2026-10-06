"""Add price history and indicators to the screen and stage it in site/.

    python3 build.py

data.js is the universe plus the dated macro events, and the only file a
refresh edits. index.html does all the scoring, sizing and rendering in the
browser. This script's only job is to fetch daily bars from Yahoo Finance,
work out the indicators the page scores from (moving averages, ATR, RSI,
20-day range, returns), look up each share's next earnings date and the FX
rates the sizing needs, write all of it into site/data.js next to the
universe, and copy the page and its assets alongside.
"""

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import market

LONDON = ZoneInfo("Europe/London")
OUT = Path("site")
COPY = ["index.html", "manifest.webmanifest", "sw.js", "icon-192.png", "icon-512.png", "apple-touch-icon.png"]
PREFIX = "window.__SCREEN__ ="


def load_screen(path="data.js"):
    """data.js is a JS assignment wrapping a JSON literal; read the literal."""
    text = Path(path).read_text()
    start = text.index(PREFIX) + len(PREFIX)
    end = text.rindex("}") + 1
    return json.loads(text[start:end])


def main():
    now = datetime.now(LONDON)
    data = load_screen()
    names = data["names"]
    symbols = [n["symbol"] for n in names]
    fx = list(data["fx"].values())
    print(f"building {now:%A %-d %B %H:%M}: {len(symbols)} instruments, {len(fx)} fx")

    bars = market.download(symbols + fx)
    ind = {s: market.indicators(df) for s, df in bars.items() if df is not None}
    live = sum(1 for s in symbols if s in ind)
    if live < len(symbols) * 3 // 4:
        sys.exit(f"only {live}/{len(symbols)} instruments priced - not publishing")
    missing_fx = [p for p in fx if p not in ind]
    if missing_fx:
        sys.exit(f"no FX rate for {', '.join(missing_fx)} - sizing would be wrong, not publishing")

    earnings = {}
    for n in names:
        if n["cls"] == "share":
            # A hand-set date in data.js wins over Yahoo, which has none for some UK names.
            earnings[n["symbol"]] = n.get("earnings") or market.next_earnings(n["symbol"], now.date())
            time.sleep(0.3)
    print(f"  earnings dates found for {sum(1 for v in earnings.values() if v)}/{len(earnings)} shares")

    staged = dict(data)
    staged["ind"] = {s: v for s, v in ind.items() if s in symbols}
    staged["rates"] = {cur: ind[pair]["close"] for cur, pair in data["fx"].items()}
    staged["earnings"] = earnings
    staged["built"] = now.isoformat(timespec="minutes")
    staged["live"] = live

    OUT.mkdir(exist_ok=True)
    (OUT / "data.js").write_text(
        "// Built by build.py: the universe from data.js plus indicators. Do not edit.\n"
        + PREFIX + " " + json.dumps(staged, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for f in COPY:
        shutil.copy(f, OUT / f)
    print(f"  wrote site/data.js with {live}/{len(symbols)} instruments; copied {len(COPY)} files")


if __name__ == "__main__":
    main()
