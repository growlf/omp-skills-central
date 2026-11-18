---
name: sponsors
description: Manage the sponsors section on the LFNW front page (content/contents.lr) — add a new sponsor to a level, remove one, reset to the start-of-year baseline (Title placeholder + Partners only), or restore the full prior list. Trigger when asked to add/remove a sponsor, set up sponsor levels for a new event year, or reset/restore the sponsors section.
---

# Sponsors

## What this actually is

The sponsors section is a `rows` flow block (`id: sponsors`) in `content/contents.lr`,
positioned between the CTA `columns` block and the venue `map` block. It contains
one `columns` block per **level**, in this fixed display order:

1. **Title** (`id: sponsor-title`)
2. **Partners** (`id: collaborators`)
3. **Gold** (`id: gold-sponsor`)
4. **Silver** (`id: silver-sponsor`)
5. **Bronze** (`id: bronze-sponsor`)
6. **Service** (`id: sponsors-service`)
7. **Community** (`id: sponsors-community`)

Each level's `columns` block holds zero or more `sponsor` flow blocks (from
`flowblocks/sponsor.ini`), with fields:

- `id` — short, lowercase, unique slug (used in DOM ids and the modal anchor)
- `rank` — integer; per `sponsor.ini` "lowest rank has largest presentation
  (1..7)", but in practice past entries used it loosely/inconsistently within
  a level — don't over-think it, just keep it roughly consistent with
  neighboring entries in the same level (Title→1, Partners→2, and so on
  loosely upward per level)
- `title` — sponsor's display name
- `href` — sponsor's URL (or, for the Title placeholder, the prospectus PDF)
- `description` — markdown, shown in the click-through modal; can be one line
  or several paragraphs
- `logo` — path to the logo image, always `logos/<filename>`, where the file
  itself lives in `assets/logos/<filename>` (served at the site root as
  `/logos/<filename>` — see `templates/blocks/sponsor.html`)

**Rendering caveat:** `templates/blocks/columns.html` / `rows.html` render a
`<h1>` heading for a level even if it has zero sponsors in it. An "empty"
level is not a real state — a level's `columns` block must be deleted entirely
once its last sponsor is removed, and re-created (in the correct position in
the level order above) when its first sponsor of the year is added.

## Start-of-year baseline

Every year, before real sponsors are locked in, the section should show only:

- **Title** — one placeholder sponsor advertising the slot:
  - `id: your-logo-here`, `rank: 1`, `title: Your Logo Here`
  - `href: /lfnw2026SponsorshipProspectus.pdf` (update the filename each year
    to match whatever that year's prospectus PDF is actually named/attached as
    under `content/`)
  - `description`: a short sentence inviting the org to become Title sponsor
  - `logo: logos/placeholder.svg` — a reusable dashed-box "Your Logo Here" SVG
    already sitting in `assets/logos/placeholder.svg`; don't recreate it, just
    reference it
- **Partners** — the two recurring, non-monetary partners:
  Cascade STEAM (`logos/CascadeSTEAM.svg`, https://cascadesteam.org/) and
  Jupiter Broadcasting (`logos/jb.png`, https://jupiterbroadcasting.com/).
  (Bellingham Technical College used to appear here too, as the venue/
  co-producer, but was removed entirely from the event for 2026 — see the
  [[venue]] skill. Don't re-add BTC to Partners without checking whether
  that's actually back in effect.)
- Gold, Silver, Bronze, Service, Community — **not present** (no `columns`
  block for any of them) until the first real sponsor lands in each.
- In their place, a single `markdown` block (`id: sponsors-tba`, `class:
  center`) inside the sponsors `rows` section, right after Partners and
  before the rows section ends, saying sponsorship isn't open yet — e.g.
  "The call for sponsors will begin in September." Update the month/wording
  to match that year's actual timeline. **Remove this block** as soon as the
  first real sponsor lands in any level (Gold onward) — it's a "nothing here
  yet" placeholder, not a permanent fixture, and looks wrong sitting above an
  actual sponsor level once one exists.

The exact block to paste in for this baseline (Title + Partners + the
"call for sponsors" notice) is in `reference/sponsors-baseline.lr`.

## Restoring the full prior-year list

`reference/sponsors-full-2026-pre-reset.lr` is a verbatim capture of the
complete `rows: sponsors` block as it stood before the 2026 mid-cycle reset —
every level, every sponsor, full descriptions and logos. It's a paste-back
reference, not something to blindly re-apply (sponsors change year to year;
some of these may not return). Cross-reference with the sponsor before
re-adding them, in case a href/logo/description needs updating.

The reset was done at git commit `17232fa3b82002414ef50fc8e4b0a969fc2704af` in
this repo — `git show 17232fa3:content/contents.lr` also has the untouched
original, if the reference file above ever drifts from the real history.

## Adding a sponsor

Ask the user (don't guess) for whatever isn't already obvious:

1. **Level** — Title / Partners / Gold / Silver / Bronze / Service / Community
2. **Name** (→ `title`)
3. **URL** (→ `href`)
4. **Logo file** — get the actual image file, save it to `assets/logos/` (any
   format already used elsewhere is fine: svg, png, webp, gif, jpg, avif —
   svg preferred when available), reference it as `logo: logos/<filename>`
5. **Description** — a sentence or short paragraph about the sponsor, markdown
   is fine (→ `description`)
6. **id** — derive a short lowercase slug from the name unless the user wants
   a specific one; check it doesn't collide with an existing `id` anywhere in
   `content/contents.lr`
7. **rank** — default to the next-lowest value already used in that level,
   don't ask unless the user cares

Then:

- If that level's `columns` block already exists in `content/contents.lr`,
  append a new `###### sponsor ######` entry inside its `sections:` in the
  same format as its siblings.
- If the level doesn't exist yet (was removed for being empty), create its
  `##### columns #####` block fresh, in the correct position per the level
  order above (immediately after the previous level's block, before the
  next one — or before `#### map ####` if it's the last one present), then
  add the sponsor inside it.
- After editing, clear the Lektor build cache and restart the dev container
  before checking the preview — the container's incremental build does not
  reliably pick up edits to `content/contents.lr` otherwise:

  ```
  docker compose exec server sh -c "rm -rf /root/.cache/lektor/builds/*"
  docker compose restart server
  ```

## Removing a sponsor

Delete its `###### sponsor ######` ... entry. If it was the last sponsor in
its level, delete that level's whole `##### columns #####` block too (see
rendering caveat above). Same cache-clear + restart afterward to preview.
