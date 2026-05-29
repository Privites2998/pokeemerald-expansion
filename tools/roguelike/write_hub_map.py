#!/usr/bin/env python3
"""Generate the RoguelikeHub map.bin for the chosen 'Throne Hall (short pads)'
layout -- programmatically, no porymap. Writes metatile IDs + collision +
elevation. Backs up the existing map.bin first.

Cell encoding (u16 LE): bits 0-9 metatile id, bits 10-11 collision (0=passable,
1=blocked), bits 12-15 elevation. Default elevation 3 (matches porymap's fill).
"""
import os, struct, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_map import Renderer

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP = os.path.join(REPO, "data/layouts/RoguelikeHub/map.bin")
W = Hh = 16
ELEV = 3
FLOOR, WALL = 643, 538
CARPET = [885, 886, 887]
DESK = [632, 633, 634]
CONSOLE_L, CONSOLE_R = 533, 639
HEDGE_L, HEDGE_R = 646, 647

# Metatiles the player cannot walk through.
BLOCKED = {WALL, HEDGE_L, HEDGE_R, *DESK}
# Consoles are left passable: they become step-on portals later (Roadmap T20/T22).

def build():
    g = [[FLOOR] * W for _ in range(Hh)]
    for x in range(W):
        g[0][x] = WALL
    for left in (3, 10):                  # two short portal pads (3x3)
        for r in range(3, 6):
            for i, m in enumerate(CARPET):
                g[r][left + i] = m
    g[2][4] = CONSOLE_L
    g[2][11] = CONSOLE_R
    for i, m in enumerate(DESK):           # NPC desk centered under the wall
        g[2][6 + i] = m
    for r in (3, 5, 7, 9, 11, 13):         # hedges lining the side walls
        g[r][1] = HEDGE_L
        g[r][14] = HEDGE_R
    for i, m in enumerate(CARPET):         # entrance welcome mat
        g[13][6 + i] = m
    return g

def encode(g):
    out = bytearray()
    for r in range(Hh):
        for c in range(W):
            mid = g[r][c]
            coll = 1 if mid in BLOCKED else 0
            cell = (mid & 0x3FF) | (coll << 10) | (ELEV << 12)
            out += struct.pack("<H", cell)
    return bytes(out)

if __name__ == "__main__":
    g = build()
    if os.path.exists(MAP) and not os.path.exists(MAP + ".bak"):
        shutil.copy(MAP, MAP + ".bak")
        print("backed up ->", MAP + ".bak")
    with open(MAP, "wb") as f:
        f.write(encode(g))
    print("wrote", MAP, "(%d bytes)" % os.path.getsize(MAP))
    # confirmation render
    r = Renderer(os.path.join(REPO, "data/tilesets/primary/building"),
                 os.path.join(REPO, "data/tilesets/secondary/battle_frontier"))
    r.render_grid(g, scale=5).save("/tmp/rl_render/hub_final.png")
    print("rendered /tmp/rl_render/hub_final.png")
