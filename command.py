from common import FlagSet

class Command:
 
 def __init__(self):
  self.name = ""
  self.mystery_amount = 0
  self.target = 0
  self.mystery_flag = False
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
  self.mystery_amount = rom.data[address] % 0x10
  self.target = (rom.data[address] >> 4) % 8
  self.mystery_flag = rom.flag(rom.data[address], 7)
 
 def write_target(self, rom, address):
  rom.data[address] = self.mystery_amount + (self.target << 4)
  rom.setbit(address, 7, self.mystery_flag)

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
