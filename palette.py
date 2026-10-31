"""Bloodfeed palette: one source of truth for every generator.

The Bloodfeed tape, re-dubbed in blood: the same wallpaper face remapped onto a
crimson ramp. Surfaces are red-black, never #000; glow and accents are crimson.
"""
from pathlib import Path
SOURCE_WALLPAPER = "/home/scorn/Pictures/1b6c35a7-578c-4fb3-a811-1bed374eeaf5.png"
WALLPAPER = str(Path(__file__).resolve().parent / "assets/wallpaper-blood.png")  # tools/build_wallpaper.py

# surfaces, darkest -> lightest (all carry a red cast so they read as "tinted")
VOID    = "#0a0304"   # deepest: shadows, splash base
ABYSS   = "#0e0506"   # view / text-field background
BASE    = "#150809"   # window background
SURFACE = "#1d0a0d"   # header / alt rows / panel
RAISED  = "#290e12"   # buttons
EDGE    = "#45141b"   # borders
EDGE_HI = "#641c25"

# wallpaper oxblood (the face's mid-tones)
OXBLOOD_LO = "#3f0b12"
OXBLOOD    = "#6e1120"
OXBLOOD_HI = "#98182b"
FLESH      = "#e88a90"   # brightest wallpaper tone (eye whites)

# crimson glow: the accent
CRIMSON_DEEP = "#3a0911"
CRIMSON_LO   = "#8c1024"
CRIMSON      = "#dc1f3c"
CRIMSON_HI   = "#ff5368"
CRIMSON_GLOW = "#ffa3ad"

# text: bone, warmed toward ash-pink
TEXT      = "#e8d2d0"
TEXT_HI   = "#fff1ef"
TEXT_DIM  = "#a87e80"
TEXT_MUTE = "#6b4549"

# states: negative is a hotter orange-scarlet so it never blends into the accent
NEGATIVE = "#ff6a2b"
NEUTRAL  = "#d9a24e"
POSITIVE = "#6fbf9c"
LINK     = "#ff7d8c"
VISITED  = "#d0688f"

# selection: dim, not neon
SELECT    = "#5a0d1a"
SELECT_HI = "#7a1426"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def csv(h):
    return ",".join(map(str, rgb(h)))
