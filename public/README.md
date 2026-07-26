# PortalDex price guide

Community-maintained, offline price guide for **PortalDex**, a Skylanders
collection tracker. This repository is the canonical source for figure prices;
the app bundles a snapshot and reads it locally, so it stays fully offline (no
network calls, no tracking).

## Files

| File | What it is |
|------|------------|
| [`prices.json`](prices.json) | The price guide: one entry per figure, keyed by `cid_vid`, with a `loose` and `box` price in US dollars. **This is the file you edit.** |
| [`catalog.json`](catalog.json) | Generated reference of every valid `cid_vid` → figure name. Do not edit by hand — it's regenerated from the app catalog. |
| [`scripts/validate_prices.py`](scripts/validate_prices.py) | The validator that CI runs on every change. |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: fix a number, bump `version`
and `generated`, open a pull request — or just file a **Price correction**
issue and let a maintainer do it.

## How prices reach the app

Updates are pulled into the app at build time and ship with the next release;
there is no live fetch. Each `prices.json` carries a `version` and `generated`
date, both shown in the app so players know how current their guide is.

Prices are **indicative**, not appraisals. `0` means a figure isn't priced yet.
