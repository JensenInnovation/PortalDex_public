# PortalDex price guide

Community-maintained, offline price guide for **PortalDex**, a Skylanders
collection tracker. This repository is the canonical source for figure prices;
the app bundles a snapshot and reads it locally, so it stays fully offline (no
network calls, no tracking).

## Files

| File | What it is |
|------|------------|
| [`prices.json`](prices.json) | The **Skylanders** price guide: one entry per figure, keyed by `cid_vid`, with a `loose` and `box` price in US dollars. **Edit this for Skylanders.** |
| [`catalog.json`](catalog.json) | Generated reference of every valid Skylanders `cid_vid` → figure name. Do not edit by hand — regenerated from the app catalog. |
| [`amiibo_prices.json`](amiibo_prices.json) | The **amiibo** price guide, same format, keyed by the 8-byte amiibo id as `head_tail`. **Edit this for amiibo.** |
| [`amiibo_catalog.json`](amiibo_catalog.json) | Generated reference of every valid amiibo `head_tail` → name. Do not edit by hand. |
| [`scripts/validate_prices.py`](scripts/validate_prices.py) | The validator that CI runs on every change (both guides). |

Each price file is validated against its own catalog file, so keep them together
and, when regenerating, update both.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: fix a number, bump `version`
and `generated`, open a pull request — or just file a **Price correction**
issue and let a maintainer do it.

## How prices reach the app

Updates are pulled into the app at build time and ship with the next release;
there is no live fetch. Each `prices.json` carries a `version` and `generated`
date, both shown in the app so players know how current their guide is.

Prices are **indicative**, not appraisals. `0` means a figure isn't priced yet.

## License & ownership

**Copyright © 2026 Jensen Innovation / PortalDex. All rights reserved.**

This price guide is **proprietary** — see [LICENSE.md](LICENSE.md). It is
developed openly and improved by the community, but the compiled Data is **owned
by PortalDex** and is **not** open-source/open-data. It may be used only within
the official PortalDex apps; any other use requires a written licence from
PortalDex. Contributions are governed by the Contributor Terms in
[CONTRIBUTING.md](CONTRIBUTING.md), under which contributors assign their rights
to PortalDex. The guide is not a copy of, or affiliated with, PriceCharting or
any commercial database.
