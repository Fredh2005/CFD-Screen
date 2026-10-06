// The universe and the dated macro events. This is the only file a refresh edits.
// build.py adds price history, indicators and earnings dates; index.html scores
// and renders everything in the browser.
window.__SCREEN__ = {
 "asof": "2026-10-06",
 "benchmarks": {"US": "^GSPC", "UK": "^FTSE", "DE": "^GDAXI"},
 "fx": {"USD": "GBPUSD=X", "EUR": "GBPEUR=X"},
 "names": [
  {"id": "us500",  "symbol": "^GSPC",  "name": "S&P 500",     "cfd": "US500", "cls": "index", "market": "US", "unit": "USD"},
  {"id": "us100",  "symbol": "^NDX",   "name": "Nasdaq 100",  "cfd": "US100", "cls": "index", "market": "US", "unit": "USD"},
  {"id": "uk100",  "symbol": "^FTSE",  "name": "FTSE 100",    "cfd": "UK100", "cls": "index", "market": "UK", "unit": "GBP"},
  {"id": "de40",   "symbol": "^GDAXI", "name": "DAX",         "cfd": "DE40",  "cls": "index", "market": "DE", "unit": "EUR"},

  {"id": "aapl", "symbol": "AAPL", "name": "Apple",            "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "nvda", "symbol": "NVDA", "name": "NVIDIA",           "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "msft", "symbol": "MSFT", "name": "Microsoft",        "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "googl","symbol": "GOOGL","name": "Alphabet",         "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "amzn", "symbol": "AMZN", "name": "Amazon",           "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "mu",   "symbol": "MU",   "name": "Micron",           "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "be",   "symbol": "BE",   "name": "Bloom Energy",     "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "nbis", "symbol": "NBIS", "name": "Nebius",           "cls": "share", "market": "US", "unit": "USD", "watch": true},
  {"id": "meta", "symbol": "META", "name": "Meta Platforms",   "cls": "share", "market": "US", "unit": "USD"},
  {"id": "tsla", "symbol": "TSLA", "name": "Tesla",            "cls": "share", "market": "US", "unit": "USD"},
  {"id": "avgo", "symbol": "AVGO", "name": "Broadcom",         "cls": "share", "market": "US", "unit": "USD"},
  {"id": "amd",  "symbol": "AMD",  "name": "AMD",              "cls": "share", "market": "US", "unit": "USD"},
  {"id": "nflx", "symbol": "NFLX", "name": "Netflix",          "cls": "share", "market": "US", "unit": "USD"},
  {"id": "pltr", "symbol": "PLTR", "name": "Palantir",         "cls": "share", "market": "US", "unit": "USD"},
  {"id": "orcl", "symbol": "ORCL", "name": "Oracle",           "cls": "share", "market": "US", "unit": "USD"},
  {"id": "jpm",  "symbol": "JPM",  "name": "JPMorgan Chase",   "cls": "share", "market": "US", "unit": "USD"},
  {"id": "lly",  "symbol": "LLY",  "name": "Eli Lilly",        "cls": "share", "market": "US", "unit": "USD"},
  {"id": "xom",  "symbol": "XOM",  "name": "Exxon Mobil",      "cls": "share", "market": "US", "unit": "USD"},
  {"id": "cost", "symbol": "COST", "name": "Costco",           "cls": "share", "market": "US", "unit": "USD"},

  {"id": "azn",  "symbol": "AZN.L",  "name": "AstraZeneca",     "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "shel", "symbol": "SHEL.L", "name": "Shell",           "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "hsba", "symbol": "HSBA.L", "name": "HSBC",            "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "ulvr", "symbol": "ULVR.L", "name": "Unilever",        "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "bp",   "symbol": "BP.L",   "name": "BP",              "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "rio",  "symbol": "RIO.L",  "name": "Rio Tinto",       "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "gsk",  "symbol": "GSK.L",  "name": "GSK",             "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "barc", "symbol": "BARC.L", "name": "Barclays",        "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "lloy", "symbol": "LLOY.L", "name": "Lloyds Banking",  "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "rr",   "symbol": "RR.L",   "name": "Rolls-Royce",     "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "bats", "symbol": "BATS.L", "name": "British American Tobacco", "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "glen", "symbol": "GLEN.L", "name": "Glencore",        "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "rel",  "symbol": "REL.L",  "name": "RELX",            "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "nwg",  "symbol": "NWG.L",  "name": "NatWest",         "cls": "share", "market": "UK", "unit": "GBp"},
  {"id": "ba",   "symbol": "BA.L",   "name": "BAE Systems",     "cls": "share", "market": "UK", "unit": "GBp"}
 ],
 "macro": [
  {"date": "2026-10-28", "what": "FOMC rate decision (7pm UK)",  "markets": ["US", "UK", "DE"], "src": "federalreserve.gov"},
  {"date": "2026-10-29", "what": "ECB rate decision (1.15pm UK)", "markets": ["DE"],            "src": "ecb.europa.eu"},
  {"date": "2026-11-05", "what": "Bank of England rate decision", "markets": ["UK"],            "src": "bankofengland.co.uk"},
  {"date": "2026-12-09", "what": "FOMC rate decision (7pm UK)",  "markets": ["US", "UK", "DE"], "src": "federalreserve.gov"},
  {"date": "2026-12-17", "what": "ECB rate decision",            "markets": ["DE"],            "src": "ecb.europa.eu"},
  {"date": "2026-12-17", "what": "Bank of England rate decision", "markets": ["UK"],            "src": "bankofengland.co.uk"}
 ]
};
