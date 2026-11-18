---
name: visual-regression
description: Visual regression testing to detect unintended UI changes across pages
mode: skill
triggers: visual regression,compare screenshots,update baselines,visual check
---

# Visual Regression Testing — Visual Regression Testing for lfnw-django

## Purpose
Visual regression testing to detect unintended UI changes across pages.

## What We Learned (From This Investigation)

### 1. pixelmatch-py Integration (Already Installed)
- `pip install pixelmatch pixelmatch-pil` — already in requirements-dev.txt
- `from pixelmatch.contrib.PIL import pixelmatch` — works with PIL/Pillow images
- Same YIQ color space + anti-aliasing detection algorithm as Playwright's `toHaveScreenshot()`
- **Key API:** `pixelmatch(img1, img2, diff_img, threshold=0.2)` — returns diff pixel count
- **Tolerance:** `threshold=0.2` handles AA artifacts and minor rendering differences
- **Diff image:** RGBA format — transparent where same, red where different

### 2. visual_check.py Changes
- **Added `compare_baselines()` function:** Takes screenshot path, loads baseline, resizes if needed, runs pixelmatch, saves diff on mismatch
- **Added `update_baseline()` function:** Saves current screenshot as baseline PNG
- **CLI flags:** `--compare-baselines`, `--baseline-dir`, `--diff-dir`, `--threshold`, `--max-diff-pct`, `--update-baselines`
- **Error handling:** Catches FileNotFoundError, PIL.UnidentifiedImageError, pixelmatch errors
- **Pillow compatibility:** Use `Image.Resampling.LANCZOS` (Pillow 10+), not `Image.LANCZOS`

### 3. verify.sh Integration
- **Env vars:** `VERIFY_COMPARE_BASELINES=1` to enable comparison, `VERIFY_UPDATE_BASELINES=1` to update baselines
- **Baseline dir:** `verify-shots-baselines/` — stores original baselines
- **Diff dir:** `verify-shots-diffs/` — stores diff images for failures
- **Exit codes:** Still uses 0=PASS, 1=FAIL, 3=INCOMPLETE

### 4. Critical Findings for Future Development

#### a. Form Rendering Bug
- The feedback form (`/get-involved/suggestions-feedback/`) renders correctly on production (lfnw.org) but NOT on the dev server (127.0.0.1:8880)
- **Root cause:** The dev server may have stale page content or the form is in draft state
- **Fix needed:** Check if the form is published on the dev server; if not, publish it via `python manage.py seed` or manually

#### b. Altcha Captcha Blocks Automation
- The form uses [Altcha](https://altcha.org/) — a "spam filter for the web" captcha
- **Cannot bypass programmatically** — it requires human interaction
- **Workaround options:**
  - Use a test email and fill in the form manually via browser
  - Configure Altcha to skip for test IPs in development
  - Use `ALTCHA_API_KEY` and `ALTCHA_SECRET` environment variables to disable in dev

#### c. Playwright `eval` vs `run-code`
- `pw.js eval` runs code **in the browser context** — `page` variable does NOT exist
- `pw.js run-code` runs code **in Node.js context** — `page` variable IS available
- Always use `run-code` for Playwright API calls (fill, click, etc.)

#### d. Baseline Strategy
- **Always run `--update-baselines` first** to create baselines
- **Then run `--compare-baselines`** to verify against them
- **In CI:** Never auto-update baselines — compare only, upload diff artifacts on failure
- **Local dev:** Use `--update-baselines` after intentional UI changes

### 5. Files Modified
- `scripts/visual_check.py` — Added `compare_baselines()` and `update_baseline()` functions, CLI flags
- `bin/verify.sh` — Added `VERIFY_COMPARE_BASELINES` and `VERIFY_UPDATE_BASELINES` support
- `.agents/skills/visual-regression/SKILL.md` — This file

### 6. CI/CD Recommendations
```bash
# On PRs:
VERIFY_COMPARE_BASELINES=1 python scripts/visual_check.py URL --compare-baselines
# On main (after intentional change):
VERIFY_UPDATE_BASELINES=1 python scripts/visual_check.py URL --update-baselines
```

### 7. Common Pitfalls
- **Image resizing:** If baseline and screenshot differ in dimensions, pixelmatch fails. Always resize baseline to match screenshot dimensions using `Image.resize()` with `Image.Resampling.LANCZOS`
- **Threshold tuning:** `threshold=0.2` works for most pages. Lower (0.1) for strict pixel-perfect, higher (0.3) for pages with dynamic content
- **File permissions:** Ensure `verify-shots-baselines/` and `verify-shots-diffs/` exist and are writable
- **Dev server state:** Always verify the page renders correctly before running visual checks

### 8. Next Steps (Future Work)
- Add automated screenshot comparison in CI/CD pipeline
- Consider adding `--mask` option to ignore dynamic content (timestamps, ads, etc.)
- Explore `pytest-playwright-visual-snapshot` for test-driven visual regression
- Add per-page baseline configuration in `visual_check.py --config`
