---
name: featured-speakers
description: Manage speaker content in two places on the LFNW site — the "Featured Speakers" block on the front page (content/contents.lr) and the standalone Speakers page (content/speakers/contents.lr) — including swapping between a live Sessionize embed and a static placeholder, and the Speakers nav-bar link. Trigger when asked to add/remove/refresh featured speakers, the speaker wall, the Speakers page/listing, or the Sessionize embed(s).
---

# Featured Speakers

## Two independent surfaces — don't confuse them

1. **Homepage "Featured Speakers"** — an `html` flow block (`id:
   featured-speakers`) in `content/contents.lr`, between the `header`
   markdown block and the `cta` columns block.
2. **Standalone Speakers page** — `content/speakers/contents.lr`, linked from
   the top nav via `databags/navbar.ini`'s `[speakers]` entry (`href:
   /speakers`). Has its own `html` block (`id: speakers-list`).

Each can independently be either:
- **Live**: a `<script>` embed of a Sessionize widget. The homepage uses the
  **SpeakerWall** widget (`view/SpeakerWall`); the Speakers page uses the
  **Speakers** list widget (`view/Speakers`). These are tied to *different*
  Sessionize event IDs historically — homepage used `4nzqubyx`, the Speakers
  page used `gbjepa1v`. Don't assume they're the same ID.
- **Placeholder**: static HTML for a single dummy speaker, no Sessionize
  dependency, no live data.

## Current state

Both are currently in **placeholder** mode (no live Sessionize embed
anywhere), and the Speakers page is **unlinked from the nav bar**.

- Homepage block (`content/contents.lr`, `id: featured-speakers`): custom
  inline-styled placeholder — an `<h1>`, an inline SVG circle-silhouette
  avatar, and "Speaker Name TBA" / "Talk Title Placeholder" / "More speakers
  to be announced soon!" text, all with inline `style=` attributes (no
  reliance on sitewide CSS classes).
- Speakers page (`content/speakers/contents.lr`, `id: speakers-list`): a
  `<div class="sz-speaker">` placeholder using the *same CSS classes*
  Sessionize's own widget would generate (`sz-speaker__photo`,
  `sz-speaker__name`, `sz-speaker__tagline`, `sz-speaker__bio`) — these
  already have real styling in `assets/app.scss` (`.speakers-list .content
  .sz-speaker*`, rounded photo, brand colors, responsive grid ≥500px), so
  this placeholder inherits that look for free. Photo is
  `/logos/speaker-placeholder.svg` (a reusable gray silhouette icon,
  distinct from `/logos/placeholder.svg` which is the sponsor "Your Logo
  Here" box — don't mix the two up).
- The two placeholders use different techniques (inline styles vs. shared
  CSS classes) because they were done in separate passes — that's a known
  inconsistency, not a bug. If asked to make them consistent, prefer the
  `sz-speaker` class approach (Speakers page) since it reuses existing CSS
  and will look right without edits if speaker names/taglines get longer.
- `databags/navbar.ini` has no `[speakers]` entry — the page still exists at
  `/speakers/` and works fine, it's just not linked from the menu.

## Going live again for a new year

For **either** surface:

1. Get that year's embed URL from the Sessionize event dashboard — homepage
   wants **Widgets → Speaker Wall**, the Speakers page wants whatever widget
   renders a full list (**Widgets → Speakers List** or similar). The event ID
   in the URL is unique per Sessionize event and changes every year.
2. Replace the placeholder `body:` content with:
   ```
   <script type="text/javascript" src="https://sessionize.com/api/v2/SESSIONIZE_ID/view/SpeakerWall"></script>
   ```
   (homepage — keep the `<h1>Featured Speakers</h1>` before it) or
   ```
   <script type="text/javascript" src="https://sessionize.com/api/v2/SESSIONIZE_ID/view/Speakers"></script>
   ```
   (Speakers page).
3. If re-enabling the Speakers page, add its nav entry back to
   `databags/navbar.ini` (position it after `[schedule]`, matching the
   original order):
   ```
   [speakers]
   label = Speakers
   href = /speakers
   ```
4. Clear the Lektor build cache and restart before previewing — the dev
   container's incremental build doesn't reliably pick up content edits
   otherwise:
   ```
   docker compose exec server sh -c "rm -rf /root/.cache/lektor/builds/*"
   docker compose restart server
   ```

## Removing / going back to placeholder

Reverse of the above: swap the `<script>` body back to the relevant
placeholder markup shown under "Current state", and remove the `[speakers]`
nav entry again if delisting the page.

## History / rationale

- Homepage Featured Speakers was introduced mid-cycle for 2026 (commit
  `22efad8`, "Extended Deadline: First MR from Morgan") once Sessionize had
  enough approved speakers to be worth showing — not a fixture that must
  exist from day one.
- Neither block has a boolean "enabled" field — visibility is purely
  presence/absence of the live-vs-placeholder `body:` content.
