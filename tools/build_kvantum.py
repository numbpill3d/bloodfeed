#!/usr/bin/env python3
"""Bloodfeed Kvantum theme: KvArcDark's engine map, recoloured.

Greys are remapped by luminance onto a blood-black ramp; blue accents become
crimson; reds become the VHS REC scarlet. GeneralColors are set from the palette.
"""
import colorsys, re, shutil, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
import palette as P

SRC = Path("/usr/share/Kvantum/KvArcDark")
OUT = R / "kvantum/Bloodfeed"
OUT.mkdir(parents=True, exist_ok=True)

def lum(h):
    r, g, b = P.rgb(h)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255

def lerp(a, b, t):
    A, B = P.rgb(a), P.rgb(b)
    return "#%02x%02x%02x" % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))

RAMP = [(0.0, "#000000"), (0.07, P.VOID), (0.145, "#160708"), (0.20, P.BASE), (0.235, "#220c0e"),
        (0.26, P.SURFACE), (0.30, "#301015"), (0.34, "#40151b"), (0.45, "#982434"), (0.58, "#ac525e"),
        (0.85, P.TEXT), (1.0, P.TEXT_HI)]

def grey(h):
    L = lum(h)
    for (l0, c0), (l1, c1) in zip(RAMP, RAMP[1:]):
        if L <= l1:
            return lerp(c0, c1, (L - l0) / (l1 - l0) if l1 > l0 else 0)
    return P.TEXT_HI

def remap(m):
    h = m.group(0).lower()
    r, g, b = (v / 255 for v in P.rgb(h))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    deg = hh * 360
    if ss > 0.45 and 195 <= deg <= 235:           # arc blue -> crimson
        nr, ng, nb = colorsys.hls_to_rgb(351 / 360, min(0.52, ll * 0.85), min(1, ss * 0.95))
    elif ss > 0.45 and 260 <= deg <= 300:         # arc purple -> rose
        nr, ng, nb = colorsys.hls_to_rgb(342 / 360, ll, ss * 0.85)
    elif ss > 0.45 and (deg < 20 or deg > 340):   # red -> REC scarlet
        return P.NEGATIVE
    else:
        return grey(h)
    return "#%02x%02x%02x" % tuple(round(v * 255) for v in (nr, ng, nb))

HEX = re.compile(r"#[0-9a-fA-F]{6}\b")
svg = HEX.sub(remap, (SRC / "KvArcDark.svg").read_text())
# text fields sit recessed (darker than buttons)
svg = re.sub(r'style="fill:#[0-9a-fA-F]{6}" id="lineedit-(normal|focused|disabled|toggled|pressed)"',
             lambda m: f'style="fill:{"#18080a" if m.group(1) != "disabled" else P.BASE}" id="lineedit-{m.group(1)}"', svg)
(OUT / "Bloodfeed.svg").write_text(svg)

cfg = (SRC / "KvArcDark.kvconfig").read_text()
cfg = HEX.sub(remap, cfg)
cfg = cfg.replace("#ffffffc8", P.TEXT).replace("#ffffff96", P.TEXT_DIM).replace("#ffffff78", P.TEXT_MUTE)
cfg = cfg.replace("#ffffffb4", P.TEXT).replace("#ffffffd2", P.TEXT_HI)
general = f"""[GeneralColors]
window.color={P.BASE}
base.color={P.ABYSS}
alt.base.color=#110607
button.color={P.RAISED}
light.color={P.EDGE_HI}
mid.light.color={P.EDGE}
dark.color={P.VOID}
mid.color={P.SURFACE}
highlight.color={P.SELECT}
inactive.highlight.color={P.CRIMSON_DEEP}
text.color={P.TEXT}
window.text.color={P.TEXT}
button.text.color={P.TEXT}
disabled.text.color={P.TEXT_MUTE}
tooltip.text.color={P.TEXT_HI}
highlight.text.color={P.TEXT_HI}
link.color={P.LINK}
link.visited.color={P.VISITED}
progress.indicator.text.color={P.TEXT_HI}
"""
cfg = re.sub(r"\[GeneralColors\].*?(?=\n\[)", general.rstrip(), cfg, flags=re.S)
cfg = re.sub(r"(?m)^comment=.*$", "comment=Bloodfeed — blood-black surfaces, crimson glow accents", cfg)
cfg = re.sub(r"(?m)^author=.*$", "author=splicer scorn; engine map adapted from KvArcDark by Tsu Jan", cfg)
# translucent menus/tooltips with blur, like the panel
cfg = re.sub(r"(?m)^translucent_windows=.*$", "translucent_windows=false", cfg)
cfg = re.sub(r"(?m)^popup_blurring=.*$", "popup_blurring=true", cfg)
(OUT / "Bloodfeed.kvconfig").write_text(cfg)
for f in ("LICENSE", "UPSTREAM-LICENSE-KVANTUM", "NOTICE"):
    p = Path.home() / ".config/Kvantum/Arterial" / f
    if p.exists():
        shutil.copy(p, OUT / f)
print("kvantum ->", OUT)
