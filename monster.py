from common import FlagSet, AttributeTable

class Monster:
 
 def __init__(self, config):
  self.config = config
  self.name = ""
  self.boss = False
  self.level = 0
  self.hp = 0
  self.gp = 0
  self.xp = 0
  self.attack_index = 0
  self.defense_index = 0
  self.magic_defense_index = 0
  self.speed_index = 0
  self.drop_rate = 0
  self.drop_table = 0
  self.behaviour = 0
  self.lunar = False
  self.has_attributes = False
  self.has_resistances = False
  self.has_weaknesses = False
  self.has_magic_power = False
  self.has_races = False
  self.has_reaction = False
  self.attributes = AttributeTable()
  self.resistances = AttributeTable()
  self.weaknesses = FlagSet()
  self.magic_power = 0
  self.races = FlagSet()
  self.reaction = 0
  self.size = 0
  self.palette = 0
  self.sprite1 = 0
  self.sprite2 = 0
  self.display_sprite = 0
  self.special_size = 0
 
 def read(self, rom, address):
  self.level = rom.data[address] % 0x80
  self.boss = rom.flag(address, 7)
  self.hp = rom.data[address + 1] + rom.data[address + 2] * 0x100
  self.attack_index = rom.data[address + 3]
  self.defense_index = rom.data[address + 4]
  self.magic_defense_index = rom.data[address + 5]
  self.speed_index = rom.data[address + 6]
  self.drop_table = rom.data[address + 7] % 0x40
  self.drop_rate = rom.data[address + 7] >> 6
  self.behaviour = rom.data[address + 8]
  self.has_attributes = rom.flag(address + 9, 7)
  self.has_resistances = rom.flag(address + 9, 6)
  self.has_weaknesses = rom.flag(address + 9, 5)
  self.has_magic_power = rom.flag(address + 9, 4)
  self.has_races = rom.flag(address + 9, 3)
  self.has_reaction = rom.flag(address + 9, 2)
  offset = 10
  if self.has_attributes:
   self.attributes.read(rom, address + offset)
   offset += 3
  if self.has_resistances:
   self.resistances.read(rom, address + offset)
   offset += 3
  if self.has_weaknesses:
   self.weaknesses.from_byte(rom.data[address + offset])
   offset += 1
  if self.has_magic_power:
   self.magic_power = rom.data[address + offset]
   offset += 1
  if self.has_races:
   self.races.read(rom, address + offset)
   offset += 1
  if self.has_reaction:
   self.reaction = rom.data[address + offset]

 def write(self, rom, address):
  rom.data[address] = self.level % 0x80
  rom.setbit(address, 7, self.boss)
  rom.data[address + 1] = self.hp % 0x100
  rom.data[address + 2] = self.hp >> 8
  rom.data[address + 3] = self.attack_index
  rom.data[address + 4] = self.defense_index
  rom.data[address + 5] = self.magic_defense_index
  rom.data[address + 6] = self.speed_index
  rom.data[address + 7] = self.drop_table + (self.drop_rate << 6)
  rom.data[address + 8] = self.behaviour
  rom.data[address + 9] = 0
  rom.setbit(address + 9, 7, self.has_attributes)
  rom.setbit(address + 9, 6, self.has_resistances)
  rom.setbit(address + 9, 5, self.has_weaknesses)
  rom.setbit(address + 9, 4, self.has_magic_power)
  rom.setbit(address + 9, 3, self.has_races)
  rom.setbit(address + 9, 2, self.has_reaction)
  offset = 10
  if self.has_attributes:
   self.attributes.write(rom, address + offset)
   offset += 3
  if self.has_resistances:
   self.resistances.write(rom, address + offset)
   offset += 3
  if self.has_weaknesses:
   self.weaknesses.write(rom, address + offset)
   offset += 1
  if self.has_magic_power:
   rom.data[address + offset] = self.magic_power
   offset += 1
  if self.has_races:
   self.races.write(rom, address + offset)
   offset += 1
  if self.has_reaction:
   rom.data[address + offset] = self.reaction
   offset += 1
  # We need to return the length of the record so the main function can
  # compute the pointer table correctly.
  return offset
 
 def room_needed(self):
  result = 10
  if self.has_attributes:
   result += 3
  if self.has_resistances:
   result += 3
  if self.has_weaknesses:
   result += 1
  if self.has_magic_power:
   result += 1
  if self.has_races:
   result += 1
  if self.has_reaction:
   result += 1
  return result
 
 def read_name(self, rom, address, text):
  bytelist = rom.data[address:address + rom.MONSTER_NAME_WIDTH]
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 def write_name(self, rom, address, text):
  newname = text.ff4text(self.name)
  newname = newname.ljsut(rom.MONSTER_NAME_WIDTH, text.ff4text(" "))
  rom.inject(address, text.to_bytes(newname))
 
 def read_visuals(self, rom, address):
  self.size = rom.data[address]
  self.palette = rom.data[address + 1]
  self.sprite1 = rom.data[address + 2]
  self.sprite2 = rom.data[address + 3]
 
 def write_visuals(self, rom, address):
  rom.data[address] = self.size
  rom.data[address + 1] = self.palette
  rom.data[address + 2] = self.sprite1
  rom.data[address + 3] = self.sprite2
 
 def read_gp(self, rom, address):
  self.gp = rom.read_wide(address)
 
 def write_gp(self, rom, address):
  rom.write_wide(address, self.gp)
 
 def read_xp(self, rom, address):
  self.xp = rom.read_wide(address)
 
 def write_xp(self, rom, address):
  rom.write_wide(address, self.xp)
  
 def display(self, main):
  result = ""
  result += "Name: {}".format(self.name)
  if self.boss:
   result += " (BOSS)"
  result += "\n"
  result += "Level: {}\n".format(self.level)
  result += "HP:    {}\n".format(self.hp)
  result += "GP:    {}\n".format(self.gp)
  result += "Exp:   {}\n".format(self.xp)
  result += "Attack:  [{}]\n".format(main.text.hex(self.attack_index))
  result += "Defense: [{}]\n".format(main.text.hex(self.defense_index))
  result += "M.Def.:  [{}]\n".format(main.text.hex(self.magic_defense_index))
  result += "Speed:   [{}]\n".format(main.text.hex(self.speed_index))
  droprate = main.config.drop_rates[self.drop_rate]
  result += "Drop Rate:  {} ({})\n".format(self.drop_rate, droprate)
  result += "Drop Table: [{}]\n".format(self.drop_table)
  result += "Behaviour:  [{}]".format(main.text.hex(self.behaviour))
  if self.has_attributes:
   result += "\n"
   result += "Adds: "
   result += self.attributes.display(main)
  if self.has_resistances:
   result += "\n"
   result += "Resists: "
   result += self.resistances.display(main)
  if self.has_weaknesses:
   result += "\n"
   result += "Weakness: "
   result += self.weaknesses.display(main, main.config.element_names)
  if self.has_magic_power:
   result += "\n"
   result += "M.Power: {}".format(self.magic_power)
  if self.has_races:
   result += "\n"
   result += "Races: "
   result += self.races.display(main, main.config.race_names)
  if self.has_reaction:
   result += "\n"
   result += "Reaction: [{}]".format(main.text.hex(self.reaction))
  return result

 # This gives the monster one or more additional weaknesses. You can specify it as 
 # an index, as a string matching one of the element names in the config, or as a 
 # list of either of the above. This also automatically sets the monster's
 # "has_weaknesses" flag.
 def add_weakness(self, weakness):

  # Convert the parameter to a list of element flag indexes.
  weaknesslist = self.config.index_list(weakness, "elements")
  
  # Then process the list.
  if len(weaknesslist) > 0:
   for index in weaknesslist:
    self.weaknesses.flags[index] = True

   # Make sure we set the "has_weaknesses" flag.
   self.has_weaknesses = True
 
 # This sets the monster's weaknesses to the given list. All flags included in the
 # list will be set in the monster's weaknesses, and all flags not included will be
 # unset. The flags can be specified by name as per the config or by index. A single
 # string or integer will be interpreted as a list containing only that flag. If
 # this results in the monster having no weaknesses, its "has_weaknesses" flag will
 # be unset.
 def set_weakness(self, weakness):

  # Convert the parameter to a list of element flag indexes.
  weaknesslist = self.config.index_list(weakness, "elements")

  # Then process the list.
  for index in range(len(self.config.element_names)):
   if index in weaknesslist:
    self.weaknesses.flags[index] = True
   else:
    self.weaknesses.flags[index] = False

  # Update the "has_weaknesses" flag appropriately.
  self.has_weaknesses = (len(self.weaknesses.flags) > 0)

 # This removes an element from the monster's weaknesses. You can specify it as an
 # index, as a string matching one of the element names in the config, or as a list
 # of either of the above. If this results in the monster having no remaining
 # weaknesses, it will unset the monster's "has_weaknesses" flag.
 def remove_weakness(self, weakness):

  # Convert the parameter to a list of element flag indexes.
  weaknesslist = self.config.index_list(weakness, "elements")

  # Then process the list.
  for index in weaknesslist:
   self.weaknesses.flags[index] = False

  # Update the "has_weaknesses" flag appropriately.
  self.has_weaknesses = (len(self.weaknesses.flags) > 0)

 # This gives the monster one or more additional resistances. You can specify it as 
 # an index, as a string matching one of the element names in the config, or as a 
 # list of either of the above. This also automatically sets the monster's
 # "has_resistances" flag.
 def add_resistance(self, resistance):

  # Convert the parameter to a list of element flag indexes.
  resistancelist = self.config.index_list(resistance, "elements")
  
  # Then process the list.
  if len(resistancelist) > 0:
   for index in resistancelist:
    self.resistances.flags[index] = True

   # Make sure we set the "has_resistances" flag.
   self.has_resistance = True
 
 # This sets the monster's resistances to the given list. All flags included in the
 # list will be set in the monster's resistances, and all flags not included will be
 # unset. The flags can be specified by name as per the config or by index. A single
 # string or integer will be interpreted as a list containing only that flag. If
 # this results in the monster having no resistances, its "has_resistances" flag 
 # will be unset.
 def set_resistance(self, resistance):

  # Convert the parameter to a list of element flag indexes.
  resistancelist = self.config.index_list(resistance, "elements")

  # Then process the list.
  for index in range(len(self.config.element_names)):
   if index in resistancelist:
    self.resistancees.flags[index] = True
   else:
    self.resistancees.flags[index] = False

  # Update the "has_resistances" flag appropriately.
  self.has_resistances = (len(self.resistances.flags) > 0)

 # This removes an element from the monster's weaknesses. You can specify it as an
 # index, as a string matching one of the element names in the config, or as a list
 # of either of the above. If this results in the monster having no remaining
 # resistances, it will unset the monster's "has_resistances" flag.
 def remove_resistance(self, resistance):

  # Convert the parameter to a list of element flag indexes.
  resistancelist = self.config.index_list(resistance, "elements")

  # Then process the list.
  for index in resistancelist:
   self.resistances.flags[index] = False

  # Update the "has_resistances" flag appropriately.
  self.has_resistances = (len(self.resistances.flags) > 0)

 # This gives the monster one or more additional races. You can specify it as an
 # index, as a string matching one of the race names in the config, or as a list of
 # either of the above. This also automaticaly sets the monster's "has_races" flag.
 def add_race(self, race):
  
  # Convert the parameter to a list of race flag indexes.
  racelist = self.config.index_list(race, "races")

  # Then process the list.
  if len(racelist) > 0:
   for index in racelist:
    self.races.flags[index] = True
  
   # Make sure we set the "has_races" flag.
   self.has_races = True
 
 # This sets the monster's races to the given list. All flags included in the list
 # will be set in the monster's races, and all the flags not included will be unset.
 # The flags can be specified by name as per the config or by index. A single string
 # or integer will be interpreted as a list containing only that flag. If this
 # results in the monster having no races, its "has_races" flag will be unset.
 def set_race(self, race):
  
  # Convert the parameter to a list of race indexes.
  racelist = self.config.index_list(race, "races")

  # Then process the list.
  for index in range(len(self.config.race_names)):
   if index in racelist:
    self.races.flags[index] = True
   else:
    self.races.flags[index] = False

  # Update the "has_races" flag appropriately.
  self.has_races = (len(self.races.flags) > 0)

 # This removes an elemtn from teh monster's races. You can specify it as an index,
 # as a string matching one of the race names in teh config, or as a list of eihter
 # of the above. If this results in the monster having no remaining races, it will
 # unset the monster's "has_races" flag.
 def remove_race(self, race):

  # Convert the parameter to a list of race indexes.
  racelist = self.config.index_list(race, "races")

  # Then process the list.
  for index in racelist:
   self.races.flag[index] = False

  # Update the "has_races" flag appropriately.
  self.has_races = (len(self.races.flags) > 0)
