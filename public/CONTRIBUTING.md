# Contributing prices

This repo holds the community price guide for **PortalDex**, a Skylanders
collection tracker. It's a single file, [`prices.json`](prices.json), that lists
an indicative **loose** and **box** price (in US dollars) for every figure the
app knows about. The app bundles a snapshot of this file and reads it offline —
your changes reach players in the next app release.

You don't need to be a developer. There are two ways to help.

## Option A — Open an issue (easiest)

Use **Issues → New issue → Price correction** and fill in the figure, the
suggested price, and where the number comes from. A maintainer will apply it.

## Option B — Edit the file yourself (pull request)

1. Open [`prices.json`](prices.json) and click the ✏️ (edit) button on GitHub.
2. Find the figure. Entries are keyed by `"cid_vid"` and the `name` is there
   only so you can read them — for example:

   ```json
   "18_10240": {"name": "Double Trouble (Series 2)", "loose": 10, "box": 20},
   ```

3. Change **only** the `loose` and/or `box` number. Rules:
   - **Whole US dollars**, no decimals, no `$`, no thousands separators
     (write `12`, not `$12.00` or `12.5`).
   - `0` means *"no price yet"* — leave it 0 if you don't have a figure.
   - A **box** (sealed/in-box) price should not be lower than its **loose**
     price; if your source says otherwise the sample is probably unreliable.
   - **Do not** rename anything, change a `name`, or add/remove keys. New
     figures are added by the maintainer from the app catalog.
4. At the top of the file, increment `"version"` by 1 and set `"generated"` to
   today's date (`YYYY-MM-DD`).
5. Propose the change as a pull request.

## What the automated check does

Every change runs **Validate prices** (a GitHub Action). It confirms the file
is valid JSON, every key is a real figure, names are untouched, prices are sane
whole-dollar numbers, all currencies are present, and the version was bumped. If
it's red, open the check to see exactly what to fix. You can run the same check
locally:

```bash
python scripts/validate_prices.py
```

## A note on accuracy

These are **indicative** prices to help at a flea market or for a rough
collection value — not appraisals. Prefer recent **sold** prices over asking
prices, and cite your source in the issue or PR so others can verify it.

## Contributor Terms (please read before contributing)

The price guide is **owned by PortalDex (Jensen Innovation)** and licensed under
[LICENSE.md](LICENSE.md). Contributions are welcome, but by submitting one you
agree to the following so that the compiled guide has a single, clear owner.

By submitting any contribution (an issue, a pull request, or price data in any
form) you:

1. **Represent** that the contribution is your own work, or that you otherwise
   have the right to submit it, and that submitting it does not violate anyone
   else's rights.
2. **Assign** to PortalDex, to the maximum extent permitted by law, all right,
   title, and interest (including copyright and any database rights) in your
   contribution — and, to the extent any such rights cannot be assigned, grant
   PortalDex a perpetual, worldwide, irrevocable, royalty-free, **exclusive**,
   sublicensable licence to use, reproduce, modify, publish, and distribute it.
   The result is that **PortalDex owns the compiled Data** and is the only party
   that may licence it to others.
3. **Understand** that contributions are **unpaid and voluntary**, that you will
   not receive royalties or compensation, and that PortalDex is under no
   obligation to use your contribution.
4. **Retain** the right to use the individual facts you personally submitted
   (e.g. a single figure's price) elsewhere for your own purposes. What you may
   **not** do is copy or reuse the **compiled guide** (in whole or substantial
   part) outside the official PortalDex apps without a licence — see LICENSE.md.

If you do not agree to these terms, please do not submit contributions.
