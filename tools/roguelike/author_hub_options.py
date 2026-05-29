#!/usr/bin/env python3
"""Author candidate RoguelikeHub layouts (16x16) and render each to PNG.

These are DIRECTION mockups for Steph to choose between -- floor theme, portal
style, decoration vibe. Walls are approximate (a single back-wall row); the
chosen option gets refined afterward. Each grid is a 2D list of metatile IDs.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_map import Renderer
from PIL import Image, ImageDraw, ImageFont

W = H = 16
WALL = 538            # back-wall tile
SCALE = 4

def room(floor):
    g = [[floor for _ in range(W)] for _ in range(H)]
    for x in range(W):
        g[0][x] = WALL    # back wall along the top row
    return g

def stamp(g, top, left, block):
    for r, row in enumerate(block):
        for c, mid in enumerate(row):
            if mid is not None:
                g[top + r][left + c] = mid

# multi-tile features
SEAL   = [[592, 593, 594, 595], [608, 609, 610, 611]]  # grey eye medallion (4x2)
CARPET = [[885, 886, 887]]                              # red runner (3x1)
COUNTER= [[632, 633, 634]]                              # service desk (3x1)
PLANT  = 615
HEDGE_L, HEDGE_R = 646, 647
CONSOLE_A, CONSOLE_B = 533, 639                         # teleporter pads

def opt_atrium():
    g = room(512)                       # blue floor
    stamp(g, 2, 6, COUNTER)             # NPC counter near the wall
    stamp(g, 6, 6, SEAL)                # central grey medallion
    g[13][7] = CONSOLE_B                # portal console, bottom-center
    g[13][8] = CONSOLE_B
    for (r, c) in [(2,1),(2,14),(13,1),(13,14)]:
        g[r][c] = PLANT                 # potted plants in the corners
    return g, "A - Frontier Atrium", "Blue floor, grey seal centerpiece, twin portal consoles, NPC desk under the wall."

def opt_throne():
    g = room(643)                       # cream floor
    # red carpet runner up the center, entrance (bottom) -> portal (top)
    for r in range(3, 14):
        stamp(g, r, 6, CARPET)
    g[2][7] = CONSOLE_A                 # portal console at head of the carpet
    stamp(g, 2, 9, COUNTER)             # NPC desk off to the side
    for r in range(2, 14, 2):           # hedges lining both walls
        g[r][1] = HEDGE_L; g[r][14] = HEDGE_R
    return g, "B - Throne Hall", "Cream floor, red carpet runner leading to a single portal console, hedge-lined walls."

def opt_vault():
    g = room(570)                       # yellow grid floor
    stamp(g, 2, 6, COUNTER)
    # row of blue emblem accent pads
    for c in (4, 7, 10):
        g[8][c] = 522; g[8][c+1] = 524
    g[12][7] = CONSOLE_A; g[12][8] = CONSOLE_B
    g[6][2] = 679; g[6][13] = 679       # statues flanking
    for (r, c) in [(2,1),(2,14)]:
        g[r][c] = PLANT
    return g, "C - Golden Vault", "Yellow tiled floor, blue emblem accent pads, statues, two portal consoles."

def opt_twin():
    g = room(642)                       # glossy blue floor
    # two portals side by side -- foreshadows the branching-door run mechanic
    g[8][5] = CONSOLE_A; g[8][6] = CONSOLE_A
    g[8][9] = CONSOLE_B; g[8][10] = CONSOLE_B
    stamp(g, 2, 6, COUNTER)
    for (r, c) in [(13,2),(13,13),(2,1),(2,14)]:
        g[r][c] = PLANT
    return g, "D - Twin Pads (minimal)", "Glossy blue floor, two distinct portals side-by-side (branch motif), sparse decor."

OPTIONS = [opt_atrium, opt_throne, opt_vault, opt_twin]

if __name__ == "__main__":
    out = "/tmp/rl_render"
    os.makedirs(out, exist_ok=True)
    r = Renderer("data/tilesets/primary/building", "data/tilesets/secondary/battle_frontier")
    rendered = []
    for fn in OPTIONS:
        g, title, desc = fn()
        img = r.render_grid(g, scale=SCALE)
        fname = f"hub_{title.split(' ')[0]}.png"
        img.save(os.path.join(out, fname))
        rendered.append((title, desc, img))
    # contact sheet: 2x2 with titles
    cw = rendered[0][2].width; ch = rendered[0][2].height
    pad = 28; cols = 2
    rows = (len(rendered) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*(cw+16)+16, rows*(ch+pad+16)+16), (30, 30, 36))
    d = ImageDraw.Draw(sheet)
    try: f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
    except: f = ImageFont.load_default()
    for i, (title, desc, img) in enumerate(rendered):
        rr, cc = divmod(i, cols)
        x = 16 + cc*(cw+16); y = 16 + rr*(ch+pad+16)
        d.text((x, y), title, fill=(235, 220, 130), font=f)
        sheet.paste(img, (x, y+pad))
    sheet.save(os.path.join(out, "hub_options.png"))
    print("wrote hub options + contact sheet to", out)
