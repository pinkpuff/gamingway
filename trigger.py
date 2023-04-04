# A trigger is something that happens when you interact with certain tiles on a map.
# There are three types of triggers:
#  * Teleport Trigger - Stepping on the tile causes you to teleport somewhere else.
#  * Treasure Trigger - Interacting with the tile causes gives you money or an item.
#  * Launcher Trigger - Stepping on the tile invokes an event launcher. (A Launcher
#                       is something that may cause one of a list of plot events to
#                       be executed depending on the settings of certain flags.)
# The main Trigger object simply holds the (x, y) coordinates of the trigger; the
# other information depends on which type of trigger it is, so those get their own
# child objects.
class Trigger:

 def __init__(self):
  self.x = 0
  self.y = 0
  self.type = ""

 def read(self, rom, address):
  self.x = rom.data[address]
  self.y = rom.data[address + 1]

 def write(self, rom, address):
  rom.data[address] = self.x
  rom.data[address + 1] = self.y

# A TeleportTrigger is something that causes the party to be transported to a new
# location. It will almost certainly be a new map and a new set of coordinates, and
# will place you in the destination facing a certain direction. The door to a shop
# is a good example of a teleport trigger. It places you in the shop map, usually
# facing up. Note that anytime the party teleports like this, their previous
# location is added to the "warp stack", which has a finite size, so if you
# teleport too many times in a row without either warping (which removes the most
# recent location from the stack) or exiting to the overworld (which clears the
# entire stack) can cause the next warp to glitch out the game.
class TeleportTrigger(Trigger):

 def __init__(self):
  super().__init__()
  self.map = 0
  self.new_x = 0
  self.new_y = 0
  self.facing = 0
 
 def read(self, rom, address):
  super().read(rom, address)
  self.map = rom.data[address + 2]
  self.new_x = rom.data[address + 3] % 0x20
  self.facing = rom.data[address + 3] >> 5
  self.new_y = rom.data[address + 4]
 
 def write(self, rom, address):
  super().write(rom, address)
  rom.data[address + 2] = self.map
  rom.data[address + 3] = (self.new_x % 0x20) + (self.facing << 5)
  rom.data[address + 4] = self.new_y

class TreasureTrigger(Trigger):

 def __init__(self):
  super().__init__()
  self.trapped = False
  self.formation = 0
  self.has_money = False
  self.contents = 0

 def read(self, rom, address):
  super().read(rom, address)
  self.formation = rom.data[address + 3] % 0x20
  self.trapped = rom.flag(address + 3, 6)
  self.has_money = not rom.flag(address + 3, 7)
  self.contents = rom.data[address + 4]
 
 def write(self, rom, address):
  super().write(rom, address)
  rom.data[address + 3] = self.formation % 0x20
  rom.setbit(address + 3, 6, self.trapped)
  rom.setbit(address + 3, 7, self.has_money)
  rom.data[address + 4] = self.contents

class LauncherTrigger(Trigger):

 def __init__(self):
  super().__init__()
  self.launcher = 0

 def read(self, rom, address):
  super().read(rom, address)
  self.eventcall = rom.data[address + 3]
 
 def write(self, rom, address):
  super().write(rom, address)
  rom.data[address + 3] = self.launcher
