#!/usr/bin/env python3
"""Генерує оригінальні SVG-ілюстрації для сайту про тірамісу."""
import os
import sys
import xml.etree.ElementTree as ET

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def shade(h, f):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(c * f))) for c in rgb(h))


def mix(a, b):
    return '#%02x%02x%02x' % tuple((x + y) // 2 for x, y in zip(rgb(a), rgb(b)))


def svg_wrap(w, h, title, desc, bg, body, rx=24):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-labelledby="t d">\n'
        f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n'
        f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>\n{body}\n</svg>\n'
    )


def save(name, content):
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    ET.parse(path)  # перевірка well-formed
    print('ok', name)


ST = 'stroke="#140a05" stroke-opacity="0.45" stroke-width="1"'


def prism(uid, top, dust, cream, ca, cb, topping=''):
    edge = shade(top, 0.7)
    pore = shade(cb, 0.8)
    mid = mix(ca, cb)
    defs = (
        f'<defs>'
        f'<linearGradient id="soak{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{ca}"/><stop offset="1" stop-color="{cb}"/></linearGradient>'
        f'<pattern id="pores{uid}" width="14" height="10" patternUnits="userSpaceOnUse">'
        f'<circle cx="3" cy="3" r="1.3" fill="{pore}" fill-opacity="0.6"/>'
        f'<circle cx="10" cy="7.5" r="1" fill="{pore}" fill-opacity="0.6"/></pattern>'
        f'<pattern id="dust{uid}" width="9" height="9" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="0.9" fill="{dust}" fill-opacity="0.75"/>'
        f'<circle cx="6.5" cy="6" r="0.7" fill="{dust}" fill-opacity="0.75"/></pattern>'
        f'</defs>'
    )
    side = (
        f'<polygon points="340,150 400,118 400,128 340,160" fill="{shade(edge, 0.8)}" {ST}/>'
        f'<polygon points="340,160 400,128 400,176 340,208" fill="{shade(cream, 0.8)}" {ST}/>'
        f'<polygon points="340,208 400,176 400,220 340,252" fill="{shade(mid, 0.8)}" {ST}/>'
        f'<polygon points="340,252 400,220 400,268 340,300" fill="{shade(cream, 0.8)}" {ST}/>'
        f'<polygon points="340,300 400,268 400,312 340,344" fill="{shade(mid, 0.8)}" {ST}/>'
    )
    front = (
        f'<rect x="80" y="150" width="260" height="10" fill="{edge}" {ST}/>'
        f'<rect x="80" y="160" width="260" height="48" fill="{cream}" {ST}/>'
        f'<rect x="80" y="208" width="260" height="44" fill="url(#soak{uid})" {ST}/>'
        f'<rect x="80" y="208" width="260" height="44" fill="url(#pores{uid})"/>'
        f'<rect x="80" y="252" width="260" height="48" fill="{cream}" {ST}/>'
        f'<rect x="80" y="300" width="260" height="44" fill="url(#soak{uid})" {ST}/>'
        f'<rect x="80" y="300" width="260" height="44" fill="url(#pores{uid})"/>'
    )
    top_face = (
        f'<polygon points="80,150 340,150 400,118 140,118" fill="{top}" {ST}/>'
        f'<polygon points="80,150 340,150 400,118 140,118" fill="url(#dust{uid})"/>'
    )
    return defs + side + front + top_face + topping


PLATE = (
    '<ellipse cx="240" cy="345" rx="222" ry="56" fill="#E9E1D3"/>'
    '<ellipse cx="240" cy="343" rx="178" ry="40" fill="#FBF7EF"/>'
    '<ellipse cx="244" cy="338" rx="168" ry="22" fill="#000" fill-opacity="0.22"/>'
)


def specks(color, pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' for x, y, r in pts)


SPECKS = [(150, 92, 2.2), (232, 70, 1.7), (300, 96, 2.4), (352, 62, 1.5), (190, 48, 1.3), (272, 36, 1.9), (118, 66, 1.4)]


def labels():
    rows = [(155, 'какао'), (184, 'крем'), (230, 'савоярді'), (276, 'крем'), (322, 'савоярді')]
    out = ''
    for y, text in rows:
        out += (
            f'<line x1="70" y1="{y}" x2="78" y2="{y}" stroke="#BDA98F" stroke-width="1"/>'
            f'<text x="66" y="{y + 4}" text-anchor="end" font-family="Consolas, monospace" '
            f'font-size="12.5" fill="#BDA98F">{text}</text>'
        )
    return out


def scene(uid, title, desc, bg, top, dust, cream, ca, cb, speck_color, topping='', with_labels=False):
    body = PLATE + prism(uid, top, dust, cream, ca, cb, topping) + specks(speck_color, SPECKS)
    if with_labels:
        body += labels()
    return svg_wrap(480, 430, title, desc, bg, body)


def strawberry(cx, cy):
    seeds = ''.join(
        f'<circle cx="{cx + dx}" cy="{cy + dy}" r="0.9" fill="#F7D56B"/>'
        for dx, dy in [(-5, -3), (4, -4), (0, 1), (-6, 4), (6, 3), (0, 8)]
    )
    return (
        f'<path d="M{cx} {cy + 13} C{cx - 16} {cy + 4} {cx - 13} {cy - 12} {cx} {cy - 10} '
        f'C{cx + 13} {cy - 12} {cx + 16} {cy + 4} {cx} {cy + 13} Z" fill="#D9304F" stroke="#8E1A31" stroke-width="1"/>'
        f'<path d="M{cx - 8} {cy - 10} L{cx} {cy - 17} L{cx + 8} {cy - 10} L{cx + 3} {cy - 8} '
        f'L{cx} {cy - 12} L{cx - 3} {cy - 8} Z" fill="#4E8B3A"/>' + seeds
    )


def caramel_topping():
    drizzle = (
        '<path d="M100 144 C130 124 150 150 180 132 S230 148 260 128 S310 146 340 126 S380 132 392 122" '
        'fill="none" stroke="#7A3F0C" stroke-width="4.5" stroke-linecap="round"/>'
        '<path d="M100 144 C130 124 150 150 180 132 S230 148 260 128 S310 146 340 126 S380 132 392 122" '
        'fill="none" stroke="#E7A545" stroke-width="1.6" stroke-linecap="round" stroke-opacity="0.8"/>'
    )
    salt = ''.join(
        f'<rect x="{x}" y="{y}" width="5" height="5" fill="#FFFFFF" transform="rotate({r} {x + 2} {y + 2})"/>'
        for x, y, r in [(150, 128, 20), (210, 140, -15), (270, 126, 35), (330, 134, 10), (240, 122, -30)]
    )
    return drizzle + salt


# --- hero + смаки ---
save('hero-tiramisu.svg', scene(
    'h', 'Шматок тірамісу в розрізі',
    'Шматок класичного тірамісу на білій тарілці: зверху какао, нижче по черзі шари крему маскарпоне та печива савоярді.',
    '#2B1B12', '#5E3519', '#8A5530', '#F4E8CB', '#D2A25F', '#93602E', '#A9724A', with_labels=True))

save('flavor-classic.svg', scene(
    'c', 'Класичне тірамісу', 'Шматок класичного тірамісу з какао зверху.',
    '#3A2418', '#5E3519', '#8A5530', '#F4E8CB', '#D2A25F', '#93602E', '#A9724A'))

save('flavor-matcha.svg', scene(
    'm', 'Тірамісу з матчею', 'Шматок тірамісу із зеленою пудрою матчі зверху та зеленкуватим кремом.',
    '#1F3322', '#6E9B4A', '#A5CC7A', '#E4EDCB', '#D2A25F', '#93602E', '#9CC272'))

straw = strawberry(190, 131) + strawberry(250, 128) + strawberry(310, 132)
save('flavor-strawberry.svg', scene(
    's', 'Полуничне тірамісу', 'Шматок тірамісу з рожевим кремом і свіжою полуницею на верхівці.',
    '#4A2230', '#E58AA0', '#F5B5C3', '#FBE3E3', '#D2A25F', '#93602E', '#F5B5C3', topping=straw))

save('flavor-caramel.svg', scene(
    'k', 'Тірамісу із солоною карамеллю', 'Шматок тірамісу з карамельною ниткою та кристаликами морської солі зверху.',
    '#4A2E14', '#C98A3C', '#E0A95A', '#F7E4BE', '#D2A25F', '#93602E', '#E0A95A', topping=caramel_topping()))


# --- історія: еспресо ---
def bean(cx, cy, rot, s=1.0):
    return (
        f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
        f'<ellipse rx="22" ry="14" fill="#4A2A15"/>'
        f'<ellipse cx="-6" cy="-6" rx="8" ry="3" fill="#7A4B27" fill-opacity="0.6"/>'
        f'<path d="M-20 0 C-8 -7 8 7 20 0" fill="none" stroke="#1E0F07" stroke-width="2.2" stroke-linecap="round"/></g>'
    )


espresso = (
    '<defs><radialGradient id="cof" cx="45%" cy="40%" r="65%">'
    '<stop offset="0" stop-color="#7A4B27"/><stop offset="0.6" stop-color="#3A1E0E"/><stop offset="1" stop-color="#22110A"/>'
    '</radialGradient></defs>'
    '<circle cx="215" cy="185" r="132" fill="#EFE7D8"/>'
    '<circle cx="215" cy="185" r="112" fill="#DCD1BE"/>'
    '<path d="M296 160 h52 a24 24 0 0 1 0 48 h-52" fill="none" stroke="#FBF7EF" stroke-width="15" stroke-linecap="round"/>'
    '<circle cx="215" cy="185" r="88" fill="#FBF7EF" stroke="#CFC5B2" stroke-width="2"/>'
    '<circle cx="215" cy="185" r="68" fill="url(#cof)"/>'
    '<ellipse cx="190" cy="160" rx="22" ry="9" fill="#FFFFFF" fill-opacity="0.22" transform="rotate(-25 190 160)"/>'
    + bean(70, 300, -20) + bean(400, 290, 25, 1.1) + bean(120, 330, 40, 0.9) + bean(430, 80, -35, 0.9) + bean(60, 60, 15, 0.8)
    + specks('#A9724A', [(380, 40, 2), (420, 150, 1.6), (30, 190, 1.8), (350, 330, 2.2), (260, 335, 1.4)])
)
save('story-espresso.svg', svg_wrap(
    480, 360, 'Чашка еспресо зверху',
    'Чашка міцного еспресо на блюдці, поруч розсипані кавові зерна.', '#3A2418', espresso))

# --- історія: савоярді ---
cookies = (
    '<defs><linearGradient id="ck" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#EBCB92"/><stop offset="1" stop-color="#C99A5B"/></linearGradient>'
    '<pattern id="sugar" width="12" height="10" patternUnits="userSpaceOnUse">'
    '<circle cx="3" cy="3" r="1" fill="#FFF6E0" fill-opacity="0.8"/><circle cx="9" cy="7" r="0.8" fill="#FFF6E0" fill-opacity="0.8"/>'
    '</pattern></defs>'
)
for y, rot in [(80, -6), (130, 4), (180, -3), (230, 6), (280, -4)]:
    cookies += (
        f'<g transform="translate(240 {y}) rotate({rot})">'
        f'<rect x="-125" y="-24" width="250" height="48" rx="22" fill="url(#ck)" stroke="#8A5A28" stroke-opacity="0.5"/>'
        f'<rect x="-125" y="-24" width="250" height="48" rx="22" fill="url(#sugar)"/>'
        f'<path d="M-100 -12 C-40 -18 40 -18 100 -12" fill="none" stroke="#FFF6E0" stroke-opacity="0.45" stroke-width="3" stroke-linecap="round"/></g>'
    )
save('story-savoiardi.svg', svg_wrap(
    480, 360, 'Печиво савоярді',
    'Стос довгастого печива савоярді, присипаного цукром.', '#2B1B12', cookies))

# --- застосунок ---
app = (
    '<rect x="50" y="20" width="260" height="600" rx="38" fill="#1B100B"/>'
    '<rect x="60" y="34" width="240" height="572" rx="30" fill="#FFF7E8"/>'
    '<rect x="140" y="42" width="80" height="8" rx="4" fill="#1B100B"/>'
    '<text x="80" y="88" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="700" fill="#2A170F">Тіра Мі Су</text>'
    '<text x="80" y="108" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="#6B5645">Доставка за 45–60 хв</text>'
    '<rect x="76" y="124" width="208" height="190" rx="18" fill="#2B1B12"/>'
    '<ellipse cx="180" cy="244" rx="82" ry="11" fill="#EFE7D8"/>'
    '<rect x="112" y="150" width="136" height="7" fill="#5E3519"/>'
    '<rect x="112" y="157" width="136" height="22" fill="#F4E8CB"/>'
    '<rect x="112" y="179" width="136" height="20" fill="#C99A5B"/>'
    '<rect x="112" y="199" width="136" height="22" fill="#F4E8CB"/>'
    '<rect x="112" y="221" width="136" height="20" fill="#C99A5B"/>'
    '<text x="92" y="274" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700" fill="#F3E8D5">Класичний</text>'
    '<text x="92" y="296" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#FFC53D">95 грн</text>'
    '<rect x="76" y="334" width="208" height="44" rx="22" fill="#FFC53D"/>'
    '<text x="180" y="361" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700" fill="#1B100B">Замовити</text>'
    '<rect x="76" y="396" width="208" height="56" rx="14" fill="#E9DEC9"/>'
    '<text x="92" y="429" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#2A170F">Матча · 110 грн</text>'
    '<rect x="76" y="462" width="208" height="56" rx="14" fill="#E9DEC9"/>'
    '<text x="92" y="495" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#2A170F">Полуничний · 105 грн</text>'
    '<line x1="60" y1="548" x2="300" y2="548" stroke="#E0D3BC"/>'
    '<circle cx="110" cy="578" r="8" fill="#6B5645" fill-opacity="0.45"/>'
    '<circle cx="180" cy="578" r="8" fill="#FFC53D"/>'
    '<circle cx="250" cy="578" r="8" fill="#6B5645" fill-opacity="0.45"/>'
)
save('app-mockup.svg', svg_wrap(
    360, 640, 'Мобільний застосунок Тіра Мі Су',
    'Екран застосунку: картка класичного тірамісу з ціною 95 грн, кнопка «Замовити» і список інших смаків.',
    '#F4ECDD', app))
