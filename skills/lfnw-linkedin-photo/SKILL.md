---
name: lfnw-linkedin-photo
description: "Extract and upload profile photos from LinkedIn to the LFNW Django site (django-filer). Use for: lfnw,linkedin photo,profile photo,volunteer photo,board member photo,extract photo,upload photo"
mode: skill
triggers: lfnw,linkedin photo,profile photo,volunteer photo,board member photo,extract photo,upload photo
---

# LFNW LinkedIn Photo Extraction

Extract profile photos from LinkedIn and upload them to the LFNW Django site (django-filer).

## Setup

- Open a Playwright browser for the user to log into LinkedIn. Wait for them to log in.
- **Use Playwright Python** (`/tmp/shared-browser-pw/bin/python3`) — connect via CDP: `connect_over_cdp("http://127.0.0.1:9222")`. **Never use OpenCode's `browser.evaluate`** — returns `{}`.
- Django app: `lfnw_django-dev-app-1` container
- Ask user where to store images, then set that as the download folder (create if needed)

## Workflow

Process ONE person at a time.

1. **Search:** Use Playwright to `context.new_page()`. Wait for the page to load, then navigate to `page.goto("https://www.linkedin.com/search/results/people/?keywords=<FIRST%20LAST>&origin=global-search-bar_sidebar")`. **REUSE this same page for every search** — always navigate the existing search page to the new URL. Do NOT create a new page per person. After processing, navigate it to the next search or close it.
2. **Login (if needed):** If the page redirects to LinkedIn login, the operator logs in.
3. **Find the right person:** Use Playwright to query the DOM: `page.query_selector('a[aria-label="View <Name>'"'"'s profile"]')`. Verify they match expected details (company, role). Get the `href`.
4. **Open profile:** Use `page.goto(href)` with the URL from step 3. Wait 3 seconds for the profile to load.
5. **Check for profile photo:** Use Playwright: `el = page.query_selector('[aria-label="Profile photo"] img')`. If `el` is `None`, the person has no uploaded profile photo — **skip the rest of the workflow** and report: `"<Name> has no profile photo on LinkedIn."`
6. **Extract photo URL:** Use Playwright to get the `srcset` from `page.query_selector('[aria-label="Profile photo"] img')`. Parse entries (`URL WIDTH`), select the **highest resolution** (e.g. `800w`).
7. **Show user** the URL preview (asset ID e.g. `D5603AQ...`) and ask for confirmation.
7. **Download:** `curl -L -o /tmp/<name>.jpg "<url>"`.
8. **Preview:** `browser.preview(path="/tmp/<name>.jpg")` to show the operator.
9. **Upload:** Copy into Django container (`docker cp /tmp/<name>.jpg lfnw_django-dev-app-1:/tmp/<name>.jpg`), then Django shell:
   ```python
   v = Volunteer.objects.filter(first_name__iexact='F', last_name__iexact='L').first()
   fi = FilerImage(file=ContentFile(open('/tmp/<name>.jpg','rb').read(), name='<name>.jpg'),
                   original_filename='F L photo', default_alt_text='F L')
   fi.save(); v.photo_id = fi.pk; v.save(); print(f'Updated -> FilerImage #{fi.pk}')
   ```

## Key details

- LinkedIn **does use `srcset`** — contains multiple sizes (100w, 200w, 400w, 800w). Always pick the largest.
- `profile-displayphoto-shrink` = main photo; `profile-framedphoto-shrink` = circular badge. Both work.
- `?e=` / `&t=` = expiry token + HMAC (valid ~2 weeks). Always use `data-loaded="true"` images.
- The `<figure>` inside `[aria-label="Profile photo"]` is `aria-hidden="true"` (normal, contains SVG placeholder).
- `img[alt]` on the profile photo itself is empty — alt text lives on other images (`"View {name}'s profile"`).

## Do NOT

- Rely on OpenCode's `browser.evaluate` — always use the Playwright Python client.
- Hardcode LinkedIn URLs — derive from the person's name and other data supplied.
- Use the `src` attribute alone — the srcset has the highest resolution versions.
- Create a new page/tab per person — always reuse the same search page via `page.goto()`
