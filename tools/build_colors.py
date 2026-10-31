#!/usr/bin/env python3
"""Bloodfeed KDE colour scheme + Konsole colorscheme + kitty theme."""
import sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
import palette as P
c = P.csv

def group(bg, alt, fg=P.TEXT, inact=P.TEXT_DIM, focus=P.CRIMSON, hover=P.CRIMSON_HI, active=P.TEXT_HI):
    return f"""BackgroundAlternate={c(alt)}
BackgroundNormal={c(bg)}
DecorationFocus={c(focus)}
DecorationHover={c(hover)}
ForegroundActive={c(active)}
ForegroundInactive={c(inact)}
ForegroundLink={c(P.LINK)}
ForegroundNegative={c(P.NEGATIVE)}
ForegroundNeutral={c(P.NEUTRAL)}
ForegroundNormal={c(fg)}
ForegroundPositive={c(P.POSITIVE)}
ForegroundVisited={c(P.VISITED)}
"""

scheme = f"""[ColorEffects:Disabled]
Color={c(P.BASE)}
ColorAmount=0
ColorEffect=0
ContrastAmount=0.6
ContrastEffect=1
IntensityAmount=0.15
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={c(P.VOID)}
ColorAmount=0.05
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Window]
{group(P.BASE, P.SURFACE)}
[Colors:View]
{group(P.ABYSS, "#110607")}
[Colors:Button]
{group(P.RAISED, P.EDGE)}
[Colors:Header]
{group(P.SURFACE, P.RAISED)}
[Colors:Header][Inactive]
{group(P.BASE, P.SURFACE, fg=P.TEXT_DIM, inact=P.TEXT_MUTE, focus=P.CRIMSON_LO)}
[Colors:Tooltip]
{group(P.VOID, P.BASE)}
[Colors:Complementary]
{group(P.VOID, P.BASE)}
[Colors:Selection]
{group(P.SELECT, P.CRIMSON_DEEP, fg=P.TEXT_HI, inact=P.TEXT, active="#ffffff")}
[General]
ColorScheme=Bloodfeed
Name=Bloodfeed
shadeSortColumn=true
AccentColor={c(P.CRIMSON)}
frame={c(P.EDGE)}
inactiveFrame={c(P.SURFACE)}

[KDE]
contrast=4

[WM]
activeBackground={c(P.SURFACE)}
activeBlend={c(P.CRIMSON)}
activeForeground={c(P.TEXT)}
inactiveBackground={c(P.BASE)}
inactiveBlend={c(P.EDGE)}
inactiveForeground={c(P.TEXT_MUTE)}
"""
(R / "colors").mkdir(exist_ok=True)
(R / "colors/Bloodfeed.colors").write_text(scheme)

# terminal: 16 colours tuned for the blood-black bg
term = dict(
    bg=P.BASE, fg=P.TEXT, cursor=P.CRIMSON_HI, sel_bg=P.SELECT, sel_fg=P.TEXT_HI,
    c=["#2a1215", "#e0283f", "#6fbf9c", "#d9a24e", "#b8475a", "#e05a8a", "#d98c7a", "#c4aaa8",
       "#5a2a30", "#ff5368", "#94e0bd", "#f2c27a", "#e0707e", "#ff8cb0", "#ffb39e", "#fff1ef"])
names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
k = ["[General]\nDescription=Bloodfeed\nOpacity=0.94\nBlur=true\nWallpaper=\n",
     f"[Background]\nColor={c(term['bg'])}\n", f"[BackgroundIntense]\nColor={c(P.SURFACE)}\n",
     f"[BackgroundFaint]\nColor={c(term['bg'])}\n",
     f"[Foreground]\nColor={c(term['fg'])}\n", f"[ForegroundIntense]\nColor={c(P.TEXT_HI)}\n",
     f"[ForegroundFaint]\nColor={c(P.TEXT_DIM)}\n"]
for i, n in enumerate(names):
    k.append(f"[Color{i}]\nColor={c(term['c'][i])}\n")
    k.append(f"[Color{i}Intense]\nColor={c(term['c'][i + 8])}\n")
    k.append(f"[Color{i}Faint]\nColor={c(term['c'][i])}\n")
(R / "terminal/Bloodfeed.colorscheme").write_text("\n".join(k))

profile = """[Appearance]
ColorScheme=Bloodfeed
Font=Terminess Nerd Font,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1

[Cursor Options]
CursorShape=1
CustomCursorColor=255,83,104
UseCustomCursorColor=true

[General]
Name=Bloodfeed
Parent=FALLBACK/
TerminalMargin=10

[Scrolling]
ScrollBarPosition=2
"""
(R / "terminal/Bloodfeed.profile").write_text(profile)

kitty = [f"# Bloodfeed — kitty theme", f"background {term['bg']}", f"foreground {term['fg']}",
         f"cursor {term['cursor']}", f"cursor_text_color {P.VOID}", f"selection_background {term['sel_bg']}",
         f"selection_foreground {term['sel_fg']}", f"url_color {P.LINK}",
         f"active_border_color {P.CRIMSON}", f"inactive_border_color {P.EDGE}",
         f"active_tab_background {P.CRIMSON_DEEP}", f"active_tab_foreground {P.TEXT_HI}",
         f"inactive_tab_background {P.BASE}", f"inactive_tab_foreground {P.TEXT_DIM}",
         f"tab_bar_background {P.VOID}", "background_opacity 0.94"]
kitty += [f"color{i} {v}" for i, v in enumerate(term["c"])]
(R / "terminal/bloodfeed-kitty.conf").write_text("\n".join(kitty) + "\n")
print("colors + terminal written")
