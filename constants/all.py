import constants.spells as spells
import constants.spellbooks as spellbooks
import constants.items as items
import constants.characters as characters
import constants.maps as maps

# Creates aliases for the player spells.
def set_spell_constants(main):
 spells.set_spell_constants(main)

# Creates aliases for the spellbooks.
def set_spellbook_constants(main):
 spellbooks.set_spellbook_constants(main)

# Constants referencing particular items.
def set_item_constants(main):
 items.set_item_constants(main)

# Constants referencing the characters.
def set_character_constants(main):
 characters.set_character_constants(main)

# Constants referencing the maps.
def set_map_constants(main):
 maps.set_map_constants(main)
