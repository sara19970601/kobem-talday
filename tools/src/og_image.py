"""Social card (og-image.jpg, 1200×630) and site icons (favicon.png, apple-touch-icon.png).
Uses the embedded Literata / Inter subsets (Latin, Cyrillic, Cyrillic Ext) with per-letter
fallback, so every Kazakh letter is drawn. Needs Pillow and fontTools (+ brotli for woff2).
Usage: python3 -I og_image.py tools_dir out_dir"""
import io, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

tools, out = sys.argv[1:3]
SUBSETS = ['latin', 'cyrillic', 'cyrillic-ext']

def faces(fam, wght, size):
    """One PIL font per subset (static instance at `wght`) with its character set."""
    res = []
    for sub in SUBSETS:
        p = os.path.join(tools, 'fonts', 'fontsource-variable-%s-5.3.0/package/files/%s-%s-wght-normal.woff2' % (fam, fam, sub))
        f = TTFont(p)
        f = instancer.instantiateVariableFont(f, {'wght': wght})
        f.flavor = None
        buf = io.BytesIO(); f.save(buf); buf.seek(0)
        res.append((set(f.getBestCmap()), ImageFont.truetype(buf, size)))
    return res

def draw_text(d, xy, text, fonts, fill):
    x, y = xy
    for ch in text:
        font = next((f for cmap, f in fonts if ord(ch) in cmap), fonts[0][1])
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch)
    return x

INK, BLUE, GOLD_INK, BG = '#17233B', '#234A8F', '#8A5A12', '#F7F4EE'

# Social card
W, H = 1200, 630
img = Image.new('RGB', (W, H), BG)
photo = Image.open(os.path.join(tools, 'photos', 'cover.webp')).convert('RGB')
pw = 460
scale = max(pw / photo.width, H / photo.height)
photo = photo.resize((int(photo.width * scale) + 1, int(photo.height * scale) + 1), Image.LANCZOS)
left = (photo.width - pw) // 2
img.paste(photo.crop((left, 0, left + pw, H)), (W - pw, 0))
d = ImageDraw.Draw(img)
d.rectangle([W - pw - 8, 0, W - pw - 1, H], fill='#C98B2B')
title1 = title2 = faces('literata', 700, 58)
draw_text(d, (64, 140), 'Көркем шығарманы', title1, INK)
draw_text(d, (64, 214), 'талдау', title2, INK)
sub = faces('inter', 600, 32)
draw_text(d, (64, 312), 'Көркем шығарманы талдауға', sub, BLUE)
draw_text(d, (64, 352), 'арналған тегін платформа', sub, BLUE)
small = faces('inter', 500, 25)
draw_text(d, (64, 420), 'Сабақ жоспары · рубрика · Зертхана', small, INK)
draw_text(d, (64, 458), 'Терминдер сөздігі · балалар әдебиеті', small, INK)
draw_text(d, (64, 530), 'korkemtaldau.com', faces('inter', 700, 28), GOLD_INK)
img.save(os.path.join(out, 'og-image.jpg'), quality=86, optimize=True, progressive=True)

# Icons: a blue tile with a gold «К»
for name, size in [('favicon.png', 48), ('apple-touch-icon.png', 180)]:
    big = 512
    ic = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    di = ImageDraw.Draw(ic)
    di.rounded_rectangle([0, 0, big - 1, big - 1], radius=big // 5 if name == 'favicon.png' else 0, fill=BLUE)
    f = faces('literata', 800, 360)
    font = f[1][1]
    w = font.getlength('К')
    bbox = font.getbbox('К')
    di.text(((big - w) / 2, (big - (bbox[3] + bbox[1])) / 2), 'К', font=font, fill='#E9B85A')
    ic.resize((size, size), Image.LANCZOS).save(os.path.join(out, name))
print('og-image.jpg, favicon.png, apple-touch-icon.png ->', out)
