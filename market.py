"""Price history, indicators and earnings dates for the screen, from Yahoo Finance.

No API key to keep alive. Everything is defensive: a symbol Yahoo will not
answer for comes back as None and the page leaves it off, saying so.
"""

import math
import time
from datetime import date

import pandas as pd
import yfinance as yf

HISTORY = "14mo"      # enough bars for a 200-day average with room to spare
CHART_BARS = 90       # closes sent to the page for the card chart


def _num(value, places=4):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value) or math.isinf(value):
        return None
    return round(value, places)


def _clean(df):
    """Daily bars with a close, minus Yahoo's occasional 100x pence/pounds glitch."""
    if df is None or df.empty or "Close" not in df:
        return None
    df = df.dropna(subset=["Close", "High", "Low"])
    if len(df) < 60:
        return None
    median = df["Close"].rolling(10, min_periods=3, center=True).median()
    ratio = df["Close"] / median
    return df[(ratio > 0.2) & (ratio < 5)]


def download(symbols):
    """{symbol: DataFrame or None}. One batch call, then a retry for any gaps."""
    out = {}
    try:
        data = yf.download(symbols, period=HISTORY, interval="1d", group_by="ticker",
                           auto_adjust=False, progress=False, threads=True)
    except Exception as exc:  # noqa: BLE001 - anything from Yahoo is a soft failure
        print(f"  batch download failed: {type(exc).__name__}")
        data = None
    for s in symbols:
        try:
            out[s] = _clean(data[s]) if data is not None else None
        except KeyError:
            out[s] = None
    for s in [s for s, df in out.items() if df is None]:
        time.sleep(1)
        try:
            out[s] = _clean(yf.Ticker(s).history(period=HISTORY, auto_adjust=False))
        except Exception as exc:  # noqa: BLE001
            print(f"  history failed for {s}: {type(exc).__name__}")
    missing = [s for s, df in out.items() if df is None]
    if missing:
        print(f"  no history for: {', '.join(missing)}")
    return out


def indicators(df):
    """The numbers index.html scores from. Plain floats; None where too short."""
    c, h, l = df["Close"], df["High"], df["Low"]
    prev = c.shift(1)
    tr = pd.concat([h - l, (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / 14, adjust=False).mean()           # Wilder's ATR(14)
    delta = c.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    rsi = 100 - 100 / (1 + gain / loss)                        # Wilder's RSI(14)
    sma20, sma50, sma200 = c.rolling(20).mean(), c.rolling(50).mean(), c.rolling(200).mean()

    n = len(c)
    last = float(c.iloc[-1])

    def ret(k):
        return _num(last / float(c.iloc[-1 - k]) - 1, 5) if n > k else None

    year = c.iloc[-252:]
    return {
        "bar": df.index[-1].date().isoformat(),
        "close": _num(last),
        "prev": _num(c.iloc[-2]),
        "atr": _num(atr.iloc[-1]),
        "rsi": _num(rsi.iloc[-1], 1),
        "sma20": _num(sma20.iloc[-1]),
        "sma50": _num(sma50.iloc[-1]),
        "sma200": _num(sma200.iloc[-1]),
        "slope50": _num(sma50.iloc[-1] - sma50.iloc[-11]) if n > 60 else None,
        "hi20": _num(h.iloc[-21:-1].max()),                     # the 20 sessions before today
        "lo20": _num(l.iloc[-21:-1].min()),
        "high52": _num(year.max()),
        "low52": _num(year.min()),
        "r5": ret(5), "r21": ret(21), "r63": ret(63),
        "chart": {
            "c": [_num(x) for x in c.iloc[-CHART_BARS:]],
            "m20": [_num(x) for x in sma20.iloc[-CHART_BARS:]],
            "m50": [_num(x) for x in sma50.iloc[-CHART_BARS:]],
        },
    }


def next_earnings(symbol, today=None):
    """The next earnings date Yahoo knows of, as ISO text, or None."""
    today = today or date.today()
    try:
        cal = yf.Ticker(symbol).calendar or {}
        dates = cal.get("Earnings Date") or []
        future = sorted(d for d in dates if isinstance(d, date) and d >= today)
        return future[0].isoformat() if future else None
    except Exception as exc:  # noqa: BLE001
        print(f"  calendar failed for {symbol}: {type(exc).__name__}")
        return None
