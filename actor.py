class Actor:

 def __init__(self):
  self.name_index = 0
  self.initialize = False
  self.store = False
  self.load_slot = 0
  self.store_slot = 0
  self.level_link = 0
  self.commands = [0, 0, 0, 0, 0]
  self.equipped = [0, 0, 0, 0, 0]
  self.ammo = [0, 0]
  
 def read_name(self, rom, address):
  self.name_index = rom.data[address]
 
 def write_name(self, rom, address):
  rom.data[address] = self.name_index
  
 def read_loading(self, rom, address):
  self.load_slot = rom.data[address] % 0x80
  self.initialize = rom.flag(address, 7)
 
 def write_loading(self, rom, address):
  rom.data[address] = self.load_slot
  rom.setbit(address, 7, self.initialize)
  
 def read_storing(self, rom, address):
  self.store_slot = rom.data[address] % 0x80
  self.store = rom.flag(address, 7)
 
 def write_storing(self, rom, address):
  rom.data[address] = self.store_slot
  rom.setbit(address, 7, self.store)

 def read_commands(self, rom, address):
  for index in range(5):
   self.commands[index] = rom.data[address + index]
 
 def write_commands(self, rom, address):
  for index in range(5):
   rom.data[address + index] = self.commands[index]
 
 def read_equipped(self, rom, address):
  self.equipped[2] = rom.data[address]
  self.equipped[3] = rom.data[address + 1]
  self.equipped[4] = rom.data[address + 2]
  self.equipped[0] = rom.data[address + 3]
  self.ammo[0] = rom.data[address + 4]
  self.equipped[1] = rom.data[address + 5]
  self.ammo[1] = rom.data[address + 6]
 
 def write_equipped(self, rom, address):
  rom.data[address] = self.equipped[2]
  rom.data[address + 1] = self.equipped[3]
  rom.data[address + 2] = self.equipped[4]
  rom.data[address + 3] = self.equipped[0]
  rom.data[address + 4] = self.ammo[0]
  rom.data[address + 5] = self.equipped[1]
  rom.data[address + 6] = self.ammo[1]
 
 def display(self, main):
  result = ""
  for command in self.commands:
   result += "[{}] ".format(main.text.hex(command))
  return result