from levelup import LevelUp

# A Character is essentially a set of stats and levelups. The other information that
# one might normally associate with a character in the colloquial sense are tracked
# by different objects such as Jobs and Actors.
class Character:
 
 def __init__(self):
  self.name = ""
  
  # I'm not sure what exactly this does but it is at the very least used in the
  # levelup reading routine.
  self.id = 0
  
  # Left-handed and right-handed are tracked independently. Characers can be one or
  # the other or both, or technically neither ("D-handed"), though I don't think it
  # works the way you might expect. For example, I don't think a D-handed character
  # can equip two shields.
  self.left_handed = False
  self.right_handed = False
  
  # The character's associated Job, referenced by index.
  # For example, when Rydia changes from her young self to her older self, this is
  # what changes. The rest of her stats and levelups remain the same.
  self.job = 0
  
  # The character's starting level.
  self.level = 0
  
  # These bytes appear to always be 0 in vanilla. Wasted space? Maybe, but I
  # figure I should track them anyway in case there are any later revelations or in
  # case someone decides to make use of them somehow in a hack or something.
  self.mystery_bytes = [0, 0, 0, 0]
  
  # The character's starting HP. There is a current and a max that are tracked
  # separately, so if for some reason you want the character to start injured or
  # something, you could do that.
  self.current_hp = 0
  self.max_hp = 0
  
  # Likewise for MP.
  self.current_mp = 0
  self.max_mp = 0
  
  # These are the character's starting base stats (STR, AGI, VIT, WIS, WIL).
  self.stats = [0, 0, 0, 0, 0]

  # These do appear to contain some kind of data in vanilla but I'm not sure what
  # it is or what it means.
  self.mystery_bytes2 = [0, 0, 0]
  
  # Starting Exp.
  self.xp = 0
  
  # In vanilla, these contain the same data for each character, but they aren't
  # all 00s. They all contain the sequence 0x00, 0x10, 0x00. I have no idea what
  # that could signify.
  self.mystery_bytes3 = [0, 0, 0]
  
  # The starting amount of Exp required "To Next Level".
  self.tnl = 0
  
  # The list of levelups associated with the character. Levelups after level 70 are
  # handled differently from regular levelups, hence why they are tracked
  # separately.
  self.levelups = []
  self.after70 = []

 # Read the character record from the given address.
 def read(self, rom, address):
  self.id = rom.data[address] % 0x40
  self.left_handed = rom.flag(address, 6)
  self.right_handed = rom.flag(address, 7)
  self.job = rom.data[address + 1]
  self.level = rom.data[address + 2]
  for index in range(4):
   self.mystery_bytes[index] = rom.data[address + 3 + index]
  self.current_hp = rom.data[address + 7] + rom.data[address + 8] * 0x100
  self.max_hp = rom.data[address + 9] + rom.data[address + 10] * 0x100
  self.current_mp = rom.data[address + 11] + rom.data[address + 12] * 0x100
  self.max_mp = rom.data[address + 13] + rom.data[address + 14] * 0x100
  for index in range(5):
   self.stats[index] = rom.data[address + 15 + index]
  for index in range(3):
   self.mystery_bytes2[index] = rom.data[address + 20 + index]
  self.xp = rom.data[address + 23] + rom.data[address + 24] * 0x100
  self.xp += rom.data[address + 25] * 0x10000
  for index in range(3):
   self.mystery_bytes3[index] = rom.data[address + 26 + index]
  self.tnl = rom.data[address + 29] + rom.data[address + 30] * 0x100
  self.tnl += rom.data[address + 31] * 0x10000

 # Write the character record back to the rom at the given address.
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
 
 # Read the levelups for this character from the given address.
 def read_levelups(self, rom, address):
  
  # The address given in the parameter is not the actual address to the data itself
  # but rather the address of the pointer. Whatever pointer information is read from
  # that address gets the character's (starting level - 1) x 5 added to it. Thus,
  # changing the character's starting level will change where it starts looking for
  # the levelup data. Basically the pointer should point to the first levelup after
  # the starting level.
  pointer = rom.LEVELUP_TABLE_BONUS + (self.level - 1) * 5
  pointer += rom.data[address] + rom.data[address + 1] * 0x100
  
  # For levelups as far as level 69, we simply create a new LevelUp object and let
  # its "read" function do the heavy lifting.
  self.levelups = []
  for index in range(71):
   levelup = LevelUp()
   self.levelups.append(levelup)
   if index >= self.level:
    levelup.read(rom, pointer + (index - self.level) * 5)

  # Levelups after level 70 don't get their own HP, MP, or TNL; they use the
  # HP, MP, and TNL from the level 69 levelup. Each character has eight "After 70"
  # levelups from which the game will pick a random one each time they gain a level
  # after level 70. Since the HP, MP, and TNL are static, the only variable is the
  # stat bonus, which can be encoded as a single byte, so the entire 70+ levelup
  # chart can be encoded in 8 bytes.
  self.after70 = []
  for index in range(8):
   levelup = LevelUp()
   self.after70.append(levelup)
   offset = (70 - self.level) * 5 + index
   levelup.statbonus.read(rom, pointer + offset)
 
 # Write the character's levelup data back to the rom.
 def write_levelups(self, rom, address, bonus):

  # This tracks whether we've passed the end of the levelup table.
  valid = (bonus < rom.LEVELUP_TABLE_END)
  
  if valid:

   # The parent function tracks where we left off writing the levelup tables
   # in the "bonus" parameter, so this is returned at the end.
   # From this, we compute the pointer to write based on the starting level.
   # But otherwise, the data is just written contiguously.
   pointer = bonus - rom.LEVELUP_TABLE_BONUS - (self.level - 1) * 5
   # print("{:X} = {:X}".format(rom.data[address] + rom.data[address + 1] * 0x100, pointer))
   rom.data[address] = pointer % 0x100
   rom.data[address + 1] = pointer >> 8
      
   # Then we once again defer to the LevelUp object to write itself to the computed
   # address.
   for index in range(self.level, 70):
    if valid:
     if bonus >= rom.LEVELUP_TABLE_END:
      print("Bleed past end of levelup data. Writing halted.")
      vaild = False
     else:
      self.levelups[index].write(rom, bonus)
      bonus += 5
   
   # And likewise for the "after level 70" data.
   for index, levelup in enumerate(self.after70):
    if valid:
     if bonus >= rom.LEVELUP_TABLE_END:
      print("Bleed past end of levelup data. Writing halted.")
      vaild = False
     else:
      levelup.statbonus.write(rom, bonus)
      bonus += 1
   
  return bonus

 # Returns a string containing this character's information.
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

