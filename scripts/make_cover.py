#!/usr/bin/env python3
"""README 封面图：炭黑渐变 + 香槟金刊头 + 编辑排版大数字"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 860
BG_TOP, BG_BOT = (10, 11, 14), (18, 20, 26)
GOLD, PAPER, DIM = (201, 174, 110), (233, 230, 223), (142, 138, 128)

img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / H
    c = tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
    for x in range(W):
        px[x, y] = c
d = ImageDraw.Draw(img)

FD = "/usr/share/fonts/truetype/dejavu/"
serif_b = lambda s: ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)
sans_r = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)
sans_b = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)

def spaced(dr, xy, text, font, fill, ls):
    """手绘字距"""
    x, y = xy
    for ch in text:
        dr.text((x, y), ch, font=font, fill=fill)
        x += dr.textlength(ch, font=font) + ls

# 刊头
spaced(d, (W//2 - 330, 150), "LLM PRICE ATLAS", serif_b(52), GOLD, 14)
d.text((W//2 - 254, 236), "Every AI price, verified and traceable.", font=sans_r(22), fill=DIM)

# 双细线
for off in (300, 304):
    d.line([(120, off), (W-120, off)], fill=(201, 174, 110, 40), width=1)

# 大数字编辑排版
stats = [("92", "PROVIDERS"), ("581", "MODELS"), ("1,323", "API PRICES"), ("194", "PLANS")]
col_w = W // len(stats)
for i, (num, lab) in enumerate(stats):
    cx = col_w * i + col_w // 2
    f_num = serif_b(64)
    w = d.textlength(num, font=f_num)
    d.text((cx - w/2, 380), num, font=f_num, fill=PAPER)
    f_lab = sans_b(16)
    w2 = d.textlength(lab, font=f_lab)
    d.text((cx - w2/2, 476), " ".join(lab), font=f_lab, fill=DIM)
    if i:
        d.line([(col_w*i, 385), (col_w*i, 500)], fill=(60, 62, 68), width=1)

# 底部
d.line([(120, 700), (W-120, 700)], fill=(50, 52, 58), width=1)
msg = "Dual-timestamp provenance · Official-source verified · Offline single-file explorer"
w = d.textlength(msg, font=sans_r(19))
d.text(((W-w)/2, 736), msg, font=sans_r(19), fill=DIM)

out = "/mnt/d/PROJECT/AI模型价格库/docs/cover.png"
img.save(out, optimize=True)
import os
print(f"cover: {os.path.getsize(out)//1024} KB")
