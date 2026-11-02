#!/usr/bin/env python3
"""Paints every illustration on the site into src/assets/illustrations."""
import math, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from watercolor import *
from scipy.ndimage import gaussian_filter as gf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "src/assets/illustrations")
EV = os.path.join(OUT, "events")
FONT = os.path.join(ROOT, "node_modules/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff")


def out(n):
    return os.path.join(OUT, n + ".webp")


def ring(c, r, a0, a1, n=40, squash=1.0):
    return [(c[0] + math.cos(a) * r, c[1] + math.sin(a) * r * squash) for a in np.linspace(a0, a1, n)]


def corner(seed, big=135):
    p = Painting(1000, 1000, seed)
    p.eucalyptus(bez((230, 120), (480, 70), (820, 60)), size=30, spacing=52)
    p.eucalyptus(bez((110, 240), (60, 500), (70, 800)), size=28, spacing=52)
    p.branch(bez((280, 210), (480, 190), (680, 250)), leaf_len=86, spacing=58)
    p.branch(bez((210, 300), (240, 460), (190, 680)), leaf_len=82, spacing=56)
    p.branch(bez((120, 110), (300, 20), (540, 20)), leaf_len=70, spacing=60, color="paleSage", color2="sage")
    p.lavender(300, 300, 0.75, 300)
    p.spray(420, 180, 0.2, 240)
    p.spray(170, 440, 1.25, 230)
    p.spray(330, 340, 0.85, 240, tone="rose")
    p.rose(175, 165, big)
    p.rose(395, 120, big * 0.62, tone="blush", deep="rose", dark="deeprose")
    p.rose(110, 395, big * 0.66, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(345, 280, 56)
    p.wildflower(250, 345, 40, tone="paleSage", deep="sage")
    p.wildflower(530, 150, 38)
    p.wildflower(120, 560, 36, tone="champagne", deep="ochre", centre="brown")
    p.bud(610, 320, 0.4, 62)
    p.bud(285, 610, 1.3, 56)
    p.splatter(420, 420, 95, 22, "rose", 0.5)
    p.splatter(600, 110, 80, 10, "sage", 0.5)
    return p


def arch():
    W, H = 1000, 1300
    p = Painting(W, H, 21)
    c, R = (500, 500), 280
    # fine double line, drawn by a steady hand
    for rr, dens in ((R + 12, 0.85), (R + 26, 0.45)):
        path = [(c[0] - rr, 1140)] + ring(c, rr, math.pi, math.tau, 70) + [(c[0] + rr, 1140)]
        p.pen(path, "burgundy", 1.8, dens, wobble=0.5)
    # a pale halo behind the arch that bleeds out into the paper
    for x, y, r in ((270, 340, 95), (730, 990, 95), (280, 1080, 80)):
        p.blob(x, y, r, color="blush", density=0.3, color2="champagne", bleed=7, wet=8, edge=0.1)
    # climbing vines
    p.branch(bez((205, 1130), (150, 800), (205, 480)), leaf_len=78, spacing=62)
    p.eucalyptus(bez((795, 1040), (880, 760), (800, 460)), size=25, spacing=54)
    p.branch(bez((230, 320), (340, 130), (560, 90)), leaf_len=78, spacing=58)
    p.eucalyptus(bez((260, 260), (150, 200), (60, 250)), size=28, spacing=46)
    p.branch(bez((820, 1130), (920, 1120), (960, 1000)), leaf_len=74, spacing=50, color="paleSage", color2="sage")
    p.branch(bez((170, 1160), (70, 1120), (40, 980)), leaf_len=74, spacing=50, color="paleSage", color2="sage")
    p.branch(bez((560, 1200), (700, 1240), (880, 1210)), leaf_len=70, spacing=52)
    p.lavender(120, 1190, -1.0, 280)
    p.spray(790, 1130, -0.6, 210)
    p.spray(110, 270, -2.5, 120)
    # flowers: top-left cluster
    p.rose(232, 262, 118)
    p.rose(390, 145, 72, tone="blush", deep="rose", dark="deeprose")
    p.rose(115, 385, 66, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(320, 245, 42)
    p.wildflower(500, 118, 32)
    p.wildflower(130, 240, 34, tone="champagne", deep="ochre", centre="brown")
    p.bud(610, 76, 0.1, 50)
    # foot: bottom-right cluster
    p.rose(775, 1095, 128)
    p.rose(610, 1170, 78, tone="blush", deep="rose", dark="deeprose")
    p.rose(905, 960, 70, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(860, 1180, 46)
    p.wildflower(690, 1050, 34, tone="paleSage", deep="sage")
    # foot: left
    p.rose(205, 1160, 92, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(310, 1205, 36)
    p.wildflower(100, 1065, 30, tone="champagne", deep="ochre", centre="brown")
    p.splatter(120, 700, 50, 10, "rose")
    p.splatter(900, 640, 60, 12, "sage")
    p.save(out("arch"), quality=80)


def wreath():
    p = Painting(900, 900, 33)
    c = (450, 450)
    for i in range(16):
        a0 = i / 16 * math.tau
        pts = ring(c, 268 + (i % 3) * 12, a0, a0 + 0.62, 12)
        if i % 3 == 2:
            p.eucalyptus(pts, size=20, spacing=30, density=0.65)
        else:
            p.branch(pts, leaf_len=66, spacing=38, stem_w=2.0, color=("sage" if i % 2 else "paleSage"), color2="deepSage")
    p.pen(ring(c, 232, 0, math.tau, 120), "burgundy", 1.5, 0.6)
    for a, r, tone in ((2.4, 86, "rose"), (3.02, 60, "blush"), (1.72, 58, "blush"), (-0.65, 66, "rose"), (-0.1, 44, "blush")):
        x, y = c[0] + math.cos(a) * 280, c[1] + math.sin(a) * 280
        p.rose(x, y, r, tone=tone, deep="deeprose" if tone == "rose" else "rose", dark="burgundy" if tone == "rose" else "deeprose")
    for a, r in ((1.2, 34), (3.5, 30), (-1.2, 30), (0.5, 28)):
        p.wildflower(c[0] + math.cos(a) * 285, c[1] + math.sin(a) * 285, r)
    p.splatter(450, 800, 90, 10)
    p.save(out("wreath"), (760, 760), 80)


def sprig(name, seed, flip=False):
    p = Painting(760, 320, seed)
    p.branch(bez((370, 200), (240, 140), (50, 200)), leaf_len=58, spacing=42)
    p.branch(bez((390, 200), (530, 130), (710, 200)), leaf_len=58, spacing=42)
    p.eucalyptus(bez((360, 170), (280, 80), (180, 60)), size=16, spacing=30)
    p.spray(420, 170, -0.8, 110)
    p.rose(380, 190, 62)
    p.wildflower(290, 215, 28)
    p.wildflower(465, 225, 24, tone="paleSage", deep="sage")
    p.splatter(380, 270, 70, 8)
    p.save(out(name), (570, 240), 80)


def small_flower():
    p = Painting(340, 200, 12)
    p.branch(bez((170, 120), (100, 90), (20, 130)), leaf_len=38, spacing=28, stem_w=1.6)
    p.branch(bez((170, 120), (240, 90), (320, 130)), leaf_len=38, spacing=28, stem_w=1.6)
    p.wildflower(170, 112, 34)
    p.save(out("flourish"), (255, 150), 82)


def garland():
    p = Painting(1400, 240, 41)
    path = bez((40, 70), (480, 230), (920, 200), (1360, 70), n=60)
    p.pen(path, "deepSage", 1.8, 0.6)
    pts = resample(path, 23)
    tan = np.gradient(pts, axis=0)
    for i in range(1, 22):
        a = math.atan2(tan[i][1], tan[i][0])
        p.leaf(*pts[i], a + (0.9 if i % 2 else -0.9), 62 * p.r.uniform(.75, 1.1), color="sage" if i % 3 else "paleSage")
    for i, r in ((6, 30), (11, 50), (16, 30)):
        p.rose(*pts[i], r, tone="rose" if r > 40 else "blush", deep="deeprose" if r > 40 else "rose")
    for i, r in ((3, 20), (8, 22), (14, 22), (19, 20)):
        p.wildflower(*pts[i], r)
    p.save(out("garland"), (1050, 180), 78)


def vine():
    """Tall side vine for the welcome section."""
    p = Painting(420, 1100, 52)
    path = bez((340, 1090), (60, 800), (360, 420), (120, 30), n=70)
    p.branch(path, leaf_len=72, spacing=46)
    p.eucalyptus(bez((260, 700), (390, 610), (400, 470)), size=19, spacing=34)
    p.spray(180, 860, -2.5, 120)
    p.rose(255, 545, 76)
    p.rose(145, 300, 46, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(190, 800, 38)
    p.wildflower(305, 900, 28, tone="champagne", deep="ochre", centre="brown")
    p.bud(120, 90, -1.8, 40)
    p.splatter(240, 660, 110, 14)
    p.save(out("vine"), (330, 864), 78)


# ------------------------------------------------------------ envelope
def env_flap():
    # art sits inside the flap's triangle: top corners and along the diagonals
    p = Painting(1200, 500, 61)
    p.branch(bez((36, 10), (170, 60), (360, 170)), leaf_len=56, spacing=44, stem_w=2)
    p.branch(bez((1164, 10), (1030, 60), (840, 170)), leaf_len=56, spacing=44, stem_w=2)
    p.eucalyptus(bez((260, 6), (400, 30), (520, 90)), size=15, spacing=30)
    p.eucalyptus(bez((940, 6), (800, 30), (680, 90)), size=15, spacing=30)
    p.rose(120, 44, 66)
    p.rose(1080, 44, 66)
    p.wildflower(225, 72, 26)
    p.wildflower(975, 72, 26)
    p.wildflower(300, 26, 20, tone="paleSage", deep="sage")
    p.wildflower(900, 26, 20, tone="paleSage", deep="sage")
    p.save(out("env-flap"), (900, 375), 80)


def env_pocket():
    p = Painting(1200, 800, 62)
    # bottom corners, climbing the side edges
    p.branch(bez((60, 760), (40, 600), (60, 400)), leaf_len=60, spacing=44, stem_w=2)
    p.branch(bez((1140, 760), (1160, 600), (1140, 400)), leaf_len=60, spacing=44, stem_w=2)
    p.branch(bez((110, 740), (280, 790), (480, 770)), leaf_len=58, spacing=44, stem_w=2)
    p.branch(bez((1090, 740), (920, 790), (720, 770)), leaf_len=58, spacing=44, stem_w=2)
    p.eucalyptus(bez((120, 690), (240, 660), (330, 590)), size=16, spacing=30)
    p.eucalyptus(bez((1080, 690), (960, 660), (870, 590)), size=16, spacing=30)
    p.spray(170, 660, -1.1, 120)
    p.spray(1030, 660, -2.0, 120)
    p.rose(105, 715, 84)
    p.rose(1095, 715, 84)
    p.rose(235, 740, 46, tone="blush", deep="rose", dark="deeprose")
    p.rose(965, 740, 46, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(70, 590, 28)
    p.wildflower(1130, 590, 28)
    p.wildflower(330, 770, 22, tone="paleSage", deep="sage")
    p.wildflower(870, 770, 22, tone="paleSage", deep="sage")
    p.save(out("env-pocket"), (900, 600), 80)


def env_liner():
    p = Painting(1200, 520, 63)
    p.wash([(-20, -20), (1220, -20), (1220, 540), (-20, 540)], "rose", 0.62, color2="blush", edge=0, wet=0, layers=2, var=0.01, depth=1, grain=0.6)
    for x in range(100, 1200, 200):
        p.branch(bez((x, 500), (x - 30, 330), (x + 20, 170)), leaf_len=56, spacing=42, stem_w=1.8)
    for x, y, r in ((200, 160, 58), (600, 90, 72), (1000, 160, 58), (400, 290, 40), (800, 290, 40)):
        p.rose(x, y, r, tone="blush", deep="rose", dark="deeprose")
    p.save(out("env-liner"), (900, 390), 76)


def wax_seal():
    from PIL import ImageFont
    S = 720
    r = np.random.default_rng(7)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    ang = np.arctan2(yy - S / 2, xx - S / 2)
    wob = sum(r.uniform(6, 15) * np.sin(ang * k + r.random() * 6.28) for k in (2, 3, 5, 7, 9))
    rad = np.hypot(xx - S / 2, yy - S / 2)
    outer = 300 + wob
    mask = gf(np.clip(outer - rad, 0, 1), 1.4)
    # height: a raised rim, sunk centre, raised letters
    h = np.clip((outer - rad) / 26, 0, 1) ** 0.6 * 1.0
    well = gf(np.clip(218 - rad, 0, 1), 7) * -0.5
    txt = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(txt)
    f1, f2 = ImageFont.truetype(FONT, 215), ImageFont.truetype(FONT, 118)
    d.text((S / 2 - 104, S / 2 - 12), "E", font=f1, fill=255, anchor="mm")
    d.text((S / 2, S / 2 + 18), "&", font=f2, fill=255, anchor="mm")
    d.text((S / 2 + 108, S / 2 - 12), "P", font=f1, fill=255, anchor="mm")
    letters = gf(np.asarray(txt, dtype=np.float32) / 255, 2.2)
    bump = gf(r.random((S, S), dtype=np.float32), 22) * 12
    H = (h + well + letters * 0.5 + bump) * 34
    H = gf(H, 1.8)
    gy, gx = np.gradient(H)
    nz = 1 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    lx, ly, lz = -0.48, -0.62, 0.62
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    spec = np.clip(nx * lx * 0.6 + ny * ly * 0.6 + nz * 0.8, 0, 1) ** 26
    base = hex2("#D9A6A2")[None, None] * 0.9
    shade = (0.56 + 0.62 * dif)[..., None]
    rgb = base * shade + spec[..., None] * 0.28
    rgb = rgb * (1 + (gf(r.random((S, S), dtype=np.float32), 14)[..., None] - 0.5) * 0.7)
    out_img = np.dstack([np.clip(rgb, 0, 1), mask])
    Image.fromarray((out_img * 255).astype(np.uint8), "RGBA").resize((300, 300), Image.LANCZOS).save(out("seal"), "WEBP", quality=88, alpha_quality=90, method=6)


# ------------------------------------------------------------ event scenes
def ground(p, color="blush", color2="champagne", d=0.34, cx=400, cy=400, r=300):
    p.blob(cx, cy, r, r * 0.92, 0, color, d, color2=color2, bleed=12, wet=9, edge=0.15, var=0.28)


def paisley(p, x, y, s, a, color="wine"):
    """The boteh: a teardrop whose tip curls over."""
    tip, bot = (0.8, -1.12), (0.0, 0.98)
    cur = np.vstack([bez(tip, (-0.75, -1.15), (-1.12, 0.92), bot, n=20), bez(bot, (0.92, 1.0), (1.02, -0.2), tip, n=20)])
    ca, sa = math.cos(a), math.sin(a)
    def T(u, v, k=1.0):
        u, v = u * s * k, v * s * k
        return (x + u * ca - v * sa, y + u * sa + v * ca)
    P = [T(u, v) for u, v in cur]
    p.wash(np.array(P), "rose", 0.3, color2="champagne", wet=1, layers=4, var=0.04, depth=2, edge=0.8)
    p.pen(P, color, 1.8, 0.85, wobble=0.15)
    p.pen([T(u - .04, v + .12, .52) for u, v in cur], color, 1.2, 0.65, wobble=0.1)
    p.blob(*T(-.05, .22), s * .12, color=color, density=0.7, sides=6, layers=3, depth=1, wet=0.4)
    for u, v in cur[1:-1:3]:
        q = T(u, v, 1.2)
        p.blob(q[0], q[1], 2.1, color=color, density=0.8, sides=6, layers=2, depth=1, wet=0.3)


def mehendi():
    p = Painting(800, 800, 71)
    ground(p, "champagne", "blush", 0.42)
    c = (400, 395)
    ink = "wine"
    # the henna mandala, drawn with a cone-fine line
    p.blob(*c, 92, color="ochre", density=0.34, color2="rose", wet=3, edge=0.8)
    p.pen(ring(c, 40, 0, math.tau, 40), ink, 1.8, 0.9)
    p.pen(ring(c, 92, 0, math.tau, 60), ink, 1.6, 0.8)
    for i in range(8):
        a = i / 8 * math.tau
        tipx, tipy = c[0] + math.cos(a) * 88, c[1] + math.sin(a) * 88
        for d in (-1, 1):
            q = bez((c[0] + math.cos(a + d * .4) * 42, c[1] + math.sin(a + d * .4) * 42),
                    (c[0] + math.cos(a + d * .42) * 72, c[1] + math.sin(a + d * .42) * 72), (tipx, tipy), n=12)
            p.pen(q, ink, 1.4, 0.8, wobble=0.1)
    for i in range(16):
        a = (i + 0.5) / 16 * math.tau
        bx, by = c[0] + math.cos(a) * 100, c[1] + math.sin(a) * 100
        p.petal(bx, by, a, 46, 25, "rose", 0.5, color2="deeprose", layers=5, wet=0.7, tip=0.8)
        L = [(bx + math.cos(a + o) * s, by + math.sin(a + o) * s) for o, s in ((0.42, 26), (0.24, 44), (0, 54), (-0.24, 44), (-0.42, 26))]
        p.pen(L, ink, 1.3, 0.75, wobble=0.1)
        p.blob(c[0] + math.cos(a) * 168, c[1] + math.sin(a) * 168, 2.6, color=ink, density=0.85, sides=6, layers=2, depth=1, wet=0.3)
    p.pen(ring(c, 178, 0, math.tau, 110), ink, 1.3, 0.55)
    for a in (0.8, 2.36, 3.93, 5.5):
        paisley(p, c[0] + math.cos(a) * 250, c[1] + math.sin(a) * 250, 42, a + 2.2, ink)
    p.wildflower(*c, 34, tone="blush", deep="rose")
    for a in (0, 1.57, 3.14, 4.71):
        x, y = c[0] + math.cos(a) * 248, c[1] + math.sin(a) * 248
        p.branch(ring(c, 248, a - 0.34, a + 0.34, 14), leaf_len=42, spacing=30, stem_w=1.6)
        p.wildflower(x, y, 25, tone="champagne", deep="ochre", centre="brown")
    p.splatter(400, 400, 260, 18, "ochre", 0.5)
    p.save(os.path.join(EV, "mehendi.webp"), (680, 680), 80)


def marigold(p, x, y, r, tone="champagne", deep="ochre"):
    p.lift(x, y, r * .9, r * .9, .9)
    p.blob(x, y, r, color=tone, density=0.85, color2=deep, wet=0.6, layers=5, var=0.24, sides=11, edge=1.5)
    for i in range(6):
        a = p.r.random() * math.tau
        p.pen(ring((x, y), r * p.r.uniform(.35, .8), a, a + 1.1, 6), "ochre", 1.3, 0.8, wobble=0.1)


def parasol(p, x, y, s):
    """A ceremonial chhatri on a slender pole."""
    p.stroke([(x, y - s * 0.5), (x + 3, y + s * 1.45)], 5, "ochre", 0.75, "brown", taper=(0.9, 0.7), wobble=0.3)
    top = [(x + math.cos(a) * s, y + math.sin(a) * s * 0.62) for a in np.linspace(math.pi, math.tau, 26)]
    scal = []
    for i in range(6):
        x0 = x + s - i * (2 * s / 6)
        scal += [(x0 - (2 * s / 6) * t, y + math.sin(t * math.pi) * s * 0.12) for t in np.linspace(0, 1, 7)]
    dome = np.array(top + scal)
    p.wash(dome, "rose", 0.72, color2="deeprose", wet=1.4, layers=8, var=0.05, depth=2, edge=1.4, fade=(x - s * .3, y - s * .4, s * 1.5, .55, 1.2))
    for a in np.linspace(math.pi + 0.5, math.tau - 0.5, 5):
        p.pen([(x, y - s * 0.62), (x + math.cos(a) * s * 0.99, y + 2)], "burgundy", 1.2, 0.5, wobble=0.2)
    p.pen(top, "burgundy", 1.5, 0.7)
    p.pen(scal, "burgundy", 1.4, 0.75)
    for i in range(6):
        x0 = x + s - (i + .5) * (2 * s / 6)
        p.pen([(x0, y + s * .12), (x0, y + s * .24)], "ochre", 1.2, 0.9)
        p.blob(x0, y + s * .27, 4.2, color="ochre", density=0.9, sides=6, layers=3, depth=1, wet=0.4)
    p.blob(x, y - s * 0.68, 8, color="ochre", density=0.95, wet=0.5, layers=4)


def jaan():
    p = Painting(800, 800, 72)
    ground(p, "blush", "champagne", 0.36, 400, 420, 310)
    # toran: strands of marigold and rose hung across the top
    rope = bez((62, 128), (260, 188), (540, 188), (738, 128), n=50)
    pts = resample(rope, 13)
    p.pen(rope, "deepSage", 2.0, 0.75)
    for i, (x, y) in enumerate(pts):
        L = [5, 3, 6, 2, 5, 3, 7, 3, 5, 2, 6, 3, 5][i]
        for j in range(L):
            yy = y + j * 30
            r = 13 - j * 0.45
            marigold(p, x + p.r.uniform(-2, 2), yy, r, *(("blush", "rose") if j % 3 == 2 else ("champagne", "ochre")))
        if i % 2 == 0:
            p.leaf(x, y + L * 30 - 12, 1.57 + p.r.uniform(-.3, .3), 36, density=0.7)
    for x, y in pts[::2]:
        p.leaf(x, y, -1.2, 40)
        p.leaf(x, y, -1.95, 40, color="paleSage", color2="sage")
    parasol(p, 400, 395, 142)
    # the procession's path, scattered with petals
    for side in (-1, 1):
        x0 = 400 + side * 250
        p.branch(bez((400 + side * 95, 690), (400 + side * 180, 650), (x0 + side * 40, 530)), leaf_len=58, spacing=38)
        p.spray(400 + side * 150, 680, -1.57 + side * 0.5, 130)
    p.rose(280, 680, 66)
    p.rose(520, 680, 66)
    p.rose(400, 708, 44, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(190, 662, 30)
    p.wildflower(610, 662, 30)
    for _ in range(26):
        x, y = 400 + p.r.normal(0, 160), 620 + p.r.uniform(-30, 130)
        p.petal(x, y, p.r.random() * 6.28, 15, 10, "rose", 0.6, layers=3, wet=0.4, depth=2, tip=0.8)
    p.save(os.path.join(EV, "jaan-swagat.webp"), (680, 680), 80)


def hasta():
    p = Painting(800, 800, 73)
    ground(p, "blush", "rose", 0.3, 400, 400, 320)
    # mandap: four slender posts and a domed canopy
    posts = [(150, 700), (252, 640), (548, 640), (650, 700)]
    for x, y in posts:
        top = 262 if x in (150, 650) else 278
        p.wash(np.array([(x - 8, top), (x + 8, top), (x + 8, y), (x - 8, y)]), "champagne", 0.75, color2="ochre", wet=0.7, layers=5, var=0.02, depth=1, edge=1.4)
        p.pen([(x - 8, top), (x - 8, y)], "burgundy", 1.2, 0.5, wobble=0.2)
        p.pen([(x + 8, top), (x + 8, y)], "burgundy", 1.2, 0.5, wobble=0.2)
        for d in (0.3, 0.65):
            yy = top + (y - top) * d
            p.pen([(x - 12, yy), (x + 12, yy)], "burgundy", 1.4, 0.6, wobble=0.1)
    p.pen(bez((130, 702), (400, 730), (670, 702)), "burgundy", 1.4, 0.45)
    p.pen([(252, 640), (548, 640)], "burgundy", 1.2, 0.3)
    dome = [(400 + math.cos(a) * 285, 262 + math.sin(a) * 158) for a in np.linspace(math.pi, math.tau, 30)]
    scal = []
    for i in range(8):
        x0 = 685 - i * (570 / 8)
        scal += [(x0 - (570 / 8) * t, 262 + math.sin(t * math.pi) * 28) for t in np.linspace(0, 1, 7)]
    p.wash(np.array(dome + scal), "rose", 0.6, color2="deeprose", wet=1.8, layers=9, var=0.03, depth=2, edge=1.2, fade=(280, 150, 480, .5, 1.1))
    p.pen(dome, "burgundy", 1.7, 0.7)
    p.pen(scal, "burgundy", 1.5, 0.75)
    for a in np.linspace(math.pi + 0.55, math.tau - 0.55, 5):
        p.pen([(400, 104), (400 + math.cos(a) * 280, 258)], "burgundy", 1.1, 0.42)
    # blossoms cascading from each corner
    for x, s in ((130, 1), (670, -1)):
        p.branch(bez((x, 250), (x + s * 18, 360), (x - s * 10, 510)), leaf_len=44, spacing=34, stem_w=1.5)
        p.rose(x, 248, 52)
        p.wildflower(x + s * 50, 215, 24)
        p.wildflower(x + s * 18, 335, 20, tone="champagne", deep="ochre", centre="brown")
        p.wildflower(x + s * -6, 430, 17)
    p.rose(400, 95, 44)
    # swagged garland across the opening
    sw = bez((252, 300), (400, 410), (548, 300), n=26)
    q = resample(sw, 17)
    for i, (x, y) in enumerate(q):
        if i % 2:
            p.leaf(x, y, 1.57 + p.r.uniform(-.7, .7), 28, density=0.7)
        marigold(p, x, y, 11, *(("blush", "rose") if i % 3 == 0 else ("champagne", "ochre")))
    # two garlands, joined: the ceremony's heart
    for cx, tone, deep in ((362, "blush", "rose"), (438, "champagne", "ochre")):
        g = ring((cx, 520), 62, 0, math.tau, 24, 1.0)[:-1]
        for i, (x, y) in enumerate(g):
            marigold(p, x, y, 9.5, tone if i % 3 else "rose", deep)
    p.branch(bez((230, 690), (300, 640), (370, 680)), leaf_len=48, spacing=32, stem_w=1.5)
    p.branch(bez((570, 690), (500, 640), (430, 680)), leaf_len=48, spacing=32, stem_w=1.5)
    p.rose(400, 695, 58)
    p.wildflower(318, 702, 28)
    p.wildflower(482, 702, 28)
    p.splatter(400, 620, 180, 14)
    p.save(os.path.join(EV, "hasta-melap.webp"), (680, 680), 80)


def candle(p, x, base, h, w=20):
    top = base - h
    p.blob(x, top - 24, 42, color="champagne", density=0.5, bleed=5, wet=9, edge=0.0)
    p.lift(x, top - 22, 11, 22, 1, 6)
    p.wash(np.array([(x - w / 2, top), (x + w / 2, top + 2), (x + w / 2, base), (x - w / 2, base)]), "blush", 0.55, color2="champagne", wet=0.6, layers=4, var=0.02, depth=1, edge=1.5)
    p.pen([(x, top), (x + 1, top - 8)], "brown", 1.4, 0.9, wobble=0)
    fl = [(x, top - 42), (x + 8, top - 22), (x + 5, top - 10), (x, top - 6), (x - 5, top - 10), (x - 8, top - 22)]
    p.wash(np.array(fl), "ochre", 0.95, color2="champagne", wet=0.7, layers=4, var=0.06, depth=2, edge=1.1, fade=(x, top - 8, 34, 1.6, .5))


def reception():
    p = Painting(800, 800, 74)
    # evening sky, soft and dark at the crown
    p.blob(400, 300, 340, 280, 0, "dusk", 0.55, color2="rose", bleed=14, wet=10, edge=0.12)
    p.blob(400, 170, 250, 130, 0, "burgundy", 0.2, bleed=12, wet=10, edge=0.1)
    for _ in range(24):
        a, d = p.r.uniform(math.pi * 1.03, math.pi * 1.97), p.r.uniform(245, 335)
        x, y = 400 + math.cos(a) * d, 410 + math.sin(a) * d
        p.lift(x, y, p.r.uniform(2, 4.5), None, 1, 1.2)
    # floral arch of the stage
    c = (400, 455)
    for a0, a1 in ((math.pi, math.pi * 1.5), (math.pi * 1.5, math.tau)):
        p.branch(ring(c, 248, a0, a1, 24), leaf_len=66, spacing=38, stem_w=2)
    p.eucalyptus(ring(c, 278, math.pi * 1.1, math.pi * 1.45, 12), size=17, spacing=28)
    p.eucalyptus(ring(c, 278, math.pi * 1.55, math.pi * 1.9, 12), size=17, spacing=28)
    p.pen(ring(c, 205, math.pi, math.tau, 60), "burgundy", 1.4, 0.5)
    for a, r, t in ((1.0, 74, "rose"), (.82, 50, "blush"), (1.2, 52, "blush"), (.66, 42, "rose"), (1.36, 42, "rose"), (.5, 34, "blush"), (1.5, 34, "blush"), (.24, 38, "rose"), (1.76, 38, "rose"), (.04, 44, "blush"), (1.96, 44, "blush")):
        A = math.pi + (a / 2) * math.pi
        p.rose(c[0] + math.cos(A) * 252, c[1] + math.sin(A) * 252, r, tone=t, deep="deeprose" if t == "rose" else "rose", dark="burgundy" if t == "rose" else "deeprose")
    # the stage: one low painted platform with a fine edge
    p.wash(np.array([(120, 610), (680, 610), (760, 668), (40, 668)]), "blush", 0.5, color2="champagne", wet=1, layers=6, var=0.015, depth=1, edge=1.0)
    p.pen([(120, 610), (680, 610)], "burgundy", 1.3, 0.55)
    p.pen([(40, 668), (760, 668)], "burgundy", 1.3, 0.5)
    p.pen([(120, 610), (40, 668)], "burgundy", 1.2, 0.4)
    p.pen([(680, 610), (760, 668)], "burgundy", 1.2, 0.4)
    # candles, grouped in threes either side
    for x, h in ((92, 112), (140, 72), (188, 44), (612, 44), (660, 72), (708, 112)):
        candle(p, x, 662, h, 18)
    p.branch(bez((60, 700), (260, 738), (390, 696)), leaf_len=48, spacing=36, stem_w=1.5)
    p.branch(bez((740, 700), (540, 738), (410, 696)), leaf_len=48, spacing=36, stem_w=1.5)
    p.rose(400, 706, 52)
    p.wildflower(300, 712, 26)
    p.wildflower(500, 712, 26)
    p.save(os.path.join(EV, "reception.webp"), (680, 680), 80)


def vrat():
    p = Painting(800, 800, 75)
    ground(p, "champagne", "blush", 0.22, 400, 430, 250)
    # kalash: an old, simple form, painted in one breath
    prof = [(0, 0), (34, 6), (42, 26), (32, 48), (68, 84), (112, 150), (120, 208), (92, 272), (54, 312), (66, 328), (0, 332)]
    x0, y0 = 400, 268
    L = [(x0 - a, y0 + b) for a, b in prof]
    R = [(x0 + a, y0 + b) for a, b in prof]
    poly = np.array(R + L[::-1][1:-1])
    p.wash(poly, "champagne", 0.62, color2="blush", wet=1.6, layers=8, var=0.018, depth=2, edge=1.3, fade=(355, 390, 170, .55, 1.25))
    p.pen(L, "burgundy", 1.7, 0.75, wobble=0.2)
    p.pen(R, "burgundy", 1.7, 0.75, wobble=0.2)
    p.pen(bez((x0 - 111, 416), (x0, 462), (x0 + 111, 416)), "burgundy", 1.3, 0.55)
    p.pen(bez((x0 - 117, 446), (x0, 494), (x0 + 117, 446)), "burgundy", 1.3, 0.55)
    p.wildflower(x0, 400, 28, tone="blush", deep="rose")
    # mango leaves fanned at the mouth
    for a in (-2.55, -2.2, -1.85, -1.29, -0.94, -0.59):
        p.leaf(x0 + math.cos(a) * 18, y0 + 10, a, 138, 44, density=0.75)
    p.leaf(x0, y0 + 6, -1.57, 120, 40, color="paleSage", color2="sage", density=0.8)
    p.blob(x0, 250, 36, 32, 0, "ochre", 0.5, color2="champagne", wet=1.2, layers=7, var=0.1)
    # a single low sprig and a few fallen petals
    p.pen(bez((180, 612), (400, 640), (620, 612)), "burgundy", 1.2, 0.35)
    p.branch(bez((220, 622), (260, 610), (310, 620)), leaf_len=36, spacing=26, stem_w=1.3)
    p.wildflower(216, 618, 20)
    for x, y in ((540, 610), (572, 626), (606, 606)):
        p.petal(x, y, p.r.random() * 6.28, 18, 12, "rose", 0.6, layers=3, wet=0.4, depth=2)
    p.save(os.path.join(EV, "vrat.webp"), (680, 680), 80)


def coupe(p, x, y, tilt, s=1.0):
    ca, sa = math.cos(tilt), math.sin(tilt)
    T = lambda u, v: (x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
    bowl = [T(u, v) for u, v in [(-96, 0), (-90, 34), (-64, 66), (-26, 86), (0, 90), (26, 86), (64, 66), (90, 34), (96, 0)]]
    liquid = np.array([T(u, v) for u, v in [(-88, 24), (-64, 62), (-26, 84), (0, 88), (26, 84), (64, 62), (88, 24), (40, 30), (-40, 18)]])
    p.lift(x, y + 40 * s, 92 * s, 50 * s, 0.75)
    p.wash(liquid, "champagne", 0.9, color2="ochre", wet=1.2, layers=6, var=0.04, depth=2, edge=1.5)
    for _ in range(9):
        u, v = p.r.uniform(-50, 50), p.r.uniform(32, 76)
        p.lift(*T(u, v), 2.4, None, 0.9, 0.8)
    p.pen(resample(np.array(bowl), 30), "burgundy", 1.9, 0.85)
    rim = [T(math.cos(a) * 96, math.sin(a) * 15) for a in np.linspace(0, math.tau, 36)]
    p.pen(rim, "burgundy", 1.6, 0.75)
    p.pen([T(-2, 90), T(-3, 248)], "burgundy", 1.8, 0.8, wobble=0.15)
    p.pen([T(3, 90), T(4, 248)], "burgundy", 1.6, 0.6, wobble=0.15)
    p.pen([T(math.cos(a) * 58, 254 + math.sin(a) * 9) for a in np.linspace(0, math.tau, 26)], "burgundy", 1.6, 0.75)


def star(p, x, y, s):
    p.pen([(x - s, y), (x + s, y)], "ochre", 1.2, 0.9, wobble=0.05)
    p.pen([(x, y - s), (x, y + s)], "ochre", 1.2, 0.9, wobble=0.05)
    p.blob(x, y, s * 0.2, color="ochre", density=0.9, sides=6, layers=2, depth=1, wet=0.3)


def cocktail():
    p = Painting(800, 800, 76)
    p.blob(400, 330, 320, 270, 0, "dusk", 0.45, color2="champagne", bleed=14, wet=10, edge=0.12)
    p.branch(bez((110, 660), (120, 480), (70, 330)), leaf_len=64, spacing=42)
    p.branch(bez((690, 660), (680, 480), (730, 330)), leaf_len=64, spacing=42)
    p.eucalyptus(bez((180, 668), (260, 620), (350, 680)), size=15, spacing=26)
    p.eucalyptus(bez((620, 668), (540, 620), (450, 680)), size=15, spacing=26)
    coupe(p, 296, 250, 0.2, 1.15)
    coupe(p, 504, 250, -0.2, 1.15)
    for x, y, s in ((400, 112, 14), (306, 92, 8), (494, 88, 9), (162, 175, 9), (640, 165, 10), (400, 195, 6), (225, 90, 5), (580, 70, 5)):
        star(p, x, y, s)
    p.splatter(400, 130, 150, 18, "ochre", 0.7, (0.8, 2.2))
    p.rose(160, 655, 74)
    p.rose(640, 655, 74)
    p.rose(272, 700, 46, tone="blush", deep="rose", dark="deeprose")
    p.rose(528, 700, 46, tone="blush", deep="rose", dark="deeprose")
    p.wildflower(400, 702, 34)
    p.wildflower(84, 580, 24, tone="champagne", deep="ochre", centre="brown")
    p.wildflower(716, 580, 24, tone="champagne", deep="ochre", centre="brown")
    p.save(os.path.join(EV, "cocktail.webp"), (680, 680), 80)


# ------------------------------------------------------------ map
def venue_map():
    p = Painting(1000, 760, 81)
    # the sea, a wash that fades out before it reaches the sheet's edge
    p.wash(np.array([(-40, -40), (150, -40), (240, 160), (190, 330), (260, 520), (210, 800), (-40, 800)]),
           "paleSage", 0.55, color2="sage", wet=7, bleed=5, layers=9, var=0.08, edge=0.8)
    for i in range(5):
        x = 70 + i * 22
        p.pen([(x + math.sin(y / 52 + i) * 9, y) for y in range(180 + i * 50, 300 + i * 50, 12)], "deepSage", 1.1, 0.4)
    for x, y, r in ((560, 170, 80), (790, 560, 92), (360, 610, 66)):
        p.blob(x, y, r, r * .8, 0.3, "sage", 0.28, color2="paleSage", bleed=4, wet=4, edge=0.5)
    roads = [bez((230, 80), (480, 220), (590, 390), (960, 450)), bez((280, 700), (420, 480), (530, 390), (760, 30)),
             bez((250, 340), (420, 330), (560, 400), (740, 730)), bez((640, 30), (660, 260), (820, 300), (980, 240))]
    for r_ in roads:
        p.stroke(r_, 8, "champagne", 0.75, None, taper=(1, 1), wobble=0.3, wet=0.8, edge=1.0)
        p.pen(r_ + np.array([0, 5.5]), "brown", 0.9, 0.35, wobble=0.2)
        p.pen(r_ - np.array([0, 5.5]), "brown", 0.9, 0.35, wobble=0.2)
    for m in (bez((400, 240), (470, 150), (540, 90)), bez((710, 440), (760, 520), (860, 520)), bez((440, 370), (420, 300), (340, 240)), bez((500, 560), (600, 560), (650, 660)), bez((820, 300), (850, 200), (930, 140))):
        p.pen(m, "brown", 1.0, 0.32, wobble=0.3)
    # dotted route to the flower that marks the place
    route = resample(bez((300, 690), (390, 520), (470, 460), (570, 396)), 19)
    for x, y in route[:-2]:
        p.blob(x, y, 3.3, color="burgundy", density=0.85, sides=6, layers=2, depth=1, wet=0.3)
    p.branch(bez((585, 400), (660, 360), (720, 390)), leaf_len=46, spacing=32, stem_w=1.5)
    p.branch(bez((585, 400), (500, 345), (450, 330)), leaf_len=46, spacing=32, stem_w=1.5)
    p.rose(585, 392, 62)
    # compass
    cx, cy, R = 730, 590, 50
    p.pen(ring((cx, cy), R, 0, math.tau, 50), "burgundy", 1.3, 0.6)
    p.pen(ring((cx, cy), R - 7, 0, math.tau, 50), "burgundy", 1.0, 0.4)
    for a, l, tone in ((-1.57, 60, "burgundy"), (0, 42, "rose"), (1.57, 42, "rose"), (3.14, 42, "rose")):
        ca, sa = math.cos(a), math.sin(a)
        p.wash(np.array([(cx + ca * l, cy + sa * l), (cx - sa * 9, cy + ca * 9), (cx + sa * 9, cy - ca * 9)]), tone, 0.8, wet=0.4, layers=3, var=0.01, depth=1, edge=0.8)
    p.save(out("map"), (800, 608), 80)


# ------------------------------------------------------------ placeholders, petals, paper
def placeholder(name, seed, kind):
    p = Painting(600, 800, seed)
    tones = {"a": ("blush", "champagne"), "b": ("paleSage", "blush"), "c": ("champagne", "rose"), "plain": ("blush", "champagne")}[kind]
    p.wash(np.array([(-40, -40), (640, -40), (640, 840), (-40, 840)]), tones[0], 0.34, color2=tones[1], wet=0, layers=2, var=0.01, depth=1, edge=0, grain=0.5)
    p.blob(300, 400, 210, 280, 0, tones[1], 0.1, bleed=12, wet=10, edge=0.1)
    if kind == "a":
        p.branch(bez((480, 800), (420, 560), (500, 300)), leaf_len=70, spacing=52)
        p.rose(470, 690, 88, tone="rose")
    elif kind == "b":
        p.eucalyptus(bez((70, 800), (160, 540), (90, 260)), size=30, spacing=56, color="sage", color2="deepSage")
        p.wildflower(130, 680, 50)
    else:
        p.branch(bez((20, 140), (220, 180), (360, 60)), leaf_len=62, spacing=46)
        p.rose(90, 110, 74, tone="rose")
    p.save(out(name), (360, 480), 66)


def petals():
    for i, (tone, deep) in enumerate((("rose", "deeprose"), ("blush", "rose"), ("champagne", "rose"))):
        p = Painting(120, 120, 90 + i)
        p.petal(26, 62, -0.25 + i * 0.25, 78, 56, tone, 0.85, color2=deep, wet=0.9, layers=6, tip=0.7)
        p.save(out(f"petal-{i + 1}"), (60, 60), 80)


def paper(name, base, amp, q=78):
    r = np.random.default_rng(101)
    S = 360
    n = lambda s: gf(r.random((S, S), dtype=np.float32), s, mode="wrap")
    norm = lambda a: (a - a.mean()) / a.std()
    fib = norm(gf(r.random((S, S)), (0.5, 2.6), mode="wrap")) + norm(gf(r.random((S, S)), (2.6, 0.5), mode="wrap"))
    t = norm(n(0.8)) * 0.7 + fib * 0.5 + norm(n(7)) * 0.25
    b = hex2(base) * 255
    a = np.clip(b[None, None] + t[..., None] * amp, 0, 255).astype(np.uint8)
    Image.fromarray(a, "RGB").save(out(name), "WEBP", quality=q, method=6)


JOBS = dict(corner=lambda: (corner(11).save(out("corner-a"), (800, 800), 78), corner(14, 118).save(out("corner-b"), (800, 800), 78)),
            arch=arch, wreath=wreath, sprigs=lambda: (sprig("sprig-a", 15), sprig("sprig-b", 16)), flourish=small_flower,
            garland=garland, vine=vine, flap=env_flap, pocket=env_pocket, liner=env_liner, seal=wax_seal,
            mehendi=mehendi, jaan=jaan, hasta=hasta, reception=reception, vrat=vrat, cocktail=cocktail, map=venue_map,
            ph=lambda: (placeholder("placeholder-a", 201, "a"), placeholder("placeholder-b", 202, "b"), placeholder("placeholder-c", 203, "c"), placeholder("placeholder-plain", 204, "plain")),
            petals=petals, paper=lambda: (paper("paper-ivory", "#F8F3ED", 1.5), paper("paper-white", "#FFFCF8", 1.1)))

if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    pick = sys.argv[1:] or list(JOBS)
    for k in pick:
        JOBS[k]()
        print("painted", k, flush=True)
