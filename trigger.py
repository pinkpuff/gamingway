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

  # The x coordinate of the tile where this trigger is located.
  self.x = 0

  # The y coordinate of the tile where this trigger is located.
  self.y = 0

  # This is simply a string indicating whether the trigger is a teleport, treasure,
  # or launcher trigger. Technically it's probably redundant, but I find it makes it
  # easier when you need to check the trigger type.
  # This has to be set manually though, so be careful of that. If it starts causing
  # more trouble than it saves, I might cut it entirely, but we'll see what happens.
  self.type = ""

 # Read the coordinates from the rom.
 def read(self, rom, address):
  self.x = rom.data[address]
  self.y = rom.data[address + 1]

 # Write the coordinates back to the rom.
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

  # Inherit the tile coordinates and type string from the parent object.
  super().__init__()

  # This is the index of the map where the teleport will send you.
  self.map = 0

  # This is the x coordinate in the new map where you will be teleported.
  self.new_x = 0
  
  # This is the y coordinate in the new map where you will be teleported.
  self.new_y = 0

  # This is the way you will be facing after teleporting.
  self.facing = 0
 
 # Read the teleport data from the rom.
 def read(self, rom, address):

  # Let the parent object handle the coordinates.
  super().read(rom, address)
  
  # Then parse the data specific to teleport triggers.
  self.map = rom.data[address + 2]
  self.new_x = rom.data[address + 3] % 0x20
  self.facing = rom.data[address + 3] >> 5
  self.new_y = rom.data[address + 4]
 
 # Write the teleport data back to the rom.
 def write(self, rom, address):

  # Let the parent object handle the coordinates.
  super().write(rom, address)

  # Then encode the data specific to the teleport triggers.
  rom.data[address + 2] = self.map
  rom.data[address + 3] = (self.new_x % 0x20) + (self.facing << 5)
  rom.data[address + 4] = self.new_y

# A TreasureTrigger is something that causes the party to receive money or an item
# when examining it by being adjacent to the tile it's on and pressing the A button.
# This only happens once; after that, the tile is simply considered an ordinary
# solid tile (even if the tile it's on is not normally solid, such as the water
# tiles in the town that contain treasures, for example; they're still solid even
# after you picked up the item).
class TreasureTrigger(Trigger):

 def __init__(self):

  # Inherit the tile coordinates and type string from the parent object.
  super().__init__()

  # This flag determines whether there is a battle upon opening the chest.
  self.trapped = False
  
  # This is the index of the formation of the battle you fight upon opening the
  # chest, if any.
  self.formation = 0

  # This flag determines whether the chest has money or an item in it.
  self.has_money = False

  # If the chest has an item, this is the index of the item; otherwise, if it has
  # money, it's the "price code" of the item. FF4 stores GP amounts in a compressed
  # form where, if the high bit is set, the GP amount is the rest of the byte times
  # 10; if it is unset, the GP amount is the rest of the byte times 1000.
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
