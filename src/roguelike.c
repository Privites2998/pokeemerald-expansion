#include "global.h"
#include "event_data.h"
#include "roguelike.h"
#include "constants/flags.h"
#include "constants/vars.h"

// Resets all current-run state so a new run starts clean. Meta-progression
// (VAR_ROGUELIKE_META_*, FLAG_ROGUELIKE_META_*) is deliberately left alone --
// see the run-vs-meta split documented in include/constants/{vars,flags}.h.
void RoguelikeReset(void)
{
    u16 i;

    // Clear run flags (0x020-0x02F). Meta flags (0x030-0x03F) untouched.
    for (i = FLAG_ROGUELIKE_RUN_FLAGS_START; i <= FLAG_ROGUELIKE_RUN_FLAGS_END; i++)
        FlagClear(i);

    // Clear run vars (0x40F7-0x40FB). Meta vars (0x40FC-0x40FE) untouched.
    for (i = VAR_ROGUELIKE_RUN_START; i <= VAR_ROGUELIKE_RUN_END; i++)
        VarSet(i, 0);

    // Scratch var sits after the meta block; always reset it too.
    VarSet(VAR_ROGUELIKE_SCRATCH, 0);
}
