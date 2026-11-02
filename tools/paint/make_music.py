#!/usr/bin/env python3
"""Synthesises a short, gentle music-box loop as a stand-in background track."""
import numpy as np, subprocess, wave, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SR = 44100
BEAT = 0.46
A4 = 440.0
f = lambda m: A4 * 2 ** ((m - 69) / 12)
CH = [[50, 57, 62, 66, 69, 74], [47, 54, 59, 62, 66, 71], [43, 50, 55, 59, 62, 67], [45, 52, 57, 61, 64, 69]]
PAT = [0, 2, 3, 4, 5, 4, 3, 2]
MEL = [[None, None, 78, None, 76, None, 74, None], [None, None, 74, None, 73, None, 71, None],
       [None, None, 71, None, 74, None, 79, None], [None, 78, None, 76, None, 73, None, None]]
bars = 8
N = int(SR * BEAT * 8 * bars) + SR * 4
L = np.zeros(N); R = np.zeros(N)
def tone(buf, t, freq, amp, dec):
    n = int(SR * dec * 4); i = max(0, int(t * SR))
    x = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * x) + .32 * np.sin(4 * np.pi * freq * x) * np.exp(-x * 5) + .1 * np.sin(2 * np.pi * freq * 4.2 * x) * np.exp(-x * 14)
    s *= np.exp(-x / dec) * np.minimum(x / .004, 1) * amp
    e = min(i + n, N); buf[i:e] += s[: e - i]
r = np.random.default_rng(4); t = 0.0
for bar in range(bars):
    c = CH[bar % 4]; m = MEL[bar % 4]
    for b in range(8):
        tt = t + b * BEAT + r.normal(0, .005)
        n = c[PAT[b]]; pan = .5 + .25 * np.sin(b)
        a = .15 * r.uniform(.8, 1.05)
        tone(L, tt, f(n), a * (1 - pan), .9); tone(R, tt, f(n), a * pan, .9)
        if m[b] and bar >= 2:
            tone(L, tt, f(m[b]), .17, 1.2); tone(R, tt, f(m[b]), .15, 1.2)
    t += 8 * BEAT
ir = np.exp(-np.arange(int(SR * 2.2)) / (SR * .55)) * r.normal(0, 1, int(SR * 2.2)) * .02
wet = lambda x: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
Lw, Rw = L + wet(L) * .9, R + wet(R) * .9
end = int(t * SR); Lw, Rw = Lw[:end], Rw[:end]
fade = int(SR * 1.5); env = np.ones(end); env[:int(SR*.05)] = np.linspace(0, 1, int(SR*.05)); env[-fade:] = np.linspace(1, 0, fade)
pk = max(abs(Lw).max(), abs(Rw).max())
pcm = (np.stack([Lw, Rw], 1) * env[:, None] / pk * .7 * 32767).astype(np.int16)
tmp = "/tmp/bg.wav" if len(sys.argv) < 2 else sys.argv[1]
with wave.open(tmp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "80k", os.path.join(ROOT, "src/assets/music/background.mp3")], check=True)
