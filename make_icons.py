"""Home-screen icons, in the same house style as the other apps.

Dark tile, a small mark up top, the name in a serif wordmark in the page's own
accent colour, a hairline rule, then what the thing does in spaced-out sans.
Run once and commit the PNGs; CI copies them rather than rebuilding them.

    python3 make_icons.py
"""

from PIL import Image, ImageDraw, ImageFont

BG = "#131519"        # the page's dark background
ACCENT = "#4FB5B0"    # the page's dark-mode accent
UP = "#6DBE8E"
DOWN = "#E87A70"
RULE = "#3A3A42"
SUB = "#8E9AAB"

SERIF = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def rounded_tile(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.225), fill=BG)
    return img, d


def centred(d, y, text, font, fill, tracking=0):
    widths = [d.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (d.im.size[0] - total) / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += w + tracking


def arrows(d, size):
    """An up arrow and a down arrow side by side - long or short."""
    cy, h, w = size * 0.29, size * 0.17, size * 0.07
    lw = max(2, int(size * 0.02))
    for cx, colour, up in [(size * 0.43, UP, True), (size * 0.57, DOWN, False)]:
        top, bot = cy - h / 2, cy + h / 2
        d.line([cx, top, cx, bot], fill=colour, width=lw)
        tip, base = (top, top + w) if up else (bot, bot - w)
        d.line([cx - w * 0.75, base, cx, tip, cx + w * 0.75, base], fill=colour, width=lw, joint="curve")


def build(size):
    img, d = rounded_tile(size)
    arrows(d, size)
    wordmark = ImageFont.truetype(SERIF, int(size * 0.2))
    subtitle = ImageFont.truetype(SANS, int(size * 0.058))
    centred(d, size * 0.41, "CFD", wordmark, ACCENT)
    ry = size * 0.655
    d.line([size * 0.34, ry, size * 0.66, ry], fill=RULE, width=max(1, int(size * 0.006)))
    centred(d, size * 0.70, "SCREEN", subtitle, SUB, tracking=size * 0.028)
    return img


if __name__ == "__main__":
    for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")]:
        build(size).save(name)
        print(f"wrote {name} ({size}x{size})")
