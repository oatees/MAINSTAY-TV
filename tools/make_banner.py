"""Build the cover banner for a YouTube research breakdown doc.

Renders a 1600x900 PNG: dark navy field, small-caps kicker, oversized title with
one accent word, blue rule, subtitle, and three numbered cards on the right.

Usage:
    python tools/make_banner.py <out.png> [--title-a "DONT " --title-b "STOP" ...]

Defaults match the DONT STOP breakdown; edit CONFIG for other videos.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
NAVY = "#0B1F3A"
NAVY_CARD = "#102A4C"
CARD_BORDER = "#23405F"
BLUE = "#2563EB"
BLUE_SOFT = "#6FA8FF"
WHITE = "#FFFFFF"
BODY = "#C9D6E5"
MUTED = "#8FA8C4"
DIM = "#4A6485"

FONT_DIR = Path(r"C:\Windows\Fonts")

CONFIG = {
    "kicker": "YOUTUBE RESEARCH BREAKDOWN:",
    "title_a": "DONT ",
    "title_b": "STOP",
    "subtitle": "A structured analysis of a 32-second branded hip-hop Short.",
    "hashtags": "#patrickxxlee  #dontstop  #doaa2  #newmusic",
    "stats": ["0:32 RUNTIME", "1 LOCATION", "~31 CUTS"],
    "cards": [
        ("01", "HOOK", "Repeated 4x in the first 16s"),
        ("02", "PERFORMANCE", "One alley, one visual signature"),
        ("03", "CUT RHYTHM", "~31 cuts in 32 seconds"),
    ],
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, tracking: float):
    """Draw text with letter spacing, returning the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def tracked_width(draw: ImageDraw.ImageDraw, text, fnt, tracking: float) -> float:
    return sum(draw.textlength(ch, font=fnt) + tracking for ch in text) - tracking


def wrap(draw, text, fnt, max_width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def build(out_path: str, cfg: dict = CONFIG) -> None:
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # soft blue wash on the right so the flat navy has some depth
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for x in range(760, W):
        alpha = int(20 * (x - 760) / (W - 760))
        wd.line([(x, 0), (x, H)], fill=(37, 99, 235, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), wash).convert("RGB")
    draw = ImageDraw.Draw(img)

    left = 96

    # kicker
    kicker_font = font("segoeuib.ttf", 21)
    draw_tracked(draw, (left, 118), cfg["kicker"], kicker_font, BLUE_SOFT, 4.5)

    # title: shrink until both words fit the left column
    title_a, title_b = cfg["title_a"], cfg["title_b"]
    max_title_w = 840
    size = 168
    while size > 60:
        tf = font("ariblk.ttf", size)
        if draw.textlength(title_a, font=tf) + draw.textlength(title_b, font=tf) <= max_title_w:
            break
        size -= 4
    tf = font("ariblk.ttf", size)
    title_y = 168
    draw.text((left, title_y), title_a, font=tf, fill=WHITE)
    b_x = left + draw.textlength(title_a, font=tf)
    draw.text((b_x, title_y), title_b, font=tf, fill=BLUE)

    # blue rule
    rule_y = title_y + size + 46
    draw.rectangle([left, rule_y, left + 132, rule_y + 6], fill=BLUE)

    # subtitle
    sub_font = font("segoeui.ttf", 28)
    sub_y = rule_y + 44
    for line in wrap(draw, cfg["subtitle"], sub_font, 760):
        draw.text((left, sub_y), line, font=sub_font, fill=BODY)
        sub_y += 42

    # stat strip
    stats = cfg.get("stats", [])
    if stats:
        stat_font = font("segoeuib.ttf", 17)
        stat_y = H - 176
        sx = left
        for i, stat in enumerate(stats):
            if i:
                draw.text((sx, stat_y - 2), "·", font=stat_font, fill=DIM)
                sx += draw.textlength("·", font=stat_font) + 22
            sx = draw_tracked(draw, (sx, stat_y), stat, stat_font, "#7E97B4", 2.0)
            sx += 22

    # hashtags
    tag_font = font("segoeui.ttf", 18)
    draw_tracked(draw, (left, H - 92), cfg["hashtags"], tag_font, DIM, 1.6)

    # right-hand cards
    card_x, card_w = 976, 528
    card_h, gap = 132, 26
    total = len(cfg["cards"]) * card_h + (len(cfg["cards"]) - 1) * gap
    card_y = (H - total) // 2

    num_font = font("segoeuib.ttf", 15)
    label_font = font("segoeuib.ttf", 27)
    cap_font = font("segoeui.ttf", 17)

    for num, label, caption in cfg["cards"]:
        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + card_h],
            radius=10,
            fill=NAVY_CARD,
            outline=CARD_BORDER,
            width=2,
        )
        draw.rectangle([card_x, card_y + 18, card_x + 4, card_y + card_h - 18], fill=BLUE)
        draw.text((card_x + 30, card_y + 24), num, font=num_font, fill=BLUE_SOFT)
        draw.text((card_x + 30, card_y + 46), label, font=label_font, fill=WHITE)
        draw.text((card_x + 30, card_y + 88), caption, font=cap_font, fill=MUTED)
        card_y += card_h + gap

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    print(f"saved {out_path} ({W}x{H})")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "banner.png"
    build(target)
