"""Génère hero.svg : fenêtre de terminal macOS avec un chat ASCII animé et la présentation de Sami.

Usage : python3 make_hero.py hero.svg
"""
import math
import sys
from html import escape

W, H = 846, 378
T = 4.0                 # durée d'une boucle d'animation (s)
N = 48                  # images par boucle
CW, LH, FS = 4.32, 7.2, 7.2   # largeur d'un caractère, interligne, taille de police du chat
COLS, ROWS = 66, 24
RAMP = " .:-=+*#%@"

# ---------- chat : formes signées (négatif = dedans), en pixels du panneau ----------

def ellipse(px, py, cx, cy, rx, ry):
    return (math.hypot((px - cx) / rx, (py - cy) / ry) - 1) * min(rx, ry)

def capsule(px, py, ax, ay, bx, by, r):
    vx, vy, wx, wy = bx - ax, by - ay, px - ax, py - ay
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / (vx * vx + vy * vy)))
    return math.hypot(wx - vx * t, wy - vy * t) - r

def triangle(px, py, a, b, c):
    def edge(p, q):
        ex, ey = q[0] - p[0], q[1] - p[1]
        return ((px - p[0]) * ey - (py - p[1]) * ex) / math.hypot(ex, ey)
    d = min(abs(capsule(px, py, *a, *b, 0)), abs(capsule(px, py, *b, *c, 0)), abs(capsule(px, py, *c, *a, 0)))
    e1, e2, e3 = edge(a, b), edge(b, c), edge(c, a)
    inside = (e1 <= 0 and e2 <= 0 and e3 <= 0) or (e1 >= 0 and e2 >= 0 and e3 >= 0)
    return -d if inside else d

def smin(a, b, k):
    h = max(0.0, min(1.0, 0.5 + 0.5 * (b - a) / k))
    return b * (1 - h) + a * h - k * h * (1 - h)

CX = COLS * CW / 2   # axe vertical du chat

def cat_sdf(px, py, sway):
    body = ellipse(px, py, CX, 114, 58, 48)
    head = ellipse(px, py, CX, 52, 44, 34)
    d = smin(body, head, 10)
    for s in (-1, 1):
        d = min(d, triangle(px, py, (CX + s * 44, 48), (CX + s * 40, 2), (CX + s * 8, 28)))   # oreilles
        d = min(d, ellipse(px, py, CX + s * 22, 160, 17, 9))                                 # pattes avant
    # queue : chaîne de capsules qui balance davantage vers le bout
    prev = (CX + 44, 158)
    for i in range(1, 13):
        s = i / 12
        x = CX + 44 + 66 * s + sway * 16 * s ** 3
        y = 158 + 4 * s - 92 * s ** 3
        d = min(d, capsule(px, py, *prev, x, y, 7 - 2 * s))
        prev = (x, y)
    return d

def eyes(px, py, blink):
    ry = 1.2 if blink else 7
    return min(ellipse(px, py, CX - 17, 50, 6, ry), ellipse(px, py, CX + 17, 50, 6, ry))

def cat_frame(k):
    sway = math.sin(2 * math.pi * k / N)
    blink = k in (30, 31)
    rows = []
    LX, LY, LZ = -0.45, -0.6, 0.66          # lumière venant d'en haut à gauche
    for r in range(ROWS):
        line = ""
        for c in range(COLS):
            px, py = (c + 0.5) * CW, (r + 0.5) * LH
            d = cat_sdf(px, py, sway)
            if d > 0:
                line += " "; continue
            if eyes(px, py, blink) < 0 or ellipse(px, py, CX, 65, 4.5, 3) < 0:   # yeux et nez
                line += " "; continue
            e = 1.5                                       # « dôme » : normale tirée du gradient de distance
            gx = cat_sdf(px + e, py, sway) - cat_sdf(px - e, py, sway)
            gy = cat_sdf(px, py + e, sway) - cat_sdf(px, py - e, sway)
            depth = min(1.0, -d / 18)
            nx, ny, nz = gx * (1 - depth), gy * (1 - depth), 2 * e * (0.4 + depth)
            n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
            L = max(0.0, (nx * LX + ny * LY) / n + nz / n * LZ)
            line += RAMP[max(1, min(len(RAMP) - 1, int(L * (len(RAMP) - 1) + 0.5)))]
        rows.append(line)
    return rows

def cls(ch):
    i = RAMP.find(ch)
    return "d" if i < 4 else "m" if i < 7 else "h"

def row_svg(line, x0, y):
    s = line.rstrip()
    start = len(s) - len(s.lstrip())
    s = s.strip()
    if not s:
        return ""
    runs, cur, buf = [], None, ""
    for ch in s:
        c = cls(ch) if ch != " " else (cur or "d")
        if c != cur and buf:
            runs.append((cur, buf)); buf = ""
        cur = c; buf += ch
    runs.append((cur, buf))
    inner = "".join(f'<tspan class="{c}">{escape(t)}</tspan>' for c, t in runs)
    return f'<tspan x="{x0 + start * CW:.1f}" y="{y:.1f}">{inner}</tspan>'

# ---------- SVG ----------

def build():
    ox = 24 + (306 - COLS * CW) / 2        # centré dans le panneau gauche (24 → 330)
    oy = 92 + LH * 0.8                     # entre le nom (y 76) et la ville (y 276)
    frames = []
    for k in range(N):
        body = "".join(row_svg(r, ox, oy + i * LH) for i, r in enumerate(cat_frame(k)))
        frames.append(f'<text class="f{" f0" if k == 0 else ""}" style="animation-delay:{-(T - k * T / N):.3f}s">{body}</text>')

    def t(x, y, text, fill, size=13, bold=False, a="", anchor=None):
        w = ' font-weight="700"' if bold else ""
        an = f' text-anchor="{anchor}"' if anchor else ""
        return f'<g class="a {a}"><text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{w}{an}>{escape(text)}</text></g>'

    X = 354
    parts = [
        # barre de titre macOS : feux tricolores et répertoire courant
        '<g class="a a0"><path d="M5 12a12 12 0 0 1 12-12h812a12 12 0 0 1 12 12v18H5z" fill="#161616"/>'
        '<circle cx="25" cy="15" r="5.5" fill="#ff5f57"/><circle cx="43" cy="15" r="5.5" fill="#febc2e"/>'
        '<circle cx="61" cy="15" r="5.5" fill="#28c840"/>'
        '<text x="423" y="19.5" font-size="12" fill="#6b6b6b" text-anchor="middle">~/sami-krm</text></g>',
        '<rect x="24" y="46" width="798" height="248" rx="8" fill="none" stroke="#3a3a3a" stroke-width="1.2" pathLength="1" class="dr"/>',
        '<g class="a a1"><rect x="38" y="38" width="76" height="16" fill="#0c0c0c"/>'
        '<text x="45" y="50.5" font-size="13" fill="#a1a1a1">sami-krm</text></g>',
        '<path class="dv" d="M330 68V272" stroke="#3a3a3a" stroke-width="1.2"/>',
        f'<g class="cat">{"".join(frames)}</g>',
        t(177, 76, "Sami Krim", "#ededed", 14.5, True, "a2", "middle"),
        t(177, 276, "Montpellier, France", "#6b6b6b", 12.5, False, "a3", "middle"),
        t(X, 80, "À propos", "#ededed", 13, True, "a4"),
        t(X, 102, "Étudiant en BUT Informatique à l'IUT de Montpellier.", "#a1a1a1", 12.5, False, "a5"),
        t(X, 122, "Je crée des apps mobiles, macOS et web.", "#a1a1a1", 12.5, False, "a5"),
        '<path class="a a6" d="M354 136H798" stroke="#3a3a3a" stroke-width="1"/>',
        t(X, 164, "Stack", "#ededed", 13, True, "a6"),
        t(X, 186, "Swift · SwiftUI · TypeScript · React Native · Python", "#a1a1a1", 12.5, False, "a7"),
        t(X, 214, "Projets", "#ededed", 13, True, "a8"),
        t(X, 236, "Notchlet · HabilleToi · WebLooping · MasterBait", "#a1a1a1", 12.5, False, "a9"),
        # zone de saisie
        '<g class="a a10"><rect x="24" y="308" width="798" height="38" rx="6" fill="none" stroke="#575757" stroke-width="1.2"/>'
        '<text x="38" y="332" font-size="13.5" fill="#ededed">&gt;</text>'
        '<rect class="bl" x="56" y="320" width="8.1" height="16" fill="#ededed"/>'
        '<text x="68" y="332" font-size="13.5" fill="#6b6b6b">Essaie « git clone github.com/sami-krm/Notchlet »</text></g>',
        t(38, 364, "? pour les raccourcis", "#6b6b6b", 12, False, "a11"),
    ]
    delays = "".join(f".a{i}{{animation-delay:{0.1 + i * 0.12:.2f}s}}" for i in range(12))
    style = (
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;white-space:pre}"
        ".d{fill:#4d4d4d}.m{fill:#9b9b9b}.h{fill:#f4f4f4}"
        f".f{{font-size:{FS}px;opacity:0;animation:fr {T}s step-end infinite}}.f0{{opacity:1}}"
        f"@keyframes fr{{0%{{opacity:1}}{100 / N:.3f}%{{opacity:0}}100%{{opacity:0}}}}"
        ".cat{opacity:0;animation:in .9s ease-out .5s forwards}@keyframes in{to{opacity:1}}"
        ".dr{stroke-dasharray:1;stroke-dashoffset:1;animation:dr .9s cubic-bezier(.65,0,.35,1) .1s forwards}"
        "@keyframes dr{to{stroke-dashoffset:0}}"
        ".a{opacity:0;animation:up .5s cubic-bezier(.2,.8,.2,1) forwards}"
        "@keyframes up{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}" + delays +
        ".bl{animation:bl 1.05s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        ".dv{transform-origin:330px 170px;transform:scaleY(0);animation:dv .6s cubic-bezier(.2,.8,.2,1) .6s forwards}"
        "@keyframes dv{to{transform:none}}"
        "@media (prefers-reduced-motion:reduce){.a,.cat,.dv,.dr{animation:none;opacity:1;transform:none;stroke-dashoffset:0}.f,.bl{animation:none}}"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        'aria-label="Fenêtre de terminal macOS de Sami Krim, Montpellier, France, avec un chat ASCII animé. '
        'Étudiant en BUT Informatique, apps mobiles, macOS et web. Stack : Swift, SwiftUI, TypeScript, React Native, Python.">'
        f"<title>Sami Krim</title><style>{style}</style>"
        '<defs><clipPath id="win"><rect x="5" y="0" width="836" height="374" rx="12"/></clipPath></defs>'
        '<rect x="5" y="0" width="836" height="374" rx="12" fill="#0c0c0c"/>'
        f'<g clip-path="url(#win)">{"".join(parts)}</g></svg>'
    )

if __name__ == "__main__":
    svg = build()
    assert svg.count('class="f') == N and "<script" not in svg
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{len(svg) // 1024} Ko")
