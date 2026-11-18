---
name: homepage-ctas
description: Manage the header "Take our Survey" block and the CTA button row (Individual Sponsorship / Call for Sponsors / Discord / T-Shirts) on the LFNW front page (content/contents.lr). Trigger when asked to add/remove/restore the survey block, or any of the call-to-action cards near the top of the homepage.
---

# Homepage CTAs

## The two pieces

1. **Survey block** — plain markdown lines inside the `header` markdown flow
   block in `content/contents.lr` (same block as the logo and date/venue
   tagline), not a separate flow block of its own.
2. **CTA card row** — the `cta` `columns` flow block (`id: cta`), a `sections`
   list of `call` flow blocks (see `flowblocks/call.ini`: `title`, `lead`,
   `description`, `href`, `button_label`). Sits right after the `header`
   block (and after Featured Speakers, if present).

## Current state

Both the Survey block and the "Call for Sponsors" CTA card are **removed**,
per explicit user request, to be restored later ("when the fest begins" /
when sponsorship season opens). The `cta` row currently has only:
Individual Sponsorship, LinuxFest Northwest Discord Server, Get Your
T-Shirts.

## Restoring the Survey block

Goes inside the `header` markdown block, right after the date/venue tagline
line (e.g. `### April 24 - 26, 2026 • ...`) and before the next flow block
marker (`#### html ####` or `#### columns ####`, whichever comes first):

```
#### We are looking forward to seeing you at LFNW 2026!

Share your feedback and help shape the future of the fest

<a aria-label="Close" href="https://docs.google.com/forms/d/e/1FAIpQLSdWnGbpISHggz0tjM1CJwbtYgZ--J5lXsSDX5mdkNdsZnqemQ/viewform" target="_blank" class="cta-button">Take our Survey</a>
```

The heading wording ("We are looking forward to...") and the Google Form link
are whatever was current when last removed — check with the user whether the
form link should be refreshed for the new cycle before restoring verbatim.

## Restoring the "Call for Sponsors" CTA card

Goes inside the `cta` columns block's `sections:`, between "Individual
Sponsorship" and "LinuxFest Northwest Discord Server" (original order):

```
##### call #####
title: Call for Sponsors
-----
lead: 
-----
description:

Sponsoring LinuxFest Northwest shows your support of this 

FREE educational event celebrating Open Source Software
-----
href: /lfnw2026SponsorshipProspectus.pdf
-----
button_label: Download the Prospectus
```

`href` must point at that year's actual prospectus PDF filename/attachment
under `content/` — confirm it still exists before restoring.

## After any edit

Clear the Lektor build cache and restart before previewing — the dev
container's incremental build doesn't reliably pick up content edits
otherwise:

```
docker compose exec server sh -c "rm -rf /root/.cache/lektor/builds/*"
docker compose restart server
```
