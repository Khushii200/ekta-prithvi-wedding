"""A small watercolor engine.

Pigment is simulated with the Beer-Lambert law: every wash multiplies the light
passing through the paper, so overlapping washes glaze the way real paint does.
Edges pool darker, pigment granulates into the paper grain, and every shape is
built from many randomly deformed layers, which gives the soft imperfect edge.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter as gf


def hex2(c):
    c = c.lstrip("#")
    return np.array([int(c[i : i + 2], 16) / 255 for i in (0, 2, 4)])


PAL = {
    "blush": "#EDD3CB",
    "rose": "#D9A6A2",
    "deeprose": "#BC7B7C",
    "burgundy": "#813F4B",
    "wine": "#6B3240",
    "sage": "#A7AD91",
    "paleSage": "#C8CCB6",
    "deepSage": "#7D8869",
    "olive": "#5F6A50",
    "champagne": "#D9C5A7",
    "ochre": "#C8A36E",
    "brown": "#6E5448",
    "dusk": "#A98B93",
}


def col(name):
    return hex2(PAL.get(name, name))


class Painting:
    def __init__(self, w, h, seed=1):
        self.w, self.h = w, h
        self.r = np.random.default_rng(seed)
        self.T = np.ones((h, w, 3), dtype=np.float32)
        r = self.r
        n = lambda s: gf(r.random((h, w), dtype=np.float32), s, mode="wrap")
        norm = lambda a: (a - a.min()) / (a.max() - a.min() + 1e-6)
        self.low = norm(n(38) + 0.5 * n(14))
        self.mix = norm(n(26) + 0.4 * n(8))
        # paper grain: fine tooth, used for granulation and dry-brush
        self.grain = norm(n(0.8) + 0.8 * n(1.8))
        # very slow variation for big washes, so skies don't go blotchy
        self.vlow = norm(n(150) + 0.35 * n(60))
        self.vmix = norm(n(120) + 0.3 * n(50))

    # ---- shape helpers -------------------------------------------------
    def _deform(self, pts, depth, var):
        r = self.r
        pts = np.asarray(pts, dtype=np.float32)
        for _ in range(depth):
            nxt = np.roll(pts, -1, axis=0)
            seg = nxt - pts
            ln = np.hypot(seg[:, 0], seg[:, 1])[:, None]
            nor = np.stack([-seg[:, 1], seg[:, 0]], 1)
            mid = (pts + nxt) / 2 + nor * r.normal(0, var, (len(pts), 1)) * 0.5
            mid += r.normal(0, 1, mid.shape) * ln * var * 0.12
            out = np.empty((len(pts) * 2, 2), dtype=np.float32)
            out[0::2], out[1::2] = pts, mid
            pts = out
            var *= 0.82
        return pts

    def wash(self, pts, color, density=0.6, color2=None, edge=0.9, wet=1.2, layers=10,
             var=0.34, depth=4, fade=None, grain=0.35, bleed=0.0):
        """Lay one wash of pigment inside a polygon.

        fade = (x, y, radius, near, far): density multiplier by distance from a point.
        bleed > 0 lets the wash feather out unevenly, as if laid on damp paper.
        """
        pts = np.asarray(pts, dtype=np.float32)
        pad = int(14 + wet * 3 + bleed * 3 + np.ptp(pts, axis=0).max() * var * 0.45)
        x0 = max(int(pts[:, 0].min()) - pad, 0)
        y0 = max(int(pts[:, 1].min()) - pad, 0)
        x1 = min(int(pts[:, 0].max()) + pad, self.w)
        y1 = min(int(pts[:, 1].max()) + pad, self.h)
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        w, h = x1 - x0, y1 - y0
        mask = np.zeros((h, w), dtype=np.float32)
        base = self._deform(pts, 1, var)
        for _ in range(layers):
            p = self._deform(base, depth, var) - (x0, y0)
            im = Image.new("L", (w, h), 0)
            ImageDraw.Draw(im).polygon([tuple(q) for q in p], fill=255)
            mask += np.asarray(im, dtype=np.float32) / 255
        mask /= layers
        large = max(w, h) > 300
        low = (self.vlow if large else self.low)[y0:y1, x0:x1]
        grainf = self.grain[y0:y1, x0:x1]
        mixf = (self.vmix if large else self.mix)[y0:y1, x0:x1]
        m = gf(mask, wet) if wet > 0 else mask
        if bleed > 0:
            soft = gf(mask, bleed * 3)
            m = np.clip(m * (1 - 0.6 * low) + soft * (0.25 + 1.1 * low), 0, 1)
        pool = np.clip(m - gf(m, max(3.0, 2.5 + wet * 1.5)), 0, 1)
        d = m * ((0.82 + 0.36 * low) if large else (0.55 + 0.9 * low)) + pool * edge * 1.6
        d *= 1 + grain * (grainf - 0.5) * 1.6
        if fade is not None:
            fx, fy, rad, near, far = fade
            yy, xx = np.mgrid[y0:y1, x0:x1]
            t = np.clip(np.hypot(xx - fx, yy - fy) / rad, 0, 1)
            t = t * t * (3 - 2 * t)
            d *= near + (far - near) * t
        d = (d * density)[..., None]
        A = -np.log(np.clip(color if isinstance(color, np.ndarray) else col(color), 0.02, 0.995))
        if color2 is not None:
            A2 = -np.log(np.clip(col(color2) if not isinstance(color2, np.ndarray) else color2, 0.02, 0.995))
            k = (np.clip(mixf * 1.1 - 0.05, 0, 1) if large else np.clip((mixf - 0.32) * 2.6, 0, 1))[..., None]
            ab = A * (1 - k) + A2 * k
        else:
            ab = A
        self.T[y0:y1, x0:x1] *= np.exp(-d * ab)

    # ---- marks ---------------------------------------------------------
    def stroke(self, path, width, color, density=0.8, color2=None, taper=(0.25, 0.1), wobble=0.5,
               wet=0.6, edge=0.4, layers=4, grain=0.5):
        """A pressure-sensitive brush stroke along a polyline."""
        p = resample(np.asarray(path, dtype=np.float32), max(8, int(arclen(path) / 5)))
        n = len(p)
        t = np.linspace(0, 1, n)
        pres = np.minimum(taper[0] + (1 - taper[0]) * np.clip(t * 6, 0, 1),
                          taper[1] + (1 - taper[1]) * np.clip((1 - t) * 3.4, 0, 1))
        wig = gf(self.r.normal(0, 1, n), 2) * 1.8
        pres = pres * (1 + 0.28 * wig)
        tan = np.gradient(p, axis=0)
        tan /= np.hypot(tan[:, 0], tan[:, 1])[:, None] + 1e-6
        nor = np.stack([-tan[:, 1], tan[:, 0]], 1)
        off = gf(self.r.normal(0, 1, n), 3) * wobble * 2.2
        c = p + nor * off[:, None]
        hw = (width * pres / 2)[:, None]
        poly = np.concatenate([c + nor * hw, (c - nor * hw)[::-1]])
        self.wash(poly, color, density, color2, edge=edge, wet=wet, layers=layers, var=0.05, depth=1, grain=grain)

    def pen(self, path, color="burgundy", width=1.6, density=1.0, wobble=0.5):
        self.stroke(path, width, color, density, taper=(0.5, 0.3), wobble=wobble, wet=0.35, edge=0, layers=2, grain=0.25)

    def blob(self, x, y, rx, ry=None, angle=0, color="rose", density=0.5, sides=9, **kw):
        ry = rx if ry is None else ry
        a = np.linspace(0, 2 * math.pi, sides, endpoint=False)
        px, py = rx * np.cos(a), ry * np.sin(a)
        ca, sa = math.cos(angle), math.sin(angle)
        pts = np.stack([x + px * ca - py * sa, y + px * sa + py * ca], 1)
        self.wash(pts, color, density, **kw)

    def petal(self, x, y, angle, length, width, color="rose", density=0.5, color2=None, tip=0.55, **kw):
        """Teardrop from base (x, y) pointing along angle. Pigment gathers at the base."""
        ts = np.linspace(0, 1, 7)
        prof = np.sin(ts * math.pi) ** 0.8 * (0.72 + 0.5 * ts)
        ca, sa = math.cos(angle), math.sin(angle)
        L = [(x + ca * t * length - sa * width * .5 * w, y + sa * t * length + ca * width * .5 * w) for t, w in zip(ts, prof)]
        R = [(x + ca * t * length + sa * width * .5 * w, y + sa * t * length - ca * width * .5 * w) for t, w in zip(ts, prof)]
        pts = np.array(L + R[::-1][1:-1])
        kw.setdefault("fade", (x, y, length * 1.1, 1.35, tip))
        kw.setdefault("var", 0.2)
        self.wash(pts, color, density, color2, **kw)

    def splatter(self, x, y, spread, n=14, color="rose", density=0.55, size=(0.8, 3.2)):
        for _ in range(n):
            a = self.r.random() * math.tau
            d = abs(self.r.normal(0, spread))
            s = self.r.uniform(*size)
            self.blob(x + math.cos(a) * d, y + math.sin(a) * d, s, color=color, density=density,
                      sides=6, layers=3, depth=2, wet=0.4, var=0.3, edge=1.2)

    # ---- botanicals ----------------------------------------------------
    def leaf(self, x, y, angle, length, width=None, color="sage", color2="deepSage", density=0.62, vein=True):
        """Two brushed halves with a sliver of dry paper left along the midrib."""
        width = width or length * 0.36
        ca, sa = math.cos(angle), math.sin(angle)
        bend = self.r.uniform(-0.14, 0.14) * length
        ts = np.linspace(0, 1, 7)
        spine = np.array([(x + ca * t * length - sa * bend * math.sin(t * math.pi),
                           y + sa * t * length + ca * bend * math.sin(t * math.pi)) for t in ts])
        for side, dk in ((1, 1.0), (-1, self.r.uniform(0.62, 0.95))):
            w = np.sin(ts * math.pi) ** 0.75 * width * 0.5 * side
            gap = 0.9 * side
            out = spine + np.stack([-sa * (w + gap), ca * (w + gap)], 1)
            inn = spine + np.stack([-sa * gap * np.ones(7), ca * gap * np.ones(7)], 1)
            pts = np.concatenate([inn, out[::-1][1:-1]])
            self.wash(pts, color, density * dk, color2, var=0.12, depth=3, layers=6, wet=0.7, edge=0.9,
                      fade=(x, y, length, 1.25, 0.72))
        if vein:
            self.pen(spine, color2, width=max(0.8, length * 0.012), density=0.55, wobble=0.15)

    def stem(self, path, width=3.2, color="deepSage", color2="olive", density=0.85):
        self.stroke(path, width, color, density, color2, taper=(0.9, 0.2), wobble=0.35)

    def branch(self, path, leaf_len=44, spacing=38, color="sage", color2="deepSage", stem_w=2.6, spread=0.72,
               density=0.6, terminal=True):
        path = np.asarray(path, dtype=np.float32)
        self.stem(path, stem_w)
        n = max(2, int(arclen(path) / spacing))
        p = resample(path, n + 2)
        tan = np.gradient(p, axis=0)
        for i in range(1, n + 1):
            f = 1 - (i / (n + 2)) * 0.5
            ang = math.atan2(tan[i][1], tan[i][0])
            side = 1 if i % 2 else -1
            self.leaf(p[i][0], p[i][1], ang + side * (spread + self.r.uniform(-0.18, 0.18)),
                      leaf_len * f * self.r.uniform(0.82, 1.12), color=color, color2=color2, density=density)
        if terminal:
            ang = math.atan2(tan[-1][1], tan[-1][0])
            self.leaf(p[-1][0], p[-1][1], ang, leaf_len * 0.72, color=color, color2=color2, density=density)

    def eucalyptus(self, path, size=22, spacing=30, color="paleSage", color2="sage", density=0.7):
        path = np.asarray(path, dtype=np.float32)
        self.stem(path, 2.0, "dusk", "deepSage", 0.7)
        n = max(2, int(arclen(path) / spacing))
        p = resample(path, n + 1)
        tan = np.gradient(p, axis=0)
        for i in range(1, n + 1):
            ang = math.atan2(tan[i][1], tan[i][0])
            sc = 1 - 0.55 * i / (n + 1)
            for side in (1, -1):
                a = ang + side * 1.25
                s = size * sc * self.r.uniform(0.85, 1.15)
                self.blob(p[i][0] + math.cos(a) * s * 0.9, p[i][1] + math.sin(a) * s * 0.9, s, s * 0.74, a,
                          color, density * self.r.uniform(0.7, 1.15), color2=color2, wet=0.8, var=0.14, layers=6, edge=1.1)

    def lift(self, x, y, rx, ry=None, strength=1.0, soft=2.0):
        """Reserve paper: the painter works around whatever comes next."""
        ry = rx if ry is None else ry
        x0, x1 = max(int(x - rx - 8), 0), min(int(x + rx + 8), self.w)
        y0, y1 = max(int(y - ry - 8), 0), min(int(y + ry + 8), self.h)
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot((xx - x) / rx, (yy - y) / ry)
        m = np.clip((1 - d) * max(rx, ry) / soft, 0, 1)[..., None] * strength
        self.T[y0:y1, x0:x1] = self.T[y0:y1, x0:x1] ** (1 - m)

    def rose(self, x, y, r, tone="rose", deep="deeprose", dark="burgundy", density=1.0):
        rng = self.r
        spin = rng.random() * math.tau
        self.lift(x, y, r * 0.92, r * 0.88)
        # pale ground wash, wet edge
        self.blob(x, y, r * 0.95, r * 0.9, spin, "blush", 0.62 * density, color2=tone, wet=2.2, bleed=1.2, var=0.2, edge=0.7)
        # outer petals: broad, pale, each leaving a dry rim where it meets the next
        n = 6
        for i in range(n):
            a = spin + i / n * math.tau + rng.uniform(-0.14, 0.14)
            px, py = x + math.cos(a) * r * 0.52, y + math.sin(a) * r * 0.52
            self.blob(px, py, r * 0.47, r * 0.36, a + math.pi / 2, tone, 0.2 * density, color2="blush",
                      wet=0.8, var=0.12, layers=7, edge=2.0, fade=(x, y, r, 1.5, 0.5))
        # cupped middle petals
        n = 5
        for i in range(n):
            a = spin + 0.6 + i / n * math.tau + rng.uniform(-0.18, 0.18)
            px, py = x + math.cos(a) * r * 0.31, y + math.sin(a) * r * 0.31
            self.blob(px, py, r * 0.31, r * 0.19, a + math.pi / 2, tone, 0.26 * density, color2=deep,
                      wet=0.7, var=0.12, layers=6, edge=2.0, fade=(x, y, r * 0.55, 1.5, 0.55))
        # ordered crescents, one ring at a time, that describe the folds
        for ring, (rad, cnt, w) in enumerate(((0.72, 4, 0.05), (0.48, 4, 0.06), (0.3, 3, 0.065))):
            a0 = spin + ring * 0.9
            for i in range(cnt):
                aa = a0 + i / cnt * math.tau + rng.uniform(-0.2, 0.2)
                sweep = rng.uniform(0.75, 1.15)
                rr = r * rad * rng.uniform(0.95, 1.05)
                arc = [(x + math.cos(aa + s) * rr, y + math.sin(aa + s) * rr * 0.94) for s in np.linspace(0, sweep, 9)]
                self.stroke(arc, r * w, deep, (0.26 + ring * 0.09) * density, taper=(0.08, 0.05), wobble=0.3, wet=0.9, edge=0.8)
        # heart of the rose
        self.blob(x, y, r * 0.15, r * 0.13, spin, deep, 0.42 * density, color2=dark, wet=1.0, var=0.2)
        sp = [(x + math.cos(spin + t * 1.5) * r * (0.03 + 0.021 * t), y + math.sin(spin + t * 1.5) * r * (0.03 + 0.021 * t)) for t in np.linspace(0, 5, 24)]
        self.stroke(sp, r * 0.03, dark, 0.42 * density, taper=(0.5, 0.2), wobble=0.15, wet=0.6)

    def wildflower(self, x, y, r, tone="blush", deep="rose", centre="ochre", petals=5, density=0.75):
        rng = self.r
        spin = rng.random() * math.tau
        self.lift(x, y, r * 0.8, r * 0.8, 0.85)
        for i in range(petals):
            a = spin + i / petals * math.tau + rng.uniform(-0.12, 0.12)
            self.petal(x, y, a, r * rng.uniform(0.9, 1.08), r * 0.8, tone, density, color2=deep, wet=0.8, layers=6, edge=1.2, tip=0.65)
        self.blob(x, y, r * 0.17, color=centre, density=1.0, wet=0.5, layers=4)
        self.splatter(x, y, r * 0.12, 6, "brown", 0.7, (0.5, 1.2))

    def bud(self, x, y, angle, s, tone="rose", deep="deeprose"):
        self.petal(x, y, angle, s, s * 0.62, tone, 0.75, color2=deep, wet=0.7, layers=6, tip=0.6)
        for d in (-0.5, 0.5):
            self.leaf(x, y, angle + d, s * 0.5, s * 0.17, density=0.7, vein=False)

    def spray(self, x, y, angle, length, tone="champagne", dots=14, fan=0.8):
        """Cow-parsley: hair-thin stems ending in dots."""
        rng = self.r
        tipx, tipy = x + math.cos(angle) * length, y + math.sin(angle) * length
        self.pen([(x, y), ((x + tipx) / 2 + rng.uniform(-6, 6), (y + tipy) / 2 + rng.uniform(-6, 6)), (tipx, tipy)], "deepSage", 1.4, 0.8)
        for _ in range(dots):
            a = angle + rng.uniform(-fan, fan)
            l = length * rng.uniform(0.18, 0.46)
            ex, ey = tipx + math.cos(a) * l, tipy + math.sin(a) * l
            self.pen([(tipx, tipy), (ex, ey)], "deepSage", 0.9, 0.55, wobble=0.1)
            self.blob(ex, ey, rng.uniform(1.8, 4.2), color=tone, density=0.95, sides=6, layers=4, depth=2, wet=0.4, color2="ochre")

    def lavender(self, x, y, angle, length, tone="dusk"):
        tipx, tipy = x + math.cos(angle) * length, y + math.sin(angle) * length
        self.stem([(x, y), (tipx, tipy)], 1.6)
        for t in np.linspace(0.55, 1.0, 9):
            px, py = x + (tipx - x) * t, y + (tipy - y) * t
            s = length * 0.045 * (1.25 - t * 0.5)
            for side in (-1, 1):
                self.blob(px + side * math.cos(angle + 1.57) * s * 0.7, py + side * math.sin(angle + 1.57) * s * 0.7,
                          s, s * 0.7, angle + side, tone, 0.8, color2="rose", wet=0.6, layers=4, sides=7)

    # ---- output --------------------------------------------------------
    def rgba(self):
        """Convert transmittance to straight-alpha RGBA over white paper."""
        T = np.clip(self.T, 0, 1)
        a = 1 - T.min(axis=2)
        rgb = np.where(a[..., None] > 1e-4, (T - (1 - a[..., None])) / np.maximum(a[..., None], 1e-4), 1.0)
        out = np.dstack([np.clip(rgb, 0, 1), a])
        return Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA")

    def save(self, path, size=None, quality=82):
        im = self.rgba()
        if size:
            im = im.resize(size, Image.LANCZOS)
        im.save(path, "WEBP", quality=quality, alpha_quality=85, method=6)


def arclen(p):
    p = np.asarray(p, dtype=np.float32)
    return float(np.hypot(*np.diff(p, axis=0).T).sum())


def resample(p, n):
    p = np.asarray(p, dtype=np.float32)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    t = np.linspace(0, d[-1], n)
    return np.stack([np.interp(t, d, p[:, 0]), np.interp(t, d, p[:, 1])], 1)


def bez(p0, p1, p2, p3=None, n=30):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = map(lambda v: np.array(v, dtype=np.float32), (p0, p1, p2))
    if p3 is None:
        return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2
    p3 = np.array(p3, dtype=np.float32)
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3
