"""Draw the 24 November 2026 newspaper front page with Pillow.

Run:  python3 draw_image.py
Writes entry.png (1024x1024) next to this file. Everything is drawn
from the story list below, so the picture is fully reproducible.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
NAVY = (27, 47, 74)
GOLD = (232, 183, 58)
RED = (176, 30, 36)
INK = (20, 20, 20)
TEAL = (18, 120, 110)


def font(name, size):
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif-reg": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans-reg": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, face, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=face) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, face, max_w, leading, colour=INK):
    x, y = xy
    for line in wrap(draw, text, face, max_w):
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def jets(draw, ox, oy):
    for dx, dy, s in [(0, 0, 1.0), (-70, 55, 0.9)]:
        x, y = ox + dx, oy + dy
        draw.line([(x - 110, y + 8), (x - 30, y + 8)], fill=(40, 90, 180), width=4)
        for i in range(4):
            draw.line([(x - 105 + i * 18, y + 4), (x - 95 + i * 18, y + 4)],
                      fill=(40, 90, 180), width=4)
        body = [(x, y), (x + 55, y + 12), (x + 95, y + 12), (x + 55, y + 22),
                (x + 30, y + 38), (x + 18, y + 18), (x - 5, y + 30), (x + 8, y + 12)]
        draw.polygon(body, fill=NAVY)


def chip(draw, ox, oy):
    draw.rectangle([ox, oy, ox + 110, oy + 110], fill=NAVY)
    for i in range(3):
        draw.line([(ox + 20 + i * 35, oy - 12), (ox + 20 + i * 35, oy)],
                  fill=INK, width=5)
        draw.line([(ox + 20 + i * 35, oy + 110), (ox + 20 + i * 35, oy + 122)],
                  fill=INK, width=5)
    draw.rectangle([ox + 35, oy + 40, ox + 75, oy + 70], fill=GOLD)
    draw.ellipse([ox - 12, oy - 12, ox + 122, oy + 122], outline=RED, width=7)
    draw.line([(ox - 5, oy + 105), (ox + 115, oy + 5)], fill=RED, width=7)


def building(draw, ox, oy):
    draw.rectangle([ox, oy + 30, ox + 130, oy + 110], fill=(120, 105, 80))
    draw.polygon([(ox, oy + 30), (ox + 65, oy), (ox + 130, oy + 30)], fill=(150, 40, 40))
    for r in range(2):
        for c in range(4):
            draw.rectangle([ox + 12 + c * 30, oy + 45 + r * 30,
                            ox + 32 + c * 30, oy + 65 + r * 30], fill=GOLD)


def dome(draw, ox, oy):
    draw.pieslice([ox + 25, oy - 5, ox + 105, oy + 65], 180, 360, fill=NAVY)
    draw.rectangle([ox + 60, oy - 18, ox + 70, oy], fill=NAVY)
    draw.rectangle([ox, oy + 60, ox + 130, oy + 115], fill=NAVY)
    for i in range(5):
        draw.rectangle([ox + 10 + i * 24, oy + 72, ox + 26 + i * 24, oy + 105],
                       fill=PAPER)


def chart(draw, ox, oy):
    for gy in range(4):
        y = oy + gy * 32
        draw.line([(ox, y), (ox + 170, y)], fill=(210, 205, 190), width=2)
    pts = [(ox, oy + 90), (ox + 40, oy + 62), (ox + 75, oy + 72),
           (ox + 110, oy + 30), (ox + 145, oy + 18), (ox + 170, oy + 8)]
    draw.line(pts, fill=TEAL, width=6, joint="curve")
    draw.polygon([(ox + 170, oy + 8), (ox + 152, oy + 2), (ox + 158, oy + 22)],
                 fill=TEAL)


def panel(draw, x, y, w, h, kicker, head, body, icon):
    draw.rectangle([x, y, x + w, y + 8], fill=NAVY)
    draw.rectangle([x, y, x + w, y + h], outline=(190, 180, 160), width=2)
    draw.text((x + 16, y + 18), kicker, font=font("sans", 22), fill=RED)
    para(draw, (x + 16, y + 48), head, font("serif", 24), 440, 28)
    para(draw, (x + 16, y + 102), body, font("sans-reg", 18), 285, 23)
    icon(draw, x + w - 165, y + 95)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((28, 18), "THE WORLD IN ONE DAY", font=font("serif", 62), fill=(255, 255, 255))
    d.text((28, 96), "TUESDAY,  24  NOVEMBER  2026", font=font("sans", 30), fill=GOLD)
    d.text((640, 100), "SIX STORIES  \u2022  ONE DAY", font=font("sans", 22), fill=(255, 255, 255))

    d.text((28, 168), "KOREA  \u2022  ULLEUNG ISLAND", font=font("sans", 23), fill=RED)
    y = para(d, (28, 196), "RUSSIAN JETS SPARK KOREA ALERT",
             font("serif", 50), 540, 56)
    y = para(d, (28, y + 6), "Seoul scrambles fighter jets after several Russian "
             "warplanes enter its air-defence zone; islanders are told to shelter.",
             font("sans-reg", 23), 570, 30)
    jets(d, 830, 230)
    d.text((640, 420), "NO VIOLATION", font=font("sans", 28), fill=NAVY)
    d.line([(28, 470), (996, 470)], fill=(190, 180, 160), width=2)

    panel(d, 28, 486, 472, 196, "WASHINGTON, USA", "US blacklists Megaspeed",
          "Commerce lists the firm at the heart of the Nvidia spy scandal; "
          "an Alibaba Singapore unit is listed too.", chip)
    panel(d, 524, 486, 472, 196, "KYIV, UKRAINE", "Zelensky seeks four-way talks",
          "Kyiv's president calls for Ukraine, Russia, the US and Europe to "
          "meet soon; fresh strikes hit the Kyiv region.", building)
    panel(d, 28, 692, 472, 196, "BEIJING, CHINA", "China death sentence for spy",
          "An official surnamed Ma is sentenced to death for spying for an "
          "unnamed foreign country, state media says.", dome)
    panel(d, 524, 692, 472, 196, "TOKYO & SEOUL", "Asia stocks roar back",
          "Nikkei jumps 3.9% and the Kospi 6.1% as Huang's return revives the "
          "AI trade; Samsung rises 7%.", chart)

    d.rectangle([0, 902, W, H], fill=NAVY)
    d.text((28, 914), "ALSO IN INDONESIA", font=font("sans", 22), fill=GOLD)
    d.text((28, 940), "24 dead in factory fire", font=font("serif", 32), fill=(255, 255, 255))
    para(d, (28, 978), "Rescuers search for ~30 missing after a candy factory "
        "blaze in Banten; toll confirmed Monday.", font("sans-reg", 18), 610, 21,
        colour=(230, 230, 230))
    d.line([(660, 918), (660, 1006)], fill=(120, 140, 170), width=2)
    d.text((682, 914), "ALSO", font=font("sans", 22), fill=GOLD)
    para(d, (682, 942), "EU hunts new ECB chief as Lagarde resigns. "
        "COP31 talks stall over fossil fuels.", font("sans-reg", 19), 300, 24,
        colour=(230, 230, 230))

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
