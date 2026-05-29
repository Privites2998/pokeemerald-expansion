# Save-data strategy

How roguelike state is persisted. Decision recorded for Roadmap T6.

## Background: how the save works

The game keeps its persistent state in a few big structs in RAM that get
written to the cartridge's save memory in fixed-size **sectors**:

- **`SaveBlock1`** — the large one, spans multiple sectors. Most gameplay
  state lives here: vars, flags, the party, the bag, event state.
- **`SaveBlock2`** — single sector. Player identity, options, play time.
- **`SaveBlock3`** — added by the expansion for extra/boxed data.

Vars and flags are *already inside* `SaveBlock1`, so anything stored in a var
or flag is saved and loaded for free — no serialization code, no sector
juggling.

There's a hard ceiling: each block must fit in its sector budget
(`SECTOR_DATA_SIZE` × number of sectors). The expansion ships a checker in the
debug menu (and `STATIC_ASSERT`s in code) that fail the build if a block
overflows. So "just add a field" is cheap *only while there's headroom*.

## The decision

**Two-phase, lowest-blast-radius first:**

### Phase 1 (now): scalar vars + flags
All current roguelike state is a handful of scalar counters and booleans, so it
lives in reserved vars/flags — no new save code at all:
- Run vars `0x40F7–0x40FB`, meta vars `0x40FC–0x40FE`, scratch `0x40FF`.
- Run flags `0x020–0x02F`, meta flags `0x030–0x03F`.

See `docs/architecture.md` for the run-vs-meta split. This covers act number,
rooms cleared, currency, the unlock bitfield, the run seed, etc.

### Phase 2 (when scalars run out): one struct field on `SaveBlock1`
The picked-boon list, the room graph, and richer per-run data won't fit in
scalar vars. When we hit that wall, **extend an existing block — specifically
`SaveBlock1` — by adding a single field:**

```c
struct RoguelikeSaveData {
    // run state (cleared by RoguelikeReset)
    // meta state (persists)
};
// ...inside struct SaveBlock1:
    struct RoguelikeSaveData roguelike;
```

## Why extend `SaveBlock1` rather than add a new save block

| | Extend `SaveBlock1` (chosen) | New save block / sector |
|---|---|---|
| Code to write | One struct + one field. Save/load is automatic. | New sector IDs, read/write wiring, copy logic, asserts. |
| Risk | Low. Save format changes, but the engine handles the block already. | High. Touching sector machinery is the classic save-corruption footgun. |
| Save-compat | Adding fields shifts offsets → **old saves invalidated.** Fine pre-release. | Same offset issue, plus more surface to get wrong. |
| Space | Uses `SaveBlock1` headroom (finite — watch the build asserts). | More room, but we don't need it for an MVP. |

A brand-new save block only earns its complexity if roguelike data grows large
(many KB) or we want it isolated from engine state. For MVP scope, neither is
true, so we don't pay that cost.

## Practical rules

- **Back up your `.sav` before any session that changes save layout** (the
  Phase-2 work, and Roadmap tasks 49 / 65). Layout changes invalidate existing
  saves — expected during dev, but back up so you don't lose a test profile.
- **Keep the run/meta split inside the struct too** — group run fields and meta
  fields, so the reset logic clears one region and leaves the other, exactly
  like the var/flag blocks do now.
- **Watch the link-time memory report.** `SaveBlock1` shares the EWRAM budget
  (~87% used). Big additions there can fail the link; keep the struct lean.
