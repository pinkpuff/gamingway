from common import StatBuff

# This represents a single levelup for a single character.
class LevelUp:

 def __init__(self):
 
  # The "StatBuff" is a common object used not only here but in equipment as well.
  # It defines which stats increase and by how much (they all increase by the same
  # amount).
  self.statbonus = StatBuff(True)
  
  # In addition to stat bonuses, a levelup also grants bonuses to HP and MP.
  self.hp = 0
  self.mp = 0
  
  # TNL stands for "To Next Level" and indicates how much more Exp the character
  # will need for their next level.
  self.tnl = 0
 
 # Read the information for this LevelUp from the given address.
 def read(self, rom, address):
  self.statbonus.read(rom, address)
  self.hp = rom.data[address + 1]
  self.mp = rom.data[address + 2] % 0x20
  self.tnl = rom.data[address + 3] + rom.data[address + 4] * 0x100
  self.tnl += (rom.data[address + 2] >> 5) * 0x10000
 
 # Write this LevelUp's information back to the rom at the specified address.
 def write(self, rom, address):
  self.statbonus.write(rom, address)
  rom.data[address + 1] = self.hp
  rom.data[address + 2] = self.mp % 0x20 + ((self.tnl >> 16) << 5)
  rom.data[address + 3] = self.tnl % 0x100
  rom.data[address + 4] = (self.tnl >> 8) % 0x100
 
 # Return a string containing this LevelUp's information.
 def display(self, main):
  result = ""
  result += "{} / ".format(self.statbonus.display(main))
  result += "HP: +{:3} / ".format(self.hp)
  result += "MP: +{:2} / ".format(self.mp)
  result += "TNL: {:6}".format(self.tnl)
  return result

