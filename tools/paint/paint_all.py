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


# Four bouquets, each tucked into the top-left corner of its sheet, so no screen
# shows the same arrangement twice. (x, y, radius, flower, tone)
BOUQUETS = {
    # a full, round mass in the corner with arms along both edges
    "a": dict(seed=111, arms=[(0.05, 640), (0.32, 520), (0.62, 470), (0.95, 520), (1.28, 640), (0.18, 360), (1.1, 380)],
              blooms=[(560, 70, 62, "rose", "blush"), (70, 560, 66, "rose", "blush"), (470, 205, 50, "wild", None),
                      (215, 400, 46, "wild", None), (390, 300, 58, "rose", "blush"), (300, 255, 92, "peony", "blush"),
                      (95, 360, 112, "peony", "rose"), (375, 95, 108, "rose", "blush"), (150, 150, 150, "rose", "rose")],
              buds=[(690, 120, 0.2), (130, 700, 1.4), (520, 330, 0.7)], berries=[(260, 120, -0.1), (120, 300, 1.7)]),
    # a cascade that tumbles down the left edge
    "b": dict(seed=112, arms=[(0.05, 430), (0.35, 380), (1.25, 820), (1.45, 900), (1.05, 700), (1.6, 760), (0.75, 420)],
              blooms=[(330, 110, 66, "rose", "blush"), (110, 760, 64, "rose", "blush"), (220, 620, 58, "wild", None),
                      (90, 610, 86, "peony", "blush"), (240, 450, 74, "rose", "blush"), (120, 440, 104, "rose", "rose"),
                      (260, 260, 98, "peony", "blush"), (115, 215, 140, "rose", "rose")],
              buds=[(80, 880, 1.6), (430, 70, 0.1), (330, 560, 1.0)], berries=[(200, 330, 0.9), (60, 520, 1.6), (420, 160, 0.4)]),
    # a long, low sweep along the top edge
    "c": dict(seed=113, arms=[(0.0, 900), (0.12, 820), (-0.05, 760), (0.3, 560), (1.3, 420), (0.85, 380), (1.0, 300)],
              blooms=[(740, 70, 54, "rose", "blush"), (90, 340, 66, "rose", "blush"), (610, 120, 50, "wild", None),
                      (520, 70, 84, "peony", "blush"), (390, 170, 70, "rose", "blush"), (300, 75, 116, "rose", "rose"),
                      (150, 210, 104, "peony", "rose"), (95, 85, 120, "rose", "blush")],
              buds=[(860, 90, 0.05), (110, 480, 1.5), (450, 250, 0.9)], berries=[(650, 40, 0.15), (230, 300, 1.0)]),
    # an offset crescent, opening towards the page
    "d": dict(seed=114, arms=[(0.1, 700), (0.4, 600), (0.75, 520), (1.1, 600), (1.4, 720), (0.55, 340)],
              blooms=[(610, 110, 60, "wild", None), (110, 610, 58, "wild", None), (500, 160, 70, "rose", "blush"),
                      (150, 500, 72, "rose", "blush"), (420, 300, 54, "rose", "blush"), (360, 110, 100, "peony", "blush"),
                      (110, 350, 96, "peony", "rose"), (255, 220, 128, "rose", "rose"), (70, 90, 84, "rose", "blush")],
              buds=[(720, 140, 0.25), (140, 720, 1.35), (560, 290, 0.75)], berries=[(330, 360, 0.8), (420, 40, 0.0), (40, 420, 1.55)]),
}


def bouquet(style):
    b = BOUQUETS[style]
    p = Painting(1000, 1000, b["seed"])
    rng = p.r
    blooms = b["blooms"]
    big = [q for q in blooms if q[2] >= 80]
    # greenery is painted first, around the flowers, so the flowers sit in front of it
    p.stencil([(x, y, r * (0.92 if k != "wild" else 0.8)) for x, y, r, k, _ in blooms])
    for x, y, r, *_ in big:
        p.blob(x, y, r * 1.6, r * 1.4, 0, "paleSage", 0.18, color2="blush", bleed=6, wet=8, edge=0.1)
    for i, (a, L) in enumerate(b["arms"]):
        a += rng.uniform(-0.06, 0.06)
        ox, oy = big[i % len(big)][:2]
        x0, y0 = ox + rng.uniform(-20, 20), oy + rng.uniform(-20, 20)
        ex, ey = 60 + math.cos(a) * L, 60 + math.sin(a) * L
        dx, dy = ex - x0, ey - y0
        bend = rng.uniform(-0.16, 0.16)
        mid = ((x0 + ex) / 2 - dy * bend, (y0 + ey) / 2 + dx * bend)
        kind = i % 3
        if kind == 0:
            p.branch(bez((x0, y0), mid, (ex, ey)), leaf_len=rng.uniform(80, 98), spacing=rng.uniform(34, 42))
        elif kind == 1:
            p.eucalyptus(bez((x0, y0), mid, (ex, ey)), size=rng.uniform(26, 33), spacing=rng.uniform(36, 42))
        else:
            p.branch(bez((x0, y0), mid, (ex, ey)), leaf_len=rng.uniform(68, 82), spacing=rng.uniform(32, 40),
                     color="paleSage", color2="sage")
    # short leafy stems peeking out between neighbouring blooms
    for x, y, r, *_ in blooms:
        for _ in range(2):
            a = math.atan2(y - 60, x - 60) + rng.uniform(-1.3, 1.3)
            L = r * rng.uniform(1.5, 2.1)
            p.branch(bez((x, y), (x + math.cos(a) * L * 0.55 + rng.uniform(-15, 15), y + math.sin(a) * L * 0.55), (x + math.cos(a) * L, y + math.sin(a) * L)),
                     leaf_len=rng.uniform(50, 66), spacing=rng.uniform(26, 32), stem_w=1.8,
                     color=rng.choice(["sage", "paleSage", "sage"]), color2="deepSage", terminal=rng.random() < 0.6)
    for x, y, r, *_ in big[:3]:
        a = math.atan2(y - 60, x - 60) + rng.uniform(-0.6, 0.6)
        p.spray(x, y, a, r + rng.uniform(150, 210), tone=rng.choice(["champagne", "rose"]))
    ox, oy = big[-1][:2]
    p.lavender(ox, oy, math.atan2(oy - 40, ox - 40) + rng.uniform(-0.4, 0.4), rng.uniform(320, 400))
    for x, y, a in b["berries"]:
        p.berries(x, y, a, rng.uniform(90, 130))
    for x, y, a in b["buds"]:
        p.bud(x, y, a, rng.uniform(52, 66))
    p.mask = None
    # blooms, smallest first, on clean paper
    for i, (x, y, r, kind, tone) in enumerate(blooms):
        if kind == "rose":
            if tone == "blush" and i % 3 == 1:
                tone, deep, dark = "champagne", "ochre", "brown"
            else:
                deep, dark = ("deeprose", "burgundy") if tone == "rose" else ("rose", "deeprose")
            p.rose(x, y, r, tone=tone, deep=deep, dark=dark, reserve=0)
        elif kind == "peony":
            p.peony(x, y, r, tone=tone, deep="deeprose" if tone == "rose" else "rose", dark="burgundy" if tone == "rose" else "deeprose")
        else:
            p.wildflower(x, y, r, *(("champagne", "ochre", "brown") if rng.random() < 0.4 else ("blush", "rose", "ochre")))
    for x, y, r, *_ in big[-3:]:
        a = rng.random() * math.tau
        p.wildflower(x + math.cos(a) * r * 1.0, y + math.sin(a) * r * 1.0, rng.uniform(22, 30),
                     *(("paleSage", "sage", "ochre") if rng.random() < 0.3 else ("blush", "rose", "ochre")))
    p.splatter(380, 380, 140, 24, "rose", 0.5)
    p.splatter(560, 160, 90, 10, "sage", 0.5)
    p.save(out(f"corner-{style}"), (800, 800), 80)


def arch():
    W, H = 1000, 1300
    p = Painting(W, H, 21)
    rng = p.r
    c, R = (500, 500), 280
    # fine double line, drawn by a steady hand
    for rr, dens in ((R + 12, 0.85), (R + 26, 0.45)):
        path = [(c[0] - rr, 1140)] + ring(c, rr, math.pi, math.tau, 70) + [(c[0] + rr, 1140)]
        p.pen(path, "burgundy", 1.8, dens, wobble=0.5)
    # (x, y, r, kind, tone): crown at top left, a heavy foot at bottom right, a lighter foot at left,
    # and a small bloom on each flank where the trailing sprays start
    blooms = [(520, 108, 46, "wild", None), (150, 250, 42, "wild", None), (345, 255, 60, "rose", "champagne"),
              (112, 392, 82, "rose", "blush"), (392, 142, 90, "peony", "blush"), (232, 262, 132, "rose", "rose"),
              (92, 640, 52, "rose", "blush"), (910, 610, 50, "peony", "blush"),
              (870, 1185, 50, "wild", None), (700, 1012, 56, "rose", "champagne"), (905, 955, 80, "rose", "blush"),
              (612, 1178, 90, "peony", "blush"), (775, 1095, 140, "rose", "rose"),
              (95, 1062, 44, "wild", None), (322, 1212, 54, "rose", "champagne"), (205, 1160, 100, "peony", "blush")]
    p.stencil([(x, y, r * (0.92 if k != "wild" else 0.8)) for x, y, r, k, _ in blooms])
    for x, y, r in ((270, 330, 150), (760, 1060, 160), (220, 1130, 110)):
        p.blob(x, y, r, color="paleSage", density=0.2, color2="blush", bleed=7, wet=8, edge=0.1)
    # climbing vines up both sides of the arch
    p.branch(bez((205, 1130), (150, 800), (205, 480)), leaf_len=80, spacing=40)
    p.eucalyptus(bez((795, 1040), (880, 760), (800, 460)), size=26, spacing=40)
    p.branch(bez((232, 262), (340, 130), (580, 80)), leaf_len=80, spacing=40)
    p.eucalyptus(bez((232, 262), (150, 190), (40, 250)), size=28, spacing=40)
    p.branch(bez((232, 262), (120, 300), (60, 470)), leaf_len=70, spacing=36, color="paleSage", color2="sage")
    p.branch(bez((392, 142), (500, 60), (690, 50)), leaf_len=64, spacing=34, color="paleSage", color2="sage")
    p.branch(bez((775, 1095), (920, 1120), (980, 980)), leaf_len=76, spacing=38, color="paleSage", color2="sage")
    p.branch(bez((205, 1160), (70, 1120), (20, 960)), leaf_len=74, spacing=38, color="paleSage", color2="sage")
    p.branch(bez((612, 1178), (720, 1250), (900, 1230)), leaf_len=70, spacing=36)
    p.branch(bez((775, 1095), (840, 900), (960, 820)), leaf_len=66, spacing=36)
    # trailing sprays off each flank: the names rest among these
    for sx, dirn, y0 in ((92, -1, 640), (910, 1, 610)):
        p.branch(bez((sx, y0), (sx + dirn * 60, y0 - 40), (sx + dirn * 140, y0 - 10)), leaf_len=58, spacing=30, stem_w=1.8)
        p.eucalyptus(bez((sx, y0), (sx + dirn * 50, y0 + 50), (sx + dirn * 120, y0 + 70)), size=20, spacing=30)
        p.branch(bez((sx, y0), (sx - dirn * 10, y0 + 100), (sx + dirn * 20, y0 + 200)), leaf_len=56, spacing=30, stem_w=1.6,
                 color="paleSage", color2="sage")
        p.spray(sx, y0, -1.57 + dirn * 0.9, 150, tone="rose")
        p.berries(sx, y0, dirn * 0.2 + (math.pi if dirn < 0 else 0), 110)
    for x, y, r, *_ in blooms:
        for _ in range(2 if r > 80 else 1):
            a = math.atan2(y - 650, x - 500) + rng.uniform(-1.2, 1.2)
            L = r * rng.uniform(1.4, 1.9)
            p.branch(bez((x, y), (x + math.cos(a) * L * 0.55, y + math.sin(a) * L * 0.55), (x + math.cos(a) * L, y + math.sin(a) * L)),
                     leaf_len=rng.uniform(46, 60), spacing=28, stem_w=1.6, color=rng.choice(["sage", "paleSage"]), color2="deepSage")
    p.lavender(120, 1190, -1.0, 290)
    p.lavender(232, 262, -2.2, 260)
    p.spray(790, 1130, -0.6, 220)
    p.spray(110, 270, -2.5, 140)
    p.berries(392, 142, -1.2, 120)
    p.berries(775, 1095, 0.3, 130)
    p.bud(640, 70, 0.1, 54)
    p.bud(960, 900, -1.3, 50)
    p.mask = None
    for i, (x, y, r, kind, tone) in enumerate(blooms):
        if kind == "rose":
            deep, dark = {"rose": ("deeprose", "burgundy"), "blush": ("rose", "deeprose"), "champagne": ("ochre", "brown")}[tone]
            p.rose(x, y, r, tone=tone, deep=deep, dark=dark, reserve=0)
        elif kind == "peony":
            p.peony(x, y, r, tone=tone, deep="rose", dark="deeprose")
        else:
            p.wildflower(x, y, r, *(("champagne", "ochre", "brown") if i % 2 else ("blush", "rose", "ochre")))
    p.splatter(120, 760, 50, 10, "rose")
    p.splatter(900, 720, 60, 12, "sage")
    p.fade_edges(70)
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
def env_cluster(p, blooms, greens):
    """Paint greenery around a set of blooms, then the blooms on clean paper."""
    p.stencil([(x, y, r * (0.92 if k != "wild" else 0.8)) for x, y, r, k, _ in blooms])
    for g in greens:
        g()
    p.mask = None
    for x, y, r, kind, tone in blooms:
        if kind == "rose":
            deep, dark = {"rose": ("deeprose", "burgundy"), "blush": ("rose", "deeprose"), "champagne": ("ochre", "brown")}[tone]
            p.rose(x, y, r, tone=tone, deep=deep, dark=dark, reserve=0)
        elif kind == "peony":
            p.peony(x, y, r, tone=tone, deep="rose", dark="deeprose")
        else:
            p.wildflower(x, y, r, *(("champagne", "ochre", "brown") if tone == "champagne" else ("blush", "rose", "ochre")))


def env_flap():
    # art sits inside the flap's triangle: top corners and along the diagonals
    p = Painting(1200, 500, 61)
    blooms = []
    greens = []
    for s, x0 in ((1, 0), (-1, 1200)):
        X = lambda u, x0=x0, s=s: x0 + s * u
        blooms += [(X(300), 30, 22, "wild", "blush"), (X(230), 80, 30, "wild", "champagne"), (X(195), 30, 44, "rose", "champagne"),
                   (X(60), 110, 46, "peony", "blush"), (X(120), 46, 74, "rose", "rose")]
        greens += [lambda X=X, s=s: p.branch(bez((X(120), 46), (X(240), 90), (X(380), 180)), leaf_len=58, spacing=30, stem_w=2),
                   lambda X=X, s=s: p.eucalyptus(bez((X(195), 30), (X(330), 20), (X(500), 70)), size=17, spacing=28),
                   lambda X=X, s=s: p.branch(bez((X(60), 110), (X(80), 170), (X(150), 210)), leaf_len=50, spacing=28, stem_w=1.6, color="paleSage", color2="sage"),
                   lambda X=X, s=s: p.berries(X(120), 46, 0.5 if s > 0 else math.pi - 0.5, 120),
                   lambda X=X, s=s: p.spray(X(150), 60, 0.35 if s > 0 else math.pi - 0.35, 170)]
    env_cluster(p, blooms, greens)
    p.save(out("env-flap"), (900, 375), 80)


def env_pocket():
    p = Painting(1200, 800, 62)
    blooms = []
    greens = []
    for s, x0 in ((1, 0), (-1, 1200)):
        X = lambda u, x0=x0, s=s: x0 + s * u
        blooms += [(X(70), 560, 30, "wild", "blush"), (X(330), 770, 26, "wild", "champagne"), (X(250), 760, 48, "rose", "champagne"),
                   (X(60), 640, 58, "peony", "blush"), (X(190), 690, 54, "peony", "blush"), (X(105), 735, 92, "rose", "rose")]
        greens += [lambda X=X, s=s: p.branch(bez((X(105), 735), (X(40), 560), (X(60), 380)), leaf_len=62, spacing=32, stem_w=2),
                   lambda X=X, s=s: p.branch(bez((X(105), 735), (X(280), 790), (X(500), 770)), leaf_len=60, spacing=32, stem_w=2),
                   lambda X=X, s=s: p.eucalyptus(bez((X(190), 690), (X(280), 640), (X(380), 600)), size=18, spacing=28),
                   lambda X=X, s=s: p.branch(bez((X(60), 640), (X(130), 520), (X(110), 450)), leaf_len=50, spacing=28, stem_w=1.6, color="paleSage", color2="sage"),
                   lambda X=X, s=s: p.spray(X(190), 690, -1.1 if s > 0 else -2.0, 150),
                   lambda X=X, s=s: p.berries(X(250), 760, -0.9 if s > 0 else math.pi + 0.9, 110),
                   lambda X=X, s=s: p.lavender(X(105), 735, -0.75 if s > 0 else math.pi + 0.75, 220)]
    env_cluster(p, blooms, greens)
    p.fade_edges(24)
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
    base = hex2("#C48589")[None, None] * 0.92
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


def mango_leaf(p, x, y, a, L, curl=0.25):
    """Long, glossy mango leaf with a drooping, curved spine."""
    ts = np.linspace(0, 1, 9)
    ca, sa = math.cos(a), math.sin(a)
    sp = np.array([(x + ca * t * L - sa * curl * L * t * t, y + sa * t * L + ca * curl * L * t * t) for t in ts])
    w = np.sin(ts * math.pi) ** 0.7 * L * 0.15
    tan = np.gradient(sp, axis=0)
    tan /= np.hypot(tan[:, 0], tan[:, 1])[:, None]
    nor = np.stack([-tan[:, 1], tan[:, 0]], 1)
    for side, dk in ((1, 1.0), (-1, 0.75)):
        out_ = sp + nor * (w[:, None] + 0.8) * side
        inn = sp + nor * 0.8 * side
        p.wash(np.concatenate([inn, out_[::-1][1:-1]]), "sage", 0.72 * dk, "deepSage", var=0.08, depth=3, layers=6, wet=0.7,
               edge=1.1, fade=(x, y, L, 1.2, 0.75))
    p.pen(sp, "olive", max(1.0, L * 0.011), 0.6, wobble=0.1)


def vrat():
    p = Painting(800, 800, 75)
    ground(p, "champagne", "blush", 0.26, 400, 440, 270)
    x0 = 400
    # brass kalash: a full round belly, a pinched neck and a flared lip
    belly_c, br = (x0, 470), 132
    prof = [(0, 0), (40, 4), (52, 20), (38, 40), (34, 58)]
    neck = [(x0 + a, 268 + b) for a, b in prof]
    bowl = [(x0 + math.cos(t) * br * 1.02, belly_c[1] + math.sin(t) * br * 0.95) for t in np.linspace(-1.2, 1.35, 22)]
    base = [(x0 + 70, 598), (x0 + 82, 618), (x0 - 82, 618), (x0 - 70, 598)]
    left = [(2 * x0 - u, v) for u, v in bowl[::-1]]
    left_neck = [(2 * x0 - u, v) for u, v in neck[::-1]]
    poly = np.array(neck + bowl + base + left + left_neck)
    p.wash(poly, "ochre", 0.62, color2="champagne", wet=1.6, layers=9, var=0.015, depth=2, edge=1.5,
           fade=(x0 + 60, 520, 230, 1.35, 0.55))
    # the shine and the shadow side
    p.lift(x0 - 56, 440, 34, 70, 0.5, 60)
    p.blob(x0 + 74, 500, 52, 104, 0.2, "brown", 0.2, wet=10, bleed=4, var=0.2, edge=0.05)
    p.pen(np.array(neck + bowl), "brown", 1.5, 0.55, wobble=0.25)
    p.pen(np.array(left + left_neck), "brown", 1.5, 0.55, wobble=0.25)
    p.pen(base + [base[0]], "brown", 1.3, 0.5)
    # a red thread wound at the neck, with a short tassel
    for k in range(4):
        y = 316 + k * 5
        p.stroke(bez((x0 - 36, y), (x0, y + 7), (x0 + 36, y), n=12), 3.2, "burgundy", 0.75, "deeprose", taper=(0.8, 0.8), wobble=0.2)
    p.stroke(bez((x0 + 30, 330), (x0 + 42, 360), (x0 + 34, 392), n=10), 3, "burgundy", 0.7, taper=(0.8, 0.3))
    # a band of marigolds draped across the belly, and a painted motif under it
    sw = resample(bez((x0 - 126, 418), (x0, 476), (x0 + 126, 418), n=30), 13)
    for i, (x, y) in enumerate(sw):
        marigold(p, x, y, 11.5, *(("blush", "rose") if i % 4 == 2 else ("champagne", "ochre")))
    p.wildflower(x0 - 8, 520, 30, tone="rose", deep="deeprose", centre="ochre")
    for a in (0, 1.57, 3.14, 4.71):
        p.blob(x0 - 8 + math.cos(a) * 46, 520 + math.sin(a) * 46, 4, color="burgundy", density=0.8, sides=6, layers=2, depth=1, wet=0.3)
    # coconut sitting in a crown of mango leaves; the leaves are painted around it
    p.stencil([(x0, 214, 50)], soft=2)
    for a, L, cu in ((-2.75, 150, 0.32), (-2.35, 160, 0.22), (-1.95, 150, 0.12), (-1.2, 150, -0.12), (-0.8, 160, -0.22),
                     (-0.4, 150, -0.32), (-1.57, 130, 0.04), (-2.6, 120, -0.1), (-0.55, 120, 0.1)):
        mango_leaf(p, x0 + math.cos(a) * 30, 262, a, L, cu)
    p.mask = None
    p.blob(x0, 214, 50, 56, 0.1, "brown", 0.7, color2="ochre", wet=1.4, layers=8, var=0.08, edge=1.4, fade=(x0 - 20, 190, 80, 0.6, 1.3))
    for k in range(9):
        u = -38 + k * 9.5
        p.pen(bez((x0 + u * 0.25, 162), (x0 + u * 1.15, 205), (x0 + u * 0.8, 262), n=10), "brown", 0.9, 0.35, wobble=0.35)
    p.stroke(bez((x0 - 20, 150), (x0, 132), (x0 + 22, 150), n=10), 3.2, "burgundy", 0.7, taper=(0.6, 0.6))
    # a small lit diya beside it, petals scattered on the ground
    dx, dy = 600, 610
    p.wash(np.array([(dx - 44, dy - 10), (dx + 44, dy - 10), (dx + 30, dy + 14), (dx - 30, dy + 14)]), "ochre", 0.7, color2="brown",
           wet=0.8, layers=5, var=0.03, depth=1, edge=1.4)
    p.blob(dx, dy - 60, 50, color="champagne", density=0.45, bleed=5, wet=9, edge=0.0)
    p.wash(np.array([(dx, dy - 52), (dx + 9, dy - 32), (dx + 6, dy - 18), (dx, dy - 13), (dx - 6, dy - 18), (dx - 9, dy - 32)]),
           "ochre", 0.95, color2="champagne", wet=0.7, layers=4, var=0.06, depth=2, edge=1.1, fade=(dx, dy - 18, 34, 1.6, .5))
    p.pen(bez((150, 630), (400, 660), (650, 630)), "brown", 1.1, 0.3)
    p.branch(bez((180, 640), (230, 600), (290, 630)), leaf_len=40, spacing=26, stem_w=1.3)
    p.rose(196, 628, 40, tone="blush", deep="rose", dark="deeprose", reserve=0.5)
    for x, y in ((300, 650), (480, 660), (520, 646), (690, 648), (240, 668)):
        p.petal(x, y, p.r.random() * 6.28, 18, 12, "rose" if x % 3 else "ochre", 0.6, layers=3, wet=0.4, depth=2)
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
def tree(p, x, y, s, tone="sage"):
    p.pen([(x, y), (x + 1, y + s * 0.9)], "brown", 1.4, 0.55, wobble=0.2)
    p.blob(x, y, s * 0.62, s * 0.7, 0, tone, 0.62, color2="deepSage", wet=0.9, var=0.3, layers=6, edge=1.4,
           fade=(x - s * 0.3, y - s * 0.3, s * 1.2, 0.7, 1.3))


def house(p, x, y, s, roof="deeprose"):
    p.wash(np.array([(x - s, y), (x + s, y), (x + s, y + s * 1.1), (x - s, y + s * 1.1)]), "champagne", 0.55, color2="blush",
           wet=0.6, layers=4, var=0.03, depth=1, edge=1.2)
    p.wash(np.array([(x - s * 1.25, y + 2), (x, y - s * 0.9), (x + s * 1.25, y + 2)]), roof, 0.6, color2="burgundy",
           wet=0.6, layers=4, var=0.04, depth=1, edge=1.4)
    p.blob(x, y + s * 0.62, s * 0.22, s * 0.32, 0, "brown", 0.5, sides=6, layers=2, depth=1, wet=0.3)


def venue_map():
    p = Painting(1000, 760, 81)
    rng = p.r
    # the sea, laid wet so it blooms into the land
    p.wash(np.array([(-40, -40), (170, -40), (250, 170), (200, 340), (270, 520), (220, 800), (-40, 800)]),
           "paleSage", 0.62, color2="sage", wet=9, bleed=7, layers=9, var=0.1, edge=0.6)
    for i in range(7):
        y = 140 + i * 82 + rng.uniform(-14, 14)
        x = 40 + rng.uniform(0, 90)
        p.stroke(bez((x, y), (x + 30, y - 7), (x + 66, y), n=10), 2.4, "deepSage", 0.4, "sage", taper=(0.2, 0.2), wobble=0.4)
    # land: loose, overlapping washes rather than outlines
    for x, y, rx, ry, t1, t2 in ((560, 200, 260, 170, "champagne", "paleSage"), (780, 540, 230, 170, "paleSage", "champagne"),
                                  (420, 600, 200, 140, "blush", "champagne"), (840, 170, 170, 130, "paleSage", "sage")):
        p.blob(x, y, rx, ry, rng.uniform(-0.3, 0.3), t1, 0.26, color2=t2, bleed=9, wet=10, edge=0.25, var=0.3)
    # roads brushed in one stroke each, the way a hand-drawn map does it
    roads = [bez((230, 80), (480, 220), (590, 390), (960, 450)), bez((280, 700), (420, 480), (530, 390), (760, 30)),
             bez((250, 340), (420, 330), (560, 400), (740, 730)), bez((640, 30), (660, 260), (820, 300), (980, 240))]
    for r_ in roads:
        p.stroke(r_, 13, "champagne", 0.62, "ochre", taper=(0.7, 0.7), wobble=0.9, wet=1.2, edge=1.3)
    # little groves and rooftops dotted across the town
    for x, y, s in ((380, 150, 22), (420, 175, 17), (700, 110, 20), (735, 135, 16), (880, 600, 24), (910, 630, 18),
                    (350, 520, 18), (650, 640, 22), (890, 330, 18), (470, 300, 14), (300, 420, 16)):
        tree(p, x, y, s * 1.7, rng.choice(["sage", "paleSage", "sage"]))
    for x, y, s, roof in ((520, 255, 15, "deeprose"), (545, 268, 11, "ochre"), (690, 470, 14, "rose"), (715, 488, 11, "deeprose"),
                          (430, 420, 13, "ochre"), (800, 380, 12, "rose"), (620, 140, 12, "deeprose")):
        house(p, x, y, s * 1.6, roof)
    # the route, dotted in burgundy, to the wreath that marks The Club
    route = resample(bez((300, 690), (390, 520), (470, 470), (520, 440)), 15)
    for x, y in route[:-2]:
        p.blob(x, y, 3.6, color="burgundy", density=0.8, sides=6, layers=2, depth=1, wet=0.4)
    cx, cy = 590, 392
    p.stencil([(cx, cy, 52)], soft=2)
    p.branch(ring((cx, cy), 84, math.pi * 0.9, math.pi * 2.0, 22), leaf_len=50, spacing=26, stem_w=1.6)
    p.branch(ring((cx, cy), 84, -0.1, math.pi * 0.95, 22), leaf_len=50, spacing=26, stem_w=1.6, color="paleSage", color2="sage")
    p.mask = None
    house(p, cx, cy - 8, 30, "burgundy")
    for a, r, tone in ((-0.6, 40, "rose"), (2.4, 34, "blush"), (1.2, 26, "blush")):
        p.rose(cx + math.cos(a) * 84, cy + math.sin(a) * 84, r, tone=tone, deep="deeprose" if tone == "rose" else "rose", reserve=0.5)
    # a painted compass flower in the corner
    kx, ky = 870, 690
    for a, l, tone in ((-1.57, 46, "burgundy"), (0, 30, "rose"), (1.57, 30, "rose"), (3.14, 30, "rose")):
        p.petal(kx, ky, a, l, 18, tone, 0.75, color2="deeprose", wet=0.6, layers=5, tip=0.7)
    p.blob(kx, ky, 5, color="ochre", density=0.9, sides=7, layers=3, depth=1, wet=0.4)
    p.splatter(600, 380, 200, 16, "rose", 0.45)
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


# ------------------------------------------------------------ envelope paper, washes, small marks
def cotton(name, base, amp, q=80):
    """Heavier cotton paper than paper(): long fibres, a few flecks, gentle cloudiness."""
    r = np.random.default_rng(102)
    S = 512
    n = lambda s: gf(r.random((S, S), dtype=np.float32), s, mode="wrap")
    norm = lambda a: (a - a.mean()) / a.std()
    fib = norm(gf(r.random((S, S)), (0.6, 4.5), mode="wrap")) + norm(gf(r.random((S, S)), (4.5, 0.6), mode="wrap"))
    cloud = norm(n(22) + 0.6 * n(9))
    t = norm(n(0.7)) * 0.5 + fib * 1.0 + cloud * 0.8
    flecks = (r.random((S, S)) > 0.99993).astype(np.float32)
    flecks = gf(flecks, 1.1) * 22
    b = hex2(base) * 255
    a = b[None, None] + t[..., None] * amp - flecks[..., None] * np.array([18, 24, 26])
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB").save(out(name), "WEBP", quality=q, method=6)


def wash_band(name, tone, tone2, w=1600, h=520, seed=301, dens=0.3):
    """A loose horizontal wash that fades to nothing at every edge, for laying between sections."""
    p = Painting(w, h, seed)
    rng = p.r
    for i in range(5):
        x = w * (0.12 + i * 0.19) + rng.uniform(-60, 60)
        y = h * 0.5 + rng.uniform(-40, 40)
        p.blob(x, y, rng.uniform(220, 300), rng.uniform(110, 150), rng.uniform(-0.2, 0.2), tone, dens * rng.uniform(0.7, 1.1),
               color2=tone2, bleed=16, wet=18, edge=0.08, var=0.3)
    p.splatter(w * 0.3, h * 0.5, 140, 10, tone2, 0.35)
    p.splatter(w * 0.75, h * 0.45, 140, 10, tone, 0.35)
    p.fade_edges(int(h * 0.42))
    p.save(out(name), (w // 2, h // 2), 72)


def count_wash():
    p = Painting(1400, 520, 311)
    p.blob(700, 260, 560, 170, 0, "blush", 0.32, color2="champagne", bleed=14, wet=14, edge=0.3, var=0.25)
    p.blob(520, 250, 280, 120, 0.1, "rose", 0.14, bleed=10, wet=12, edge=0.2)
    p.stencil([(700, 260, 470)], soft=30)
    for sx, dirn in ((130, 1), (1270, -1)):
        p.branch(bez((sx, 300), (sx + dirn * 130, 180), (sx + dirn * 320, 170)), leaf_len=78, spacing=34)
        p.eucalyptus(bez((sx, 300), (sx + dirn * 140, 400), (sx + dirn * 300, 400)), size=26, spacing=34)
        p.spray(sx, 300, -1.57 + dirn * 0.7, 140)
    p.mask = None
    for sx, dirn in ((130, 1), (1270, -1)):
        p.rose(sx, 300, 116, reserve=0)
        p.peony(sx + dirn * 120, 390, 70, tone="blush")
        p.wildflower(sx + dirn * 110, 200, 38)
    p.save(out("count-wash"), (1050, 390), 76)


def check_flower():
    p = Painting(200, 200, 321)
    p.wildflower(100, 100, 70, tone="rose", deep="deeprose", centre="ochre", density=0.95)
    p.save(out("check-flower"), (64, 64), 86)


JOBS = dict(corner=lambda: [bouquet(s) for s in BOUQUETS],
            arch=arch, wreath=wreath, sprigs=lambda: (sprig("sprig-a", 15), sprig("sprig-b", 16)), flourish=small_flower,
            garland=garland, vine=vine, flap=env_flap, pocket=env_pocket, liner=env_liner, seal=wax_seal,
            mehendi=mehendi, jaan=jaan, hasta=hasta, reception=reception, vrat=vrat, cocktail=cocktail, map=venue_map,
            ph=lambda: (placeholder("placeholder-a", 201, "a"), placeholder("placeholder-b", 202, "b"), placeholder("placeholder-c", 203, "c"), placeholder("placeholder-plain", 204, "plain")),
            petals=petals, paper=lambda: (paper("paper-ivory", "#F8F3ED", 1.5), paper("paper-white", "#FFFCF8", 1.1), cotton("paper-cotton", "#FBF4EA", 2.6)),
            washes=lambda: (wash_band("wash-gold", "champagne", "ochre", seed=301, dens=0.32), wash_band("wash-rose", "blush", "rose", seed=302),
                            wash_band("wash-dusk", "dusk", "rose", seed=303, dens=0.26), wash_band("wash-sage", "paleSage", "champagne", seed=304)),
            count=count_wash, check=check_flower)

if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    pick = sys.argv[1:] or list(JOBS)
    for k in pick:
        JOBS[k]()
        print("painted", k, flush=True)
