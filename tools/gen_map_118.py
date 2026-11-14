# -*- coding: utf-8 -*-
"""מפת סניף 118 לפריסה+ — SVG מאויר, לפי הקואורדינטות של 'מפת החנות 118.docx' (נקודות PDF, 595x842).
הרצה: python tools/gen_map_118.py  → map-118.svg
"""
import random, os
random.seed(118)
OUT = os.path.join(os.path.dirname(__file__), '..', 'map-118.svg')
E = []
a = E.append
PROD = ['#e8483b', '#f39c34', '#f5c842', '#58b85c', '#3d8fd6', '#8a5cc2', '#e86a9a', '#2bb3a8', '#f0e6d2']

def rect(x0, y0, x1, y1, fill, stroke='none', sw=0, rx=0, extra=''):
    a(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

def text(x, y, s, size=9, fill='#203550', w=800, rot=0, anchor='middle', extra=''):
    t = f' transform="rotate({rot} {x} {y})"' if rot else ''
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="central"{t} {extra}>{s}</text>')

def stock_h(x0, y0, x1, y1, pal=PROD):
    """שורת מוצרים אופקית (מדף נראה מלמעלה)"""
    x = x0
    while x < x1 - 1:
        w = random.uniform(3.2, 6.5)
        w = min(w, x1 - x)
        rect(x, y0, x + w - .6, y1, random.choice(pal), rx=.8)
        x += w

def stock_v(x0, y0, x1, y1, pal=PROD):
    y = y0
    while y < y1 - 1:
        h = random.uniform(3.2, 6.5)
        h = min(h, y1 - y)
        rect(x0, y, x1, y + h - .6, random.choice(pal), rx=.8)
        y += h

def gondola_h(x0, y0, x1, y1):
    rect(x0 + 1.5, y0 + 2, x1 + 1.5, y1 + 2, 'rgba(20,35,56,.18)', rx=2)  # צל
    rect(x0, y0, x1, y1, '#dfe4ea', '#9aa7b6', .6, 2)
    m = (y0 + y1) / 2
    stock_h(x0 + 2, y0 + 1.6, x1 - 2, m - .8)
    stock_h(x0 + 2, m + .8, x1 - 2, y1 - 1.6)
    a(f'<line x1="{x0+1}" y1="{m}" x2="{x1-1}" y2="{m}" stroke="#8e9bab" stroke-width="1"/>')

def shelf_v(x0, y0, x1, y1, base='#dfe4ea', edge='#9aa7b6', pal=PROD):
    rect(x0 + 1.2, y0 + 1.5, x1 + 1.2, y1 + 1.5, 'rgba(20,35,56,.16)', rx=2)
    rect(x0, y0, x1, y1, base, edge, .6, 2)
    stock_v(x0 + 1.4, y0 + 2, x1 - 1.4, y1 - 2, pal)

def shelf_h(x0, y0, x1, y1, base='#dfe4ea', edge='#9aa7b6', pal=PROD):
    rect(x0 + 1.2, y0 + 1.5, x1 + 1.2, y1 + 1.5, 'rgba(20,35,56,.16)', rx=2)
    rect(x0, y0, x1, y1, base, edge, .6, 2)
    stock_h(x0 + 2, y0 + 1.4, x1 - 2, y1 - 1.4, pal)

def zone(cx, cy, rx, ry, color):
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="4 3"/>')

def label(x, y, he, emoji='', size=10, rot=0, color='#203550'):
    s = (emoji + ' ' if emoji else '') + he
    a(f'<g class="lbl"{f" transform=\"rotate({rot} {x} {y})\"" if rot else ""}>')
    w = len(s) * size * .52 + 10
    rect(x - w / 2, y - size * .78, x + w / 2, y + size * .78, 'rgba(255,253,248,.92)', color, .6, size * .7)
    text(x, y + .5, s, size, color, 800)
    a('</g>')

def head_box(x0, y0, x1, y1):
    rect(x0 + 1.5, y0 + 2, x1 + 1.5, y1 + 2, 'rgba(20,35,56,.22)', rx=3)
    rect(x0, y0, x1, y1, '#fffdf8', '#203550', 1, 3)
    # מדפים קטנים
    for i in range(1, 4):
        yy = y0 + (y1 - y0) * i / 4
        a(f'<line x1="{x0+3}" y1="{yy:.1f}" x2="{x1-3}" y2="{yy:.1f}" stroke="#CFAB6F" stroke-width=".7"/>')

def pallet(x0, y0, x1, y1):
    rect(x0 + 1, y0 + 1.5, x1 + 1, y1 + 1.5, 'rgba(20,35,56,.22)', rx=1.5)
    rect(x0, y0, x1, y1, '#c48a4f', '#7a5230', .6, 1.5)
    n = max(2, int((x1 - x0) / 6))
    for i in range(1, n):
        xx = x0 + (x1 - x0) * i / n
        a(f'<line x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y1}" stroke="#8d6038" stroke-width=".5"/>')
    rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, '#e0b47a', '#9c6d3f', .5, 1)

def spot(cx, cy, label_, r=11, size=None):
    size = size or (8.6 if len(label_) <= 2 else 7.4 if len(label_) <= 3 else 6.2)
    a(f'<g class="spot" data-id="{label_}" style="cursor:pointer">')
    a(f'<circle cx="{cx}" cy="{cy+1.4}" r="{r}" fill="rgba(20,35,56,.35)"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f7f1e3" stroke="#203550" stroke-width="1.1"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r-2}" fill="none" stroke="#CFAB6F" stroke-width=".6"/>')
    text(cx, cy + .4, label_, size, '#1b2a3e', 900, extra='class="sl"')
    a(f'<circle class="dot" cx="{cx + r*.72:.1f}" cy="{cy - r*.72:.1f}" r="3.2" fill="#9aa7b6" stroke="#fff" stroke-width=".8"/>')
    a('</g>')

def person(cx, cy, s=1, color='#203550'):
    a(f'<circle cx="{cx}" cy="{cy - 3*s}" r="{2.2*s}" fill="{color}"/>')
    a(f'<path d="M{cx-3.6*s},{cy+3*s} q{3.6*s},{-6.5*s} {7.2*s},0 z" fill="{color}"/>')

def chair(cx, cy):
    rect(cx - 3, cy - 3, cx + 3, cy + 3, '#CFAB6F', '#8a6c3a', .5, 1.5)
    rect(cx + 2.4, cy - 3.5, cx + 4.2, cy + 3.5, '#8a6c3a', rx=.8)

# ───────── קנבס ─────────
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 845" font-family="Heebo, Arial, sans-serif" direction="rtl">')
a('<defs><pattern id="tile" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#f6f1e6"/>'
  '<path d="M14 0H0V14" fill="none" stroke="#e7dfcf" stroke-width=".6"/></pattern>'
  '<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#e9e5dc"/><line x1="0" y1="0" x2="0" y2="8" stroke="#d6d0c3" stroke-width="3"/></pattern>'
  '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe6f7"/><stop offset="1" stop-color="#5fb4dc"/></linearGradient>'
  '<linearGradient id="frz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c67bd0"/><stop offset="1" stop-color="#8e3b9c"/></linearGradient>'
  '<linearGradient id="cool" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a7aa3"/><stop offset="1" stop-color="#15506e"/></linearGradient>'
  '</defs>')
a('<rect width="600" height="845" fill="#fbf9f4"/>')
OUTLINE = '13,10 586,10 586,551 494,551 494,744 446,744 446,833 84,833 84,772 13,772'
a(f'<polygon points="{OUTLINE}" fill="url(#tile)"/>')
# שטח אחורי (מחסן)
rect(15, 12, 100, 321, 'url(#hatch)')

# ───────── אזורים (רקע) ─────────
zone(508, 133, 62, 113, '#155f82')      # חלב
zone(514, 408, 62, 140, '#0e9ed4')      # פארם
zone(99, 589, 80, 82, '#4ea72d')        # ירקות
zone(72, 734, 51, 52, '#4ea72d')        # לחם
zone(286, 734, 46, 37, '#4ea72d')       # פיצוחים

# ───────── קפואים ─────────
rect(214, 12, 433, 25, 'url(#frz)', '#6d2a78', .6, 2)
stock_h(216, 14, 431, 23, ['#f3d6f7', '#ffffff', '#e2b8ea', '#cfe8ff'])
label(323, 18.5, 'קפואים', '❄', 7, color='#6d2a78')
rect(236, 63, 406, 80, 'url(#frz)', '#6d2a78', .6, 2)
stock_h(238, 65, 404, 78, ['#f3d6f7', '#ffffff', '#e2b8ea', '#cfe8ff'])
label(321, 71.5, 'קפואים', '❄', 7, color='#6d2a78')
gondola_h(236, 80, 406, 99)
for (x0, x1, lb) in [(207, 236, 'F2'), (406, 435, 'F1')]:
    rect(x0 + 1.5, 65, x1 + 1.5, 100, 'rgba(20,35,56,.22)', rx=3)
    rect(x0, 63, x1, 98, '#f0c3f5', '#8e3b9c', 1, 3)
    stock_v(x0 + 4, 67, x1 - 4, 94, ['#ffffff', '#e2b8ea', '#cfe8ff'])

# ───────── חלב ─────────
rect(434, 12, 564, 25, 'url(#cool)', '#042333', .6, 2); stock_h(436, 14, 562, 23, ['#ffffff', '#dff1fb', '#f6e7a8', '#bfe0f2'])
rect(566, 11, 584, 262, 'url(#cool)', '#042333', .6, 2); stock_v(568, 13, 582, 260, ['#ffffff', '#dff1fb', '#f6e7a8', '#bfe0f2'])
rect(503, 250, 564, 262, 'url(#cool)', '#042333', .6, 2); stock_h(505, 252, 562, 260, ['#ffffff', '#dff1fb', '#bfe0f2'])
for (x0, y0, x1, y1) in [(466, 94, 547, 117), (468, 167, 550, 190)]:
    rect(x0 + 1.5, y0 + 2, x1 + 1.5, y1 + 2, 'rgba(20,35,56,.18)', rx=2)
    rect(x0, y0, x1, y1, 'url(#cool)', '#042333', .6, 2)
    stock_h(x0 + 2, y0 + 2, x1 - 2, (y0 + y1) / 2 - .6, ['#ffffff', '#dff1fb', '#f6e7a8'])
    stock_h(x0 + 2, (y0 + y1) / 2 + .6, x1 - 2, y1 - 2, ['#ffffff', '#dff1fb', '#f6e7a8'])
label(508, 141, 'מוצרי חלב', '🥛', 9.5, color='#155f82')
rect(450, 240, 478, 254, '#fff7e0', '#a8864a', .6, 2); text(464, 247.5, '🥚 ביצים', 5.5, '#7a5a20', 900)

# ───────── פארם ─────────
shelf_h(468, 263, 584, 276, '#d8eef9', '#0e9ed4', ['#ffffff', '#ffd1e0', '#bfe6f7', '#d7f3d0', '#fff1b8'])
shelf_h(472, 537, 584, 550, '#d8eef9', '#0e9ed4', ['#ffffff', '#ffd1e0', '#bfe6f7', '#d7f3d0', '#fff1b8'])
shelf_v(567, 276, 584, 536, '#d8eef9', '#0e9ed4', ['#ffffff', '#ffd1e0', '#bfe6f7', '#d7f3d0', '#fff1b8'])
for (x0, y0, x1, y1) in [(468, 316, 545, 326), (468, 357, 544, 367), (468, 396, 545, 406), (472, 493, 548, 503), (476, 446, 537, 458)]:
    shelf_h(x0, y0, x1, y1, '#d8eef9', '#0e9ed4', ['#ffffff', '#ffd1e0', '#bfe6f7', '#d7f3d0', '#fff1b8'])
label(512, 428, 'פארם והיגיינה', '🧴', 9, color='#0b6f97')

# ───────── שתייה חריפה / בירות ─────────
shelf_v(471, 552, 491, 719, '#ffe0c7', '#c4581b', ['#7a2e10', '#c4581b', '#3c6e2f', '#e9c46a', '#5b3a29'])
label(481, 636, 'שתייה חריפה', '🍷', 8, rot=-90, color='#a4461a')
shelf_h(341, 680, 427, 701, '#e3efe0', '#186b23', ['#f5c842', '#3c6e2f', '#c4581b', '#ffffff', '#8d6038'])
label(384, 690.5, 'בירות', '🍺', 8, color='#186b23')

# ───────── שתייה קלה ─────────
shelf_v(208, 695, 238, 774, '#e3efe0', '#186b23', ['#e8483b', '#3d8fd6', '#58b85c', '#f39c34', '#ffffff'])
label(223, 734, 'שתייה קלה 1.5 ל׳', '🥤', 7, rot=-90, color='#186b23')

# ───────── פיצוחים / זיתים ─────────
for x0 in (252, 282, 313):
    shelf_v(x0, 696, x0 + 14, 770, '#fbe3d6', '#b5653c', ['#c48a4f', '#e0b47a', '#6e7d2c', '#3c3c20', '#f0d9a8'])
label(289, 712, 'פיצוחים / זיתים', '🥜', 7.5, color='#7a4a1e')

# ───────── ירקות ופירות ─────────
VEG = ['#e8483b', '#58b85c', '#f39c34', '#f5c842', '#8bc34a', '#c0392b', '#6a3d9a']
for x0 in (15, 66, 110, 155):
    shelf_v(x0, 509, x0 + 18, 663, '#d7f0d4', '#3c8a2a', VEG)
for (y0, lb) in [(417, 'V1'), (445, 'V2'), (473, 'V3')]:
    rect(107, y0 + 1.5, 132, y0 + 18.5, 'rgba(20,35,56,.2)', rx=2)
    rect(106, y0, 131, y0 + 17, '#f6c5ac', '#9c5a3c', .8, 2)
    text(118.5, y0 + 8.7, lb, 6.5, '#7a3a1e', 900)
label(99, 588, 'ירקות ופירות', '🍎', 9.5, color='#2f7a1f')

# ───────── לחם ─────────
BR = ['#d9a066', '#b5793e', '#f0d09a', '#8d5a2b', '#e8c38a']
for x0 in (15, 69, 112):
    shelf_v(x0, 692, x0 + 15, 772, '#f3e3cc', '#8d5a2b', BR)
shelf_h(31, 756, 69, 772, '#f3e3cc', '#8d5a2b', BR)
shelf_v(157, 695, 172, 775, '#fbe3d6', '#b5653c', BR)
label(70, 730, 'לחם · לחמניות · עוגות', '🥖', 7, color='#7a4a1e')

# ───────── דלפקים (גבינות/מעדנייה/דגים/בשר/עוף) ─────────
for (x0, x1, he) in [(87, 153, 'גבינות'), (154, 220, 'מעדנייה'), (245, 293, 'דגים'), (293, 349, 'בשר'), (361, 416, 'עוף')]:
    rect(x0 + 1.5, 805, x1 + 1.5, 826, 'rgba(20,35,56,.2)', rx=3)
    rect(x0, 803, x1, 824, 'url(#glass)', '#0e7fb0', .8, 3)
    rect(x0 + 3, 806, x1 - 3, 811, 'rgba(255,255,255,.55)', rx=1.5)
    text((x0 + x1) / 2, 817, he, 7.5, '#0b3550', 900)
    person((x0 + x1) / 2, 829, .9)

# ───────── קופות ─────────
rect(104, 16, 185, 159, 'rgba(207,171,111,.10)', '#a8864a', .8, 4, 'stroke-dasharray="4 3"')
for i in range(4):
    for j in range(2):
        cx, cy = 123 + j * 42, 34 + i * 30
        rect(cx - 9, cy - 7, cx + 9, cy + 7, '#e9eef4', '#5a6b80', .7, 2)
        rect(cx - 5, cy - 5, cx + 5, cy - 1, '#203550', rx=1)
        rect(cx - 6, cy + 1, cx + 6, cy + 4, '#CFAB6F', rx=1)
text(144.5, 151, 'קופות בשירות עצמי', 6.5, '#7a5a20', 900)
for y in (182, 215, 246, 276, 310):
    rect(141, y + 1.5, 187, y + 17.5, 'rgba(20,35,56,.18)', rx=2)
    rect(140, y, 185, y + 16, '#e9eef4', '#155f82', .7, 2)
    rect(143, y + 3, 170, y + 8, '#3a4a5c', rx=1)            # מסוע
    chair(170, y + 22 if y < 300 else y + 21)
    a(f'<path d="M{176},{y+6} l8,-3 v6 z" fill="#155f82" opacity=".55"/>')
rect(113, 188, 135, 310, '#fffdf8', '#203550', .7, 3)
text(124, 249, 'קופות', 8, '#203550', 900, rot=-90)

# ───────── דלפק שירות + כניסה ─────────
rect(17, 325, 101, 361, 'rgba(20,35,56,.25)', rx=3)
rect(16, 323, 100, 359, '#5d6670', '#2e343a', .8, 3)
rect(20, 327, 96, 333, '#7d8792', rx=2)
text(58, 344, 'דלפק שירות', 8.5, '#ffffff', 900)
a('<line x1="18" y1="373.5" x2="179" y2="373.5" stroke="#203550" stroke-width="1.4" stroke-dasharray="6 4.5"/>')
a('<path d="M40,366 h-16 m0,0 l5,-4 m-5,4 l5,4" stroke="#7a8aa0" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
text(56, 366, 'יציאה', 6.5, '#5a6b80', 800)
a('<path d="M20,392 h16 m0,0 l-5,-4 m5,4 l-5,4" stroke="#2f7a1f" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
text(53, 392, 'כניסה', 6.5, '#2f7a1f', 900)
rect(158, 340, 181, 372, '#fffdf8', '#5a6b80', .8, 2); text(169.5, 356, 'HI', 7, '#5a6b80', 900)

# ───────── גונדולות + ראשים ─────────
ROWS = [(132, 152, 'H13', 'H12'), (185, 204, 'H14', 'H11'), (238, 258, 'H15', 'H10'), (308, 328, 'lego', 'H9'),
        (425, 445, 'Sbox1', 'H8'), (477, 497, 'Sbox2', 'H7'), (529, 549, 'H1', 'H6'), (583, 603, 'H2', 'H5'), (633, 652, 'H3', 'H4')]
for (y0, y1, L, R) in ROWS:
    gondola_h(234, y0, 408, y1)
for (y0, y1, L, R) in ROWS:
    for (x0, x1, lb) in [(206, 234, L), (408, 436, R)]:
        head_box(x0, y0 - 7, x1, y1 + 7)
# מספרי מעברים
for (y, n) in [(46, 14), (113, 13), (168.5, 12), (221.5, 11), (282.5, 10), (348, 9), (398, 8), (458, 6), (512, 5), (566, 4), (618, 3), (666, 2)]:
    rect(305, y - 7.5, 343, y + 7.5, '#203550', rx=7.5)
    text(324, y + .3, f'מעבר {n}', 7, '#E8D3A6', 800)

# ───────── סטנדים ממותגים 1–9 ─────────
for (y, n) in [(415, 1), (453, 2), (469.5, 3), (506, 4), (518.5, 5), (558, 6), (572.5, 7), (612, 8), (624.5, 9)]:
    a(f'<g class="brand" data-n="{n}" style="cursor:pointer">')
    a(f'<polygon points="{213},{y-6} {228},{y-6} {231},{y} {228},{y+6} {213},{y+6} {210},{y}" fill="#e6f5fc" stroke="#0e9ed4" stroke-width=".9"/>')
    rect(231, y - 6, 244, y + 6, '#fffdf8', '#203550', .6, 2)
    text(237.5, y + .3, str(n), 6.5, '#203550', 900)
    a('</g>')

# ───────── במות/משטחים ─────────
for (lb, y0) in [('W6', 405), ('W5', 422), ('W4', 439), ('W3', 456), ('W2', 473), ('W1', 490)]:
    pallet(15, y0, 38, y0 + 16.5)
for i in range(5):
    pallet(90 + i * 18, 374.5, 108 + i * 18, 399)
for (x0, y0, x1, y1) in [(64, 413, 85, 435), (154, 413, 175, 435)]:
    rect(x0 + 1.5, y0 + 1.5, x1 + 1.5, y1 + 1.5, 'rgba(20,35,56,.25)', rx=2)
    rect(x0, y0, x1, y1, '#d9dde2', '#3a4a5c', 1, 2); rect(x0 + 5, y0 + 5, x1 - 5, y1 - 5, '#1b2a3e', rx=1)
for (x0, y0, x1, y1) in [(62, 444, 92, 461), (62, 472, 92, 489), (149, 444, 179, 461), (149, 472, 179, 489),
                         (338, 720, 365, 737), (338, 737, 365, 755), (419, 744, 445, 762), (419, 762, 445, 780), (419, 780, 445, 797), (419, 797, 445, 815)]:
    pallet(x0, y0, x1, y1)
for (x0, y0, x1, y1) in [(244, 772, 268, 790), (278, 772, 302, 790), (309, 772, 333, 790), (425, 725, 450, 743), (450, 725, 476, 743)]:
    rect(x0 + 1, y0 + 1.5, x1 + 1, y1 + 1.5, 'rgba(20,35,56,.22)', rx=2)
    rect(x0, y0, x1, y1, '#f3a64a', '#a8641a', .7, 2)
    rect(x0 + 2, y0 + 2, x1 - 2, y0 + 6, '#ffffff', rx=1)

# ───────── קירות ─────────
a(f'<polygon points="{OUTLINE}" fill="none" stroke="#203550" stroke-width="3.2" stroke-linejoin="round"/>')
a('<line x1="100" y1="12" x2="100" y2="321" stroke="#203550" stroke-width="1.6"/>')
a('<line x1="14" y1="322" x2="100" y2="322" stroke="#203550" stroke-width="1.6"/>')
a('<line x1="105" y1="160" x2="187" y2="160" stroke="#203550" stroke-width="1.4" stroke-dasharray="6 4.5"/>')

# ───────── עיגולי מקומות מיוחדים (מעל הכל) ─────────
for (y0, y1, L, R) in ROWS:
    cy = (y0 + y1) / 2
    if L == 'lego':
        text(220, cy, 'lego', 7, '#5a6b80', 800)
    else:
        spot(220, cy, L, 11.5 if len(L) > 3 else 11)
    spot(422, cy, R, 11)
spot(221.5, 80.5, 'F2', 10.5); spot(420.5, 80.5, 'F1', 10.5)
for (lb, y0) in [('W6', 405), ('W5', 422), ('W4', 439), ('W3', 456), ('W2', 473), ('W1', 490)]:
    spot(26.5, y0 + 8.25, lb, 8.2)
for i in range(5):
    spot(99 + i * 18, 386.7, f'E{i+1}', 8.2)
spot(74.5, 424, 'P1', 8.6); spot(164.5, 424, 'P4', 8.6)
spot(77, 452.5, 'P2', 8.2); spot(77, 480.5, 'P3', 8.2); spot(164, 452.5, 'P5', 8.2); spot(164, 480.5, 'P6', 8.2)
spot(351.5, 728.5, 'P8', 8.2); spot(351.5, 746, 'P7', 8.2)
spot(432, 753, 'P12', 8.6); spot(432, 771, 'P11', 8.6); spot(432, 788.5, 'P10', 8.6); spot(432, 806, 'P9', 8.2)
spot(256, 781, 'S1', 8.2); spot(290, 781, 'S2', 8.2); spot(321, 781, 'S3', 8.2); spot(437.5, 734, 'S4', 8.2); spot(463, 734, 'S5', 8.2)

a('</svg>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(E))
print('ok', OUT, sum(len(x) for x in E))
