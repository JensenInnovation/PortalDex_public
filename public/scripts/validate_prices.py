#!/usr/bin/env python3
"""Validate prices.json for the PortalDex community price guide.

Runs both locally (pre-commit) and in CI (GitHub Action) on every change to
prices.json. It is intentionally self-contained (stdlib only) so it can live in
the public, prices-only PortalDex_public repo with no other tooling.

Checks
------
Structural / scaffold:
  * file is valid JSON with no duplicate keys anywhere
  * version is an integer >= 1
  * generated is an ISO date (YYYY-MM-DD)
  * baseCurrency == "USD"
  * rates covers every required currency, each a positive number, USD == 1
Per price entry:
  * name is a non-empty string
  * loose and box are whole-dollar integers >= 0 and within a sane ceiling
Catalog cross-check (when a reference is available):
  * every price key exists in the catalog
  * every catalog key is present in prices.json (complete coverage)
  * each name matches the catalog's display name for that key
Version bump (CI, when --base is given):
  * if any price value changed vs the base revision, version must be greater

The catalog reference is, in order of preference:
  1. --catalog PATH
  2. a catalog.json next to prices.json (authoritative in the public repo)
  3. a portaldex_flutter/lib/data/figure_seed.dart parsed from the dev repo
If none is found, catalog checks are skipped with a warning (not an error), so
the same script still runs in a bare public repo that only has prices.json.

Exit code 0 = valid, 1 = one or more errors (warnings never fail the build).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

REQUIRED_CURRENCIES = {
    "USD", "EUR", "JPY", "GBP", "CNY", "AUD", "CAD", "CHF",
    "HKD", "SGD", "DKK", "SEK", "NOK", "ISK",
}
MAX_PRICE = 100_000          # a single figure over $100k is certainly a typo
KEY_RE = re.compile(r"^\d+_\d+$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> bool:
        return not self.errors


# --------------------------------------------------------------------------- #
# Locating files
# --------------------------------------------------------------------------- #

def _first_existing(*paths: str) -> str | None:
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def find_prices(explicit: str | None) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        explicit,
        os.path.join(os.getcwd(), "prices.json"),
        os.path.join(here, "prices.json"),
        os.path.join(here, "..", "prices.json"),          # public repo root
        os.path.join(here, "..", "..", "prices.json"),    # dev repo root
    ]
    found = _first_existing(*candidates)
    if not found:
        sys.exit("ERROR: could not locate prices.json (pass --prices PATH)")
    return os.path.abspath(found)


def load_catalog(explicit: str | None, prices_dir: str) -> tuple[dict[str, str], str] | None:
    """Return ({key: display_name}, source_description) or None if unavailable."""
    here = os.path.dirname(os.path.abspath(__file__))

    cat_json = _first_existing(
        explicit,
        os.path.join(prices_dir, "catalog.json"),
        os.path.join(here, "catalog.json"),
        os.path.join(here, "..", "catalog.json"),
    )
    if cat_json:
        with open(cat_json, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            sys.exit(f"ERROR: {cat_json} is not a JSON object of key -> name")
        return {str(k): str(v) for k, v in data.items()}, os.path.relpath(cat_json)

    seed = _first_existing(
        os.path.join(prices_dir, "portaldex_flutter", "lib", "data", "figure_seed.dart"),
        os.path.join(here, "..", "..", "portaldex_flutter", "lib", "data", "figure_seed.dart"),
    )
    if seed:
        return _parse_seed(seed), os.path.relpath(seed)

    return None


def _parse_seed(path: str) -> dict[str, str]:
    """Parse figure_seed.dart into {cid_vid: display_name}, deduped by key."""
    strv = r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\""

    def q(line: str, key: str) -> str | None:
        m = re.search(r"\b" + key + r":\s*(" + strv + r")", line)
        return m.group(1)[1:-1] if m else None

    def n(line: str, key: str) -> int | None:
        m = re.search(r"\b" + key + r":\s*(\d+)", line)
        return int(m.group(1)) if m else None

    out: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "_f(" not in line:
                continue
            cid, vid, name = n(line, "c"), n(line, "v"), q(line, "n")
            if cid is None or vid is None or name is None:
                continue
            key = f"{cid}_{vid}"
            if key in out:
                continue
            lbl = q(line, "lbl")
            out[key] = f"{name} ({lbl})" if lbl else name
    return out


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def _no_dup_keys(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate key {k!r}")
        seen[k] = v
    return seen


def check_scaffold(doc: dict, rep: Report) -> None:
    version = doc.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        rep.error(f'"version" must be an integer >= 1 (got {version!r})')

    gen = doc.get("generated")
    if not isinstance(gen, str):
        rep.error('"generated" must be a string date')
    else:
        try:
            datetime.date.fromisoformat(gen)
        except ValueError:
            rep.error(f'"generated" must be an ISO date YYYY-MM-DD (got {gen!r})')

    if doc.get("baseCurrency") != "USD":
        rep.error('"baseCurrency" must be "USD"')

    rates = doc.get("rates")
    if not isinstance(rates, dict):
        rep.error('"rates" must be an object')
        return
    missing = REQUIRED_CURRENCIES - rates.keys()
    if missing:
        rep.error(f"rates missing currencies: {', '.join(sorted(missing))}")
    extra = rates.keys() - REQUIRED_CURRENCIES
    if extra:
        rep.warn(f"rates has unexpected currencies: {', '.join(sorted(extra))}")
    for cur, val in rates.items():
        if not isinstance(val, (int, float)) or isinstance(val, bool) or val <= 0:
            rep.error(f"rate for {cur} must be a positive number (got {val!r})")
    if isinstance(rates.get("USD"), (int, float)) and rates["USD"] != 1:
        rep.error(f'rate for USD must be 1 (got {rates["USD"]!r})')


def check_entries(prices: dict, rep: Report) -> None:
    if not isinstance(prices, dict):
        rep.error('"prices" must be an object keyed by "cid_vid"')
        return
    for key, entry in prices.items():
        where = f"prices[{key!r}]"
        if not KEY_RE.match(key):
            rep.error(f'{where}: key is not in "cid_vid" form')
        if not isinstance(entry, dict):
            rep.error(f"{where}: entry must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            rep.error(f"{where}: name must be a non-empty string")
        for field in ("loose", "box"):
            val = entry.get(field)
            if not isinstance(val, int) or isinstance(val, bool):
                rep.error(f"{where}: {field} must be a whole-dollar integer (got {val!r})")
            elif val < 0:
                rep.error(f"{where}: {field} must be >= 0 (got {val})")
            elif val > MAX_PRICE:
                rep.error(f"{where}: {field} = {val} exceeds sane ceiling {MAX_PRICE}")
        loose, box = entry.get("loose"), entry.get("box")
        if isinstance(loose, int) and isinstance(box, int) and box and box < loose:
            rep.warn(f"{where}: box {box} is below loose {loose} — check the source")


def check_catalog(prices: dict, catalog: dict[str, str], src: str, rep: Report) -> None:
    price_keys = set(prices.keys())
    cat_keys = set(catalog.keys())

    for key in sorted(price_keys - cat_keys):
        rep.error(f"prices[{key!r}] is not a known catalog figure (per {src})")
    for key in sorted(cat_keys - price_keys):
        rep.error(f"catalog figure {key!r} is missing from prices.json (per {src})")
    for key in sorted(price_keys & cat_keys):
        want = catalog[key]
        got = prices[key].get("name")
        if got != want:
            rep.error(f'prices[{key!r}] name {got!r} != catalog {want!r}')


def check_version_bump(prices: dict, version, base_path: str, rep: Report) -> None:
    if not os.path.isfile(base_path):
        rep.warn(f"--base {base_path} not found; skipping version-bump check")
        return
    with open(base_path, encoding="utf-8") as f:
        base = json.load(f)
    base_prices = base.get("prices", {})
    base_version = base.get("version", 0)

    def values(p):
        return {k: (v.get("loose"), v.get("box")) for k, v in p.items()}

    changed = values(prices) != values(base_prices)
    if changed and not (isinstance(version, int) and version > base_version):
        rep.error(
            f"prices changed but version was not bumped "
            f"(base {base_version}, current {version}) — increment \"version\"")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the PortalDex prices.json.")
    ap.add_argument("--prices", help="path to prices.json (auto-detected otherwise)")
    ap.add_argument("--catalog", help="path to catalog.json (auto-detected otherwise)")
    ap.add_argument("--base", help="path to the previous prices.json for the version-bump check")
    args = ap.parse_args()

    prices_path = find_prices(args.prices)
    prices_dir = os.path.dirname(prices_path)

    rep = Report()

    try:
        with open(prices_path, encoding="utf-8") as f:
            doc = json.load(f, object_pairs_hook=_no_dup_keys)
    except ValueError as e:
        print(f"FAIL  {os.path.relpath(prices_path)}: invalid JSON — {e}")
        return 1

    check_scaffold(doc, rep)
    prices = doc.get("prices", {})
    check_entries(prices, rep)

    catalog = load_catalog(args.catalog, prices_dir)
    if catalog is None:
        rep.warn("no catalog reference found — key/name/coverage checks skipped")
    else:
        cat_map, src = catalog
        check_catalog(prices, cat_map, src, rep)

    if args.base:
        check_version_bump(prices, doc.get("version"), args.base, rep)

    rel = os.path.relpath(prices_path)
    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"FAIL  {e}")

    n = len(prices) if isinstance(prices, dict) else 0
    if rep.ok():
        print(f"PASS  {rel}: {n} entries valid"
              + (f", {len(rep.warnings)} warning(s)" if rep.warnings else ""))
        return 0
    print(f"\n{len(rep.errors)} error(s) in {rel}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
