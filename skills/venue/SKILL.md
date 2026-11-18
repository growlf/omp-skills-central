---
name: venue
description: Manage the event venue across the LFNW site — the homepage "Venue Map" widget (content/contents.lr), the standalone campus floor-map page (/map), and venue mentions in the project description. Trigger when asked to set/change/announce the venue, update the venue map, rebuild the campus map page, or when a venue partner (e.g. a host college) needs to be added or removed.
---

# Venue

## The two separate "map" things

Don't confuse these — they're different features, in different files:

1. **Homepage "Venue Map" widget** — a `map` flow block (`id: venue`) inside
   `content/contents.lr`'s `sections`, right before the closing of the page.
   Renders a small embedded Leaflet/OpenStreetMap widget centered on
   `lat`/`long` with a `destination` markdown blurb underneath. Fields (see
   `flowblocks/map.ini`): `id`, `class`, `lat`, `long`, `zoom`, `destination`.
   This section is optional per the README — present only when there's
   something worth showing.
2. **`/map` page** (`content/map/contents.lr`) — a full standalone page with
   an actual campus floor-map *image* and a link to an interactive room-by-room
   map (used for attendee wayfinding once a specific venue/building is locked
   in). Linked from the top nav via `databags/navbar.ini`'s `[map]` entry.
   This only makes sense once there's a confirmed physical venue with rooms to
   navigate — it was removed when the venue went back to TBA (see below).

## Current state (as of the 2026 BTC departure)

Bellingham Technical College (BTC) was removed as the venue and co-producer.
Current state:

- Project description (`lfnw.lektorproject`, also read as
  `databags/lektorproject.ini` via symlink) — co-producer list now reads just
  "Cascade STEAM and Jupiter Broadcasting". No institution is credited as
  venue/host.
- Homepage tagline (`content/contents.lr`, near the top) reads
  "April 24 - 26, 2026 • Venue To Be Announced" instead of naming a campus.
- Homepage Venue Map widget is centered on the geographic center of Holly
  Street in downtown Bellingham (`lat: 48.7508747`, `long: -122.4809831`,
  `zoom: 14`) as a neutral "somewhere in Bellingham" placeholder — it is NOT a
  real venue pin, just a rough area indicator until a venue is confirmed.
  `destination` explicitly says the venue is still being finalized.
- The `/map` campus-floor-map page and its nav entry are **removed entirely**
  (not just emptied) — an unconfirmed venue has no floor plan to show.
- `reference/map-page-btc-2026.lr` has the exact removed page content
  (heading, `../btcmap.jpg` image reference, interactive-map link) at git
  commit `e00a614d3949f2224488c0c4895db90c5fe99447` (last commit that touched
  it) for structural reference — the actual images (`btcmap.jpg`, "BTC Map
  with Legend.jpg") are untouched in `content/`, but they're specific to the
  old BTC campus and won't be reusable for a different venue's floor plan.

## Announcing a new venue

Ask the user for: venue name, address, a link (venue's own site or an
OpenStreetMap link for the "get directions" text), and — if a campus/building
floor-map image and an interactive room map exist — those too.

Then:

1. **Homepage tagline** (`content/contents.lr`) — replace "Venue To Be
   Announced" with the venue name.
2. **Venue Map widget** (`content/contents.lr`, `map` block `id: venue`) —
   set `lat`/`long` to the venue's real coordinates (look it up, e.g. via
   Nominatim: `https://nominatim.openstreetmap.org/search?q=<address>&format=json`),
   `zoom: 15`–`17` for a real street-address pin (14 was chosen for the TBA
   placeholder specifically because it shows the general neighborhood, not a
   precise point), and rewrite `destination` with the real address and a
   link to the venue's site or its OpenStreetMap node/way.
3. **Co-producer credit** — only add the venue back into
   `lfnw.lektorproject`'s `description`/`description_markdown` if the venue
   is *also* a co-producer (as BTC was) — a rented/one-off venue with no
   organizing role shouldn't be credited there.
4. **`/map` campus page** (only if a floor-map image and/or interactive map
   exist for the new venue) — recreate `content/map/contents.lr` using
   `reference/map-page-btc-2026.lr` as a structural template (same markdown +
   html flow-block shape, new image/link/heading), add the image as a content
   attachment, and re-add the `[map]` entry to `databags/navbar.ini`:
   ```
   [map]
   label = Map
   href = /map
   ```
5. Clear the Lektor build cache and restart before previewing — the dev
   container's incremental build doesn't reliably pick up edits otherwise:
   ```
   docker compose exec server sh -c "rm -rf /root/.cache/lektor/builds/*"
   docker compose restart server
   ```

## Removing a venue (going back to TBA)

Reverse of the above: swap the tagline and `destination` back to "Venue To Be
Announced" wording, re-center the map on a neutral area point (Holly Street's
center is the established placeholder for Bellingham), drop any co-producer
credit tied to that venue, and delete `content/map/contents.lr` plus its
`navbar.ini` entry if the venue had one.
