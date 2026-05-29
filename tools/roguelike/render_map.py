#!/usr/bin/env python3
"""Render pokeemerald metatile grids to PNG using the real tileset assets.

Reads a primary+secondary tileset pair (tiles.png, metatiles.bin, palettes/*.pal)
and composes either:
  - a labeled reference sheet of every metatile (--sheet), or
  - an arbitrary map from a grid of metatile IDs (used by the room authoring).

Pure stdlib + Pillow. Written for the roguelike romhack; see docs/architecture.md.
"""
import os, struct, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
TILE = 8
MT = 16  # metatile px

def load_pal(path):
    with open(path) as f:
        lines = f.read().split("\n")
    n = int(lines[2])
    cols = []
    for i in range(n):
        r, g, b = map(int, lines[3 + i].split())
        cols.append((r, g, b))
    return cols

def load_palettes(prim_dir, sec_dir):
    pals = []
    for i in range(13):  # field uses BG palettes 0..12
        d = prim_dir if i < NUM_PALS_IN_PRIMARY else sec_dir
        pals.append(load_pal(os.path.join(d, "palettes", f"{i:02}.pal")))
    return pals

def load_tiles(png):
    """Return list of 8x8 index grids (each row-major list of 64 ints 0..15)."""
    im = Image.open(png).convert("P")
    px = im.load()
    w, h = im.size
    cols, rows = w // TILE, h // TILE
    tiles = []
    for ty in range(rows):
        for tx in range(cols):
            blk = []
            for y in range(TILE):
                for x in range(TILE):
                    blk.append(px[tx * TILE + x, ty * TILE + y] & 0x0F)
            tiles.append(blk)
    return tiles

def load_metatiles(binpath):
    """Return list of metatiles; each = list of 8 (tileid, xflip, yflip, pal)."""
    data = open(binpath, "rb").read()
    out = []
    for i in range(0, len(data), 16):
        mt = []
        for j in range(8):
            v = struct.unpack_from("<H", data, i + j * 2)[0]
            mt.append((v & 0x03FF, bool(v & 0x0400), bool(v & 0x0800), (v >> 12) & 0x0F))
        out.append(mt)
    return out

class Renderer:
    def __init__(self, prim, sec):
        self.prim_tiles = load_tiles(os.path.join(prim, "tiles.png"))
        self.sec_tiles = load_tiles(os.path.join(sec, "tiles.png"))
        self.prim_mts = load_metatiles(os.path.join(prim, "metatiles.bin"))
        self.sec_mts = load_metatiles(os.path.join(sec, "metatiles.bin"))
        self.pals = load_palettes(prim, sec)

    def tile_px(self, tileid):
        if tileid < NUM_TILES_IN_PRIMARY:
            return self.prim_tiles[tileid] if tileid < len(self.prim_tiles) else [0]*64
        idx = tileid - NUM_TILES_IN_PRIMARY
        return self.sec_tiles[idx] if 0 <= idx < len(self.sec_tiles) else [0]*64

    def metatile(self, mtid):
        if mtid < NUM_METATILES_IN_PRIMARY:
            return self.prim_mts[mtid] if mtid < len(self.prim_mts) else None
        idx = mtid - NUM_METATILES_IN_PRIMARY
        return self.sec_mts[idx] if 0 <= idx < len(self.sec_mts) else None

    def render_metatile(self, mtid):
        """Return a 16x16 RGBA image of one metatile."""
        mt = self.metatile(mtid)
        out = Image.new("RGBA", (MT, MT), (0, 0, 0, 0))
        if mt is None:
            return out
        # 4 bottom-layer subtiles (opaque incl. index 0), then 4 top (index 0 transparent)
        pos = [(0, 0), (TILE, 0), (0, TILE), (TILE, TILE)]
        for layer in range(2):
            transparent0 = (layer == 1)
            for k in range(4):
                tileid, xf, yf, pal = mt[layer * 4 + k]
                blk = self.tile_px(tileid)
                palette = self.pals[pal] if pal < len(self.pals) else self.pals[0]
                ox, oy = pos[k]
                for y in range(TILE):
                    sy = (TILE - 1 - y) if yf else y
                    for x in range(TILE):
                        sx = (TILE - 1 - x) if xf else x
                        ci = blk[sy * TILE + sx]
                        if ci == 0 and transparent0:
                            continue
                        r, g, b = palette[ci]
                        out.putpixel((ox + x, oy + y), (r, g, b, 255))
        return out

    def render_grid(self, grid, scale=2):
        """grid: 2D list of metatile IDs -> RGB image."""
        h = len(grid); w = len(grid[0])
        img = Image.new("RGBA", (w * MT, h * MT), (0, 0, 0, 255))
        for gy in range(h):
            for gx in range(w):
                img.alpha_composite(self.render_metatile(grid[gy][gx]), (gx * MT, gy * MT))
        if scale != 1:
            img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
        return img.convert("RGB")

    def reference_sheet(self, ids, cols=16, scale=3, label_every=1):
        """Render the given metatile ids in a labeled grid."""
        cell = MT * scale
        pad_top = 14
        rows = (len(ids) + cols - 1) // cols
        W = cols * (cell + 4) + 4
        H = rows * (cell + pad_top + 4) + 4
        img = Image.new("RGB", (W, H), (40, 40, 48))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 9)
        except Exception:
            font = ImageFont.load_default()
        for i, mtid in enumerate(ids):
            r, c = divmod(i, cols)
            x = 4 + c * (cell + 4)
            y = 4 + r * (cell + pad_top + 4)
            d.text((x, y), f"{mtid}", fill=(220, 220, 120), font=font)
            mt = self.render_metatile(mtid).resize((cell, cell), Image.NEAREST)
            img.paste(mt, (x, y + pad_top))
        return img

if __name__ == "__main__":
    prim = os.path.join(REPO, "data/tilesets/primary/building")
    sec = os.path.join(REPO, "data/tilesets/secondary/battle_frontier")
    r = Renderer(prim, sec)
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/rl_render"
    os.makedirs(out, exist_ok=True)
    # Building primary ids 0..7, then BattleFrontier secondary ids 512.. (509 of them)
    prim_ids = list(range(len(r.prim_mts)))
    sec_ids = [NUM_METATILES_IN_PRIMARY + i for i in range(len(r.sec_mts))]
    r.reference_sheet(prim_ids, cols=8).save(os.path.join(out, "ref_primary_building.png"))
    # secondary is large; split into chunks of 128 for readability
    for ci, start in enumerate(range(0, len(sec_ids), 128)):
        chunk = sec_ids[start:start + 128]
        r.reference_sheet(chunk, cols=16).save(os.path.join(out, f"ref_secondary_bf_{ci}.png"))
    print("primary metatiles:", len(r.prim_mts), "secondary:", len(r.sec_mts))
    print("wrote reference sheets to", out)
