# Dev loop

The edit → build → test → commit cycle for this romhack. Written for someone
new to the decomp toolchain — every step spelled out.

## The loop

1. **Edit** source files in `src/`, `data/`, or `include/` (in your editor).
2. **Build** the ROM:
   ```
   gmake -j8
   ```
   - `gmake` is GNU make (on macOS, plain `make` is an older Apple version —
     always use `gmake`). It reads the `Makefile` and turns source into a ROM.
   - `-j8` builds with 8 parallel jobs (this machine has 8 cores). Faster.
   - First build from a clean tree takes a few minutes. After that it's
     **incremental** — only files you changed (and things that depend on them)
     rebuild, so it's usually seconds.
   - Output is `pokeemerald.gba` in the repo root.
3. **Test** by opening `pokeemerald.gba` in mGBA (the emulator).
   - In-overworld, press **R + START** to open the debug menu (warp, give-mon,
     flag toggles, and our "Roguelike: Reset run" entry live there).
   - Use mGBA save states (Shift+F1 to save a state, F1 to load) to jump
     straight to a test spot instead of replaying from the start.
4. **Commit** once it builds and behaves:
   ```
   git add -A
   git commit -m "Your message"
   ```
   Commit small and often. See `docs/remotes.md` for push conventions.

## A clean build

If something looks wrong and you suspect a stale build artifact:
```
gmake clean    # deletes the build/ folder
gmake -j8      # full rebuild from scratch (slow, but guaranteed clean)
```
You rarely need this — reach for it only when an incremental build behaves
inconsistently with the source.

## Common gotchas

- **`make` vs `gmake`** — use `gmake`. Apple's bundled `make` is too old.
- **Edited a `.json` map/layout file by hand?** Let porymap own those. Hand
  edits can desync the binary `.bin` layout files. (Map *content* is generated;
  see `docs/architecture.md`.)
- **New `src/*.c` file** — picked up automatically. The Makefile globs `src/`
  and both linker scripts glob `*.o(.text*)`, so no Makefile/linker edits are
  needed to add a translation unit.
- **New event-script `.inc` file** — NOT auto-discovered. You must add an
  `.include "data/scripts/.../yourfile.inc"` line to `data/event_scripts.s`,
  or the linker never sees its labels. (This is how `roguelike_init.inc` is
  wired in.)
- **New Special (script-callable C function)** — declare the C function, then
  add a `def_special FuncName` line to `data/specials.inc`. Scripts call it
  with `special FuncName`.
- **Benign warning:** every build prints
  `warning: ... has a LOAD segment with RWX permissions`. That's from the
  expansion's linker setup, not your code. Ignore it.
- **Memory-usage report** prints EWRAM/IWRAM/ROM percentages at link time.
  Watch EWRAM/IWRAM (currently ~87% each) — if you add big global structs and
  one of those hits 100%, the link fails. ROM has lots of headroom.
