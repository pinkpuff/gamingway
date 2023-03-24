import common

class LevelUp:

 def __init__(self):
  self.statbonus = common.StatBuff(True)
  self.hp = 0
  self.mp = 0
  self.tnl = 0
 
 def read(self, rom, address):
  self.statbonus.read(rom, address)
  self.hp = rom.data[address + 1]
  self.mp = rom.data[address + 2] % 0x20
  self.tnl = rom.data[address + 3] + rom.data[address + 4] * 0x100
  self.tnl += (rom.data[address + 2] >> 5) * 0x10000
 
 def write(self, rom, address):
  self.statbonus.write(rom, address)
  rom.data[address + 1] = self.hp
  rom.data[address + 2] = self.mp % 0x20 + ((self.tnl >> 16) << 5)
  rom.data[address + 3] = self.tnl % 0x100
  rom.data[address + 4] = (self.tnl >> 8) % 0x100
 
 def display(self, main):
  result = ""
  result += "{} / ".format(self.statbonus.display(main))
  result += "HP: +{:3} / ".format(self.hp)
  result += "MP: +{:2} / ".format(self.mp)
  result += "TNL: {:6}".format(self.tnl)
  return result

class Character:
 
 def __init__(self):
  self.name = ""
  self.id = 0
  self.left_handed = False
  self.right_handed = False
  self.job = 0
  self.level = 0
  self.mystery_bytes = [0, 0, 0, 0]
  self.current_hp = 0
  self.max_hp = 0
  self.current_mp = 0
  self.max_mp = 0
  self.stats = [0, 0, 0, 0, 0]
  self.mystery_bytes2 = [0, 0, 0]
  self.xp = 0
  self.mystery_bytes3 = [0, 0, 0]
  self.tnl = 0
  self.levelups = []
  self.after70 = []

 def read(self, rom, address):
  self.id = rom.data[address] % 0x40
  self.left_handed = rom.flag(address, 6)
  self.right_handed = rom.flag(address, 7)
  self.job = rom.data[address + 1]
  self.level = rom.data[address + 2]
  # The bytes at address + 3 through address + 6 appear to always be 0
  # in vanilla. Wasted space? Maybe but I'll track them anyway in case 
  # there are any later revelations or in case someone decides to make 
  # use of them somehow in a hack or something.
  for index in range(4):
   self.mystery_bytes[index] = rom.data[address + 3 + index]
  self.current_hp = rom.data[address + 7] + rom.data[address + 8] * 0x100
  self.max_hp = rom.data[address + 9] + rom.data[address + 10] * 0x100
  self.current_mp = rom.data[address + 11] + rom.data[address + 12] * 0x100
  self.max_mp = rom.data[address + 13] + rom.data[address + 14] * 0x100
  for index in range(5):
   self.stats[index] = rom.data[address + 15 + index]
  # These do appear to contain some kind of data in vanilla but I'm not sure what it is or what it means.
  for index in range(3):
   self.mystery_bytes2[index] = rom.data[address + 20 + index]
  self.xp = rom.data[address + 23] + rom.data[address + 24] * 0x100
  self.xp += rom.data[address + 25] * 0x10000
  # In vanilla, these contain the same data for each character, but they aren't all 0s.
  # They all contain 0x00, 0x10, 0x00. I have no idea what that could signify.
  for index in range(3):
   self.mystery_bytes3[index] = rom.data[address + 26 + index]
  self.tnl = rom.data[address + 29] + rom.data[address + 30] * 0x100
  self.tnl += rom.data[address + 31] * 0x10000

 def write(self, rom, address):
  rom.data[address] = self.id
  rom.setbit(address, 6, self.left_handed)
  rom.setbit(address, 7, self.right_handed)
  rom.data[address + 1] = self.job
  rom.data[address + 2] = self.level
  rom.data[address + 3] = self.mystery_bytes[0]
  rom.data[address + 4] = self.mystery_bytes[1]
  rom.data[address + 5] = self.mystery_bytes[2]
  rom.data[address + 6] = self.mystery_bytes[3]
  rom.data[address + 7] = self.current_hp % 0x100
  rom.data[address + 8] = self.current_hp >> 8
  rom.data[address + 9] = self.max_hp % 0x100
  rom.data[address + 10] = self.max_hp >> 8
  rom.data[address + 11] = self.current_mp % 0x100
  rom.data[address + 12] = self.current_mp >> 8
  rom.data[address + 13] = self.max_mp % 0x100
  rom.data[address + 14] = self.max_mp >> 8
  rom.data[address + 15] = self.stats[0]
  rom.data[address + 16] = self.stats[1]
  rom.data[address + 17] = self.stats[2]
  rom.data[address + 18] = self.stats[3]
  rom.data[address + 19] = self.stats[4]
  rom.data[address + 20] = self.mystery_bytes2[0]
  rom.data[address + 21] = self.mystery_bytes2[1]
  rom.data[address + 22] = self.mystery_bytes2[2]
  rom.data[address + 23] = self.xp % 0x100
  rom.data[address + 24] = (self.xp >> 8) % 0x100
  rom.data[address + 25] = self.xp >> 16
  rom.data[address + 26] = self.mystery_bytes3[0]
  rom.data[address + 27] = self.mystery_bytes3[1]
  rom.data[address + 28] = self.mystery_bytes3[2]
  rom.data[address + 29] = self.tnl % 0x100
  rom.data[address + 30] = (self.tnl >> 8) % 0x100
  rom.data[address + 31] = self.tnl >> 16
 
 def read_levelups(self, rom, address):
  pointer = rom.LEVELUP_TABLE_BONUS + (self.level - 1) * 5
  pointer += rom.data[address] + rom.data[address + 1] * 0x100
  self.levelups = []
  for index in range(70):
   levelup = LevelUp()
   self.levelups.append(levelup)
   if index > self.level:
    levelup.read(rom, pointer + (index - self.level) * 5)
  self.after70 = []
  for index in range(8):
   levelup = LevelUp()
   self.after70.append(levelup)
   offset = (70 - self.level) * 5 + index
   levelup.statbonus.read(rom, pointer + offset)
   # Levelups after level 70 don't get their own HP, MP, or TNL.
   # They use the HP, MP, and TNL from the level 69 levelup.
 
 def write_levelups(self, rom, address):
  pointer = rom.LEVELUP_TABLE_BONUS + (self.level - 1) * 5
  pointer += rom.data[address] + rom.data[address + 1] * 0x100
  for index in range(self.level, 70):
   offset = (index - self.level) * 5
   self.levelups[index].write(rom, pointer + offset)
  for index, levelup in enumerate(self.after70):
   offset = (70 - self.level) * 5 + index
   levelup.statbonus.write(rom, pointer + offset)

 def display(self, main):
  result = ""
  result += "Name:  {}\n".format(self.name)
  result += "ID:    {}\n".format(self.id)
  hand = "D-handed"
  if self.left_handed and self.right_handed:
   hand = "Ambidextrous"
  elif self.left_handed:
   hand = "Left-handed"
  elif self.right_handed:
   hand = "Right-handed"
  result += "Hand:  {}\n".format(hand)
  result += "Job:   [{}]\n".format(main.text.hex(self.job))
  result += "Level: {}\n".format(self.level)
  result += "Exp:   {}\n".format(self.xp)
  result += "TNL:   {}\n".format(self.tnl)
  for index, stat in enumerate(self.stats):
   result += "{}:   {}\n".format(main.config.stat_names[index], stat)
  bytestring = ""
  for index, byte in enumerate(self.mystery_bytes):
   bytestring += main.text.hex(byte)
   if index < len(self.mystery_bytes) - 1:
    bytestring += ", "
  result += "Unused:  [{}]\n".format(bytestring)
  bytestring = ""
  for index, byte in enumerate(self.mystery_bytes2):
   bytestring += main.text.hex(byte)
   if index < len(self.mystery_bytes2) - 1:
    bytestring += ", "
  result += "Mystery: [{}]\n".format(bytestring)
  bytestring = ""
  for index, byte in enumerate(self.mystery_bytes3):
   bytestring += main.text.hex(byte)
   if index < len(self.mystery_bytes3) - 1:
    bytestring += ", "
  result += "Unknown: [{}]\n".format(bytestring)
  return result

def read_characters(rom):
 characters = []
 for index in range(rom.TOTAL_CHARACTERS):
  character = Character()
  characters.append(character)
  character.read(rom, rom.CHARACTER_DATA_START + index * 32)
  offset = rom.LEVELUP_POINTERS_START + (character.id - 1) * 2
  character.read_levelups(rom, offset)
 return characters

def write_characters(rom, characters):
 for index, character in enumerate(characters):
  character.write(rom, rom.CHARACTER_DATA_START + index * 32)
  offset = rom.LEVELUP_POINTERS_START + (character.id - 1) * 2
  character.write_levelups(rom, offset)
