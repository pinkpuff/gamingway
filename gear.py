import common
import magic

# An EquipTable is essentially a list of flags indicating which jobs have permission
# to use a certain piece of equipment. Since many equipments share the same set of
# jobs that can equip them, this saves space relative to giving each equipment its 
# own individual full set of flags.
class EquipTable(common.FlagSet):

 def __init__(self):

  # An EquipTable is essentially a FlagSet with two bytes.
  super().__init__(2)
 
 # Read the flag settings from the rom.
 def read(self, rom, address):

  # We simply defer to the parent function but pass it an array of two bytes.
  super().from_bytes(rom.data[address:address + 2])
 
 # Write the flag settings back to the rom.
 def write(self, rom, address):

  # We use the parent function to encode the flags into a pair of bytes, which we
  # inject directly into the rom at the appropriate place.
  rom.inject(address, super().to_bytes())
 
 # Return a string which shows a list of the jobs whose flags are set, separated by
 # commas.
 def display(self, main):
  result = ""
  for index, flag in enumerate(self.flags):
   if flag:
    if len(result) > 0:
     result += ", "
    result += main.config.job_names[index]
  return result

# An Item is anything that can appear in the player's inventory.
# There are several Item subtypes based on what properties they have in the rom:
#  * Tool      = Something that can't be equipped or used in battle. It has no
#                corresponding class because it doesn't have any information or
#                functionality beyond that of the parent Item class.
#  * Supply    = Something that can't be equipped but can be used in battle.
#  * Equipment = Something that can be equipped onto characters.
# Equipment has two further subtypes:
#     * Weapon = Something that affects your attack damage, hit, and attributes.
#     * Armor  = Something that affects your physical and magical defense and evade
#                as well as your defense attributes (elemental/status resistances)
class Item:

 def __init__(self):

  # The item's name in ASCII. 
  # Special symbols are encoded using a three-letter code enclosed in square 
  # brackets (e.g. [HRP] or [SWD]). For a full list of codes, see config.py.
  self.name = ""

  # The price of the item.
  # Prices in FF4 are encoded in a compressed way that doesn't allow you to simply
  # have any arbitrary number be a price. If the high bit is unset, the remaining
  # bits are multiplied by 10 to arrive at the price; if it is set, the remaining
  # bits are multiplied by 1000. That means you can have a price of 50 but not 55.
  # Likewise, you can have a price of 5000, but not 5123.
  # This variable represents the "decompressed" price, and you can technically
  # change it to any number you like while editing, but be aware that when writing
  # it back to the rom, it will compress the number as outlined above into the
  # nearest price. So for example, if you set the price to 5123, it will end up as
  # a price of 5000.
  self.price = 0

  # This does not encode a description string directly, but rather the index in a
  # table of descriptions. Most items have no description, and the ones that do
  # can often have identical ones, such as "Restores HP" on all the Cure potion
  # variants, so I imagine it's being done this way to conserve space.
  self.description = 0
 
 # Read the item name from the rom. The other information is stored in different
 # places, so there are different functions for reading each of them in order to
 # avoid making a single read function that's cluttered with a bunch of different
 # addresses.
 def read_name(self, rom, address, text):

  # We use the text module's byte conversion function to parse the item name.
  bytelist = rom.data[address:address + rom.ITEM_NAME_WIDTH]

  # The name is cropped on the right to facilitate displaying and renaming but it
  # will be padded back out when we go to write it back to the rom.
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 # Write the name back to the rom.
 def write_name(self, rom, address, text):

  # First we convert it back from ASCII to FF4 text encoding.
  newname = text.ff4text(self.name)

  # Then we make sure it's exactly 9 letters long. If the given name was longer, we
  # crop it off at 9; if it's shorter, we pad it out to 9 with space characters.
  newname = newname.ljust(rom.ITEM_NAME_WIDTH, text.ff4text(" "))

  # And finally we inject the converted name into the appropriate place in the rom.
  rom.inject(address, text.to_bytes(newname))
 
 # Return a string that contains the item's information.
 # For now, it just displays the name, as that's all that's being read currently,
 # but in future it will also display the price and description.
 def display(self, main):
  return "Name: {}".format(self.name)

# This is a consumable item that can be used in battle.
class Supply(Item):

 def __init__(self, attribute_reference = []):
  super().__init__()

  # The "utility" essentially defines what the supply does when used in battle.
  # Since all the information is encoded in exactly the same way and same order as
  # it is in the spells, we simply use the spell object to encode it.
  self.utility = magic.Spell()
  
 # Read the item's utility from the rom.
 def read(self, rom, address):
  self.utility.read(rom, address)

 # Write the item's utility back to the rom. 
 def write(self, rom, address):
  self.utility.write(rom, address)
 
 # Return a string that contains the supply's information.
 def display(self, main):
  self.utility.name = self.name
  return self.utility.display(main)

# This represents an item that can be equipped onto characters. It acts as the
# parent class for both Weapons and Armors, and encodes all the information that is
# common to both.
class Equipment(Item):

 def __init__(self):
  super().__init__()

  # If a character is wearing any equipment at all that has this flag set, and you
  # are on a map that also has its "magnetic" flag set, the character will have the
  # "Magnetized" status in all battles spawned by that map.
  self.magnetic = False

  # Attributes refer to the element and status flags. For weapons, this indicates
  # what properties your physical attacks will have; for armors, it indicates what
  # elements and statuses you resist.
  # Rather than each equipment having its own independent set of flags, it instead
  # has an index into a global list of attribute tables that indicates which of
  # those tables it uses.
  self.attributes = 0

  # For weapons, this indicates the monster races your attacks will deal more damage
  # to. For armors, it indicates the monster races that will deal less damage to you
  # with their physical attacks.
  self.races = common.FlagSet()

  # This indicates what stats the equipment boosts and by how much.
  self.statbuff = common.StatBuff()

  # This indicates which jobs can use the equipment. Note that much like attributes,
  # each equipment does not get its own independent set of flags, but rather
  # references an index into a list of equip tables.
  self.equips = 0

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
  rom.data[address + 6] = (self.slots.index(self.slot) << 6) + self.equips
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

# This represents an item that can be equipped onto a character to boost their
# attack stats. 
class Weapon(Equipment):

 def __init__(self):
  super().__init__()
  self.throwable = False
  self.ranged = False
  self.litarrow = False
  self.unused_property = False
  self.hammer_flag = False
  self.axe_flag = False
  self.nerf_crits = False
  self.attack = 0
  self.hit = 0
  self.mystery_flag = False
  self.casts_spell = 0
  self.mystery_flag2 = False
  self.consumable = False
  self.throwable2 = False
  self.sprite = 0
  self.palette = 0
  self.swing = 0
  self.slash = 0
  self.casts_visual = 0 # Seems like these aren't being read yet?
  self.casts_power = 0  # ^^^

 def read(self, rom, address):
  self.magnetic = rom.flag(address, 7)
  self.throwable = rom.flag(address, 6)
  self.ranged = rom.flag(address, 5)
  self.litarrow = rom.flag(address, 4)
  self.unused_property = rom.flag(address, 3)
  self.hammer_flag = rom.flag(address, 2)
  self.axe_flag = rom.flag(address, 1)
  self.nerf_crits = rom.flag(address, 0)
  self.attack = rom.data[address + 1]
  self.hit = rom.data[address + 2] % 0x80
  self.mystery_flag = rom.flag(address + 2, 7)
  self.casts_spell = rom.data[address + 3]
  self.attributes = rom.data[address + 4]
  self.races.read(rom, address + 5)
  self.equips = rom.data[address + 6] % 0x20
  self.mystery_flag2 = rom.flag(address + 6, 5)
  self.consumable = rom.flag(address + 6, 6)
  self.bow_flag = rom.flag(address + 6, 7)
  self.statbuff.read(rom, address + 7)
 
 def write(self, rom, address):
  rom.data[address] = 0
  rom.setbit(address, 7, self.magnetic)
  rom.setbit(address, 6, self.throwable)
  rom.setbit(address, 5, self.ranged)
  rom.setbit(address, 4, self.litarrow)
  rom.setbit(address, 3, self.unused_property)
  rom.setbit(address, 2, self.hammer_flag)
  rom.setbit(address, 1, self.axe_flag)
  rom.setbit(address, 0, self.nerf_crits)
  rom.data[address + 1] = self.attack
  rom.data[address + 2] = self.hit % 0x80
  rom.setbit(address + 2, 7, self.mystery_flag)
  rom.data[address + 3] = self.casts_spell
  rom.data[address + 4] = self.attributes
  self.races.write(rom, address + 5)
  rom.data[address + 6] = self.equips % 0x20
  rom.setbit(address + 6, 5, self.mystery_flag2)
  rom.setbit(address + 6, 6, self.consumable)
  rom.setbit(address + 6, 7, self.bow_flag)
  self.statbuff.write(rom, address + 7)
 
 def read_visuals(self, rom, address):
  self.palette = rom.data[address]
  self.sprite = rom.data[address + 1]
  self.slash = rom.data[address + 2]
  self.swing = rom.data[address + 3]
  
 def write_visuals(self, rom, address):
  rom.data[address] = self.palette
  rom.data[address + 1] = self.sprite
  rom.data[address + 2] = self.slash
  rom.data[address + 3] = self.swing

 def display(self, main):
  result = ""
  result += "Name: {}\n".format(self.name)
  result += "Attack:     {}\n".format(self.attack)
  result += "Hit:        {}\n".format(self.hit)
  result += "Mystery1:   {}\n".format(self.mystery_flag)
  if len(main.spells) > self.casts_spell:
   casts = main.spells[self.casts_spell].name
  else:
   casts = text.hex(self.casts_spell)
  result += "Casts:      {}\n".format(casts)
  attributes = "[{}] ".format(main.text.hex(self.attributes))
  if len(main.attributes) > 0:
   attributes += main.attributes[self.attributes].display(main)
  result += "Attributes: {}\n".format(attributes)
  result += "Races:      {}\n".format(self.races.display(main))
  equips = "[{}] ".format(main.text.hex(self.equips))
  if len(main.equips) > 0:
   equips += main.equips[self.equips].display(main)
  result += "Equips:     {}\n".format(equips)
  result += "Mystery2:   {}\n".format(self.mystery_flag2)
  result += "Magnetic:   {}\n".format(self.magnetic)
  result += self.statbuff.display(main)
  properties = ""
  if self.throwable:
   properties += "Throwable  "
  if self.ranged:
   properties += "Ranged  "
  if self.litarrow:
   properties += "LitArrow  "
  if self.unused_property:
   properties += "Unknown  "
  if self.hammer_flag:
   properties += "Hammer  "
  if self.axe_flag:
   properties += "Axe  "
  if self.nerf_crits:
   properties += "Uncrit  "
  if self.consumable:
   properties += "Consumable  "
  if self.bow_flag:
   properties += "Bow  "
  if len(properties) > 0:
   result += "\n" + properties
  return result

def read_equips(rom):
 equips = []
 for index in range(rom.TOTAL_EQUIP_TABLES):
  equip = EquipTable()
  equips.append(equip)
  equip.read(rom, rom.EQUIP_TABLES_START + index * 2)
 return equips

def write_equips(rom, equips):
 for index, equip in enumerate(equips):
  equip.write(rom, rom.EQUIP_TABLES_START + index * 2)

def read_items(rom, text):
 items = []
 for index in range(rom.TOTAL_ITEMS):
  if index < rom.TOTAL_WEAPONS:
   item = Weapon()
   item.read(rom, rom.WEAPON_DATA_START + index * 8)
   item.read_visuals(rom, rom.WEAPON_VISUALS_START + index * 4)
  elif index < rom.ARMORS_START_INDEX + rom.TOTAL_ARMORS:
   item = Armor()
   subindex = index - rom.ARMORS_START_INDEX
   item.read(rom, rom.ARMOR_DATA_START + subindex * 8)
  elif index < rom.SUPPLIES_START_INDEX + rom.TOTAL_SUPPLIES:
   item = Supply()
   subindex = index - rom.SUPPLIES_START_INDEX
   item.read(rom, rom.SUPPLY_DATA_START + subindex * 6)
  else:
   item = Item()
  items.append(item)
  name_offset = index * rom.ITEM_NAME_WIDTH
  name_address = rom.ITEM_NAMES_START + name_offset
  item.read_name(rom, name_address, text)
 return items

def write_items(rom, text, items):
 for index, item in enumerate(items):
  if index < rom.TOTAL_WEAPONS:
   item.write(rom, rom.WEAPON_DATA_START + index * 8)
   item.write_visuals(rom, rom.WEAPON_VISUALS_START + index * 4)
  elif index >= rom.ARMORS_START_INDEX:
   if index < rom.ARMORS_START_INDEX + rom.TOTAL_ARMORS:
    subindex = index - rom.ARMORS_START_INDEX
    item.write(rom, rom.ARMOR_DATA_START + subindex * 8)
  elif index >= rom.SUPPLIES_START_INDEX:
   if index < rom.SUPPLIES_START_INDEX + rom.TOTAL_SUPPLIES:
    subindex = index - rom.SUPPLIES_START_INDEX
    item.write(rom, rom.SUPPLY_DATA_START + subindex * 6)
  name_offset = index * rom.ITEM_NAME_WIDTH
  item.write_name(rom, rom.ITEM_NAMES_START + name_offset, text)
