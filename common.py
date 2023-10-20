# A FlagSet is a generic collection of flag settings. It can be used for a wide
# variety of things, but most commonly would be for things like race flags, equip
# permission flags, elemental or status flags, and the like. A number of objects
# either extend this class or use it as a member.
class FlagSet:
 
 def __init__(self, width = 1):

  
  # The width which is the number of bytes the FlagSet spans; every eight flags is 
  # one byte. So if you need 1-8 flags, that would be a width of 1; 9-16 flags would
  # have a width of 2 and so on.
  self.width = width

  # The flags are just stored as an array of booleans.
  self.flags = [False] * 8 * width
 
 # Read eight flags from the given byte. The offset indicates which chunk of eight
 # flags the byte should be read into. The byte is treated as eight individual bits
 # which each encode a flag setting, with 0 as False and 1 as True.
 def from_byte(self, byte, offset = 0):
  for bit in range(8):
   self.flags[offset * 8 + bit] = True if (byte >> bit) & 1 else False
 
 # This constructs a byte from eight of the flags. The offset indicates which chunk
 # of eight flags to encode.
 def to_byte(self, offset = 0):
  byte = 0
  for bit in range(8):
   byte |= (1 << bit) if self.flags[offset * 8 + bit] else 0
  return byte
 
 # Read a list of bytes and encode them as flags.
 def from_bytes(self, bytes):
  for index, byte in enumerate(bytes):
   self.from_byte(byte, index)

 # Construct a list of bytes from the flags. 
 def to_bytes(self):
  result = []
  for index in range(self.width):
   result.append(self.to_byte(index))
  return result
 
 # Read the flags from the rom at the given address. The width determines how many
 # bytes to read and interpret as flag settings.
 def read(self, rom, address):
  if self.width > 1:
   self.from_bytes(rom.data[address:address + width])
  else:
   self.from_byte(rom.data[address])
 
 # Construct the appropriate number of bytes from the flags and write them to the
 # rom. The width determines the number of bytes needed.
 def write(self, rom, address):
  if self.width > 1:
   rom.inject(address, self.to_bytes())
  else:
   rom.data[address] = self.to_byte()
 
 # Return a string containing the flag information. The flagnames list is assumed to
 # be the same length as the number of flags in the FlagSet.
 def display(self, main, flagnames = []):
  result = ""
  if len(flagnames) > 0:
   for flag, name in zip(self.flags, flagnames):
    if flag:
     if len(result) > 0:
      result += ", "
     result += name
  else:
   for flag in self.flags:
    result += "X" if flag else "-"
  return result

# This represents a set of elemental and status flags. Elements and statuses seem to
# be treated as the same type of thing by the game, at least as far as most of the
# data is concerned; this library refers to them collectively as attributes. Thus it
# is common for things to have an index into a global list of these AttributeTables.
class AttributeTable(FlagSet):

 def __init__(self):
  super().__init__(3)
  
 def read(self, rom, address):
  super().from_bytes(rom.data[address:address + 3])
 
 def write(self, rom, address):
  rom.inject(address, super().to_bytes())
 
 def display(self, main, alt_statuses = False, flags = None):
  if flags == None:
   flags = self.flags
  result = ""
  for index in range(8):
   if flags[index]:
    if len(result) > 0: 
     result += ", "
    result += main.config.element_names[index]
  for index in range(8):
   if flags[index + 8]:
    if len(result) > 0:
     result += ", "
    if alt_statuses:
     result += main.config.hidden_status_names[index]
    else:
     result += main.config.persistent_status_names[index]
  for index in range(8):
   if flags[index + 16]:
    if len(result) > 0:
     result += ", "
    if alt_statuses:
     result += main.config.system_status_names[index]
    else:
     result += main.config.temporary_status_names[index]
  return result
 
 def display_alternate(self, main):
  return self.display(main, True)
 
 def display_inverted(self, main, alt_statuses = False):
  newflags = []
  for index, flag in enumerate(self.flags):
   if index < 8:
    newflags.append(flag)
   else:
    newflags.append(not flag)
  return self.display(alt_statuses, newflags)

class StatBuff:
 
 def __init__(self, levelup = False):
  self.stats = [False] * 5
  self.amount = 0
  if levelup:
   self.bonuses = [0, 1, 2, 3, 4, 5, 6, -1]
   self.penalties = [0] * 8
  else:
   self.bonuses = [3, 5, 10, 15, 5, 10, 15, 5]
   self.penalties = [0, 0, 0, 0, -5, -10, -15, -10]
 
 def read(self, rom, address):
  self.amount = rom.data[address] % 8
  for index in range(5):
   self.stats[index] = rom.flag(address, 7 - index)
 
 def write(self, rom, address):
  rom.data[address] = self.amount
  for index, stat in enumerate(self.stats):
   rom.setbit(address, 7 - index, stat)
 
 def display(self, main):
  result = ""
  for index, stat in enumerate(self.stats):
   statmod = ""
   if len(result) > 0:
    statmod = ", "
   statmod += main.config.stat_names[index] + ": "
   if stat:
    statmod += "+{:2}".format(self.bonuses[self.amount])
   else:
    statmod += "-{:2}".format(abs(self.penalties[self.amount]))
   result += statmod
  return result

def read_attributes(rom):
 attribute_tables = []
 for index in range(rom.TOTAL_ATTRIBUTE_TABLES):
  attribute_table = AttributeTable()
  attribute_tables.append(attribute_table)
  address = rom.ATTRIBUTE_TABLES_START + index * 3
  attribute_table.read(rom, address)
 return attribute_tables
