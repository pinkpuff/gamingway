from character import Character

# Read all the characters from the rom.
def read_characters(rom):
 characters = []
 for index in range(rom.TOTAL_CHARACTERS):
  character = Character()
  characters.append(character)
  character.read(rom, rom.CHARACTER_DATA_START + index * 32)
  offset = rom.LEVELUP_POINTERS_START + (character.id - 1) * 2
  character.read_levelups(rom, offset)
 return characters

# Write all the characters back to the rom.
def write_characters(rom, characters):
 for index, character in enumerate(characters):
  character.write(rom, rom.CHARACTER_DATA_START + index * 32)
  offset = rom.LEVELUP_POINTERS_START + (character.id - 1) * 2
  character.write_levelups(rom, offset)
