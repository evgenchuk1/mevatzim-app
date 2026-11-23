# -*- coding: utf-8 -*-
"""מפת סניף 118 לפריסה+ — SVG מאויר ("חי"), לפי הקואורדינטות של 'מפת החנות 118.docx' (נקודות PDF, 595x842).
v2 (14.11.2026): פרטים חיים כמו במפת 208 — מוצרים עם הצללה, ארגזי ירקות, לחמים, בקבוקים, מקררים עם דלתות זכוכית,
ויטרינות עם סחורה ואנשי צוות, קופאיות, קונים עם עגלות. בלי אליפסות צבעוניות; שמות המעברים חיוורים.
עיגולי המקומות המיוחדים — ללא שינוי.
הרצה: python tools/gen_map_118.py  → map-118.svg
"""
import random, os
random.seed(118)
OUT = os.path.join(os.path.dirname(__file__), '..', 'map-118.svg')
E = []
a = E.append
PROD = ['#e8483b', '#f39c34', '#f5c842', '#58b85c', '#3d8fd6', '#8a5cc2', '#e86a9a', '#2bb3a8', '#ffffff', '#c0392b', '#1f6fb2']
SKIN = ['#f1c9a5', '#e0ac85', '#c68863', '#8d5a3b']
SHIRT = ['#3d8fd6', '#e8483b', '#58b85c', '#f39c34', '#8a5cc2', '#2bb3a8', '#e86a9a', '#5a6b80']
HAIR = ['#2b1d14', '#5a3a22', '#a0703c', '#1b1b1b', '#c9a35f']


def rect(x0, y0, x1, y1, fill, stroke='none', sw=0, rx=0, extra=''):
    a(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def text(x, y, s, size=9, fill='#203550', w=800, rot=0, anchor='middle', extra=''):
    t = f' transform="rotate({rot} {x} {y})"' if rot else ''
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="central"{t} {extra}>{s}</text>')


def shade(x0, y0, x1, y1, rx=2, dx=1.6, dy=2.2, op=.2):
    rect(x0 + dx, y0 + dy, x1 + dx, y1 + dy, f'rgba(20,35,56,{op})', rx=rx)


def item(x0, y0, x1, y1, c):
    """מוצר בודד עם הברקה"""
    rect(x0, y0, x1, y1, c, 'rgba(0,0,0,.18)', .25, .7)
    h = (y1 - y0)
    rect(x0 + .3, y0 + .3, x1 - .3, y0 + h * .38, 'rgba(255,255,255,.38)', rx=.5)


def stock_h(x0, y0, x1, y1, pal=PROD):
    x = x0
    while x < x1 - 1:
        w = min(random.uniform(2.6, 5.6), x1 - x)
        c = random.choice(pal)
        n = random.choice([1, 1, 2, 3])          # כמה יחידות מאותו מוצר ברצף
        for _ in range(n):
            if x >= x1 - 1:
                break
            w2 = min(w, x1 - x)
            inset = random.uniform(0, .9)
            item(x, y0 + inset, x + w2 - .5, y1 - inset * .4, c)
            x += w2


def stock_v(x0, y0, x1, y1, pal=PROD):
    y = y0
    while y < y1 - 1:
        h = min(random.uniform(2.6, 5.6), y1 - y)
        c = random.choice(pal)
        for _ in range(random.choice([1, 1, 2, 3])):
            if y >= y1 - 1:
                break
            h2 = min(h, y1 - y)
            inset = random.uniform(0, .9)
            item(x0 + inset, y, x1 - inset * .4, y + h2 - .5, c)
            y += h2


def gondola_h(x0, y0, x1, y1):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#f4f6f8', '#8e9bab', .7, 1.8)
    m = (y0 + y1) / 2
    stock_h(x0 + 1.8, y0 + 1.4, x1 - 1.8, m - 1)
    stock_h(x0 + 1.8, m + 1, x1 - 1.8, y1 - 1.4)
    rect(x0 + 1, m - .8, x1 - 1, m + .8, '#a9b4c2', rx=.4)         # גב הגונדולה
    a(f'<line x1="{x0+1}" y1="{y0+.6}" x2="{x1-1}" y2="{y0+.6}" stroke="#ffffff" stroke-width=".7"/>')  # פס מחירים
    a(f'<line x1="{x0+1}" y1="{y1-.6}" x2="{x1-1}" y2="{y1-.6}" stroke="#ffffff" stroke-width=".7"/>')


def shelf_v(x0, y0, x1, y1, base='#f4f6f8', edge='#8e9bab', pal=PROD):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, base, edge, .7, 1.8)
    stock_v(x0 + 1.3, y0 + 1.8, x1 - 1.3, y1 - 1.8, pal)


def shelf_h(x0, y0, x1, y1, base='#f4f6f8', edge='#8e9bab', pal=PROD):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, base, edge, .7, 1.8)
    stock_h(x0 + 1.8, y0 + 1.3, x1 - 1.8, y1 - 1.3, pal)


def fridge_h(x0, y0, x1, y1, pal, frame='#1d4f6e', glass='#cfe9f6'):
    """מקרר עם דלתות זכוכית (מבט מלמעלה-קדימה)"""
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, frame, '#0e2c3e', .7, 2)
    rect(x0 + 1.3, y0 + 1.3, x1 - 1.3, y1 - 1.3, glass, rx=1)
    stock_h(x0 + 2, y0 + 2, x1 - 2, y1 - 2, pal)
    rect(x0 + 1.3, y0 + 1.3, x1 - 1.3, y1 - 1.3, 'rgba(255,255,255,.22)', rx=1)
    n = max(2, int((x1 - x0) / 14))
    for i in range(1, n):
        xx = x0 + (x1 - x0) * i / n
        a(f'<line x1="{xx:.1f}" y1="{y0+1}" x2="{xx:.1f}" y2="{y1-1}" stroke="{frame}" stroke-width="1"/>')


def fridge_v(x0, y0, x1, y1, pal, frame='#1d4f6e', glass='#cfe9f6'):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, frame, '#0e2c3e', .7, 2)
    rect(x0 + 1.3, y0 + 1.3, x1 - 1.3, y1 - 1.3, glass, rx=1)
    stock_v(x0 + 2, y0 + 2, x1 - 2, y1 - 2, pal)
    rect(x0 + 1.3, y0 + 1.3, x1 - 1.3, y1 - 1.3, 'rgba(255,255,255,.22)', rx=1)
    n = max(2, int((y1 - y0) / 14))
    for i in range(1, n):
        yy = y0 + (y1 - y0) * i / n
        a(f'<line x1="{x0+1}" y1="{yy:.1f}" x2="{x1-1}" y2="{yy:.1f}" stroke="{frame}" stroke-width="1"/>')


def crates_v(x0, y0, x1, y1):
    """עמדת ירקות: ארגזי עץ עם פירות"""
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#8d6038', '#5e3d20', .7, 1.5)
    y = y0 + 1.2
    FR = [('#e8483b', '#b52d22'), ('#58b85c', '#3a8a3e'), ('#f39c34', '#c9761c'), ('#f5c842', '#c9a020'), ('#8bc34a', '#5f8f2c'),
          ('#7b2d8b', '#561d62'), ('#c0392b', '#8e2a20'), ('#ffe08a', '#d2b45a'), ('#6aa84f', '#4b7a37')]
    while y < y1 - 3:
        h = min(random.uniform(8, 12), y1 - 1.2 - y)
        rect(x0 + 1, y, x1 - 1, y + h - .8, '#c48a4f', '#7a5230', .4, .8)
        c, d = random.choice(FR)
        r = (x1 - x0 - 3) / 6.2
        yy = y + r + .9
        while yy < y + h - r - .6:
            xx = x0 + 1.6 + r
            while xx < x1 - 1.4 - r * .6:
                a(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{r:.2f}" fill="{c}" stroke="{d}" stroke-width=".3"/>')
                a(f'<circle cx="{xx-r*.3:.1f}" cy="{yy-r*.3:.1f}" r="{r*.32:.2f}" fill="rgba(255,255,255,.45)"/>')
                xx += r * 2.05
            yy += r * 1.9
        y += h


def bread_v(x0, y0, x1, y1):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#e9d3b0', '#8d5a2b', .7, 1.8)
    y = y0 + 2.5
    BR = ['#c98a45', '#b5793e', '#e2b46e', '#9c6430', '#d8a35d']
    while y < y1 - 3:
        c = random.choice(BR)
        rx = (x1 - x0) / 2 - 1.8
        a(f'<ellipse cx="{(x0+x1)/2:.1f}" cy="{y+2:.1f}" rx="{rx:.1f}" ry="2.2" fill="{c}" stroke="#7a4a1e" stroke-width=".3"/>')
        a(f'<path d="M{(x0+x1)/2-rx*.5:.1f},{y+1.4:.1f} l1.2,1.2 m1.8,-1.2 l1.2,1.2 m1.8,-1.2 l1.2,1.2" stroke="#f3dcb4" stroke-width=".45" fill="none"/>')
        y += 5


def bottles_v(x0, y0, x1, y1, pal):
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#f3e6d6', '#a4461a', .7, 1.8)
    r = 1.5
    y = y0 + 2.6
    while y < y1 - 2:
        x = x0 + 2.6
        c = random.choice(pal)
        while x < x1 - 2:
            a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="rgba(0,0,0,.3)" stroke-width=".25"/>')
            a(f'<circle cx="{x-.4:.1f}" cy="{y-.4:.1f}" r=".5" fill="rgba(255,255,255,.6)"/>')
            x += 3.3
        y += 3.3


def person(cx, cy, s=1, shirt=None, seated=False):
    shirt = shirt or random.choice(SHIRT)
    skin = random.choice(SKIN)
    hair = random.choice(HAIR)
    a(f'<ellipse cx="{cx+.6*s}" cy="{cy+3.6*s}" rx="{3.4*s}" ry="{1.3*s}" fill="rgba(20,35,56,.22)"/>')
    a(f'<rect x="{cx-3*s:.1f}" y="{cy-.4*s:.1f}" width="{6*s:.1f}" height="{4.4*s:.1f}" rx="{2*s:.1f}" fill="{shirt}" stroke="rgba(0,0,0,.25)" stroke-width=".3"/>')
    a(f'<circle cx="{cx}" cy="{cy-2.3*s:.1f}" r="{2.1*s:.1f}" fill="{skin}"/>')
    a(f'<path d="M{cx-2.1*s:.1f},{cy-2.4*s:.1f} a{2.1*s:.1f},{2.1*s:.1f} 0 0 1 {4.2*s:.1f},0 q{-2.1*s:.1f},{-1*s:.1f} {-4.2*s:.1f},0 z" fill="{hair}"/>')


def cart(cx, cy, s=1, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    a(f'<g{t}>')
    a(f'<rect x="{cx-4.2*s:.1f}" y="{cy-3*s:.1f}" width="{8.4*s:.1f}" height="{6*s:.1f}" rx=".8" fill="rgba(20,35,56,.18)" transform="translate(.8 1.2)"/>')
    a(f'<rect x="{cx-4.2*s:.1f}" y="{cy-3*s:.1f}" width="{8.4*s:.1f}" height="{6*s:.1f}" rx=".8" fill="#e9eef3" stroke="#6d7c8e" stroke-width=".55"/>')
    for i in range(1, 4):
        a(f'<line x1="{cx-4.2*s+2.1*s*i:.1f}" y1="{cy-3*s:.1f}" x2="{cx-4.2*s+2.1*s*i:.1f}" y2="{cy+3*s:.1f}" stroke="#a9b4c2" stroke-width=".3"/>')
    for c, dx, dy in [(random.choice(PROD), -2.2, -1), (random.choice(PROD), .6, .3), (random.choice(PROD), -1, 1.2)]:
        rect(cx + dx * s, cy + dy * s - 1.2 * s, cx + dx * s + 2.4 * s, cy + dy * s + .8 * s, c, rx=.4)
    a(f'<line x1="{cx+4.2*s:.1f}" y1="{cy-3.2*s:.1f}" x2="{cx+4.2*s:.1f}" y2="{cy+3.2*s:.1f}" stroke="#3a4a5c" stroke-width="1.1" stroke-linecap="round"/>')
    a('</g>')


def shopper(cx, cy, rot=0):
    """קונה עם עגלה; rot=0 → העגלה משמאל לקונה"""
    cart(cx - 10, cy + 1, 1.35, rot)
    person(cx, cy - 1, 1.4)


def label(x, y, he, emoji='', size=10, rot=0, color='#203550'):
    s = (emoji + ' ' if emoji else '') + he
    a(f'<g class="lbl"{f" transform=\"rotate({rot} {x} {y})\"" if rot else ""}>')
    w = len(s) * size * .52 + 10
    rect(x - w / 2 + .8, y - size * .78 + 1.2, x + w / 2 + .8, y + size * .78 + 1.2, 'rgba(20,35,56,.18)', rx=size * .7)
    rect(x - w / 2, y - size * .78, x + w / 2, y + size * .78, 'rgba(255,253,248,.95)', color, .6, size * .7)
    text(x, y + .5, s, size, color, 800)
    a('</g>')


def aisle(x, y, n):
    """שם מעבר — חיוור, נטוי, לא בולט"""
    text(x, y, f'מעבר {n}', 8.5, '#e3a9b6', 600, extra='font-style="italic" opacity=".85"')


def head_box(x0, y0, x1, y1):
    shade(x0, y0, x1, y1, 3, 1.8, 2.4, .25)
    rect(x0, y0, x1, y1, '#ffffff', '#203550', 1, 3)
    for i in range(1, 4):
        yy = y0 + (y1 - y0) * i / 4
        a(f'<line x1="{x0+2}" y1="{yy:.1f}" x2="{x1-2}" y2="{yy:.1f}" stroke="#CFAB6F" stroke-width=".7"/>')
    for i in range(4):   # מוצרים בצדדים של ראש הגונדולה
        yy = y0 + (y1 - y0) * i / 4 + 1.5
        rect(x0 + 1.4, yy, x0 + 3.6, yy + (y1 - y0) / 4 - 3, random.choice(PROD), rx=.5)
        rect(x1 - 3.6, yy, x1 - 1.4, yy + (y1 - y0) / 4 - 3, random.choice(PROD), rx=.5)


def pallet(x0, y0, x1, y1):
    shade(x0, y0, x1, y1, 1.5, 1.2, 1.8, .25)
    rect(x0, y0, x1, y1, '#c48a4f', '#7a5230', .6, 1.5)
    n = max(2, int((x1 - x0) / 6))
    for i in range(1, n):
        xx = x0 + (x1 - x0) * i / n
        a(f'<line x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y1}" stroke="#8d6038" stroke-width=".5"/>')
    # ארגזי קרטון
    rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, '#e0b47a', '#9c6d3f', .5, 1)
    a(f'<line x1="{(x0+x1)/2:.1f}" y1="{y0+2}" x2="{(x0+x1)/2:.1f}" y2="{y1-2}" stroke="#c9975a" stroke-width=".6"/>')
    rect(x0 + 2.4, y0 + 2.4, x1 - 2.4, y0 + 4, 'rgba(255,255,255,.35)', rx=.5)


def spot(cx, cy, label_, r=11, size=None):
    size = size or (8.6 if len(label_) <= 2 else 7.4 if len(label_) <= 3 else 6.2)
    a(f'<g class="spot" data-id="{label_}" style="cursor:pointer">')
    a(f'<circle cx="{cx}" cy="{cy+1.4}" r="{r}" fill="rgba(20,35,56,.35)"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f7f1e3" stroke="#203550" stroke-width="1.1"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r-2}" fill="none" stroke="#CFAB6F" stroke-width=".6"/>')
    text(cx, cy + .4, label_, size, '#1b2a3e', 900, extra='class="sl"')
    a(f'<circle class="dot" cx="{cx + r*.72:.1f}" cy="{cy - r*.72:.1f}" r="3.2" fill="#9aa7b6" stroke="#fff" stroke-width=".8"/>')
    a('</g>')


def chair(cx, cy):
    a(f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="#2e343a"/>')
    rect(cx + 2, cy - 3.6, cx + 4, cy + 3.6, '#2e343a', rx=1)


# ───────── קנבס ─────────
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 845" font-family="Heebo, Arial, sans-serif" direction="rtl">')
a('<defs><pattern id="tile" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#f7f3ea"/>'
  '<rect width="8" height="8" fill="#f2ede2"/><rect x="8" y="8" width="8" height="8" fill="#f2ede2"/>'
  '<path d="M16 0H0V16" fill="none" stroke="#e6ddcb" stroke-width=".5"/></pattern>'
  '<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#e9e5dc"/><line x1="0" y1="0" x2="0" y2="8" stroke="#d6d0c3" stroke-width="3"/></pattern>'
  '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f6fd"/><stop offset="1" stop-color="#9fd3ec"/></linearGradient>'
  '<linearGradient id="frz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e2f6"/><stop offset="1" stop-color="#d9b4e0"/></linearGradient>'
  '<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8792"/><stop offset="1" stop-color="#4d555e"/></linearGradient>'
  '<radialGradient id="light" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
  '</defs>')
a('<rect width="600" height="845" fill="#fbf9f4"/>')
OUTLINE = '13,10 586,10 586,551 494,551 494,744 446,744 446,833 84,833 84,772 13,772'
a(f'<polygon points="{OUTLINE}" fill="url(#tile)"/>')
for (cx, cy) in [(320, 200), (320, 420), (320, 620), (110, 560), (520, 380)]:   # תאורה רכה על הרצפה
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="120" ry="90" fill="url(#light)"/>')
rect(15, 12, 100, 321, 'url(#hatch)')   # שטח אחורי

# ───────── קפואים ─────────
FRZ = ['#ffffff', '#cfe8ff', '#f8d7da', '#d4edda', '#fff3cd', '#e2c6ee', '#a8d5f2']
fridge_h(214, 12, 433, 25, FRZ, '#7a3f86', 'url(#frz)')
label(323, 18.5, 'קפואים', '❄', 7, color='#6d2a78')
fridge_h(236, 63, 406, 80, FRZ, '#7a3f86', 'url(#frz)')
label(321, 71.5, 'קפואים', '❄', 7, color='#6d2a78')
gondola_h(236, 80, 406, 99)
for (x0, x1) in [(207, 236), (406, 435)]:
    shade(x0, 63, x1, 98, 3)
    rect(x0, 63, x1, 98, '#7a3f86', '#4f2257', 1, 3)
    rect(x0 + 2, 65, x1 - 2, 96, 'url(#frz)', rx=2)
    stock_v(x0 + 4, 67, x1 - 4, 94, FRZ)
    rect(x0 + 2, 65, x1 - 2, 96, 'rgba(255,255,255,.25)', rx=2)

# ───────── חלב ─────────
DAI = ['#ffffff', '#ffffff', '#dff1fb', '#f6e7a8', '#bfe0f2', '#3d8fd6', '#f8d7da']
fridge_h(434, 12, 564, 25, DAI)
fridge_v(566, 11, 584, 262, DAI)
fridge_h(503, 250, 564, 262, DAI)
fridge_h(466, 94, 547, 117, DAI)
fridge_h(468, 167, 550, 190, DAI)
label(508, 141, 'מוצרי חלב', '🥛', 9.5, color='#155f82')
shade(450, 240, 478, 254)
rect(450, 240, 478, 254, '#fff7e0', '#a8864a', .6, 2)
for i in range(5):
    for j in range(2):
        a(f'<ellipse cx="{453.5+i*5}" cy="{244+j*5}" rx="1.9" ry="1.5" fill="{random.choice(["#f3e1c4", "#ffffff", "#e8cfa5"])}" stroke="#c9a76b" stroke-width=".3"/>')
text(464, 257.5, 'ביצים', 5, '#7a5a20', 900)

# ───────── פארם ─────────
PH = ['#ffffff', '#ffd1e0', '#bfe6f7', '#d7f3d0', '#fff1b8', '#e86a9a', '#2bb3a8', '#3d8fd6', '#8a5cc2']
shelf_h(468, 263, 584, 276, '#eef7fc', '#0e9ed4', PH)
shelf_h(472, 537, 584, 550, '#eef7fc', '#0e9ed4', PH)
shelf_v(567, 276, 584, 536, '#eef7fc', '#0e9ed4', PH)
for (x0, y0, x1, y1) in [(468, 316, 545, 326), (468, 357, 544, 367), (468, 396, 545, 406), (472, 493, 548, 503), (476, 446, 537, 458)]:
    shelf_h(x0, y0, x1, y1, '#eef7fc', '#0e9ed4', PH)
label(512, 428, 'פארם והיגיינה', '🧴', 9, color='#0b6f97')

# ───────── שתייה חריפה / בירות ─────────
bottles_v(471, 552, 491, 719, ['#3c6e2f', '#7a2e10', '#5b3a29', '#e9c46a', '#2f4f2f', '#a31f34', '#d9d2c5'])
label(481, 636, 'שתייה חריפה', '🍷', 8, rot=-90, color='#a4461a')
shade(341, 680, 427, 701)
rect(341, 680, 427, 701, '#e3efe0', '#186b23', .7, 1.8)
x = 343.5
while x < 425:
    c = random.choice(['#f5c842', '#3c6e2f', '#c4581b', '#1f6fb2', '#8d6038'])
    for yy in (683.5, 688.5, 693.5, 698):
        a(f'<circle cx="{x:.1f}" cy="{yy}" r="1.7" fill="{c}" stroke="rgba(0,0,0,.3)" stroke-width=".25"/>')
    x += 3.6
label(384, 690.5, 'בירות', '🍺', 8, color='#186b23')

# ───────── שתייה קלה ─────────
shade(208, 695, 238, 774)
rect(208, 695, 238, 774, '#e3efe0', '#186b23', .7, 1.8)
y = 697.5
while y < 772:
    c = random.choice(['#e8483b', '#3d8fd6', '#58b85c', '#f39c34', '#1b1b1b', '#f5c842'])
    for xx in (211.5, 215.5, 219.5, 223.5, 227.5, 231.5, 235):
        a(f'<circle cx="{xx}" cy="{y:.1f}" r="1.7" fill="{c}" stroke="rgba(0,0,0,.3)" stroke-width=".25"/>')
        a(f'<circle cx="{xx-.4}" cy="{y-.4:.1f}" r=".5" fill="rgba(255,255,255,.6)"/>')
    y += 3.8
label(223, 734, 'שתייה קלה 1.5 ל׳', '🥤', 7, rot=-90, color='#186b23')

# ───────── פיצוחים / זיתים ─────────
NUT = ['#c48a4f', '#e0b47a', '#6e7d2c', '#3c3c20', '#f0d9a8', '#8d5a2b', '#a5b04a']
for x0 in (252, 282, 313):
    shade(x0, 696, x0 + 14, 770)
    rect(x0, 696, x0 + 14, 770, '#f6ece0', '#b5653c', .7, 1.8)
    y = 698
    while y < 767:
        c = random.choice(NUT)
        rect(x0 + 1.5, y, x0 + 12.5, y + 4.5, '#ffffff', '#b9a68c', .3, 1)
        for k in range(5):
            a(f'<circle cx="{x0+3+k*2.1:.1f}" cy="{y+2.3+random.uniform(-.6,.6):.1f}" r=".9" fill="{c}"/>')
        y += 5.6
label(289, 712, 'פיצוחים / זיתים', '🥜', 7.5, color='#7a4a1e')

# ───────── ירקות ופירות ─────────
for x0 in (15, 66, 110, 155):
    crates_v(x0, 509, x0 + 18, 663)
for (y0, lb) in [(417, 'V1'), (445, 'V2'), (473, 'V3')]:
    crates_v(106, y0, 131, y0 + 17)
    rect(110, y0 + 4, 127, y0 + 13, 'rgba(255,253,248,.9)', '#9c5a3c', .5, 2)
    text(118.5, y0 + 8.7, lb, 6, '#7a3a1e', 900)
label(99, 588, 'ירקות ופירות', '🍎', 9.5, color='#2f7a1f')

# ───────── לחם ─────────
for x0 in (15, 69, 112):
    bread_v(x0, 692, x0 + 15, 772)
shade(31, 756, 69, 772)
rect(31, 756, 69, 772, '#e9d3b0', '#8d5a2b', .7, 1.8)
for k in range(6):
    a(f'<ellipse cx="{35+k*6}" cy="764" rx="2.6" ry="5" fill="{random.choice(["#c98a45", "#e2b46e", "#b5793e"])}" stroke="#7a4a1e" stroke-width=".3"/>')
bread_v(157, 695, 172, 775)
label(70, 730, 'לחם · לחמניות · עוגות', '🥖', 7, color='#7a4a1e')

# ───────── דלפקים (גבינות/מעדנייה/דגים/בשר/עוף) ─────────
GOODS = {'גבינות': (['#f5d76e', '#f1c40f', '#fff3c4', '#e6b450'], 'wedge'), 'מעדנייה': (['#e8a0a0', '#d86f6f', '#f3c6b8', '#b85c5c'], 'oval'),
         'דגים': (['#b8c4cf', '#8fa1b3', '#d7dee5', '#f39c8a'], 'fish'), 'בשר': (['#b8322a', '#d24a3f', '#9e2a22', '#e06b5f'], 'oval'),
         'עוף': (['#f3c6a0', '#e8b088', '#f7d9bd'], 'oval')}
for (x0, x1, he) in [(87, 153, 'גבינות'), (154, 220, 'מעדנייה'), (245, 293, 'דגים'), (293, 349, 'בשר'), (361, 416, 'עוף')]:
    for k in range(2):  # אנשי צוות מאחורי הדלפק
        person(x0 + (x1 - x0) * (k + 1) / 3, 828, 1.0, '#ffffff')
    shade(x0, 803, x1, 824, 3)
    rect(x0, 803, x1, 824, '#dfe7ee', '#0e7fb0', .8, 3)
    rect(x0 + 2, 805, x1 - 2, 820, 'url(#glass)', rx=2)
    pal, kind = GOODS[he]
    xx = x0 + 5
    while xx < x1 - 4:
        c = random.choice(pal)
        if kind == 'wedge':
            a(f'<path d="M{xx-2.5:.1f},{809.5} l5,-2 v4 z" fill="{c}" stroke="#c9a020" stroke-width=".3"/>')
        elif kind == 'fish':
            a(f'<path d="M{xx-3:.1f},{809} q3,-2.4 6,0 l1.5,-1.4 v2.8 l-1.5,-1.4 q-3,2.4 -6,0 z" fill="{c}" stroke="#6d7c8e" stroke-width=".3"/>')
        else:
            a(f'<ellipse cx="{xx:.1f}" cy="809" rx="2.5" ry="1.8" fill="{c}" stroke="rgba(0,0,0,.25)" stroke-width=".3"/>')
        xx += 5.6
    rect(x0 + 2, 805, x1 - 2, 807, 'rgba(255,255,255,.6)', rx=1)
    text((x0 + x1) / 2, 816.5, he, 7.5, '#0b3550', 900)

# ───────── קופות ─────────
rect(104, 16, 185, 159, 'rgba(207,171,111,.08)', '#a8864a', .8, 4, 'stroke-dasharray="4 3"')
for i in range(4):
    for j in range(2):
        cx, cy = 123 + j * 42, 32 + i * 29
        shade(cx - 9, cy - 7, cx + 9, cy + 7)
        rect(cx - 9, cy - 7, cx + 9, cy + 7, '#e9eef4', '#5a6b80', .7, 2)
        rect(cx - 6, cy - 5, cx + 6, cy, '#1b2a3e', rx=1)
        rect(cx - 5, cy - 4.2, cx + 5, cy - .8, '#3d8fd6', rx=.6)
        rect(cx - 6, cy + 1.5, cx + 6, cy + 4.5, '#CFAB6F', rx=1)
for (cx, cy) in [(144, 44), (144, 102)]:
    person(cx, cy, 1.3)
text(144.5, 151, 'קופות בשירות עצמי', 6.5, '#7a5a20', 900)
for y in (182, 215, 246, 276, 310):
    shade(140, y, 185, y + 16)
    rect(140, y, 185, y + 16, '#e9eef4', '#155f82', .7, 2)
    rect(142, y + 2.5, 168, y + 8, '#2e343a', rx=1)                 # מסוע
    for k in range(3):
        rect(144 + k * 7, y + 3.4, 148 + k * 7, y + 7, random.choice(PROD), rx=.5)
    rect(170, y + 2, 182, y + 13, '#cfd8e2', '#5a6b80', .4, 1)      # קופה רושמת
    rect(172, y + 3.5, 180, y + 7.5, '#1b2a3e', rx=.6)
    chair(172, y + 22 if y < 300 else y + 21)
    person(172, (y + 22 if y < 300 else y + 21) - 1, 1.15, '#c0392b')   # קופאית
    if y in (215, 276):
        shopper(198, y + 9)
rect(113, 188, 135, 310, '#fffdf8', '#203550', .7, 3)
text(124, 249, 'קופות', 8, '#203550', 900, rot=-90)

# ───────── דלפק שירות + כניסה ─────────
person(40, 317, 1.2, '#c0392b'); person(70, 317, 1.2, '#c0392b')
shade(16, 323, 100, 359, 3)
rect(16, 323, 100, 359, 'url(#desk)', '#2e343a', .8, 3)
rect(20, 326, 96, 332, '#9aa4ae', rx=2)
rect(26, 327, 36, 331, '#1b2a3e', rx=.6); rect(60, 327, 70, 331, '#1b2a3e', rx=.6)
text(58, 345, 'דלפק שירות', 8.5, '#ffffff', 900)
a('<line x1="18" y1="373.5" x2="179" y2="373.5" stroke="#203550" stroke-width="1.4" stroke-dasharray="6 4.5"/>')
rect(13, 361, 17, 400, '#bfe6f7', '#5fb4dc', .6, 1)   # דלתות זכוכית
a('<path d="M40,366 h-16 m0,0 l5,-4 m-5,4 l5,4" stroke="#7a8aa0" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
text(56, 366, 'יציאה', 6.5, '#5a6b80', 800)
a('<path d="M20,392 h16 m0,0 l-5,-4 m5,4 l-5,4" stroke="#2f7a1f" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
text(53, 392, 'כניסה', 6.5, '#2f7a1f', 900)
for k in range(3):   # עגלות בכניסה
    cart(32 + k * 4, 381, 1.1)
shade(158, 340, 181, 372)
rect(158, 340, 181, 372, '#fffdf8', '#5a6b80', .8, 2)   # סטנד E8 (במה ליד הכניסה, 9 מוצרים) — העיגול נוסף למטה עם שאר המקומות

# ───────── גונדולות + ראשים ─────────
ROWS = [(132, 152, 'H13', 'H12'), (185, 204, 'H14', 'H11'), (238, 258, 'H15', 'H10'), (308, 328, 'lego', 'H9'),
        (425, 445, 'Sbox1', 'H8'), (477, 497, 'Sbox2', 'H7'), (529, 549, 'H1', 'H6'), (583, 603, 'H2', 'H5'), (633, 652, 'H3', 'H4')]
for (y0, y1, L, R) in ROWS:
    gondola_h(234, y0, 408, y1)
for (y0, y1, L, R) in ROWS:
    for (x0, x1, lb) in [(206, 234, L), (408, 436, R)]:
        head_box(x0, y0 - 7, x1, y1 + 7)
for (y, n) in [(46, 14), (113, 13), (168.5, 12), (221.5, 11), (282.5, 10), (348, 9), (398, 8), (458, 6), (512, 5), (566, 4), (618, 3), (666, 2)]:
    aisle(324, y, n)

# קונים במעברים ובאזורים
for (cx, cy) in [(268, 168), (380, 221.5), (270, 282.5), (385, 348), (262, 398), (380, 458), (272, 566), (388, 618), (262, 666),
                 (272, 46), (388, 113), (520, 214), (530, 470), (60, 600), (140, 610), (250, 788), (390, 790), (60, 742), (300, 718)]:
    shopper(cx, cy)
person(460, 590, 1.4); person(470, 300, 1.4)

# ───────── סטנדים ממותגים 1–9 ─────────
for (y, n) in [(415, 1), (453, 2), (469.5, 3), (506, 4), (518.5, 5), (558, 6), (572.5, 7), (612, 8), (624.5, 9)]:
    a(f'<g class="brand" data-n="{n}" style="cursor:pointer">')
    a(f'<polygon points="{213},{y-6} {228},{y-6} {231},{y} {228},{y+6} {213},{y+6} {210},{y}" fill="#ff9f43" stroke="#c4581b" stroke-width=".9"/>')
    for k in range(3):
        rect(213.5 + k * 4.7, y - 4, 216.8 + k * 4.7, y + 4, random.choice(PROD), rx=.5)
    rect(231, y - 6, 244, y + 6, '#fffdf8', '#203550', .6, 2)
    text(237.5, y + .3, str(n), 6.5, '#203550', 900)
    a('</g>')

# ───────── במות/משטחים ─────────
for (lb, y0) in [('W6', 405), ('W5', 422), ('W4', 439), ('W3', 456), ('W2', 473), ('W1', 490)]:
    pallet(15, y0, 38, y0 + 16.5)
for i in range(7):
    pallet(90 + i * 18, 374.5, 108 + i * 18, 399)
for (x0, y0, x1, y1) in [(64, 413, 85, 435), (154, 413, 175, 435)]:
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#d9dde2', '#3a4a5c', 1, 2); rect(x0 + 5, y0 + 5, x1 - 5, y1 - 5, '#1b2a3e', rx=1)
for (x0, y0, x1, y1) in [(62, 444, 92, 461), (62, 472, 92, 489), (149, 444, 179, 461), (149, 472, 179, 489),
                         (338, 720, 365, 737), (338, 737, 365, 755), (419, 744, 445, 762), (419, 762, 445, 780), (419, 780, 445, 797), (419, 797, 445, 815)]:
    pallet(x0, y0, x1, y1)
for (x0, y0, x1, y1) in [(244, 772, 268, 790), (278, 772, 302, 790), (309, 772, 333, 790), (425, 725, 450, 743), (450, 725, 476, 743)]:
    shade(x0, y0, x1, y1)
    rect(x0, y0, x1, y1, '#f3a64a', '#a8641a', .7, 2)
    rect(x0 + 2, y0 + 2, x1 - 2, y0 + 6, '#ffffff', rx=1)

# ───────── קירות ─────────
a(f'<polygon points="{OUTLINE}" fill="none" stroke="#203550" stroke-width="3.2" stroke-linejoin="round"/>')
a('<line x1="100" y1="12" x2="100" y2="321" stroke="#203550" stroke-width="1.6"/>')
a('<line x1="14" y1="322" x2="100" y2="322" stroke="#203550" stroke-width="1.6"/>')
a('<line x1="105" y1="160" x2="187" y2="160" stroke="#203550" stroke-width="1.4" stroke-dasharray="6 4.5"/>')

# ───────── עיגולי מקומות מיוחדים (מעל הכל, ללא שינוי) ─────────
for (y0, y1, L, R) in ROWS:
    cy = (y0 + y1) / 2
    if L == 'lego':
        text(220, cy, 'lego', 7, '#5a6b80', 800)
    else:
        spot(220, cy, L, 11.5 if len(L) > 3 else 11)
    spot(422, cy, R, 11)
spot(221.5, 80.5, 'F2', 10.5); spot(420.5, 80.5, 'F1', 10.5)
spot(169.5, 356, 'E8', 9.5)
for (lb, y0) in [('W6', 405), ('W5', 422), ('W4', 439), ('W3', 456), ('W2', 473), ('W1', 490)]:
    spot(26.5, y0 + 8.25, lb, 8.2)
for i in range(7):
    spot(99 + i * 18, 386.7, f'E{i+1}', 8.2)
spot(74.5, 424, 'P1', 8.6); spot(164.5, 424, 'P4', 8.6)
spot(77, 452.5, 'P2', 8.2); spot(77, 480.5, 'P3', 8.2); spot(164, 452.5, 'P5', 8.2); spot(164, 480.5, 'P6', 8.2)
spot(351.5, 728.5, 'P8', 8.2); spot(351.5, 746, 'P7', 8.2)
spot(432, 753, 'P12', 8.6); spot(432, 771, 'P11', 8.6); spot(432, 788.5, 'P10', 8.6); spot(432, 806, 'P9', 8.2)
spot(256, 781, 'S1', 8.2); spot(290, 781, 'S2', 8.2); spot(321, 781, 'S3', 8.2); spot(437.5, 734, 'S4', 8.2); spot(463, 734, 'S5', 8.2)

a('</svg>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(E))
print('ok', OUT, sum(len(x) for x in E))
