#!/usr/bin/env python3
"""Assemble repos/bloodfeed-global: the look-and-feel package at the root plus the
pieces its defaults name (colours, Plasma style, Aurorae, Kvantum, icons) under extras/.

    python3 tools/make-global.py
Run tools/make-shots.py (and the splash/gallery renders) first.
"""
import shutil, subprocess, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "repos/bloodfeed-global"
LNF = ROOT / "plasma/look-and-feel/scorn.bloodfeed"
GPL = Path("/usr/share/licenses/spdx/GPL-3.0-or-later.txt")
SHOTS = {"desktop.jpg": "desktop.png", "splash.jpg": "splash.png", "splash-rewind.jpg": "splash-rew.png",
         "widgets.jpg": "gallery.png", "decoration.jpg": "decoration.png", "panel.jpg": "panel.png",
         "palette.jpg": "colors.png", "icons.jpg": "icons.png"}
EXTRAS = {"colors/Bloodfeed.colors": ROOT / "colors/Bloodfeed.colors",
          "plasma/Bloodfeed": ROOT / "plasma/desktoptheme/Bloodfeed",
          "aurorae/Bloodfeed": ROOT / "aurorae/Bloodfeed",
          "kvantum/Bloodfeed": ROOT / "kvantum/Bloodfeed",
          "icons/Bloodfeed": ROOT / "icons/Bloodfeed"}
TOPICS = ["bloodfeed", "kde", "plasma6", "plasma-6", "dark", "vhs", "scanlines", "crimson", "red", "blood", "horror",
          "analog-horror", "retro", "glow", "global-theme", "look-and-feel", "splash-screen", "ksplash", "kde-theme", "kvantum"]

INSTALL = r'''#!/usr/bin/env bash
# Bloodfeed — Global Theme (Plasma 6) — install.
#   ./install.sh          copy everything into your home, change nothing
#   ./install.sh --apply  copy, then switch Plasma (and Kvantum) to Bloodfeed
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
D=${XDG_DATA_HOME:-$HOME/.local/share}
C=${XDG_CONFIG_HOME:-$HOME/.config}
put() { rm -rf "$2"; mkdir -p "$(dirname "$2")"; cp -a "$1" "$2"; }

put "$HERE/contents" "$D/plasma/look-and-feel/scorn.bloodfeed/contents"
cp "$HERE/metadata.json" "$D/plasma/look-and-feel/scorn.bloodfeed/"
install -Dm644 "$HERE/extras/colors/Bloodfeed.colors" "$D/color-schemes/Bloodfeed.colors"
put "$HERE/extras/plasma/Bloodfeed"  "$D/plasma/desktoptheme/Bloodfeed"
put "$HERE/extras/aurorae/Bloodfeed" "$D/aurorae/themes/Bloodfeed"
put "$HERE/extras/icons/Bloodfeed"   "$D/icons/Bloodfeed"
put "$HERE/extras/kvantum/Bloodfeed" "$C/Kvantum/Bloodfeed"
echo "Installed: global theme, colour scheme, Plasma style, Aurorae, icons, Kvantum."

if [[ ${1:-} == --apply ]]; then
    kwriteconfig6 --file Kvantum/kvantum.kvconfig --group General --key theme Bloodfeed
    plasma-apply-lookandfeel -a scorn.bloodfeed
    qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
    echo "Applied. Restart apps to pick up the Kvantum style."
else
    echo "Apply: System Settings → Colors & Themes → Global Theme → Bloodfeed, or ./install.sh --apply"
fi
'''

README = """# Bloodfeed — Global Theme (Plasma 6)

A VHS tape dubbed in blood: red-black surfaces, faint scanlines and tape grain, a crimson glow on whatever has focus, and a rewind/play splash screen. One install switches the whole Plasma desktop.

![desktop](screenshots/desktop.jpg)

Bloodfeed is the crimson cut of [Nightfeed](https://github.com/numbpill3d/nightfeed-global). Same tape, same face, re-lit: every surface carries a red cast instead of cobalt, accents glow crimson instead of violet, and the text is warm bone.

## Features

- **Splash screen:** the tape rewinds (`REW ◀◀`, fast tracking band) and then plays (`PLAY ▶`, **SIGNAL BLEEDING**). Crimson tape blocks fill as Plasma's six startup stages arrive.
- **Everything the global theme points at ships in this repo,** so applying it never falls back to Breeze:
  - **Colour scheme:** blood-black surfaces (window `#150809`, views `#0e0506`, borders `#45141b`), crimson accent `#dc1f3c`, dim oxblood selections `#5a0d1a`, bone text `#e8d2d0`. Negative is a hotter scarlet-orange so errors never blend into the accent.
  - **Plasma style:** blood-black glass panel, popups and tooltips with tiled scanlines and grain, a crimson glow seam and crimson-tinted shadows. Translucent and solid variants.
  - **Aurorae window decoration:** scanline title bar with tape-grain streaks, a crimson seam, a crimson glow around the active window, and VCR transport buttons.
  - **Kvantum widget style:** KvArcDark's engine map recoloured onto a red-black ramp with crimson sliders, checks and progress bars, and recessed text fields.
  - **Icons:** crimson folders and places with pale-pink glyphs, plus a VHS `▶ PLAY` launcher icon, over Tela circle dark.
- **Ships no panel layout,** so applying it never rearranges your panels or widgets.

![splash](screenshots/splash.jpg)
![splash-rewind](screenshots/splash-rewind.jpg)
![widgets](screenshots/widgets.jpg)
![decoration](screenshots/decoration.jpg)
![panel](screenshots/panel.jpg)
![icons](screenshots/icons.jpg)
![palette](screenshots/palette.jpg)

## Requirements

- Plasma 6.
- [Kvantum](https://github.com/tsujan/Kvantum) (`kvantum` package) for the widget style. Without it, apps use your fallback Qt style.
- [Tela circle icon theme](https://github.com/vinceliuice/Tela-circle-icon-theme), dark variant (`Tela-circle-dark`). The Bloodfeed icons only replace folders and places and inherit everything else from it.

## Install

```bash
git clone https://github.com/numbpill3d/bloodfeed-global
cd bloodfeed-global && ./install.sh           # copy only
./install.sh --apply                          # copy and switch to Bloodfeed
```

Without `--apply`, pick **Bloodfeed** in System Settings → Colors & Themes → Global Theme. Global themes can't set the Kvantum theme, so open Kvantum Manager and pick **Bloodfeed** there (`--apply` does this for you).

To install only the look-and-feel package and splash, download `scorn.bloodfeed.tar.gz` from [Releases](https://github.com/numbpill3d/bloodfeed-global/releases) and use System Settings → Colors & Themes → Global Theme → Install from File. The splash alone can be picked under Colors & Themes → Splash Screen.

## Layout

| path | installs to |
|---|---|
| `metadata.json`, `contents/` | `~/.local/share/plasma/look-and-feel/scorn.bloodfeed/` |
| `extras/colors/Bloodfeed.colors` | `~/.local/share/color-schemes/` |
| `extras/plasma/Bloodfeed` | `~/.local/share/plasma/desktoptheme/` |
| `extras/aurorae/Bloodfeed` | `~/.local/share/aurorae/themes/` |
| `extras/icons/Bloodfeed` | `~/.local/share/icons/` |
| `extras/kvantum/Bloodfeed` | `~/.config/Kvantum/` |

## Tags

{tags}

## Credits and licence

By splicer scorn (voidrane). GPL-3.0-or-later.
OSD font: Terminess Nerd Font (Terminus, SIL OFL 1.1), bundled with its licence.
Kvantum engine map adapted from KvArcDark by Tsu Jan (Kvantum, GPL-3.0).
Folder artwork recoloured from Tela circle icon theme by Vince Liuice (GPL-3.0).
"""


def main():
    D.mkdir(parents=True, exist_ok=True)
    for c in D.iterdir():
        if c.name != ".git":
            shutil.rmtree(c) if c.is_dir() and not c.is_symlink() else c.unlink()
    shutil.copy2(LNF / "metadata.json", D)
    shutil.copytree(LNF / "contents", D / "contents")
    for dst, src in EXTRAS.items():
        t = D / "extras" / dst
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, t, symlinks=True) if src.is_dir() else shutil.copy2(src, t)
    (D / "screenshots").mkdir()
    for n, s in SHOTS.items():
        subprocess.run(["magick", str(ROOT / "screenshots" / s), "-quality", "90", str(D / "screenshots" / n)], check=True)
    (D / "README.md").write_text(README.replace("{tags}", " ".join(f"`{t}`" for t in TOPICS)))
    shutil.copy(GPL, D / "LICENSE")
    (D / "install.sh").write_text(INSTALL); (D / "install.sh").chmod(0o755)
    dist = ROOT / "dist"; dist.mkdir(exist_ok=True)
    with tarfile.open(dist / "scorn.bloodfeed.tar.gz", "w:gz") as t:
        t.add(LNF, arcname="scorn.bloodfeed")
    with tarfile.open(dist / "bloodfeed-global-v1.0.tar.gz", "w:gz") as t:
        for c in sorted(D.iterdir()):
            if c.name != ".git":
                t.add(c, arcname=f"bloodfeed-global/{c.name}")
    (dist / "topics.txt").write_text("\n".join(TOPICS) + "\n")
    print("repo ->", D, "| dist ->", dist)


if __name__ == "__main__":
    main()
