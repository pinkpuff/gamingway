import common

class Monster:
 
 def __init__(self):
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
  self.attributes = common.AttributeTable()
  self.resistances = common.AttributeTable()
  self.weaknesses = common.FlagSet()
  self.magic_power = 0
  self.races = common.FlagSet()
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
  
def read_monsters(rom, text):
 monsters = []
 for index in range(rom.TOTAL_MONSTERS):
  monster = Monster()
  monsters.append(monster)
  pointer = rom.MONSTER_POINTERS_START + index * 2
  offset = rom.data[pointer] + rom.data[pointer + 1] * 0x100
  monster.read(rom, rom.MONSTER_DATA_BONUS + offset)
  offset = rom.MONSTER_NAME_WIDTH * index
  monster.read_name(rom, rom.MONSTER_NAMES_START + offset, text)
  monster.read_gp(rom, rom.MONSTER_GP_START + index * 2)
  monster.read_xp(rom, rom.MONSTER_XP_START + index * 2)
 return monsters

def write_monsters(rom, text, monsters):
 # It appears the monster data in the vanilla rom is not "perfectly
 # packed" as it were. The occasional monster pointer starts a byte or
 # two past where it would need to in order for the monster data to be
 # tightly packed together. However, this function DOES pack the data
 # as tightly as possible and therefore using this function can cause
 # differences with the vanilla rom, even if none of the monster data
 # has been changed.
 room_needed = 0
 for monster in monsters:
  room_needed += monster.room_needed()
 if room_needed > rom.MONSTER_DATA_ROOM:
  print("ERROR: Not enough room for monster data.")
 else:
  address = rom.MONSTER_DATA_START
  for index, monster in enumerate(monsters):
   pointer = address - rom.MONSTER_DATA_BONUS
   rom.write_wide(rom.MONSTER_POINTERS_START + index * 2, pointer)
   address += monster.write(rom, address)
  
  