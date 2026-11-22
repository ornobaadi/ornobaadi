#!/usr/bin/env python3
"""Generates the minimal README assets into ../assets (prefix m-).

Edit the data below, then run:  python scripts/minimal.py
Every card is a self-contained dark panel, so it reads the same in GitHub's
light and dark themes. The portrait is embedded as base64 because GitHub
blocks external images inside SVGs.

Rules: neutral graphite, one accent (jade) for links and one highlight per
drawing, a serif only for names, sans for everything else, no glows, no
animation, no tracked-caps labels. Text sizes are large because GitHub
scales these 1200px cards down to a third on phones.
"""
import base64
from pathlib import Path
from xml.sax.saxutils import escape as x

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
W = 1200

PAPER, PANEL, RULE, RULE2 = "#0f1011", "#16181a", "#24272a", "#33373b"
INK, MUTE, JADE = "#e9ebec", "#8c9298", "#4fc3a1"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
SANS = "-apple-system,'Segoe UI',system-ui,Roboto,Helvetica,Arial,sans-serif"

# (slug, name, status, live, line 1, line 2, stack). Live apps link to Google Play.
APPS = [
    ("popcalc", "PopCalc", "On Google Play · 5K+ downloads", True,
     "Sculpted 3D numerals, haptics and sound,",
     "scientific mode and a currency converter.",
     "Flutter · Dart · SoLoud"),
    ("zeropuff", "ZeroPuff", "On Google Play as Quit Smoking", True,
     "A calm, private quit-smoking tracker:",
     "breathe through cravings, count money saved.",
     "Flutter · Riverpod · Isar · Supabase"),
    ("ripped", "Ripped", "On Google Play", True,
     "Offline-first strength training with a",
     "generated plan that adapts as you lift.",
     "Flutter · Drift · Firebase"),
    ("twofold", "TwoFold", "On Google Play", True,
     "Read the book and play the audiobook,",
     "always back at the same page and second.",
     "Flutter · just_audio · pdfrx · SQLite"),
    ("waqt", "Waqt", "On Google Play", True,
     "The right dua for the moment you are in,",
     "each with a verified source. Seven languages.",
     "Flutter · Riverpod · adhan · SQLite"),
    ("suhbah", "Suhbah", "On Google Play", True,
     "A shared worship tracker: two people log",
     "prayers, Quran and istighfar together.",
     "Flutter · Firebase · adhan"),
]

PROJECTS = [
    ("msnovo", "MsNovo", "AI marking assistant, built at Noverse Inc.",
     "Noverse Inc.", "noverseinc.com"),
    ("chatterbox", "Chatterbox", "Real-time chat focused on fast, simple conversations.",
     "Next.js · TypeScript · Socket.IO", "chatterbox-space.vercel.app"),
    ("skyscout", "SkyScout", "Flight search on the Amadeus API with live fares and price charts.",
     "Next.js · TypeScript", "skyy-scout.vercel.app"),
]

# The résumé is the one primary action, so it alone is filled.
LINKS = [
    ("resume", "Résumé", "View PDF", True),
    ("portfolio", "Website", "ornobaadi.tech", False),
    ("linkedin", "LinkedIn", "/in/ornobaadi", False),
    ("x", "X", "@OrnobAadi", False),
    ("email", "Email", "aadi4789@gmail.com", False),
    ("whatsapp", "WhatsApp", "+880 1974 716063", False),
    ("profile", "Minimal portfolio", "profile.ornobaadi.tech", False),
]


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{x(label)}">\n'
            f'{body}\n</svg>\n')


def panel(h, w=W):
    return (f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="13.5" fill="none" stroke="{RULE}"/>')


def t(xp, yp, s, size, fam=SANS, fill=INK, extra=""):
    return f'<text x="{xp}" y="{yp}" font-family="{fam}" font-size="{size}" fill="{fill}" {extra}>{x(s)}</text>'


END = 'text-anchor="end"'
MID = 'text-anchor="middle"'


def write(name, content):
    (OUT / f"m-{name}.svg").write_text(content, encoding="utf-8")


def hero():
    img = base64.b64encode((OUT / "portrait.jpg").read_bytes()).decode()
    h = 500
    body = f'''{panel(h)}
<defs><clipPath id="arch"><path d="M800 460 V220 a160 160 0 0 1 320 0 V460 Z"/></clipPath>
<filter id="tone"><feColorMatrix type="saturate" values="0.6"/></filter></defs>
<image x="780" y="60" width="360" height="400" preserveAspectRatio="xMidYMin slice" clip-path="url(#arch)" filter="url(#tone)" xlink:href="data:image/jpeg;base64,{img}" href="data:image/jpeg;base64,{img}"/>
{t(64, 96, "Full stack engineer · Dhaka", 22, SANS, MUTE)}
{t(58, 200, "Fajlay Rabby", 104, SERIF)}
<line x1="64" y1="236" x2="124" y2="236" stroke="{JADE}" stroke-width="3"/>
{t(64, 296, "I build web products in Next.js and Android", 30, SANS)}
{t(64, 338, "apps in Flutter, end to end.", 30, SANS)}
{t(64, 420, "Open to full-time and freelance work", 22, SANS, MUTE)}'''
    write("hero", svg(W, h, body, "Fajlay Rabby (Aadi), full stack engineer in Dhaka. I build web products in Next.js and Android apps in Flutter. Open to full-time and freelance work."))


def title(slug, text):
    # Titles sit on the page itself, so they get a light-theme twin.
    h = 96
    for suffix, ink, rule in (("", INK, RULE2), ("-light", "#1f2328", "#d1d9e0")):
        body = (t(2, 56, text, 48, SERIF, ink)
                + f'<line x1="2" y1="80" x2="{W-2}" y2="80" stroke="{rule}"/>'
                + f'<line x1="2" y1="80" x2="62" y2="80" stroke="{JADE}" stroke-width="3"/>')
        write(f"title-{slug}{suffix}", svg(W, h, body, text))


def app_art(slug, ox, oy):
    """One drawing per app, about 520x220, drawn from what the app does."""
    s = ""
    if slug == "popcalc":
        # an extruded numeral beside a keypad
        for d in range(9, 0, -1):
            s += t(ox + 40 + d, oy + 190 + d, "7", 200, SERIF, RULE2, 'font-weight="700"')
        s += t(ox + 40, oy + 190, "7", 200, SERIF, JADE, 'font-weight="700"')
        for r in range(4):
            for c in range(4):
                hot = (r, c) == (3, 3)
                s += (f'<rect x="{ox+250+c*66}" y="{oy+12+r*50}" width="54" height="40" rx="10" '
                      f'fill="{JADE if hot else PANEL}" stroke="{JADE if hot else RULE2}"/>')
        return s
    if slug == "zeropuff":
        # the smoke-free clock rolling like an odometer, the month of
        # smoke-free days, and the money won back stacking up
        for i, (cur, unit) in enumerate([("12", "days"), ("04", "hrs"), ("37", "min")]):
            x0 = ox + 8 + i * 118
            s += f'<rect x="{x0}" y="{oy+8}" width="104" height="104" rx="12" fill="{PANEL}" stroke="{RULE2}"/>'
            nxt = f"{(int(cur) + 1) % 60:02d}"
            s += t(x0 + 52, oy + 30, nxt, 22, SANS, RULE2, 'font-weight="600" text-anchor="middle"')
            s += t(x0 + 52, oy + 76, cur, 40, SANS, JADE if i == 0 else INK, 'font-weight="700" text-anchor="middle"')
            s += t(x0 + 52, oy + 102, unit, 14, SANS, MUTE, MID)
        for r in range(4):
            for c in range(7):
                k = r * 7 + c
                if k > 25:
                    continue
                fill = JADE if k < 12 else (PANEL if k > 12 else PAPER)
                stroke = JADE if k <= 12 else RULE2
                s += f'<rect x="{ox+14+c*26}" y="{oy+130+r*24}" width="18" height="18" rx="4" fill="{fill}" stroke="{stroke}"/>'
        # the hold-to-breathe orb for cravings
        for r, op in ((54, ".15"), (40, ".3"), (26, ".6")):
            s += f'<circle cx="{ox+456}" cy="{oy+60}" r="{r}" fill="none" stroke="{JADE}" stroke-opacity="{op}" stroke-width="2"/>'
        s += f'<circle cx="{ox+456}" cy="{oy+60}" r="14" fill="{JADE}"/>'
        # coins stacking toward the right: money won back
        for col, n in enumerate((3, 5, 7)):
            for j in range(n):
                cx, cy = ox + 300 + col * 64, oy + 214 - j * 11
                s += (f'<ellipse cx="{cx}" cy="{cy}" rx="24" ry="8" fill="{PANEL}" stroke="{JADE if col == 2 else RULE2}" stroke-width="2"/>')
        return s
    if slug == "ripped":
        # a loaded barbell over today's sets: three done, one to go
        bar_y = oy + 74
        s += f'<rect x="{ox+10}" y="{bar_y-4}" width="500" height="8" rx="4" fill="{MUTE}"/>'
        for side in (-1, 1):
            cx = ox + 260
            for i, (pw, ph, col) in enumerate([(26, 130, JADE), (20, 104, RULE2), (16, 80, RULE2)]):
                off = 150 + sum(w + 6 for w, _, _ in [(26, 0, 0), (20, 0, 0), (16, 0, 0)][:i])
                px = cx + side * off - (pw if side < 0 else 0)
                s += f'<rect x="{px}" y="{bar_y-ph/2}" width="{pw}" height="{ph}" rx="5" fill="{col}" stroke="{PAPER}" stroke-width="2"/>'
            s += f'<rect x="{cx + side*140 - (6 if side < 0 else 0)}" y="{bar_y-14}" width="6" height="28" rx="2" fill="{INK}"/>'
        for i in range(4):
            done = i < 3
            x0 = ox + 40 + i * 116
            s += (f'<rect x="{x0}" y="{oy+168}" width="100" height="46" rx="10" fill="{PANEL}" stroke="{JADE if done else RULE2}"/>'
                  + t(x0 + 50, oy + 198, "5 reps" if done else "next", 18, SANS, INK if done else MUTE, MID))
        return s
    if slug == "twofold":
        # an open book over an audio track, the playhead on the same spot
        s += (f'<path d="M{ox+50} {oy+14} q105 -14 210 10 v150 q-105 -24 -210 -10 Z" fill="{PANEL}" stroke="{RULE2}"/>'
              f'<path d="M{ox+260} {oy+24} q105 -24 210 -10 v150 q-105 -14 -210 10 Z" fill="{PANEL}" stroke="{RULE2}"/>')
        for j in range(4):
            s += f'<rect x="{ox+80}" y="{oy+46+j*28}" width="{140-(j%2)*30}" height="6" rx="3" fill="{RULE2}"/>'
            s += f'<rect x="{ox+290}" y="{oy+42+j*28}" width="{140-(j%3)*20}" height="6" rx="3" fill="{JADE if j == 2 else RULE2}"/>'
        for i in range(40):
            hgt = 8 + (i * 37 % 26)
            s += f'<rect x="{ox+40+i*11}" y="{oy+214-hgt/2}" width="5" height="{hgt}" rx="2.5" fill="{JADE if i < 24 else RULE2}"/>'
        s += f'<circle cx="{ox+306}" cy="{oy+214}" r="8" fill="{INK}"/>'
        return s
    if slug == "waqt":
        # the day's arc with the five prayers on it; the night side holds
        # the last third, where the moon is
        import math
        cx, cy, rx, ry = ox + 230, oy + 196, 210, 170
        s += f'<line x1="{ox}" y1="{cy}" x2="{ox+520}" y2="{cy}" stroke="{RULE2}"/>'
        s += f'<path d="M{cx-rx} {cy} A{rx} {ry} 0 0 1 {cx+rx} {cy}" fill="none" stroke="{RULE2}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
        names = [("Fajr", .03), ("Dhuhr", .5), ("Asr", .72), ("Maghrib", .97)]
        for name, a in names:
            ang = math.pi * (1 - a)
            px, py = cx + rx * math.cos(ang), cy - ry * math.sin(ang)
            hot = name == "Asr"
            s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{9 if hot else 6}" fill="{JADE if hot else PAPER}" stroke="{JADE if hot else MUTE}" stroke-width="2"/>'
            if hot:
                s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="18" fill="none" stroke="{JADE}" stroke-opacity=".35" stroke-width="2"/>'
            s += t(px, py - 20 if a not in (.03, .97) else cy + 26, name, 15, SANS, INK if hot else MUTE, MID)
        s += f'<circle cx="{ox+478}" cy="{oy+118}" r="6" fill="{PAPER}" stroke="{MUTE}" stroke-width="2"/>' + t(ox + 478, oy + 146, "Isha", 15, SANS, MUTE, MID)
        s += (f'<circle cx="{ox+478}" cy="{oy+40}" r="26" fill="{JADE}"/>'
              f'<circle cx="{ox+490}" cy="{oy+31}" r="23" fill="{PAPER}"/>')
        for sx, sy, r in ((ox + 420, oy + 22, 2.5), (ox + 446, oy + 74, 2), (ox + 508, oy + 92, 2.5)):
            s += f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{MUTE}"/>'
        return s
    # suhbah: one shared arc filled from both ends, a seat per deed,
    # the two halves meeting in the middle at 100%
    import math
    cx, cy = ox + 260, oy + 214
    seats = []
    for row, (r, n) in enumerate([(120, 15), (158, 19), (196, 23)]):
        for i in range(n):
            ang = math.pi * (1 - i / (n - 1))
            seats.append((ang, cx + r * math.cos(ang), cy - r * math.sin(ang) * 0.95))
    seats.sort(key=lambda z: -z[0])
    for ang, px, py in seats:
        left = ang > math.pi / 2
        s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7.5" fill="{JADE if left else INK}"/>'
    s += t(cx, cy - 26, "100", 54, SANS, INK, 'font-weight="700" text-anchor="middle"')
    s += t(cx, cy - 2, "together", 15, SANS, MUTE, MID)
    return s


def app(slug, name, status, live, l1, l2, stack):
    w, h = 600, 540
    body = (panel(h, w)
            + f'<rect x="24.5" y="24.5" width="{w-49}" height="259" rx="12" fill="{PAPER}" stroke="{RULE}"/>'
            + app_art(slug, 40, 44)
            + t(36, 356, name, 46, SERIF) + t(38, 392, status, 20, SANS, JADE if live else MUTE)
            + t(38, 436, l1, 22, SANS) + t(38, 466, l2, 22, SANS, MUTE)
            + f'<line x1="38" y1="492" x2="{w-38}" y2="492" stroke="{RULE}"/>'
            + t(38, 520, stack, 17, SANS, MUTE)
            + (t(w - 38, 520, "Google Play ↗", 17, SANS, JADE, END) if live else ""))
    write(f"app-{slug}", svg(w, h, body, f"{name}, {status}. {l1} {l2}"))


def art(slug):
    ox, oy = 830, 36
    if slug == "msnovo":
        s = ""
        for i in range(3):
            d = i * 14
            s += f'<rect x="{ox+40-d}" y="{oy+20+d}" width="200" height="180" rx="8" fill="{PANEL}" stroke="{RULE2}"/>'
        for j in range(5):
            y = oy + 84 + j * 22
            s += f'<rect x="{ox+30}" y="{y}" width="{120-(j%3)*24}" height="6" rx="3" fill="{RULE2}"/>'
            s += (f'<path d="M{ox+168} {y+3} l6 6 l12 -12" stroke="{JADE}" stroke-width="2.5" fill="none"/>' if j != 3
                  else f'<path d="M{ox+170} {y-3} l10 10 M{ox+180} {y-3} l-10 10" stroke="{MUTE}" stroke-width="2.5"/>')
        return s
    if slug == "chatterbox":
        s = ""
        for i, (w, right) in enumerate([(170, False), (130, True), (200, False), (110, True)]):
            y = oy + 20 + i * 50
            xx = ox + 300 - w if right else ox + 20
            s += f'<rect x="{xx}" y="{y}" width="{w}" height="36" rx="18" fill="{PANEL}" stroke="{JADE if right else RULE2}"/>'
            s += f'<rect x="{xx+18}" y="{y+15}" width="{w-60}" height="6" rx="3" fill="{JADE if right else RULE2}"/>'
        return s
    if slug == "skyscout":
        # a boarding pass: route, plane and a fare stub
        s = (f'<path d="M{ox} {oy+20} h232 a14 14 0 0 0 28 0 h80 v190 h-80 a14 14 0 0 0 -28 0 h-232 Z" fill="{PANEL}" stroke="{RULE2}"/>'
             f'<line x1="{ox+246}" y1="{oy+40}" x2="{ox+246}" y2="{oy+190}" stroke="{RULE2}" stroke-dasharray="4 6"/>'
             + t(ox + 24, oy + 100, "DAC", 40, SANS, INK, 'font-weight="600"')
             + t(ox + 222, oy + 100, "DXB", 40, SANS, INK, 'font-weight="600" text-anchor="end"')
             + f'<line x1="{ox+28}" y1="{oy+132}" x2="{ox+218}" y2="{oy+132}" stroke="{RULE2}" stroke-dasharray="3 6"/>'
             + f'<path transform="translate({ox+118} {oy+132})" d="M-14 -3 L6 -3 L12 -12 L16 -12 L12 -3 L18 -3 L21 -7 L24 -7 L22 0 L24 7 L21 7 L18 3 L12 3 L16 12 L12 12 L6 3 L-14 3 Z" fill="{JADE}"/>'
             + f'<rect x="{ox+24}" y="{oy+164}" width="70" height="6" rx="3" fill="{RULE2}"/>'
             + f'<rect x="{ox+152}" y="{oy+164}" width="70" height="6" rx="3" fill="{RULE2}"/>')
        for i, hgt in enumerate([44, 62, 30, 54]):
            s += f'<rect x="{ox+268+i*16}" y="{oy+180-hgt}" width="10" height="{hgt}" rx="2" fill="{JADE if hgt == 30 else RULE2}"/>'
        return s
    s = ""
    for i in range(4):
        cx, cy = ox + 20 + (i % 2) * 150, oy + 24 + (i // 2) * 104
        hot = i == 2
        s += f'<rect x="{cx}" y="{cy}" width="134" height="90" rx="12" fill="{PANEL}" stroke="{JADE if hot else RULE2}"/>'
        s += t(cx + 22, cy + 54, "ABCD"[i], 30, SERIF, JADE if hot else MUTE)
        s += f'<rect x="{cx+62}" y="{cy+40}" width="50" height="6" rx="3" fill="{JADE if hot else RULE2}"/>'
    return s


def project(slug, name, line, stack, url):
    h = 290
    body = (panel(h) + art(slug)
            + t(54, 106, name, 60, SERIF)
            + t(56, 158, line, 24, SANS, MUTE)
            + f'<line x1="56" y1="214" x2="760" y2="214" stroke="{RULE}"/>'
            + t(56, 250, stack, 20, SANS, MUTE) + t(760, 250, url + " ↗", 20, SANS, JADE, END))
    write(f"work-{slug}", svg(W, h, body, f"{name}: {line}"))


def link(slug, label, value, primary):
    w = int(max(len(value) * 9.4, len(label) * 8) + 80)
    h = 60
    bg, fg, sub, ring = (JADE, PAPER, "#14453a", "#14453a") if primary else (PANEL, INK, MUTE, RULE2)
    cx = w - 30
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{bg}" stroke="{JADE if primary else RULE2}"/>'
            + t(20, 25, label, 12, SANS, sub)
            + t(20, 46, value, 16, SANS, fg, 'font-weight="600"')
            + f'<circle cx="{cx}" cy="30" r="13" fill="none" stroke="{ring}"/>'
            + t(cx, 35, "↗", 13, SANS, fg if primary else JADE, MID))
    (OUT / f"m-link-{slug}.svg").write_text(svg(w, h, body, f"{label}: {value}"), encoding="utf-8")


def footer():
    h = 170
    body = (panel(h) + t(W // 2, 90, "Have something to build?", 48, SERIF, INK, MID)
            + t(W // 2, 132, "Reach me on any of the links below.", 22, SANS, MUTE, MID))
    write("footer", svg(W, h, body, "Have something to build? Get in touch."))


if __name__ == "__main__":
    hero()
    for slug, text in [("apps", "Apps"), ("work", "Selected work"),
                       ("toolkit", "Toolkit"), ("activity", "Activity")]:
        title(slug, text)
    for a in APPS:
        app(*a)
    for p in PROJECTS:
        project(*p)
    for l in LINKS:
        link(*l)
    footer()
    print("ok")
