# Publishing to PortalDex_public (maintainer notes)

The community price guide lives in a **separate public repo**
(`PortalDex_public`) so contributors can propose price changes without access to
the app source. This `public/` folder in the private repo is the template for
that repo's non-data files. The two data files (`prices.json`, `catalog.json`)
are generated here and copied over.

## One-time setup

Create the public repo with this layout:

```
PortalDex_public/
├── README.md
├── CONTRIBUTING.md
├── PUBLISHING.md              (optional; maintainer-only)
├── prices.json                (from the private repo root)
├── catalog.json               (from the private repo root)
├── scripts/
│   └── validate_prices.py
└── .github/
    ├── pull_request_template.md
    ├── ISSUE_TEMPLATE/
    │   ├── price_correction.yml
    │   └── config.yml
    └── workflows/
        └── validate-prices.yml
```

Copy everything in this `public/` folder to the repo root, then add the two
generated data files from the private repo root.

## Each release — sync prices back and forth

1. **Pull merged contributions in.** Copy the public repo's `prices.json` into
   the private repo root (overwrite). This brings in community edits.
2. **Regenerate** so names/keys and `catalog.json` match the current catalog and
   the file is re-serialized canonically:

   ```bash
   python scripts/build_prices.py          # writes prices.json + catalog.json
   ```

   `build_prices.py` preserves all existing prices; it only adds/removes figures
   and refreshes `catalog.json`. It bumps `version` when the figure set changes —
   otherwise bump it yourself if you changed any numbers.
3. **Validate** before shipping:

   ```bash
   python public/scripts/validate_prices.py --prices prices.json --catalog catalog.json
   ```

4. **Bundle into the app** (Phase 3): `scripts/bundle_prices.py` copies the
   validated `prices.json` into both app bundles.
5. **Push the refreshed `prices.json` + `catalog.json` back to
   `PortalDex_public`** so the public repo and the shipped app agree.

## Why a generated `catalog.json`?

The public repo has no access to `figure_seed.dart`, so CI can't otherwise tell
whether a key is a real figure or whether a `name` was tampered with.
`catalog.json` is that authoritative reference. `validate_prices.py` falls back
to parsing `figure_seed.dart` when run inside the private repo, so both
environments validate identically.
