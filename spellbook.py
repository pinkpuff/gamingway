# A Spellbook is the list of spells someone either knows currently or will learn at
# future levels. Spellbooks are linked to Jobs, not characters. That's why, for
# example, Rydia can have a White spellbook as a child but not as an adult.
# Each character can have up to one White spellbook, up to one Black spellbook, and
# up to one Call (summon) spellbook. I think Ninja counts as a Black spellbook but
# has some kind of special hardcoding that replaces the word Black in the menu with
# the word Ninja.
class Spellbook:

 def __init__(self, spell_reference = []):

  # This represents the list of spells the job will learn and the levels at which
  # they will learn them. Spells that the spellbook begins populated with already
  # are represented by giving them a "learned level" of 0.
  self.spells = {}

  # This is a reference to the rom's spell list. This is required in order for
  # the functions that manipulate the spellbook to be able to pass references to
  # actual spells as opposed to just indexes. For example, it would be a lot more
  # convenient and intuitive to be able to type something like:
  #  ff4.RYDIA_WHITE.teach_spell(25, ff4.HEAL_SPELL)
  # as opposed to something like:
  #  ff4.RYDIA_WHITE.teach_spell(25, 18)
  self.spell_reference = spell_reference
 
 # This reads the list of spells that the spellbook begins already populated with.
 # These are stored separately in the rom from the spells that are learned at
 # later levels, so they have separate reading functions.
 def read_starting_spells(self, rom, address):

  # Each entry in the spellbook indicates an association between a level number and
  # a LIST of spell indexes, not just a single spell. This is because sometimes a
  # job can learn multiple spells at the same level. 
  self.spells[0] = []

  # This is for calculating the number of bytes we read while reading this
  # spellbooks's starting spells. This is important where it's a variable-length
  # list and the general function that reads all the spellbooks needs to know
  # where it left off, as there's no pointer table.
  offset = 0

  # Each list of starting spells is terminated in one of two ways:
  #  * It reads an FF byte; or
  #  * It has 24 entries.
  # So if you read a full spellbook worth of spells (24), the list is considered
  # done without having a FF separator. If the spellbook contains fewer starting 
  # spells than that, it will end in an FF byte to signal the end of the list.
  for index in range(24):
   offset += 1

   # If we read a FF byte, we know the list is terminated, so we can exit without
   # trying to add a spell to the list.
   if rom.data[address + index] == 0xFF:
    break

   # Otherwise it's a spell, so we add it to the list associated with "level 0".
   spell = rom.data[address + index]
   self.spells[0].append(spell)

  # Finally we return the modified address to signal to the outer function where we
  # left off reading.
  return address + offset
 
 # Write the starting spells back to the rom.
 def write_starting_spells(self, rom, address):

  # This is for tracking where we left off writing data. Since the learned spells
  # are variable-length lists, we need to report this to the parent function so it
  # knows where to pick up with writing the next list.
  offset = 0
  
  # If there are any spells to write, write them.
  if len(self.spells) > 0:
   for spell in self.spells[0]:
    rom.data[address + offset] = spell
    offset += 1
  
  # Then, even if we didn't write any spells, we need a terminating FF byte. The 
  # only situation we don't need a terminator is if we wrote a full 24 spells.
  if offset < 24:
   rom.data[address + offset] = 0xFF
   offset += 1
  
  # And make sure we report where we left off.
  return address + offset
 
 # This reads the spells learned at future levels from the rom.
 # These are stored separately in the rom from the spells that it starts with, so
 # they have separate reading functions.
 def read_spell_progression(self, rom, address):

  # We start by populating the dictionary encoding the spellbook with an empty list
  # at each level up to 99.
  for index in range(99):
   self.spells[index + 1] = []

  # Each entry in the list of learned spells consists of two bytes: a level, and a
  # spell index. The list is terminated when we read a FF byte for the level.
  # Therefore, first we read a level, then if it's not FF, we enter the loop where
  # we read a spell, add that level/spell pair to the list, and then read another
  # level byte, and so on.
  level = rom.data[address]
  offset = 1
  while level != 0xFF:
   spell = rom.data[address + offset]
   offset += 1
   self.spells[level].append(spell)
   level = rom.data[address + offset]
   offset += 1

  # And report where we left off.
  return address + offset

 # Write the spells learned at future levels back to the rom.
 def write_spell_progression(self, rom, address):
  offset = 0
  for level, page in self.spells.items():
   if level > 0:
    if len(page) > 0:
     for spell in page:
      rom.data[address + offset] = level
      offset += 1
      rom.data[address + offset] = spell
      offset += 1
  rom.data[address + offset] = 0xFF
  offset += 1
  return address + offset

 # Return a string containing all the information for this spellbook.
 def display(self, main):
  result = ""
  if len(self.spells) > 0:
   for level, page in self.spells.items():
    if level > 0:
     for spell in page:
      if len(main.spells) > spell:
       spellname = main.spells[spell].name
       result += "Lv {:02}: {}\n".format(level, spellname)
    else:
     for spell in page:
      if len(main.spells) > spell:
       result += "START: {}\n".format(main.spells[spell].name)
  if len(result) > 1:
   result = result[0:len(result) - 1]
  return result

 # Clears all spells learned at the specified level.
 # If the level is 0, it clears all starting spells.
 # If no level is specified, it clears the entire spellbook, including
 # all starting spells.
 def clear(self, level = None):
  if level == None:
   for index in range(100):
    self.spells[index] = []
  else:
   self.spells[level] = []

 # Teaches the specified spell at the specified level.
 # If the level is 0, the spell is added to the starting spells.
 # This function only works if the spell_reference has been set.
 def teach_spell(self, level, spell):
  if type(spell) != int:
   spell = self.spell_reference.index(spell)
  if not spell in self.spells[level]:
   self.spells[level].append(spell)

