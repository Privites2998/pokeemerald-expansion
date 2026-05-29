RoguelikeHub_MapScripts::
	.byte 0

@ ===========================================================================
@ Starter-select NPC (Roadmap T13-T19). Offers a 3-way choice; gives the
@ picked starter at Lv.20 and sets the run flag so it won't re-offer this run.
@ FLAG_ROGUELIKE_STARTER_CHOSEN is a RUN flag -> cleared by RoguelikeReset, so
@ each new run lets you pick again.
@ ===========================================================================
RoguelikeHub_EventScript_StarterNPC::
	lock
	faceplayer
	goto_if_set FLAG_ROGUELIKE_STARTER_CHOSEN, RoguelikeHub_EventScript_StarterAlreadyChosen
	msgbox RoguelikeHub_Text_StarterIntro, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_ROGUELIKE_STARTER, FALSE
	switch VAR_RESULT
	case 0, RoguelikeHub_EventScript_GiveTreecko
	case 1, RoguelikeHub_EventScript_GiveLitten
	case 2, RoguelikeHub_EventScript_GiveSquirtle
	case MULTI_B_PRESSED, RoguelikeHub_EventScript_StarterDeclined
	end

RoguelikeHub_EventScript_GiveTreecko::
	givemon SPECIES_TREECKO, 20, ITEM_NONE
	goto RoguelikeHub_EventScript_StarterGiven

RoguelikeHub_EventScript_GiveLitten::
	givemon SPECIES_LITTEN, 20, ITEM_NONE
	goto RoguelikeHub_EventScript_StarterGiven

RoguelikeHub_EventScript_GiveSquirtle::
	givemon SPECIES_SQUIRTLE, 20, ITEM_NONE
	goto RoguelikeHub_EventScript_StarterGiven

RoguelikeHub_EventScript_StarterGiven::
	setflag FLAG_ROGUELIKE_STARTER_CHOSEN
	msgbox RoguelikeHub_Text_StarterGiven, MSGBOX_DEFAULT
	release
	end

RoguelikeHub_EventScript_StarterAlreadyChosen::
	msgbox RoguelikeHub_Text_StarterAlready, MSGBOX_DEFAULT
	release
	end

RoguelikeHub_EventScript_StarterDeclined::
	msgbox RoguelikeHub_Text_StarterDeclined, MSGBOX_DEFAULT
	release
	end

@ ===========================================================================
@ Portal pads (Roadmap T20). Placeholder until run entry is wired (T22).
@ Both console tiles share this trigger.
@ ===========================================================================
RoguelikeHub_EventScript_Portal::
	lockall
	msgbox RoguelikeHub_Text_PortalNotYet, MSGBOX_DEFAULT
	releaseall
	end

RoguelikeHub_Text_StarterIntro:
	.string "Welcome, challenger.\p"
	.string "Choose the partner you'll take\n"
	.string "into the trial.$"

RoguelikeHub_Text_StarterGiven:
	.string "A fine choice!\p"
	.string "Your partner stands ready at Lv. 20.\p"
	.string "Step onto a portal pad when you are\n"
	.string "prepared to begin.$"

RoguelikeHub_Text_StarterAlready:
	.string "Your partner is already at your\n"
	.string "side. Good luck out there.$"

RoguelikeHub_Text_StarterDeclined:
	.string "Take your time. Speak with me when\n"
	.string "you have decided.$"

RoguelikeHub_Text_PortalNotYet:
	.string "The portal hums with energy…\p"
	.string "But the way is not open yet.$"
