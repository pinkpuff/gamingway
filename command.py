from common import FlagSet

class Command:
 
 def __init__(self):
  self.name = ""
  self.target = 0
  self.mystery_amount = 0
  self.delay_index = 0
  self.statuses = FlagSet(2)
  self.charging_stance = 0

 def read_name(self, rom, address, text):
  bytelist = rom.data[address:address + rom.COMMAND_NAME_WIDTH]
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 def write_name(self, rom, address, text):
  newname = text.ff4text(self.name)
  newname = newname.ljust(rom.COMMAND_NAME_WIDTH, text.ff4text(" "))
  rom.inject(address, text.to_bytes(newname))
 
 def read_target(self, rom, address):
  target = rom.data[address] % 8
  mystery_amount = rom.data[address] >> 3
 
 def write_target(self, rom, address):
  rom.data[address] = self.target % 8
  rom.data[address] += self.mystery_amount << 3

 def read_delay(self, rom, address):
  self.delay_index = rom.data[address]
 
 def write_delay(self, rom, address):
  rom.data[address] = self.delay_index
 
 def read_statuses(self, rom, address):
  self.statuses.from_bytes(rom.data[address:address + 2])
 
 def write_statuses(self, rom, address):
  rom.inject(address, self.statuses.to_bytes())
 
 def read_charging(self, rom, address):
  self.charging_stance = rom.data[address]

 def write_charging(self, rom, address):
  rom.data[address] = self.charging_stance