#ifndef GUARD_ROGUELIKE_H
#define GUARD_ROGUELIKE_H

// Roguelike romhack — run/meta state management.
// See data/scripts/roguelike/ for the matching event scripts and
// docs/architecture.md for where roguelike state lives.

// Clears all current-RUN vars and flags (the 0x40F7-0x40FB var block and the
// 0x020-0x02F flag block) plus the scratch var, while leaving META state
// (currency, unlocks) untouched. Called on death / return-to-hub so a fresh
// run starts clean. Registered as the special "RoguelikeReset".
void RoguelikeReset(void);

#endif // GUARD_ROGUELIKE_H
