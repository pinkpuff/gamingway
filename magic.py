from spell import Spell
from spellbook import Spellbook

# Read all the spells from the rom.
def read_spells(rom, text):

 # For the most part, we just create spells and add them to the list and use the
 # Spell object's read function. However, there are several different types of data
 # that have to be read separately.
 spells = []
 for index in range(rom.TOTAL_SPELLS):
  spell = Spell()
  spells.append(spell)
  nameoffset = index * rom.SPELL_NAME_WIDTH
  spell.read_name(rom, rom.SPELL_NAMES_START + nameoffset, text)
  spell.read(rom, rom.SPELL_DATA_START + index * 6)
  spell.read_visuals(rom, rom.SPELL_VISUALS_START + index * 4)
  spell.read_sound(rom, rom.SPELL_SOUNDS_START + index)
 return spells

# Write all the spells back to the rom.
def write_spells(rom, text, spells):
 for index, spell in enumerate(spells):
  nameoffset = index * rom.SPELL_NAME_WIDTH
  spell.write_name(rom, rom.SPELL_NAMES_START + nameoffset, text)
  spell.write(rom, rom.SPELL_DATA_START + index * 6)
  spell.write_visuals(rom, rom.SPELL_VISUALS_START + index * 4)
  spell.write_sound(rom, rom.SPELL_SOUNDS_START + index)

# Read all the spellbooks from the rom.
def read_spellbooks(rom, spells = []):
 spellbooks = []

 # We start by reading all the starting spells for all the spellbooks.
 address = rom.STARTING_SPELLS_START
 for index in range(rom.TOTAL_SPELLBOOKS):
  spellbook = Spellbook(spells)
  spellbooks.append(spellbook)
  address = spellbook.read_starting_spells(rom, address)

 # After that, we read all the spell progressions for all the spellbooks.
 address = rom.SPELL_PROGRESSIONS_START
 for index in range(rom.TOTAL_SPELLBOOKS):
  address = spellbooks[index].read_spell_progression(rom, address)

 # And return the list of spellbooks.
 return spellbooks

# Write all the spellbooks back to the rom.
def write_spellbooks(rom, spellbooks):

 # This is variable-length data, so we first need to verify there is room for all
 # the progressions.
 room_needed = 0
 for spellbook in spellbooks:

  # The terminating FF counts as one byte.
  room_needed += 1

  # Then each spell in the spellbook other than the starting spells
  # counts as two.
  for level, page in spellbook.spells.items():
   if level > 0:
    room_needed += len(page) * 2

 # If there's not enough room for everything, we output an error
 # message and don't write anything.
 if room_needed > rom.SPELL_PROGRESSIONS_ROOM:
  print("ERROR: Not enough room for spellbooks.")

 # Otherwise, we write the spellbooks.
 else:
  address = rom.STARTING_SPELLS_START
  for spellbook in spellbooks:
   address = spellbook.write_starting_spells(rom, address)
  address = rom.SPELL_PROGRESSIONS_START
  for spellbook in spellbooks:
   address = spellbook.write_spell_progression(rom, address)

