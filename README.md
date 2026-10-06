# CFD Screen

Long and short swing setups on the major indices and large-cap US and UK
shares, sized for leverage, margin, spread and overnight funding.

**Live:** https://fredh2005.github.io/cfd-screen/

Rebuilt from Yahoo Finance daily bars four times each weekday by GitHub
Actions. `data.js` holds the universe and dated events; `index.html` does the
scoring and sizing in the browser. See `CLAUDE.md` for the rules.

    pip install -r requirements.txt
    python3 build.py
    python3 -m http.server -d site

Not investment advice.
