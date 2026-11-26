#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news summary image (1024x1024).

A dark newspaper front page: one big top story, then four more stories in
a 2x2 grid, each with a small hand-drawn icon. All text is drawn with PIL
and the DejaVu fonts bundled on the system; nothing is fetched from the
network, so the output is fully deterministic.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = (13, 27, 42)        # deep navy
CARD = (27, 42, 65)      # panel navy
CARD_LINE = (52, 74, 104)
GOLD = (224, 165, 38)
RED = (192, 57, 43)
WHITE = (245, 245, 240)
GREY = (184, 196, 208)
ORANGE = (230, 126, 34)
LIGHT_BLUE = (93, 173, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAG = font("DejaVuSans-Bold.ttf", 21)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 44)
F_HERO_BODY = font("DejaVuSans.ttf", 25)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 20)
F_NUM = font("DejaVuSans-Bold.ttf", 20)

_IMG = None  # the canvas, so icon_atom can paste a rotated layer onto it


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, spacing):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def star_points(cx, cy, r_out, r_in, n=12):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_rocket(draw, cx, cy):
    # Vertical rocket: nose, body, fins, flame. Spans cy-26..cy+30.
    draw.polygon([(cx, cy - 26), (cx - 11, cy - 4), (cx + 11, cy - 4)],
                 fill=WHITE)
    draw.rectangle([cx - 11, cy - 4, cx + 11, cy + 16], fill=LIGHT_BLUE)
    draw.polygon([(cx - 11, cy + 6), (cx - 22, cy + 20), (cx - 11, cy + 16)],
                 fill=RED)
    draw.polygon([(cx + 11, cy + 6), (cx + 22, cy + 20), (cx + 11, cy + 16)],
                 fill=RED)
    draw.polygon([(cx, cy + 30), (cx - 7, cy + 18), (cx + 7, cy + 18)],
                 fill=ORANGE)
    draw.ellipse([cx - 4, cy, cx + 4, cy + 8], fill=BG)


def icon_burst(draw, cx, cy):
    draw.polygon(star_points(cx, cy, 27, 12), fill=GOLD)
    draw.polygon(star_points(cx, cy, 17, 8), fill=ORANGE)


def icon_flame(draw, cx, cy):
    pts = [(cx, cy - 28), (cx + 11, cy - 10), (cx + 17, cy + 4),
           (cx + 9, cy + 20), (cx - 9, cy + 20), (cx - 17, cy + 4),
           (cx - 11, cy - 10)]
    draw.polygon(pts, fill=ORANGE)
    inner = [(cx, cy + 17), (cx + 7, cy + 3), (cx + 3, cy - 6),
             (cx, cy - 12), (cx - 5, cy - 2), (cx - 7, cy + 8)]
    draw.polygon(inner, fill=GOLD)


def icon_atom(draw, cx, cy):
    # Nucleus plus three elliptical orbits (two drawn via a rotated layer).
    layer = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([6, 27, 58, 37], outline=GOLD, width=3)
    ld.ellipse([27, 6, 37, 58], outline=GOLD, width=3)
    rot = layer.rotate(45, resample=Image.BICUBIC)
    _IMG.paste(rot, (cx - 32, cy - 32), rot)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)


def card(draw, x, y, w, h, number, tag, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14,
                           fill=CARD, outline=CARD_LINE, width=2)
    # Number badge.
    draw.ellipse([x + 18, y + 16, x + 54, y + 52], fill=GOLD)
    tw = draw.textlength(str(number), font=F_NUM)
    draw.text((x + 36 - tw / 2, y + 22), str(number), font=F_NUM, fill=BG)
    # Tag text, kept clear of the icon on the right.
    draw.text((x + 66, y + 22), tag, font=F_TAG, fill=GOLD)
    icon(draw, x + w - 52, y + 34)
    # Headline under the tag row.
    lines = wrap(draw, headline, F_HEAD, w - 40)
    yy = draw_lines(draw, lines, F_HEAD, x + 20, y + 66, WHITE, 36)
    # Body under the headline.
    blines = wrap(draw, body, F_BODY, w - 40)
    draw_lines(draw, blines, F_BODY, x + 20, yy + 8, GREY, 27)


def main():
    global _IMG
    img = Image.new("RGB", (W, H), BG)
    _IMG = img
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W, 10], fill=RED)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((W - tw) / 2, 24), title, font=F_TITLE, fill=WHITE)
    date = "THURSDAY  ·  26 NOVEMBER 2026"
    dw = draw.textlength(date, font=F_DATE)
    draw.text(((W - dw) / 2, 100), date, font=F_DATE, fill=GOLD)
    draw.line([36, 140, W - 36, 140], fill=CARD_LINE, width=2)

    # Hero story: the tariff announcement.
    hx, hy, hw, hh = 36, 156, 952, 252
    draw.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=14,
                           fill=CARD, outline=GOLD, width=3)
    draw.rectangle([hx, hy + 14, hx + 8, hy + hh - 14], fill=RED)
    draw.text((hx + 28, hy + 20), "TOP STORY  ·  TRADE", font=F_TAG,
              fill=GOLD)
    hero_head = "U.S. unveils sweeping new tariffs on 14 trading partners"
    lines = wrap(draw, hero_head, F_HERO_HEAD, hw - 56)
    yy = draw_lines(draw, lines, F_HERO_HEAD, hx + 28, hy + 52, WHITE, 52)
    hero_body = ("Washington proposes 20–40% duties on China, the EU, Japan "
                 "and India to counter excess factory capacity. "
                 "Hearing set for 25 January.")
    blines = wrap(draw, hero_body, F_HERO_BODY, hw - 56)
    draw_lines(draw, blines, F_HERO_BODY, hx + 28, yy + 10, GREY, 32)

    # Four more stories in a 2x2 grid.
    stories = [
        (2, "WAR IN UKRAINE  ·  KYIV",
         "Russian missiles hit Kyiv mall; grain ships struck",
         "Ballistic missiles wound seven in the capital; two grain "
         "ships are hit near Odesa.",
         icon_rocket),
        (3, "GAZA  ·  MIDDLE EAST",
         "Israeli strikes kill nine in Gaza",
         "Overnight raids kill nine, including a Hamas-appointed deputy "
         "minister — the third straight night of attacks.",
         icon_burst),
        (4, "DISASTER  ·  CAIRO",
         "Cairo tanker fire kills at least 31",
         "A fuel tanker overturns and explodes on the Giza ring road; "
         "27 vehicles burn and about 21 people are hurt.",
         icon_flame),
        (5, "NORTH KOREA  ·  ASIA",
         "Kim calls for wider nuclear deployment",
         "Kim tours nuclear sites and urges wider tactical deployment; "
         "denial of its status is 'a declaration of war'.",
         icon_atom),
    ]
    cw, ch, gap = 466, 246, 20
    positions = [(36, 428), (522, 428), (36, 694), (522, 694)]
    for (number, tag, headline, body, icon), (x, y) in zip(stories,
                                                           positions):
        card(draw, x, y, cw, ch, number, tag, headline, body, icon)

    # Footer.
    foot = "Five stories from Thursday, 26 November 2026"
    fw = draw.textlength(foot, font=F_FOOT)
    draw.text(((W - fw) / 2, 962), foot, font=F_FOOT, fill=GREY)

    out = os.environ.get("ENTRY_OUT", "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
