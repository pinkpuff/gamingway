import constants.spells as spells
import constants.spellbooks as spellbooks
import constants.items as items
import constants.jobs as jobs
import constants.characters as characters
import constants.actors as actors
import constants.commands as commands
import constants.monsters as monsters
import constants.maps as maps

# This file mainly exists as a convenience so I don't have to import all those
# separate constant files in the main module. Each constant setting function just
# defers to the corresponding individual file.

# The general naming convention for the names of things is that I try to use the
# vanilla names for the things that have vanilla names. Punctuation, symbols, etc
# are skipped. 

# Names that are obvious abbreviations that could easily result in typos have both
# spellings (e.g. EXCALBUR and EXCALIBUR both point to the same item). 
# Type suffixes exist on objects that need them but not on ones where it's obvious.
# For example, the flame spear is FLAME_SPEAR but the first plain spear is just 
# SPEAR as opposed to SPEAR_SPEAR. 

# "Proper name" items like Excalibur don't have a suffix, as EXCALIBUR_SWORD seems a
# little awkward and unintuitive.

# Objects that were "dummied" or otherwise had no names in vanilla but do have names
# in Free Enterprise use the Free Enterprise naming convention. Objects that had no
# name in either use names that I personally find intuitive. Fortunately python is
# very loose with the notion of "constants" so you can just redefine them as you
# see fit, even from within your own project that you're importing Gamingway into.

def set_spell_constants(main):
 spells.set_constants(main)

def set_spellbook_constants(main):
 spellbooks.set_constants(main)

def set_item_constants(main):
 items.set_constants(main)

def set_job_constants(main):
 jobs.set_constants(main)

def set_character_constants(main):
 characters.set_constants(main)

def set_actor_constants(main):
 actors.set_constants(main)

def set_command_constants(main):
 commands.set_constants(main)

def set_monster_constants(main):
 monsters.set_constants(main)

def set_map_constants(main):
 maps.set_constants(main)
