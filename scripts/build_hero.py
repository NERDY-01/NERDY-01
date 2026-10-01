#!/usr/bin/env python3
"""Builds assets/hero.svg: symbol portrait (left) + animated contribution chart (right).
Usage: python3 scripts/build_hero.py [github_username]
Uses only the standard library. Fetches the public contribution calendar."""
import json, random, re, sys, time, urllib.request
from datetime import date, timedelta
from pathlib import Path

USER = sys.argv[1] if len(sys.argv) > 1 else "NERDY-01"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "hero.svg"

# ---------- portrait ----------
PORTRAIT = [
    '                                     .....::;:..     :..:::.                                        ',
    '                             .    ..:.     ..::.            .:::                                    ',
    '                            .....;;:          .:++        ..   ..  .                                ',
    '                            ....::                /              .::  .                             ',
    '                               .                                   .;/;:                            ',
    '                                                                       ;:                           ',
    '                                                                       :;:                          ',
    '                                                                        ..:;                        ',
    '                                            .... ..:;;;;:.               :::                        ',
    '                                    :;/+>>{><<<>>>>{>><<<+++/;..          :.                        ',
    '                                 ;+<<<>>>>>>><<<<<<<<<<<<<<<+++/;:.                                 ',
    '                                ;>>><>>>>>>><<<<<<<<<<<<<<<<<<<<<++;.                               ',
    '                               .<>>>>>>>><<<<<<<<++++<+++++++<<<>>>{{>.                             ',
    '                               /<>{>><<<++++++++++++++///////++<<>>{}}{:                            ',
    '                              .+<>>>><++++++++////////+++////++++<>{}{>+.                           ',
    '                              :/+>>><<++++++++++++///+++++++++++<<<>>>>+:                           ',
    '                              .;+<<<++<<<<>>>>><<+++++++<<<<+/;/+++>{>>>+.                          ',
    '                               +><<<<++<+<<+++<<<++++++/;..         :;+>{+                          ',
    '                              /{>+;.            ;//++;:                 +{+                         ',
    '                              {{;                .;/;:   ...:;;;//++>></: ;.                        ',
    '                             ;{+:/<<<++/;         ::.. .::          ../<+:/:                        ',
    '                             ./:<>+:           .. .;/;...         .   ./<<+;     .                  ',
    '                              +/><:    .      .:: ;<++/ .     ....:;//++<<>>   :}}*;                ',
    '                      /}}{.   <<></;:;;;;;:.::/;:.>><+<<::::::::;;//+<<><<<>; />@<;%                ',
    '                      #<{#}{..<++++/////////++++;/<><<++//<++++++++++<<<+<++/;<+#@/>}               ',
    '                     +*>*%}>+;+++/++++++++<<<<</:+<><>><<//+/+++++++/++++++// ./<%</@               ',
    '                     >{>%#}<.:++++/+++++++++++/:;<>>>>>{{+;;:;//++//+++++++;+. .:{*{+               ',
    '                      #>%}<;:+///++++++++++//;/<><<<><<<+<>{/./++//++++++++/+<  .}{*                ',
    '                      :*}}/:++///+++++++++///;+/:   ;;;    :; :/++////++++++;  ;{<}+                ',
    '                       {}>{/:;;+++++++++++++//:  ..:::.     :;;;//////++++++: <}//%                 ',
    '                        #><}>;;/++++++++++++++///;;;::::.:;///+//////+++++<;{{;:>@.                 ',
    '                         @#<+>}<<<+++++++++++//+/;;;::::.:;+//;//////++++<+ ;*%*}:                  ',
    '                          *#%@{ /><+++++///////;::;:;:. ....:/::;;;/++++<{                          ',
    '                                 ><+++++//;.                    .:;///++>+                          ',
    '                                  ><++///;:    .;;++;;////+;:   ..:;;/+++                           ',
    '                                  .<+///;;;;++;:::;/;;;;:..::;;;;:::;;/+;                           ',
    '                                   /;/;;;;;;;//;;;.       .::::::::::;;+/                           ',
    '                                   /;:::::;;;;;;;::......:..:::::::::;/>/                           ',
    '                                   ;</:...:;;;;///++//;;;;;;;;;;:..::/+>/                           ',
    '                                   ;</;:.  .;/++++++/;;;;;////;:...:;/+<<                           ',
    '                                   :<//;;:    :::;;:::::......   .:;;/+<><                          ',
    '                                   +++//;;;.                  ...::;;/+<>.*                         ',
    '                                  %</+///;;;;::::...      .::;;;::;;;;++> ;@                        ',
    '                                 >@+/////////;;///;;::::.::;;//;;:;;;//+> .@*                       ',
    '                                 @@+;///////;;//////;;;;;;/////;;;;;;//++ /@@                       ',
    '                                <@@{.///////////////+//////////;;;;;;///  }@@:                      ',
    '                                #@%@  ///////////;;;/+//;;;;//;;;;;;;;:  :#@@;                      ',
    '                                #%*%}  :;/////////;;;/+;::;;;;;;;;;;:.   {#@@;      ...             ',
    '                                #%**#<   :;///////;;::. .:;;;;;;;::.    :*%@@:      ....            ',
    '                                ##**}#;   .:;;////;;;:..::;;;;;;::.     >*@@@       .. ..   ....    ',
    '                                ##**}**:    .::;;;/;;;;;;;;::::::..    :*#%@@        .....     ..:..',
    '                                {%*}}*}{.     ..:::;;;::::.:::::..     }#%%@*        ... ..        .',
    '                                +%*}*+:;};      ..:::::::::::::.      {}*%%@+      .. ..  ..        ',
    '                                /@**;  ;>}>       ..::::::::::..     >*;:{%@         ...  ...       ',
    '                                :@#+   :<>}}<        .:::;;;;:.    +}};:.+@@          ....          ',
    '                                .@< ;:.;+<<<{{       .::;;;;;.   .>*{;..:/@*                        ',
    '                                 }.;>+;;+<<>>>{.     .::;;;;:.. :>}>;:.:;;%;                        ',
    '                                 //>{>+;/<<<>>>>+;    ..::;;:::+{}}/:::;/:>                         ',
    '                                 /<{{></;/+++>{{{}}:   ...:::;>{{}{:::;++;+                         ',
    '                                 ;>{{><+;;;//+>>>{{*.   ..:./{{{{{/::;/+/+/                         ',
    '                                 :>{{><<+;;;/+<>>>>{>   .../}{>{{{;:;////<;                         ',
    '                                 .>>>><<+/;;;/+>>>>>{   ..;{{>{{>;::;;//+<.                 .       ',
    '                                 .>>><<+++/;;//<<<<>{;   :{{{{</:.::;;//+>                 ..       ',
    '                                  <><<<+++/;:;;++<++<}   <{>>+;:..::;//++>                 .        ',
    '                                  +><<++++//;:;/++++<}  ;{>>+::..::;//+<<<                          ',
]
rows = PORTRAIT
# trim empty columns on the left/right so the portrait is as wide as its content
used = [i for line in rows for i, ch in enumerate(line) if ch != " "]
lo, hi = min(used), max(used) + 1
rows = [line[lo:hi] for line in rows]
PR, PC = len(rows), len(rows[0])
CW, CH = 6, 11
PW, PH = PC * CW, PR * CH
PS = 0.62                     # portrait scale
pw, ph = PW * PS, PH * PS
esc = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
total = sum(1 for r in rows for x in r if x != " ")
rnd = random.Random(3)
n = 0
ptext = []
for r, line in enumerate(rows):
    parts = []
    for x in line:
        if x == " ":
            parts.append(" ")
        else:
            t = n / total * 5.0 + rnd.random() * 0.1
            n += 1
            parts.append(f'<tspan class="s d{int(t/0.14)}">{esc.get(x, x)}</tspan>')
    ptext.append(f'<text x="0" y="{(r+1)*CH-2}" textLength="{PW}" lengthAdjust="spacing">{"".join(parts)}</text>')
pdelays = "".join(f".d{i}{{animation-delay:{i*0.14:.2f}s}}" for i in range(int(5.2/0.14) + 2))

# ---------- contributions ----------
req = urllib.request.Request(
    f"https://github.com/users/{USER}/contributions",
    headers={"User-Agent": "Mozilla/5.0 (profile-readme-builder)"},
)
html = None
for attempt in range(3):
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        break
    except Exception as e:
        if attempt == 2:
            raise
        time.sleep(5)
cells = {}
for m in re.finditer(
    r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?id="contribution-day-component-(\d)-(\d+)"[^>]*?data-level="(\d)"', html
):
    d, row, col, lvl = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    cells[(row, col)] = (date.fromisoformat(d), lvl)
if not cells:
    sys.exit("no contribution cells found")
tm = re.search(r"([\d,]+)\s+contributions\s+in the last year", html)
total_contrib = tm.group(1) if tm else ""
ncols = max(c for _, c in cells) + 1

STEP, SZ = 12, 10
GX = pw + 18                  # chart left edge
GW = ncols * STEP
LABEL_Y = 36
TOP = 44                      # grid top within chart block
colors = ["#6366f1", "#4ade80", "#22c55e", "#16a34a", "#15803d"]
from collections import defaultdict
bycol = defaultdict(list)
for (row, col), (d, lvl) in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    c = colors[lvl]
    fo = ' fill-opacity="1"' if lvl else ""
    bycol[col].append(
        f'<rect x="{col*STEP}" y="{TOP+row*STEP}" width="{SZ}" height="{SZ}" rx="2" fill="{c}" stroke="{c}"{fo}/>'
    )
rects = []
for col in range(ncols):
    enter = f"{col*0.03:.2f}s"
    wave = f"{1.5 + col*0.08:.2f}s"
    rects.append(
        f'<g opacity="1" stroke-width="0" fill-opacity=".28">'
        f'<set attributeName="opacity" to="0" begin="0s" end="{enter}"/>'
        f'<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{enter}" fill="freeze"/>'
        f'<animate attributeName="stroke-width" values="0;4;0;0" keyTimes="0;.1;.25;1" dur="5s" begin="{wave}" repeatCount="indefinite"/>'
        f'<animate attributeName="fill-opacity" values=".28;.9;.28;.28" keyTimes="0;.1;.25;1" dur="5s" begin="{wave}" repeatCount="indefinite"/>'
        + "".join(bycol[col]) + "</g>"
    )

# month labels
labels, last_m, last_x = [], None, -99
for col in range(ncols):
    anyc = next(((r, cells[(r, col)][0]) for r in range(7) if (r, col) in cells), None)
    if not anyc:
        continue
    r, d = anyc
    start = d - timedelta(days=r)
    if start.month != last_m:
        x = col * STEP
        if x - last_x >= 30 and col < ncols - 2:
            labels.append(f'<text class="m" x="{x}" y="{LABEL_Y}">{start.strftime("%b")}</text>')
            last_x = x
        last_m = start.month

grid_h = 7 * STEP
block_h = TOP + grid_h + 26
H = max(ph, block_h)
W = GX + GW
by = (H - block_h) / 2
title = f"{total_contrib} contributions in the last year" if total_contrib else "contributions"
FO = ' fill-opacity=".28"'
legend_x = GW - 5 * STEP - 70
legend = (
    f'<text class="m" x="{legend_x}" y="{TOP+grid_h+16}" text-anchor="end">Less</text>'
    + "".join(
        f'<rect x="{legend_x+8+i*STEP}" y="{TOP+grid_h+7}" width="{SZ}" height="{SZ}" rx="2" fill="{colors[i]}"{FO if i==0 else ""}/>'
        for i in range(5)
    )
    + f'<text class="m" x="{legend_x+8+5*STEP+4}" y="{TOP+grid_h+16}">More</text>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{PW}" y2="{PH}">
<stop offset="0" stop-color="#22d3ee"/><stop offset="0.55" stop-color="#6366f1"/><stop offset="1" stop-color="#a855f7"/>
</linearGradient>
<style>
.p text{{font-family:'DejaVu Sans Mono','Courier New',monospace;font-size:10px;fill:url(#g);white-space:pre}}
.s{{animation:t 18s linear infinite both}}
@keyframes t{{0%{{opacity:0}}2%{{opacity:1}}97%{{opacity:1}}100%{{opacity:0}}}}
{pdelays}
.m{{font:10px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#64748b}}
.h{{font:600 12px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#64748b}}
</style>
</defs>
<g class="p" xml:space="preserve" transform="translate(0,{(H-ph)/2:.1f}) scale({PS})">
{chr(10).join(ptext)}
</g>
<g transform="translate({GX:.1f},{by:.1f})">
<text class="h" x="0" y="12">{title}</text>
{"".join(labels)}
{"".join(rects)}
{legend}
</g>
</svg>'''
OUT.write_text(svg)
print(f"wrote {OUT} ({len(svg)//1024} KB), {ncols} weeks, total={total_contrib}")