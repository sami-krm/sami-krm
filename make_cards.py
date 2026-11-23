"""Génère les cartes de projets du profil (cards/*.svg), à afficher dans README.md.

Usage : python3 make_cards.py
Chaque carte : un aperçu en haut, puis le nom, une phrase et la plateforme.
"""
import base64
import os
from html import escape

W, H, TOP = 826, 372, 250   # taille d'une carte et hauteur de l'aperçu
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
HERE = os.path.dirname(os.path.abspath(__file__))

def data_uri(name, mime):
    with open(os.path.join(HERE, "assets", name), "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

def card(slug, title, desc, meta, preview):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="{escape(title)} : {escape(desc)}"><title>{escape(title)}</title>'
        f'<defs><clipPath id="c-{slug}"><rect width="{W}" height="{H}" rx="22"/></clipPath></defs>'
        f'<g clip-path="url(#c-{slug})"><rect width="{W}" height="{H}" fill="#111318"/>'
        f'<svg width="{W}" height="{TOP}" viewBox="0 0 {W} {TOP}">{preview}</svg></g>'
        f'<text x="34" y="{TOP + 56}" font-family="{SANS}" font-size="40" font-weight="700" fill="#f4f4f5">{escape(title)}</text>'
        f'<text x="34" y="{TOP + 96}" font-family="{SANS}" font-size="23" fill="#9ca3af">{escape(desc)}</text>'
        f'<text x="{W - 34}" y="{TOP + 54}" font-family="{SANS}" font-size="23" fill="#9ca3af" text-anchor="end">{escape(meta)}</text>'
        "</svg>"
    )

# ---------- aperçus ----------

def notchlet():
    bars = "".join(
        f'<rect x="{676 + i * 13}" y="60" width="8" height="34" rx="4" fill="#ff9f43">'
        f'<animate attributeName="height" values="{a};34;{b};{a}" dur="{0.9 + i * 0.13:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{94 - a};60;{94 - b};{94 - a}" dur="{0.9 + i * 0.13:.2f}s" repeatCount="indefinite"/></rect>'
        for i, (a, b) in enumerate([(12, 22), (26, 10), (8, 30), (20, 14), (14, 26)])
    )
    return (
        '<defs><linearGradient id="nw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e3a8a"/>'
        '<stop offset=".55" stop-color="#7c3aed"/><stop offset="1" stop-color="#f472b6"/></linearGradient>'
        '<linearGradient id="na" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f97316"/><stop offset="1" stop-color="#db2777"/></linearGradient></defs>'
        f'<rect width="{W}" height="{TOP}" fill="url(#nw)"/>'
        f'<rect width="{W}" height="26" fill="#000" opacity=".28"/>'
        f'<text x="22" y="18" font-family="{SANS}" font-size="13" fill="#fff">Finder   Fichier   Édition   Présentation</text>'
        f'<text x="{W - 20}" y="18" font-family="{SANS}" font-size="13" fill="#fff" text-anchor="end">lun. 9:41</text>'
        # l'île déployée sur l'encoche
        '<path d="M183 0H643V128a34 34 0 0 1-34 34H217a34 34 0 0 1-34-34Z" fill="#000"/>'
        '<rect x="208" y="34" width="96" height="96" rx="16" fill="url(#na)"/>'
        '<circle cx="256" cy="82" r="22" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="5"/>'
        f'<text x="324" y="62" font-family="{SANS}" font-size="21" font-weight="700" fill="#fff">Lecture en cours</text>'
        f'<text x="324" y="88" font-family="{SANS}" font-size="16" fill="#a1a1aa">Spotify · Musique</text>'
        '<rect x="324" y="110" width="290" height="5" rx="2.5" fill="#3f3f46"/>'
        '<rect x="324" y="110" width="120" height="5" rx="2.5" fill="#fff">'
        '<animate attributeName="width" values="40;290" dur="12s" repeatCount="indefinite"/></rect>'
        + bars +
        # pilule de batterie sous l'île
        f'<rect x="333" y="190" width="160" height="34" rx="17" fill="#000" opacity=".75"/>'
        f'<text x="413" y="212" font-family="{SANS}" font-size="15" fill="#4ade80" text-anchor="middle">⚡ 82 %  ·  En charge</text>'
    )

def habilletoi():
    icon = data_uri("habilletoi-icon.svg", "image/svg+xml")
    chips = ""
    x = 330
    for label in ("Veste en jean", "T-shirt blanc", "Baskets"):
        w = 18 + len(label) * 10
        chips += (f'<rect x="{x}" y="160" width="{w}" height="38" rx="19" fill="#fff" fill-opacity=".16"/>'
                  f'<text x="{x + w / 2}" y="185" font-family="{SANS}" font-size="16" fill="#fff" text-anchor="middle">{label}</text>')
        x += w + 12
    return (
        '<defs><linearGradient id="hb" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#A47BFF"/>'
        '<stop offset=".55" stop-color="#6C3BF0"/><stop offset="1" stop-color="#2A1366"/></linearGradient>'
        '<clipPath id="hi"><rect x="70" y="50" width="150" height="150" rx="34"/></clipPath></defs>'
        f'<rect width="{W}" height="{TOP}" fill="url(#hb)"/>'
        '<circle cx="740" cy="40" r="90" fill="#fff" opacity=".06"/><circle cx="90" cy="240" r="120" fill="#fff" opacity=".05"/>'
        f'<image href="{icon}" x="70" y="50" width="150" height="150" clip-path="url(#hi)"/>'
        '<rect x="70" y="50" width="150" height="150" rx="34" fill="none" stroke="#fff" stroke-opacity=".25"/>'
        f'<text x="330" y="78" font-family="{SANS}" font-size="17" fill="#e9d5ff">Aujourd’hui · Montpellier</text>'
        f'<text x="330" y="138" font-family="{SANS}" font-size="56" font-weight="700" fill="#fff">☀ 18°</text>'
        f'<text x="520" y="122" font-family="{SANS}" font-size="17" fill="#e9d5ff">Ensoleillé, vent léger</text>'
        + chips
    )

def weblooping():
    def entity(x, y, name, fields):
        h = 50 + 24 * len(fields)
        rows = "".join(
            f'<text x="{x + 14}" y="{y + 62 + 24 * i}" font-family="{MONO}" font-size="15" fill="#1f2937"'
            + (' text-decoration="underline"' if i == 0 else "") + f'>{f}</text>' for i, f in enumerate(fields))
        return (f'<rect x="{x}" y="{y}" width="170" height="{h}" rx="8" fill="#fff" stroke="#2563eb" stroke-width="2"/>'
                f'<path d="M{x} {y + 8}a8 8 0 0 1 8-8h154a8 8 0 0 1 8 8v26H{x}z" fill="#dbeafe"/>'
                f'<text x="{x + 85}" y="{y + 24}" font-family="{MONO}" font-size="15" font-weight="700" fill="#1e3a8a" text-anchor="middle">{name}</text>'
                + rows)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#cbd5e1"/>' for x in range(14, W, 26) for y in range(14, TOP, 26))
    return (
        f'<rect width="{W}" height="{TOP}" fill="#f8fafc"/>{dots}'
        '<path d="M232 110H352M474 110H594" stroke="#334155" stroke-width="2"/>'
        f'<text x="262" y="100" font-family="{MONO}" font-size="15" fill="#b45309">0,n</text>'
        f'<text x="534" y="100" font-family="{MONO}" font-size="15" fill="#b45309">1,1</text>'
        + entity(62, 60, "CLIENT", ["id_client", "nom", "email"])
        + entity(594, 60, "COMMANDE", ["num_cmd", "date_cmd"])
        + '<ellipse cx="413" cy="110" rx="62" ry="32" fill="#fff" stroke="#2563eb" stroke-width="2"/>'
        f'<text x="413" y="116" font-family="{MONO}" font-size="16" font-weight="700" fill="#1e3a8a" text-anchor="middle">Passer</text>'
        '<rect x="262" y="186" width="302" height="44" rx="8" fill="#0f172a"/>'
        f'<text x="280" y="214" font-family="{MONO}" font-size="14" fill="#93c5fd">CREATE TABLE <tspan fill="#fbbf24">commande</tspan> (…);</text>'
    )

def masterbait():
    bg, fish = data_uri("masterbait-bg.jpg", "image/jpeg"), data_uri("masterbait-fish.png", "image/png")
    return (
        f'<image href="{bg}" width="{W}" height="{TOP}" preserveAspectRatio="xMidYMid slice"/>'
        f'<g><image href="{fish}" x="-22" y="-10" width="270" height="270">'
        '<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="3s" repeatCount="indefinite"/></image></g>'
        f'<text x="330" y="112" font-family="{SANS}" font-size="30" font-weight="800" fill="#fff" letter-spacing="2">REQUIN BLANC</text>'
        f'<text x="330" y="150" font-family="{SANS}" font-size="20" font-weight="700" fill="#fff" letter-spacing="2">POIDS : 1 087,4 KG</text>'
        f'<rect x="330" y="170" width="132" height="34" rx="17" fill="#facc15"/>'
        f'<text x="396" y="193" font-family="{SANS}" font-size="16" font-weight="800" fill="#713f12" text-anchor="middle">DORÉ · ×3</text>'
    )

CARDS = [
    ("notchlet", "Notchlet", "Une Dynamic Island pour Mac", "macOS · Swift", notchlet),
    ("habilletoi", "HabilleToi", "Ta tenue du jour selon la météo", "iOS · Android", habilletoi),
    ("weblooping", "WebLooping", "MCD, MLD et SQL dans le navigateur", "Web", weblooping),
    ("masterbait", "MasterBait", "Jeu de pêche… gare à Cthulhu", "Python · Pygame", masterbait),
]

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "cards"), exist_ok=True)
    for slug, title, desc, meta, fn in CARDS:
        svg = card(slug, title, desc, meta, fn())
        assert "<script" not in svg
        with open(os.path.join(HERE, "cards", f"{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        print(slug, f"{len(svg) // 1024} Ko")
