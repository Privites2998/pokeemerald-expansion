# Architecture (stub)

How the roguelike layer sits on top of vanilla pokeemerald-expansion. This is a
living stub — expand it as systems land. The guiding rule: **add a thin custom
layer, lean on the engine for everything else** (battles, menus, save, text).

## What's new vs. vanilla

Everything roguelike-specific is namespaced `ROGUELIKE` / `Roguelike` so it's
greppable and easy to keep separate from engine code we pull from upstream.

| Concern | Lives in | Status |
|---------|----------|--------|
| Run + meta state (scalars) | `VAR_ROGUELIKE_*`, `FLAG_ROGUELIKE_*` | reserved (T7) |
| Run reset logic | `src/roguelike.c` → special `RoguelikeReset` | done (T10) |
| Event scripts (hub/run) | `data/scripts/roguelike/` | scaffold (T8) |
| Maps (hub, rooms) | `data/maps/RoguelikeHub/`, group `gMapGroup_Roguelike` (75) | hub stub (T11) |
| Debug hooks | `src/debug.c` Utilities menu | reset entry (T10) |

## Where roguelike state lives

State splits into two lifetimes. The split is enforced in the constant
definitions and by the reset logic — keep it that way.

### RUN state — cleared every run
Describes the run in progress. Wiped by `RoguelikeReset()` on death / return
to hub so a fresh run starts clean.
- **Vars** `0x40F7–0x40FB`: `VAR_ROGUELIKE_RUN_STATE`, `_ACT`, `_ROOMS_DONE`,
  `_CURRENT_ROOM`, `_SEED`.
- **Flags** `0x020–0x02F`: `FLAG_ROGUELIKE_STARTER_CHOSEN`,
  `FLAG_ROGUELIKE_RUN_ACTIVE`, + reserved.
- The party itself (the 3 mon) is run state too — it gets rebuilt at run start
  and cleared on death (future task M4).

### META state — persists across runs and saves
Survives death and lives in the save file. **Never** touched by the run reset.
- **Vars** `0x40FC–0x40FE`: `VAR_ROGUELIKE_META_CURRENCY`, `_META_UNLOCKS`,
  `_META_RESERVED`.
- **Flags** `0x030–0x03F`: `FLAG_ROGUELIKE_UNLOCKED_STARTER_4`, + reserved.

`VAR_ROGUELIKE_SCRATCH` (`0x40FF`) is throwaway working space for scripts and
is always reset.

### Why vars/flags (for now)
Vars and flags already live in the save block and persist for free — no
serialization code to write or corrupt. They're the right home for the handful
of scalar counters above. **Larger run structures** (the picked-boon list, the
room graph, per-run RNG beyond a seed) will outgrow scalar vars and need a
proper struct in the save block. That decision and its trade-offs are written
up separately in `docs/save-data.md`.

## Map layer

Roguelike maps live in their own map group, `gMapGroup_Roguelike` (index 75),
so they're isolated from the vanilla Hoenn maps. The hub is map 0. Rooms will
be added as further maps in this group. Wild encounters and PokéCenter/Mart
behavior get disabled per-map for roguelike maps (future tasks T29/T30).

## Entry points to know

- **`RoguelikeReset()`** (`src/roguelike.c`) — the one custom C hook so far.
  Registered as special `RoguelikeReset`; callable from any script with
  `special RoguelikeReset`.
- **`RoguelikeInit`** (`data/scripts/roguelike/roguelike_init.inc`) — empty
  no-op script label; the scaffold that proves the roguelike script tree links.
