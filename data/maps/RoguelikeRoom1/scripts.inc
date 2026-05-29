RoguelikeRoom1_MapScripts::
	.byte 0

@ ===========================================================================
@ Room 1 trainer (Roadmap T24-T26). Sight battle vs a single Lv.19 mon.
@ trainerbattle_single sets the trainer's defeat flag, so they won't re-fight.
@ Beat them, then take the exit warp at the back to return to the hub.
@ ===========================================================================
RoguelikeRoom1_EventScript_Trainer::
	trainerbattle_single TRAINER_ROGUELIKE_ROOM1, RoguelikeRoom1_Text_TrainerIntro, RoguelikeRoom1_Text_TrainerDefeat, RoguelikeRoom1_EventScript_TrainerPostBattle

RoguelikeRoom1_EventScript_TrainerPostBattle::
	msgbox RoguelikeRoom1_Text_TrainerPost, MSGBOX_DEFAULT
	release
	end

RoguelikeRoom1_Text_TrainerIntro:
	.string "You made it this far?\n"
	.string "Let's see what you've got!$"

RoguelikeRoom1_Text_TrainerDefeat:
	.string "Whoa, you're strong!$"

RoguelikeRoom1_Text_TrainerPost:
	.string "The way ahead is open.\n"
	.string "The portal at the back leads on.$"
