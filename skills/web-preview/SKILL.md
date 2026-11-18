---
name: web-preview
description: "Take screenshots and analyze rendered web pages for visual inspection. Use when the operator asks to 'see the page', 'look at the results', 'check the visual', 'preview', or 'show me what it looks like'."
metadata:
  version: "0.0.0"
  mode: skill
  triggers: screenshot, preview, look at results, visually check, show me the page, see the results, visual check, page preview, take a screenshot, check visually, see what it looks like
---

# Web Preview — Screenshot & Visual Inspection

You are the **web preview** expert. You take screenshots of web pages and present
them to the operator (and to yourself, the AI agent) for visual inspection.

## Core Principle

**The AI agent CAN see images.** When the operator asks to "look at" or "check"
a web page, you take a screenshot and show it. Do NOT say "I can't see images" —
that is wrong. The Pi coding agent receives images in conversation and can
analyze them.

## How It Works

You use the `screenshot.py` utility to capture rendered web pages:

```bash
# Quick viewport screenshot (default)
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000

# Full page screenshot (for scrollable pages)
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000 --full-page

# With text extraction
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000 --all

# Custom viewport
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000 --viewport 1920x1080

# With delay (for pages that load content)
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000 --delay 2000

# Save to specific path
python3 "$AGENTS_HOME/scripts/screenshot.py" http://localhost:8000 -o /tmp/my-preview.png
```

The screenshot is saved to `/tmp/preview.png` (or the specified path).

## Presentation Workflow

When the operator asks you to **look at** or **check** a web page:

### Step 1: Take the Screenshot

```bash
python3 "$AGENTS_HOME/scripts/screenshot.py" \
    "http://localhost:8000" \
    --full-page \
    --all \
    -o /tmp/preview.png
```

### Step 2: Show the Image to Yourself (the Agent)

```python
# Read the screenshot — this returns an image block the model can see
screenshot = await tools.read({ path: "/tmp/preview.png" })
# Then show it to the model context
image(screenshot)
```

Or in bash, just reference the file:
```
I took a screenshot of the page. Here it is:

![Page Preview](/tmp/preview.png)
```

The Pi coding agent will receive the image and can analyze it.

### Step 3: Describe What You See

After the image is in context, describe:
- Layout and structure
- Colors and styling
- Text content and hierarchy
- Any issues (overflow, misalignment, broken layouts)
- Compare with expected behavior

## When to Use Full Page vs Viewport

| Situation | Mode |
|-----------|------|
| Dashboard, single screen | Viewport (default) |
| Long article, form | Full page (`--full-page`) |
| Landing page with scrolling | Full page |
| Mobile/responsive check | Custom viewport (`--viewport 375x812`) |
| Email preview | Viewport, custom width |

## When to Add Text Extraction

Use `--all` when you need both the visual AND the text content. This is
useful when the operator also needs to verify data, content, or structure.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `playwright not installed` | `pip install playwright && playwright install chromium` |
| Black/blank screenshot | Try `--delay 2000` or check URL |
| Page not loading | Check if dev server is running (`curl -s localhost:8000`) |
| Screenshot too large | Use viewport instead of `--full-page` |
| Wrong viewport | Use `--viewport 1920x1080` or mobile sizes |

## Common Viewport Sizes

| Device | Viewport |
|--------|----------|
| Desktop | `1280x800` (default) |
| Large desktop | `1920x1080` |
| iPad | `768x1024` |
| iPhone SE | `375x667` |
| iPhone 14 Pro | `393x852` |

## Integration Notes

This skill works with:
- **agent-aiyama** — The `/agent-aiyama preview <url>` command uses this skill
- **shared-browser** — shared-browser is for collaborative admin consoles; this skill is for dev inspection
- **django-dev-env / wordpress-dev** — Use after starting dev servers

## Do NOT

- Don't say "I can't see images" — you CAN see them
- Don't rely on raw HTML alone — it misses CSS, JS, and layout
- Don't use screenshots when the operator only needs text/data
- Don't leave `/tmp/preview.png` files around — they're temporary
