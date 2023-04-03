class Trigger:

 def __init__(self):
  self.x = 0
  self.y = 0
  self.type = ""

 def read(self, rom, address):
  self.x = rom.data[address]
  self.y = rom.data[address + 1]

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

class EventCallTrigger(Trigger):

 def __init__(self):
  super().__init__()
  self.eventcall = 0

 def read(self, rom, address):
  super().read(rom, address)
  self.eventcall = rom.data[address + 3]
