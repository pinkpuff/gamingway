from monster import Monster

# Read the list of monsters from the rom.
def read_monsters(rom, text, config):
 monsters = []
 for index in range(rom.TOTAL_MONSTERS):
  monster = Monster(config)
  monsters.append(monster)
  pointer = rom.MONSTER_POINTERS_START + index * 2
  offset = rom.data[pointer] + rom.data[pointer + 1] * 0x100
  monster.read(rom, rom.MONSTER_DATA_BONUS + offset)
  offset = rom.MONSTER_NAME_WIDTH * index
  monster.read_name(rom, rom.MONSTER_NAMES_START + offset, text)
  monster.read_gp(rom, rom.MONSTER_GP_START + index * 2)
  monster.read_xp(rom, rom.MONSTER_XP_START + index * 2)
 return monsters

# Write the list of monsters back to the rom.
def write_monsters(rom, text, monsters):
 
 # It appears the monster data in the vanilla rom is not "perfectly
 # packed" as it were. The occasional monster pointer starts a byte or
 # two past where it would need to in order for the monster data to be
 # tightly packed together. However, this function DOES pack the data
 # as tightly as possible and therefore using this function can cause
 # differences with the vanilla rom, even if none of the monster data
 # has been changed.
 room_needed = 0
 for monster in monsters:
  room_needed += monster.room_needed()
 if room_needed > rom.MONSTER_DATA_ROOM:
  print("ERROR: Not enough room for monster data.")
 else:
  address = rom.MONSTER_DATA_START
  for index, monster in enumerate(monsters):
   pointer = address - rom.MONSTER_DATA_BONUS
   rom.write_wide(rom.MONSTER_POINTERS_START + index * 2, pointer)
   address += monster.write(rom, address)
  
  