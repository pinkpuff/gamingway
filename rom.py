class RomData:

 def __init__(self, data):
  self.data = data

  # Constants representing locations of various data in the rom.
  # Ordering them by address helps with debugging.
  self.MONSTER_NAMES_START =      0x71A00
  self.MONSTER_GP_START =         0x72200
  self.MONSTER_XP_START =         0x723C0
  self.MONSTER_POINTERS_START =   0x728A0
  self.MONSTER_DATA_START =       0x72A60
  self.MONSTER_DATA_END =         0x738C0
  self.ENCOUNTER_RATES_START =    0x74542
  self.ITEM_NAMES_START =         0x78200
  self.SPELL_NAMES_START =        0x78B00
  self.WEAPON_DATA_START =        0x79300
  self.ARMOR_DATA_START =         0x79600
  self.SUPPLY_DATA_START =        0x79880
  self.SPELL_DATA_START =         0x799A0
  self.WEAPON_VISUALS_START =     0x7A010
  self.SPELL_VISUALS_START =      0x7A24C
  self.SPELL_SOUNDS_START =       0x7A54F
  self.EQUIP_TABLES_START =       0x7A750
  self.ATTRIBUTE_TABLES_START =   0x7A790
  self.CHARACTER_DATA_START =     0x7AB00
  self.LEVELUP_POINTERS_START =   0x7B700
  self.LEVELUP_TABLE_START =      0x7B728
  self.LEVELUP_TABLE_END =        0x7C800
  self.SPELL_PROGRESSIONS_START = 0x7C900
  self.STARTING_SPELLS_START =    0x7CAC0
  self.MONSTER_VISUALS_START =    0x7CC00
  self.MAP_NAMES_START =          0xA9820
  self.MAP_DATA_START =           0xA9E84
  self.OVERWORLD_POINTERS_START = 0xB0200
  self.OVERWORLD_DATA_START =     0xB0680
  self.TILEMAP_POINTERS_START =   0xB8200
  self.TILEMAP_DATA_START =       0xB8500
  

  # Constants representing other values or quantities.
  self.TOTAL_ATTRIBUTE_TABLES = 128
  self.TOTAL_SPELLS = 0x48
  self.TOTAL_SPELLBOOKS = 13
  self.SPELL_NAME_WIDTH = 6
  room = self.STARTING_SPELLS_START - self.SPELL_PROGRESSIONS_START
  self.SPELL_PROGRESSIONS_ROOM = room
  self.TOTAL_EQUIP_TABLES = 32
  self.ITEM_NAME_WIDTH = 9
  self.TOTAL_ITEMS = 0x100
  self.ARMORS_START_INDEX = 0x60
  self.SUPPLIES_START_INDEX = 0xB0
  self.TOOLS_START_INDEX = 0xDE
  self.TOTAL_WEAPONS = 0x60
  self.TOTAL_ARMORS = 0x50
  self.TOTAL_SUPPLIES = 0x2E
  self.TOTAL_TOOLS = 0x22
  self.TOTAL_CHARACTERS = 13
  self.LEVELUP_TABLE_BONUS = 0x70200
  self.MONSTER_NAME_WIDTH = 8
  self.TOTAL_MONSTERS = 224
  self.MONSTER_DATA_BONUS = 0x68200
  room = self.MONSTER_DATA_END - self.MONSTER_DATA_START
  self.MONSTER_DATA_ROOM = room
  self.TOTAL_MAPS = 0x180
  self.TOTAL_MAP_NAMES = 0x79
  self.MAP_NAMES_ROOM = 1242
  self.TOTAL_OVERWORLD_TILEMAPS = 0x100
  self.TILEMAP_OVERWORLD_BONUS = 0xB8200
  self.TILEMAP_UNDERMOON_BONUS = 0xC0200

 def inject(self, address, bytelist):
  # This directly injects a sequence of bytes into the romdata, starting
  # at the given address. No safety checks or any other kind of checks
  # are made; whatever data used to be at that location is blindly
  # clobbered and replaced by the new bytes.
  for index, byte in enumerate(bytelist):
   self.data[address + index] = byte

 def flag(self, address, bit):
  # This returns a boolean value based on whether the given bit of the
  # given byte is set or not.
  return True if (self.data[address] >> bit) & 1 else False

 def setbit(self, address, bit, value = True):
  # This sets the given bit of the byte at the given address.
  # If the "value" parameter is specified, it will instead set or unset
  # the bit based on whether the value is true or false.
  if value:
   self.data[address] = self.data[address] | (1 << bit)
  else:
   self.data[address] = self.data[address] & (0xFF ^ (1 << bit))
 
 def read_wide(self, address, width = 2):
  # This reads a 16-bit (or 24-bit etc) value starting at the given
  # address and returns it as an integer.
  result = 0
  for index in range(width):
   result += self.data[address + index] * (0x100 ** index)
  return result
 
 def write_wide(self, address, number, width = 2):
  # This writes the given value at the given address and the following
  # addresses as needed. It will not exceed the given width in bytes.
  # Whatever data is at those following addresses will be completely
  # overwritten and forgotten.
  for index in range(width):
   self.data[address + index] = (number >> (8 * index)) % 0x100

 def apply_patch(self, filename, headered_rom_expected = True):
  if type(headered_rom_expected) == str:
   if headered_rom_expected in ["headered", "header"]:
    headered_rom_expected = True
   elif headered_rom_expected in ["unheadered", "no header", "headerless"]:
    headered_rom_expected = False
   else:
    print("ERROR: Unrecognized value for 'headered_rom_expected' in 'apply_patch' function.")
  with open(filename, "rb") as patchfile:
   patch = patchfile.read()
  if len(patch) >= 8:
   header = ""
   for index in range(5):
    header += chr(patch[index])
   done = False
   head = 5
   while not done:
    offset = patch[head:head + 3]
    head += 3
    if offset[0] == 0x45 and offset[1] == 0x4F and offset[2] == 0x46:
     done = True
    else:
     address = offset[0] * 0x10000 + offset[1] * 0x100 + offset[2]
     if not headered_rom_expected:
      # In this situation, the patch expects an UNHEADERED rom but the
      # roms in this library are all HEADERED. Even if an unheadered
      # rom was loaded, a blank header is added in order to make sure
      # the addresses line up for other things. So if the patch was
      # made for an unheadered rom, we need to add the size of the
      # header to the address in question in order to line it up with
      # the "headered" rom in memory.
      # There's no real way to determine for an arbitrary IPS patch
      # whether it needs a headered rom or an unheadered one; you would
      # have to just already know, or see if its creator documented
      # that information, or by trial and error.
      address += 0x200
     length = patch[head:head + 2]
     head += 2
     total = length[0] * 0x100 + length[1]
     patchstring = ""
     patchbytes = []
     if total > 0:
      for byte in patch[head:head + total]:
       patchstring += "{:02x}, ".format(byte)
       patchbytes.append(byte)
      head += total
     else:
      runlength = patch[head] * 0x100 + patch[head + 1]
      runbyte = patch[head + 2]
      head += 3
      patchstring = "{:02x}, ".format(runbyte) * runlength
      patchbytes = [runbyte] * runlength
     for index, byte in enumerate(patchbytes):
      self.data[address + index] = byte
  else:
   print("Invalid ips file: {}".format(filename))

