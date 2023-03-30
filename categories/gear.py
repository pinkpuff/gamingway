from equiptable import EquipTable
from item import Item
from supply import Supply
from armor import Armor
from weapon import Weapon

# Read all the equip tables from the rom.
def read_equips(rom):
 equips = []
 for index in range(rom.TOTAL_EQUIP_TABLES):
  equip = EquipTable()
  equips.append(equip)
  equip.read(rom, rom.EQUIP_TABLES_START + index * 2)
 return equips

# Write all the equip tables back to the rom.
def write_equips(rom, equips):
 for index, equip in enumerate(equips):
  equip.write(rom, rom.EQUIP_TABLES_START + index * 2)

# Read the entire item list from the rom.
def read_items(rom, text):
 items = []
 
 # Subtypes are determined by item index, so in order to determine which type of
 # object each item needs, we simply look at where it is in the list.
 for index in range(rom.TOTAL_ITEMS):
 
  # Weapons are first in the list.
  if index < rom.TOTAL_WEAPONS:
   item = Weapon()
   item.read(rom, rom.WEAPON_DATA_START + index * 8)
   item.read_visuals(rom, rom.WEAPON_VISUALS_START + index * 4)
  
  # Next are armors.
  elif index < rom.ARMORS_START_INDEX + rom.TOTAL_ARMORS:
   item = Armor()

   # The "subindex" refers to its index relative to other armors. So the first armor
   # would be subindex 0, even though its item index would be higher.
   subindex = index - rom.ARMORS_START_INDEX
   item.read(rom, rom.ARMOR_DATA_START + subindex * 8)
  
  # Supplies are third.
  elif index < rom.SUPPLIES_START_INDEX + rom.TOTAL_SUPPLIES:
   item = Supply()
   
   # As with armors, the subindex indicates the supply's index relative to other
   # supplies.
   subindex = index - rom.SUPPLIES_START_INDEX
   item.read(rom, rom.SUPPLY_DATA_START + subindex * 6)
  
  # And finally tools. Tools don't need their own object class; they just use the
  # generic Item parent object.
  else:
   item = Item()
  
  # Finally, we add it to the list and read its generic item information.
  items.append(item)
  name_offset = index * rom.ITEM_NAME_WIDTH
  name_address = rom.ITEM_NAMES_START + name_offset
  item.read_name(rom, name_address, text)
 
 # And return the fully constructed list.
 return items

# Write the entire item list back to the rom.
def write_items(rom, text, items):
 
 # For now we're assuming the items in the item list are still of the appropriate
 # types based on their index in the list.
 for index, item in enumerate(items):
 
  # Weapons first.
  if index < rom.TOTAL_WEAPONS:
   item.write(rom, rom.WEAPON_DATA_START + index * 8)
   item.write_visuals(rom, rom.WEAPON_VISUALS_START + index * 4)
  
  # Armors second.
  elif index >= rom.ARMORS_START_INDEX:
   if index < rom.ARMORS_START_INDEX + rom.TOTAL_ARMORS:
    subindex = index - rom.ARMORS_START_INDEX
    item.write(rom, rom.ARMOR_DATA_START + subindex * 8)
  
  # Supplies third.
  elif index >= rom.SUPPLIES_START_INDEX:
   if index < rom.SUPPLIES_START_INDEX + rom.TOTAL_SUPPLIES:
    subindex = index - rom.SUPPLIES_START_INDEX
    item.write(rom, rom.SUPPLY_DATA_START + subindex * 6)
  
  # Tools have nothing special to write beyond what gets written for all items, so
  # it doesn't get an else clause of its own. We arrive here regardless of which
  # item subtype it was.
  name_offset = index * rom.ITEM_NAME_WIDTH
  item.write_name(rom, rom.ITEM_NAMES_START + name_offset, text)
