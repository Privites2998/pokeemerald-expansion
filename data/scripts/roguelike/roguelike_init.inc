@ ==========================================================================
@ Roguelike romhack — script scaffold (Roadmap T8)
@ ==========================================================================
@ Home for run/hub event scripts. Empty no-op for now: it exists so the
@ linker sees the roguelike script tree and future .inc files have a parent
@ to live beside. Add real scripts here as the hub/run loop comes online.

RoguelikeInit::
	end

@ ---------------------------------------------------------------------------
@ Debug: clear the current run (Roadmap T10). Wired into the debug Utilities
@ menu as "Roguelike: Reset run". Calls the RoguelikeReset special, which
@ clears run state but keeps meta-progression.
@ ---------------------------------------------------------------------------
Debug_EventScript_RoguelikeReset::
	special RoguelikeReset
	msgbox RoguelikeText_RunReset, MSGBOX_DEFAULT
	release
	end

RoguelikeText_RunReset:
	.string "Roguelike run state cleared.\p"
	.string "Meta-progression kept.$"
