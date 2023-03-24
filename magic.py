class Spell:
 
 def __init__(self):
  self.name = ""
  self.delay = 0
  self.target = 0
  self.power = 0
  self.hit = 0
  self.hitsboss = True
  self.effect = 0
  self.damaging = False
  self.attributes = 0
  self.impact = False
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

