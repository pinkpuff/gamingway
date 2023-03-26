# This represents a spell that can be cast in battle.
# The same object will likely be used for "monster abilities" like ColdMist and
# Reaction and such but for now, only the 6-letter-name player spells are being
# read.
class Spell:
 
 def __init__(self):
  
  # The name of the spell in ASCII. Symbols like magic orbs use the corresponding
  # three letter code in square brackets (e.g. [BLK], [WHT], [SUM]). See text.py
  # for the full list of codes.
  self.name = ""
  
  # This is how long between inputting the command and the spell resolving. Slower
  # spells have a higher delay value.
  self.delay = 0
  
  # There are eight target types. This indicates which of the eight the spell uses.
  # The target types are enumerated in config.py.
  self.target = 0
  
  # The specific function of the spell's power depends on its effect type, but in
  # general, the higher this number is, the "stronger" the spell is. So damage
  # spells with higher power will deal more damage; healing spells with higher
  # power will heal more, etc. Some spell effects don't use it at all though.
  self.power = 0
  
  # This indicates the chance of the spell succeeding when cast. Even if a given
  # target isn't immune to the spell's effect, it still has a chance of failing.
  # For many (most?) spells, the chance of it failing is either 0 or close enough
  # to it that you don't have to consider it, especially since I think the caster's
  # spell power gets added to this number before making the check. However, I think
  # the target's magic evade is also subtracted from it (or otherwise reduces it
  # somehow) so sometimes you might see, for example, a spell from a late game
  # monster appear to do nothing; this could be because it missed due to your
  # character's magic evasion.
  self.hit = 0
  
  # This flag is set for spells that are usable on bosses. If the flag is unset,
  # monsters that have the Boss flag set will be immune to the spell.
  self.hitsboss = True
  
  # This indicates which spell effect the spell has. There is a large list of
  # effects, and this number represents the index in that list. See config.py for
  # the full list of spell effects.
  self.effect = 0
  
  # When this flag is set, if the spell deals damage, it will deal a lot more than
  # if this flag is unset. Most, if not all, of the vanilla damage spells have it
  # set, so if you set it, it will do the kind of damage you would probably expect.
  # I'm not sure what effect it has, if any, on non-damage spells.
  self.damaging = False
  
  # An attribute table is a set of flag settings for all the game's attribute
  # flags. These are things like "fire", "ice", etc, but also statuses like "mute",
  # "blind", "charm", etc. There is a list of these attribute tables in the rom and
  # things like spells and equipment use an index in this list rather than each one
  # having their own independent attribute table. So for example, say attribute
  # table 3 has the "ice" flag set and all other flags unset, then any spell or 
  # equipment that uses attribute index 3 will be considered to have the "ice" flag
  # and no other flags set. The meaning of having particular attribute flags set or
  # unset depends on what effect the spell has. For example, the "Add status"
  # effect will try to add all the statuses in the given attribute table whose 
  # flags are set. In contrast, the "Remove status" effect will try to remove all 
  # statuses from the target whose corresponding attribute flags are UNSET in the
  # spell's attribute table.
  self.attributes = 0
  
  # This flag indicates whether or not a player unit hit with the spell will show
  # the "impact" animation (the one that looks like they're getting hit).
  self.impact = False
  
  # This is the MP cost of the spell. The byte that encodes this uses the high bit
  # for something else so it physically can't be any higher than 128, but I think
  # putting it higher than 99 might cause some strange behaviour when the game
  # tries to display the MP cost, since it only expects a two digit number.
  self.mp = 0
  
  
  self.reflectable = False
  self.palette = 0
  self.sprites = 0
  self.visual1 = 0
  self.visual2 = 0
  self.sound = 0
 
 def read(self, rom, address):
  self.delay = rom.data[address] % 0x20
  self.target = rom.data[address] >> 5
  self.power = rom.data[address + 1]
  self.hit = rom.data[address + 2] % 0x80
  self.hitsboss = not rom.flag(address + 2, 7)
  self.effect = rom.data[address + 3] % 0x80
  self.damaging = not rom.flag(address + 3, 7)
  self.attributes = rom.data[address + 4] % 0x80
  self.impact = rom.flag(address + 4, 7)
  self.mp = rom.data[address + 5] % 0x80
  self.reflectable = not rom.flag(address + 5, 7)
 
 def write(self, rom, address):
  rom.data[address] = self.delay + (self.target << 5)
  rom.data[address + 1] = self.power
  rom.data[address + 2] = self.hit % 0x80
  rom.setbit(address + 2, 7, not self.hitsboss)
  rom.data[address + 3] = self.effect % 0x80
  rom.setbit(address + 3, 7, not self.damaging)
  rom.data[address + 4] = self.attributes % 0x80
  rom.setbit(address + 4, 7, self.impact)
  rom.data[address + 5] = self.mp % 0x80
  rom.setbit(address + 5, 7, not self.reflectable)
 
 def read_name(self, rom, address, text):
  bytelist = rom.data[address:address + rom.SPELL_NAME_WIDTH]
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 def write_name(self, rom, address, text):
  newname = text.ff4text(self.name)
  newname = newname.ljust(rom.SPELL_NAME_WIDTH, text.ff4text(" "))
  rom.inject(address, text.to_bytes(newname))

 def read_visuals(self, rom, address):
  self.palette = rom.data[address]
  self.sprites = rom.data[address + 1]
  self.visual1 = rom.data[address + 2]
  self.visual2 = rom.data[address + 3]
  
 def write_visuals(self, rom, address):
  rom.data[address] = self.palette
  rom.data[address + 1] = self.sprites
  rom.data[address + 2] = self.visual1
  rom.data[address + 3] = self.visual2
 
 def read_sound(self, rom, address):
  self.sound = rom.data[address]
 
 def write_sound(self, rom, address):
  rom.data[address] = self.sound
 
 def display_visuals(self, main):
  result  = "Palette: {}, ".format(main.text.hex(self.palette))
  result += "Sprites: {}, ".format(main.text.hex(self.sprites))
  result += "Visual1: {}, ".format(main.text.hex(self.visual1))
  result += "Visual2: {}, ".format(main.text.hex(self.visual2))
  result += "Sound:   {}".format(main.text.hex(self.sound))
  return result
 
 def display(self, main):
  result  = "Name: {}\n".format(self.name)
  result += "MP:     {}\n".format(self.mp)
  result += "Effect: {}\n".format(main.config.spell_effects[self.effect])
  result += "Target: {}\n".format(main.config.target_types[self.target])
  result += "Hit:    {}%\n".format(self.hit)
  result += "Power:  {}\n".format(self.power)
  result += "Delay:  {}\n".format(self.delay)
  result += "Attributes: [{}] ".format(main.text.hex(self.attributes))
  if len(main.attributes) > 0:
   if self.effect in [8, 9, 17, 28, 29]:
    result += main.attributes[self.attributes].display_alternate(main)
   elif self.effect == 11:
    result += main.attributes[self.attributes].display_inverted(main)
   else:
    result += main.attributes[self.attributes].display(main)
  properties = ""
  if self.reflectable:
   properties += "Reflectable"
  if self.hitsboss:
   if len(properties) > 0:
    properties += ", "
   properties += "Hits bosses"
  if self.damaging:
   if len(properties) > 0:
    properties += ", "
   properties += "Deals damage"
  if self.impact:
   if len(properties) > 0:
    properties += ", "
   properties += "Impact"
  if len(properties) > 0:
   result += "\n" + properties
  return result

class Spellbook:

 def __init__(self, spell_reference = []):
  self.spells = {}
  self.spell_reference = spell_reference
 
 def read_starting_spells(self, rom, address):
  self.spells[0] = []
  offset = 0
  for index in range(24):
   offset += 1
   if rom.data[address + index] == 0xFF:
    break
   spell = rom.data[address + index]
   self.spells[0].append(spell)
  return address + offset
 
 def write_starting_spells(self, rom, address):
  offset = 0
  
  # If there are any spells to write, write them.
  if len(self.spells) > 0:
   for spell in self.spells[0]:
    rom.data[address + offset] = spell
    offset += 1
  
  # Then, regardless of whether we wrote any spells or not, we need a
  # terminating FF byte. The only situation we don't need a terminator
  # is if we wrote 24 spells.
  if offset < 24:
   rom.data[address + offset] = 0xFF
   offset += 1
  
  # And make sure we report where we left off.
  return address + offset
 
 def read_spell_progression(self, rom, address):
  for index in range(99):
   self.spells[index + 1] = []
  level = rom.data[address]
  offset = 1
  while level != 0xFF:
   spell = rom.data[address + offset]
   offset += 1
   self.spells[level].append(spell)
   level = rom.data[address + offset]
   offset += 1
  return address + offset

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

 def clear(self, level = None):
  # Clears all spells learned at the specified level.
  # If the level is 0, it clears all starting spells.
  # If no level is specified, it clears the entire spellbook, including
  # all starting spells.
  if level == None:
   for index in range(100):
    self.spells[index] = []
  else:
   self.spells[level] = []

 def teach_spell(self, level, spell):
  # Teaches the specified spell at the specified level.
  # If the level is 0, the spell is added to the starting spells.
  # This function only works if the spell_reference has been set.
  if type(spell) != int:
   spell = self.spell_reference.index(spell)
  if not spell in self.spells[level]:
   self.spells[level].append(spell)

def read_spells(rom, text):
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

def write_spells(rom, text, spells):
 for index, spell in enumerate(spells):
  nameoffset = index * rom.SPELL_NAME_WIDTH
  spell.write_name(rom, rom.SPELL_NAMES_START + nameoffset, text)
  spell.write(rom, rom.SPELL_DATA_START + index * 6)
  spell.write_visuals(rom, rom.SPELL_VISUALS_START + index * 4)
  spell.write_sound(rom, rom.SPELL_SOUNDS_START + index)

def read_spellbooks(rom, spells = []):
 spellbooks = []
 address = rom.STARTING_SPELLS_START
 for index in range(rom.TOTAL_SPELLBOOKS):
  spellbook = Spellbook(spells)
  spellbooks.append(spellbook)
  address = spellbook.read_starting_spells(rom, address)
 address = rom.SPELL_PROGRESSIONS_START
 for index in range(rom.TOTAL_SPELLBOOKS):
  address = spellbooks[index].read_spell_progression(rom, address)
 return spellbooks

def write_spellbooks(rom, spellbooks):
 # First, verify there is room for all the progressions.
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

