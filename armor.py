from equipment import Equipment

# This represents an item that can be equipped onto a character to boost their
# defensive stats. 
class Armor(Equipment):

 def __init__(self):
  super().__init__()
  
  # The bonus the armor gives to physical defense.
  self.defense = 0
  
  # The bonus the armor gives to physical evade.
  self.evade = 0
  
  # The bonus the armor gives to magic defense.
  self.magic_defense = 0
  
  # The bonus the armor gives to magic evade.
  self.magic_evade = 0
  
  # I have no idea what this flag means, or if it's even used.
  self.mystery_flag = False
  
  # This flag seems to be set on shields; not sure whether it has any actual
  # in-game effect or not.
  self.shield = False
  
  # This matches up with the equip slot the item belongs in, but I seem to recall
  # that the way the game decides which item belongs in which slot is based on its
  # index in the item list and that this value is ignored. Thus, I suspect that
  # simply changing this value will not have the effect you might expect.
  self.slot = 0
 
 # Read the armor data from the rom.
 def read(self, rom, address):
  self.magic_evade = rom.data[address] % 0x80
  self.magnetic = rom.flag(address, 7)
  self.defense = rom.data[address + 1]
  self.evade = rom.data[address + 2]
  self.magic_defense = rom.data[address + 3]
  self.attributes = rom.data[address + 4] % 0x40
  self.mystery_flag = rom.flag(address + 4, 6)
  self.shield = rom.flag(address + 4, 7)
  self.races.read(rom, address + 5)
  self.equips = rom.data[address + 6] % 0x20
  self.slot = rom.data[address + 6] >> 6
  self.statbuff.read(rom, address + 7)
 
 # Write the armor data back to the rom.
 def write(self, rom, address):
  rom.data[address] = self.magic_evade
  rom.setbit(address, 7, self.magnetic)
  rom.data[address + 1] = self.defense
  rom.data[address + 2] = self.evade
  rom.data[address + 3] = self.magic_defense
  rom.data[address + 4] = self.attributes
  rom.setbit(address + 4, 6, self.mystery_flag)
  rom.setbit(address + 4, 7, self.shield)
  self.races.write(rom, address + 5)
  rom.data[address + 6] = (self.slot << 6) + self.equips
  self.statbuff.write(rom, address + 7)
 
 # Return a string containing all the armor's information.
 def display(self, main):
  result = ""
  result += "Name: {}\n".format(self.name)
  result += "Defense:  {}\n".format(self.defense)
  result += "Evade:    {}\n".format(self.evade)
  result += "M.Def:    {}\n".format(self.magic_defense)
  result += "M.Evade:  {}\n".format(self.magic_evade)
  result += "Mystery:  {}\n".format(self.mystery_flag)
  result += "Shield:   {}\n".format(self.shield)
  result += "Slot:     {}\n".format(main.config.equip_slots[self.slot])
  result += "Magnetic: {}\n".format(self.magnetic)
  result += "Resists:  [{}] ".format(main.text.hex(self.attributes))
  if len(main.attributes) > 0:
   result += main.attributes[self.attributes].display(main) + "\n"
  result += "Races: {}\n".format(self.races.display(main, main.config.race_names))
  result += "Stats: {}\n".format(self.statbuff.display(main))
  result += "Equip: [{}] ".format(main.text.hex(self.equips))
  if len(main.equips) > 0:
   result += main.equips[self.equips].display(main)
  return result

