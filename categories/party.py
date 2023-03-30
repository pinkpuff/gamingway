from character import Character
from actor import Actor
from command import Command

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

# Read all the actors from the rom.
def read_actors(rom):
 actors = []
 for index in range(rom.TOTAL_ACTORS):
  actor = Actor()
  actors.append(actor)
  actor.read_name(rom, rom.ACTOR_NAME_INDEXES_START + index)
  actor.read_loading(rom, rom.ACTOR_LOADS_START + index)
  actor.read_storing(rom, rom.ACTOR_STORES_START + index)
  actor.read_commands(rom, rom.ACTOR_COMMANDS_START + index * 5)
  actor.read_equipped(rom, rom.ACTOR_EQUIPPED_START + index * 7)
 return actors

# Write all the actors back to the rom.
def write_actors(rom, actors):
 for index, actor in enumerate(actors):
  actor.write_name(rom, rom.ACTOR_NAME_INDEXES_START + index)
  actor.write_loading(rom, rom.ACTOR_LOADS_START + index)
  actor.write_storing(rom, rom.ACTOR_STORES_START + index)
  actor.write_commands(rom, rom.ACTOR_COMMANDS_START + index * 5)
  actor.write_equipped(rom, rom.ACTOR_EQUIPPED_START + index * 7)

def read_commands(rom, text):
 commands = []
 for index in range(rom.TOTAL_COMMANDS):
  command = Command()
  commands.append(command)
  offset = index * rom.COMMAND_NAME_WIDTH
  command.read_name(rom, rom.COMMAND_NAMES_START + offset, text)
  command.read_target(rom, rom.COMMAND_TARGETS_START + index)
  command.read_statuses(rom, rom.COMMAND_STATUSES_START + index * 2)
  command.read_charging(rom, rom.COMMAND_CHARGINGS_START + index)
 return commands

def write_commands(rom, text, commands):
 for index, command in enumerate(commands):
  offset = index * rom.COMMAND_NAME_WIDTH
  command.write_name(rom, rom.COMMAND_NAMES_START + offset, text)
  command.write_target(rom, rom.COMMAND_TARGETS_START + index)
  command.write_statuses(rom, rom.COMMAND_STATUSES_START + index * 2)
  command.write_charging(rom, rom.COMMAND_CHARGINGS_START + index)