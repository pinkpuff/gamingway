import constants.spells as spells
import constants.spellbooks as spellbooks
import constants.items as items
import constants.characters as characters
import constants.actors as actors
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

def set_spell_constants(main):
 spells.set_spell_constants(main)

def set_spellbook_constants(main):
 spellbooks.set_spellbook_constants(main)

def set_item_constants(main):
 items.set_item_constants(main)

def set_character_constants(main):
 characters.set_character_constants(main)

def set_actor_constants(main):
 actors.set_actor_constants(main)

def set_map_constants(main):
 maps.set_map_constants(main)
