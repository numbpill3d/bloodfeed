#!/usr/bin/env python3
"""Re-dub the Nightfeed wallpaper in blood: brightness -> crimson ramp.

Brightness (max channel) picks a point on a black -> oxblood -> crimson ramp;
whiteness (min channel) lifts the hottest spots (eye whites) toward flesh-pink.
The source file is only read.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import palette as P

src = np.asarray(Image.open(P.SOURCE_WALLPAPER).convert("RGB")).astype(np.float32) / 255
v = src.max(axis=2)
w = src.min(axis=2)
stops = [(0.00, (2, 0, 1)), (0.10, (14, 2, 4)), (0.30, P.rgb(P.OXBLOOD_LO)), (0.55, P.rgb(P.OXBLOOD_HI)),
         (0.80, (176, 20, 40)), (1.00, P.rgb(P.CRIMSON))]
xs = [s[0] for s in stops]
out = np.stack([np.interp(v, xs, [s[1][c] for s in stops]) for c in range(3)], axis=2)
lift = np.clip((w - 0.30) / 0.6, 0, 1)[..., None] ** 1.4
out = out * (1 - lift) + np.array(P.rgb(P.FLESH), np.float32) * lift
Path(P.WALLPAPER).parent.mkdir(exist_ok=True)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(P.WALLPAPER, optimize=True)
print("wallpaper ->", P.WALLPAPER)
