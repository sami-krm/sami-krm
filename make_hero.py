"""Génère hero.svg : fenêtre de terminal avec un tore ASCII animé et la présentation de Sami."""
import math
import sys
from html import escape

W, H = 846, 378
T = 4.0          # durée d'un tour du tore (s)
N = 48           # images par tour
COLS, ROWS = 44, 24
RAMP = ".,-~:;=!*#$@"

def torus_frame(a, b):
    """Algorithme classique du « donut » : renvoie ROWS lignes de COLS caractères."""
    out = [[" "] * COLS for _ in range(ROWS)]
    zb = [[0.0] * COLS for _ in range(ROWS)]
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    R1, R2, K2 = 1.0, 2.0, 5.0
    # projection max mesurée ≈ 0.75 sur chaque axe : on remplit 95 % de la hauteur,
    # et x est étiré du rapport interligne / largeur de caractère pour garder un tore rond
    K1y = ROWS / 2 * 0.95 / 0.75
    K1x = K1y * 9.6 / 5.76
    th = 0.0
    while th < 2 * math.pi:
        ct, st = math.cos(th), math.sin(th)
        ph = 0.0
        while ph < 2 * math.pi:
            cp, sp = math.cos(ph), math.sin(ph)
            cx, cy = R2 + R1 * ct, R1 * st
            x = cx * (cb * cp + sa * sb * sp) - cy * ca * sb
            y = cx * (sb * cp - sa * cb * sp) + cy * ca * cb
            z = K2 + ca * cx * sp + cy * sa
            ooz = 1 / z
            xp, yp = int(COLS / 2 + K1x * ooz * x), int(ROWS / 2 - K1y * ooz * y)
            L = cp * ct * sb - ca * ct * sp - sa * st + cb * (ca * st - ct * sa * sp)
            if 0 <= xp < COLS and 0 <= yp < ROWS and L > 0 and ooz > zb[yp][xp]:
                zb[yp][xp] = ooz
                out[yp][xp] = RAMP[min(int(L * 8), len(RAMP) - 1)]
            ph += 0.02
        th += 0.07
    return ["".join(r) for r in out]

def cls(ch):
    i = RAMP.find(ch)
    return "d" if i < 4 else "m" if i < 8 else "h"

def row_svg(line, x0, y, cw):
    """Une ligne ASCII : tspans colorés, positionnés au premier caractère non vide."""
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
    return f'<tspan x="{x0 + start * cw:.1f}" y="{y:.1f}">{inner}</tspan>'

def build():
    fs, cw, lh = 9.6, 5.76, 9.6          # police du tore, largeur d'un caractère (0.6 em), interligne
    ox = 24 + (306 - COLS * cw) / 2       # centré dans le panneau gauche (24 → 330)
    oy = 46 + (248 - ROWS * lh) / 2 + lh * 0.8
    frames = []
    for k in range(N):
        a = 2 * math.pi * k / N
        rows = torus_frame(a + 0.6, a * 0.5 + 0.3)
        body = "".join(row_svg(r, ox, oy + i * lh, cw) for i, r in enumerate(rows))
        delay = -(T - k * T / N)
        frames.append(f'<text class="f{" f0" if k == 0 else ""}" style="animation-delay:{delay:.3f}s">{body}</text>')

    def t(x, y, text, c, size=13, weight=500, a=None):
        anim = f' class="a {a}"' if a else ""
        return f'<g{anim}><text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{c}">{escape(text)}</text></g>'

    X = 352
    right = [
        t(X, 84, "Salut, moi c'est Sami", "#f4f4f4", 17, 700, "a1"),
        t(X, 106, "Étudiant en BUT Informatique · IUT de Montpellier", "#9b9b9b", 12, 500, "a2"),
        t(X, 124, "Ancien élève en PEIP · Montpellier, France", "#9b9b9b", 12, 500, "a2"),
        t(X, 156, "À propos", "#d97757", 12.5, 700, "a3"),
        t(X, 175, "Je crée des apps mobiles, macOS et web,", "#ededed", 12.5, 500, "a3"),
        t(X, 193, "de l'idée au design jusqu'à la mise en ligne.", "#ededed", 12.5, 500, "a3"),
        t(X, 224, "Stack", "#d97757", 12.5, 700, "a4"),
        t(X, 243, "Swift · SwiftUI · TypeScript · React Native · Expo", "#ededed", 12, 500, "a4"),
        t(X, 261, "Python · JavaScript · SQL · Supabase", "#ededed", 12, 500, "a4"),
    ]
    prompt = (
        '<g class="a a5"><text x="30" y="330" font-size="13.5" fill="#d97757">❯</text>'
        '<text x="48" y="330" font-size="13.5" fill="#ededed">Notchlet · HabilleToi · WebLooping · MasterBait</text>'
        '<rect class="bl" x="444" y="319" width="8" height="15" fill="#ededed"/></g>'
        '<g class="a a6"><text x="30" y="358" font-size="11.5" fill="#4d4d4d">github.com/sami-krm · projets épinglés ci-dessous ↓</text></g>'
    )
    style = (
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;white-space:pre}"
        ".d{fill:#4d4d4d}.m{fill:#9b9b9b}.h{fill:#f4f4f4}"
        f".f{{font-size:{fs}px;opacity:0;animation:fr {T}s step-end infinite}}.f0{{opacity:1}}"
        f"@keyframes fr{{0%{{opacity:1}}{100 / N:.3f}%{{opacity:0}}100%{{opacity:0}}}}"
        ".tor{opacity:0;animation:in .9s ease-out .9s forwards}"
        "@keyframes in{to{opacity:1}}"
        ".dr{stroke-dasharray:1;stroke-dashoffset:1;animation:dr .9s cubic-bezier(.65,0,.35,1) .1s forwards}"
        "@keyframes dr{to{stroke-dashoffset:0}}"
        ".a{opacity:0;animation:up .5s cubic-bezier(.2,.8,.2,1) forwards}"
        "@keyframes up{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
        ".a0{animation-delay:.7s}.a1{animation-delay:1.0s}.a2{animation-delay:1.2s}.a3{animation-delay:1.4s}"
        ".a4{animation-delay:1.6s}.a5{animation-delay:1.9s}.a6{animation-delay:2.1s}"
        ".bl{animation:bl 1.05s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        ".dv{transform-origin:330px 170px;transform:scaleY(0);animation:dv .6s cubic-bezier(.2,.8,.2,1) .8s forwards}"
        "@keyframes dv{to{transform:none}}"
        "@media (prefers-reduced-motion:reduce){.a,.tor,.dv,.dr{animation:none;opacity:1;transform:none;stroke-dashoffset:0}.f{animation:none}.bl{animation:none}}"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Terminal de bienvenue de Sami, étudiant en BUT Informatique à Montpellier, avec un tore ASCII qui tourne. '
        f'Apps mobiles, macOS et web. Stack : Swift, SwiftUI, TypeScript, React Native, Expo, Python, JavaScript, SQL, Supabase.">'
        f"<title>Sami · sami-krm</title><style>{style}</style>"
        f'<rect x="5" y="0" width="836" height="374" rx="12" fill="#0c0c0c"/>'
        f'<rect x="24" y="46" width="798" height="248" rx="8" fill="none" stroke="#3a3a3a" stroke-width="1.2" pathLength="1" class="dr"/>'
        f'<g class="a a0"><rect x="38" y="38" width="76" height="16" fill="#0c0c0c"/>'
        f'<text x="45" y="50.5" font-size="13" fill="#a1a1a1">sami-krm</text></g>'
        f'<path class="dv" d="M330 68V272" stroke="#3a3a3a" stroke-width="1.2"/>'
        f'<g class="tor">{"".join(frames)}</g>'
        f'{"".join(right)}{prompt}</svg>'
    )

if __name__ == "__main__":
    svg = build()
    assert svg.count('class="f') == N and "<script" not in svg
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{len(svg) // 1024} Ko")
