"""Crop, resize and compress the stock photos for the site (WebP).
Usage: python3 -I prep_photos.py <dir with 8.jpg … 15.jpg> <out dir>"""
import os, sys
from PIL import Image

src, out = sys.argv[1:3]
JOBS = {
    # name: (source, crop box (l, t, r, b), output size, quality)
    'cover':  ('11.jpg', (480, 0, 1520, 1300), (640, 800), 70),     # Charyn canyon, portrait
    'library': ('9.jpg', (0, 430, 2000, 1130), (1600, 560), 68),     # laptop and notebook
    'guide':  ('10.jpg', (0, 1040, 1500, 1565), (1500, 525), 68),    # bookshelves
    'plan':   ('12.jpg', (0, 300, 2000, 1000), (1600, 560), 68),     # open books
    'help':   ('8.jpg', (400, 130, 1560, 710), (1160, 580), 68),     # Bayterek; bank sign on the right is cut off
    'kids':   ('13.jpg', (0, 230, 2000, 930), (1600, 560), 68),     # parent and child with a picture book
    'class':  ('14.jpg', (0, 40, 2000, 740), (1600, 560), 68),     # teacher reading to a class in a library
    'almaty': ('15.jpg', (0, 260, 2000, 960), (1600, 560), 68),     # Almaty, Kok-Tobe and the mountains
}
for name, (f, box, size, q) in JOBS.items():
    im = Image.open(os.path.join(src, f)).convert('RGB').crop(box).resize(size, Image.LANCZOS)
    path = os.path.join(out, name + '.webp')
    im.save(path, 'WEBP', quality=q, method=6)
    print('%-8s %s -> %dx%d  %d KB' % (name, f, size[0], size[1], os.path.getsize(path) // 1024))
