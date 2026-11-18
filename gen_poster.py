"""
Generate a premium editorial infographic summarizing world news for 18 Nov 2026.
1024x1024 PNG, ≤1 MB.  Uses Windows system fonts via PIL/Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap, math

# ── canvas ───────────────────────────────────────────────────────────────
W, H = 1024, 1024

# ── palette ──────────────────────────────────────────────────────────────
BG       = (12, 15, 24)        # near-black
PANEL    = (22, 28, 42)        # card bg
ACCENT   = (220, 55, 50)       # red accent bar / rule
GOLD     = (230, 185, 80)      # date / highlight
WHITE    = (245, 243, 240)
LGREY    = (180, 178, 172)
DGREY    = (100, 100, 105)

# category colours  (each story gets its own tint)
CAT_COLORS = [
    (220, 55, 50),    # red – war/conflict
    (60, 140, 220),   # blue – diplomacy
    (45, 175, 110),   # green – climate
    (230, 165, 50),   # amber – tech
    (170, 70, 200),   # purple – Gulf / Middle-East
    (60, 190, 190),   # teal – health
    (200, 90, 60),    # burnt-orange – markets
    (120, 160, 60),   # olive – Europe tech
]

# ── fonts (Windows) ──────────────────────────────────────────────────────
def _f(name, sz):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", sz)
    except OSError:
        return ImageFont.truetype(f"C:/Windows/Fonts/arial.ttf", sz)

TITLE_FONT   = _f("georgiab.ttf", 40)
DATE_FONT    = _f("georgiai.ttf", 18)
TAG_FONT     = _f("calibrib.ttf", 14)
HEAD_FONT    = _f("georgiab.ttf", 17)
BODY_FONT    = _f("calibri.ttf", 14)
FOOTER_FONT  = _f("calibri.ttf", 12)
NUM_FONT     = _f("impact.ttf", 28)

# ── stories ──────────────────────────────────────────────────────────────
stories = [
    {
        "tag": "CRIMEA",
        "headline": "Crimean Bridge Collapses After Massive Ukrainian Strike",
        "body": "Ukraine launched a combined drone-and-missile barrage that severed the road span of the Kerch Bridge. Zelenskyy called it 'unprecedented'; Russia suspended all bridge traffic.",
        "cat": 0,
    },
    {
        "tag": "SHENZHEN",
        "headline": "APEC Leaders' Summit Opens in Shenzhen",
        "body": "33rd APEC Economic Leaders' Meeting begins with Putin-Xi bilateral talks. Theme: 'Building an Asia-Pacific Community to Prosper Together.'",
        "cat": 1,
    },
    {
        "tag": "ANTALYA",
        "headline": "COP31 Climate Talks: $200M Pledged for Adaptation",
        "body": "Four nations commit $200 million to global climate funds in Antalya, Turkey. Scientists warn of looming tipping points as adaptation costs soar.",
        "cat": 2,
    },
    {
        "tag": "WASHINGTON",
        "headline": "US Curbs Chinese Data-Center Hardware Imports",
        "body": "New restrictions block Chinese optical transceivers for data centers, overriding Big Tech lobbying. AI chip export controls tighten further.",
        "cat": 3,
    },
    {
        "tag": "BAHRAIN",
        "headline": "Gulf Drone War: US Strikes Iran's Qeshm Island",
        "body": "After IRGC drones target US radar at Sheikh Isa Air Base, US jets hit an IRGC missile site on Qeshm Island. Kuwait also activates air defenses.",
        "cat": 4,
    },
    {
        "tag": "GLOBAL",
        "headline": "World COPD Day: 'Early Diagnosis Saves Lives'",
        "body": "Health orgs mark World COPD Day, pushing spirometry access in developing nations. Theme: early diagnosis and management for a better life.",
        "cat": 5,
    },
    {
        "tag": "MARKETS",
        "headline": "Asian Stocks Rebound on Nvidia Earnings Beat",
        "body": "Asian indices snap a four-session slide after Nvidia's strong sales forecast. US dollar holds near 19-month high as Fed rate path firms.",
        "cat": 6,
    },
    {
        "tag": "SILICON VALLEY",
        "headline": "Apple Services Hit by Global Outage",
        "body": "iCloud, App Store, Apple Pay and sign-in systems went down worldwide, disrupting millions. Former Nvidia CEO Huang says he'd return if asked.",
        "cat": 7,
    },
]

# ── draw ─────────────────────────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ── header area ──────────────────────────────────────────────────────────
# thin top accent line
d.rectangle([0, 0, W, 5], fill=ACCENT)

# masthead
d.text((W // 2, 42), "THE WORLD TODAY", anchor="mm", font=TITLE_FONT, fill=WHITE)
# date line
d.text((W // 2, 72), "Wednesday, 18 November 2026  ·  Eight stories that shaped the day",
       anchor="mm", font=DATE_FONT, fill=GOLD)

# divider
d.line([32, 92, W - 32, 92], fill=ACCENT, width=3)
d.line([32, 97, W - 32, 97], fill=DGREY, width=1)

# ── card grid: 2 cols × 4 rows ──────────────────────────────────────────
MARGIN_X  = 28
MARGIN_Y  = 110
GAP       = 12
COLS      = 2
ROWS      = 4
CARD_W    = (W - 2 * MARGIN_X - GAP) // COLS
CARD_H    = (H - MARGIN_Y - 60 - (ROWS - 1) * GAP) // ROWS   # leave 60px footer
CORNER    = 8  # rounded-corner radius (approximated)

def rounded_rect(draw, xy, fill, r=8):
    """Draw a filled rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    draw.pieslice([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=fill)
    draw.pieslice([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=fill)


def wrap_text(text, font, max_w, draw):
    """Word-wrap text to fit within max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] > max_w:
            if cur:
                lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


for idx, s in enumerate(stories):
    row, col = divmod(idx, COLS)
    cx = MARGIN_X + col * (CARD_W + GAP)
    cy = MARGIN_Y + row * (CARD_H + GAP)

    # card background
    rounded_rect(d, (cx, cy, cx + CARD_W, cy + CARD_H), PANEL, r=6)

    cat_col = CAT_COLORS[s["cat"]]

    # left accent bar
    d.rectangle([cx, cy + 6, cx + 5, cy + CARD_H - 6], fill=cat_col)

    # number badge (top-left)
    badge_x = cx + 14
    badge_y = cy + 8
    d.text((badge_x, badge_y), str(idx + 1), font=NUM_FONT, fill=cat_col)

    # tag
    tag_x = badge_x + 30
    tag_y = cy + 14
    # tag background pill
    tag_bbox = d.textbbox((0, 0), s["tag"], font=TAG_FONT)
    tw = tag_bbox[2] - tag_bbox[0] + 12
    th = tag_bbox[3] - tag_bbox[1] + 6
    d.rectangle([tag_x, tag_y, tag_x + tw, tag_y + th], fill=cat_col)
    d.text((tag_x + 6, tag_y + 2), s["tag"], font=TAG_FONT, fill=WHITE)

    # headline
    text_x = cx + 14
    text_y = tag_y + th + 8
    max_text_w = CARD_W - 28
    head_lines = wrap_text(s["headline"], HEAD_FONT, max_text_w, d)
    for ln in head_lines[:2]:
        d.text((text_x, text_y), ln, font=HEAD_FONT, fill=WHITE)
        text_y += 22

    # body
    text_y += 2
    body_lines = wrap_text(s["body"], BODY_FONT, max_text_w, d)
    for ln in body_lines[:4]:
        d.text((text_x, text_y), ln, font=BODY_FONT, fill=LGREY)
        text_y += 18

# ── footer ───────────────────────────────────────────────────────────────
footer_y = H - 40
d.line([32, footer_y - 8, W - 32, footer_y - 8], fill=ACCENT, width=2)
d.text((W // 2, footer_y + 6), "Sources: Reuters · AP · BBC · Al Jazeera  ·  18 Nov 2026  ·  Agent-rendered editorial summary",
       anchor="mm", font=FOOTER_FONT, fill=DGREY)

# thin bottom accent
d.rectangle([0, H - 4, W, H], fill=ACCENT)

# ── save ─────────────────────────────────────────────────────────────────
img.save("poster.png", optimize=True)
info = img.info
import os
sz = os.path.getsize("poster.png")
print(f"Saved poster.png  {W}x{H}  {sz/1024:.0f} KB")
