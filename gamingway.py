import rom
import config
import common
import text
import constants.all as constants
import categories.magic as magic
import categories.gear as gear
import categories.party as party
import categories.combat as combat
import categories.world as world
import categories.story as story

class FF4Rom:

 def __init__(self, filename):
  # A rom file is required in order to have a functioning FF4Rom.
  # The raw bytes are read from the rom into the "romdata" varaible, which is then
  # passed to the "rom" subcomponent. So if you create an FF4Rom called "ff4" you 
  # can access the raw bytes directly via something like "ff4.rom.data[index]".
  # Abstract game objects are not created at this stage.
  # To generate the game objects, call the "read" function.
  # The reason for doing it this way is because modified roms might store certain
  # data in different ways that are incompatible with the assumptions made by this 
  # program. Thus, if we read all the data into abstract objects from the start, it 
  # could crash the program trying to read data that may not even be relevant to the
  # changes the user wishes to make. Therefore the data reading is done only when 
  # explicitly called by the user, and only the type(s) of data requested.

  # Get the raw data from the file.
  with open(filename, "rb") as ff4file:
   romdata = list(ff4file.read())

  # Determine if the rom has a header. We default to it having a header.
  self.headered = True

  # If the first two bytes match what we expect from an unheadered rom, we assume 
  # that's what it is.
  if romdata[0:2] == [0x78, 0x18]:
   self.headered = False

   # Pad the beginning with enough 0s to make the data line up with that of a 
   # headered rom. (This will be removed when saving.)
   romdata = [0] * 0x200 + romdata
  
  # Initialize the subcomponents that handle various aspects of reading or modifying
  # the rom.
  self.rom = rom.RomData(romdata)
  self.text = text.TextInterface()
  self.config = config.Configuration()

  # Initialize the game data objects to be empty. This way you can refer to them and 
  # pass them around without causing errors even if you haven't read that particular 
  # type of data yet.
  self.attributes = []
  self.equips = []
  self.spells = []
  self.spellbooks = []
  self.items = []
  self.characters = []
  self.actors = []
  self.maps = []
  self.launchers = []
  
 # Export the raw bytes to a file.
 # This won't automatically convert the abstract game objects into bytecode; that 
 # has to be done manually using the "write" function first if you want any changes 
 # you made to be committed. So if you find yourself wondering why your rom doesn't
 # seem to have changed despite saving it, make sure you're calling "write" first.
 def save(self, filename):
  
  # The rom data variable is stored as a list, so first we need to convert it into 
  # bytes that can be written to the file.
  output = bytearray(self.rom.data)
  
  # If we had to add a placeholder header, we remove it before saving.
  if not self.headered:
   output = output[0x200:]

  # Finally, save the file.
  with open(filename, "wb") as ff4file:
   ff4file.write(output)

 # Reads all the data of the specified type from the bytes in the rom and converts 
 # it into abstract game objects. If no type is specified, it defaults to reading 
 # ALL game data. If you wish to read multiple types of data without reading all of
 # them, call this method multiple times with different arguments.
 def read(self, datatype = "all"):
  
  # Convert the given datatype to all lowercase for consistency.
  datatype = datatype.lower()
  
  # Then check for each category and subtype.
  # A full breakdown of the data category structure is in the readme.
  if datatype in ["all", "magic", "gear", "spells", "items"]:
   self.attributes = common.read_attributes(self.rom)
  if datatype in ["all", "magic", "spells"]:
   self.spells = magic.read_spells(self.rom, self.text)
   constants.set_spell_constants(self)
  if datatype in ["all", "magic", "spellbooks"]:
   self.spellbooks = magic.read_spellbooks(self.rom, self.spells)
   constants.set_spellbook_constants(self)
  if datatype in ["all", "gear", "equips"]:
   self.equips = gear.read_equips(self.rom)
  if datatype in ["all", "gear", "items"]:
   self.items = gear.read_items(self.rom, self.text)
   constants.set_item_constants(self)
  if datatype in ["all", "party", "jobs"]:
   self.jobs = party.read_jobs(self.rom, self.text)
   constants.set_job_constants(self)
  if datatype in ["all", "party", "characters"]:
   self.characters = party.read_characters(self.rom)
   constants.set_character_constants(self)
  if datatype in ["all", "party", "actors"]:
   self.actors = party.read_actors(self.rom)
   constants.set_actor_constants(self)
  if datatype in ["all", "party", "commands"]:
   self.commands = party.read_commands(self.rom, self.text)
   constants.set_command_constants(self)
  if datatype in ["all", "combat", "monsters"]:
   self.monsters = combat.read_monsters(self.rom, self.text, self.config)
   constants.set_monster_constants(self)
  if datatype in ["all", "world", "mapnames"]:
   self.map_names = world.read_map_names(self.rom, self.text)
  if datatype in ["all", "world", "maps"]:
   self.maps = world.read_maps(self.rom)
   constants.set_map_constants(self)
  if datatype in ["all", "world", "tilemaps"]:
   self.tilemaps = world.read_tilemaps(self.rom)
  if datatype in ["all", "world", "overworld"]:
   self.overworld = world.read_overworld(self.rom)
  if datatype in ["all", "world", "launchers"]:
   self.launchers = world.read_launchers(self.rom)
  if datatype in ["all", "story", "events"]:
   self.events = story.read_events(self.rom, self.config)
 
 # Writes all the data of the specified type from the abstract game objects and 
 # converts it into the raw bytes. If no type is specified, it defaults to writing 
 # ALL game data. If you wish to write multiple types of data without writing all of
 # them, call this method multiple times with different arguments.
 def write(self, datatype = "all", include_triggers = True):

  # Writing certain types of data can cause a slight misalignment in the data, the 
  # pointers, or both, even if you change nothing. I'm not completely sure why this 
  # happens, but as far as I can tell it doesn't affect actual gameplay. In any 
  # case, each type of data known to do this is tagged below with a comment to that 
  # effect.
  
  # Convert the given datatype to all lowercase for consistency.
  datatype = datatype.lower()
  if datatype in ["all", "magic", "spells"]:
   magic.write_spells(self.rom, self.text, self.spells)
  if datatype in ["all", "magic", "spellbooks"]:
   magic.write_spellbooks(self.rom, self.spellbooks)
  if datatype in ["all", "gear", "equips"]:
   gear.write_equips(self.rom, self.equips)
  if datatype in ["all", "gear", "items"]:
   gear.write_items(self.rom, self.text, self.items)
  if datatype in ["all", "party", "characters"]:
   # Something is causing the TNL values to be messed up
   party.write_characters(self.rom, self.characters)
  if datatype in ["all", "party", "actors"]:
   party.write_actors(self.rom, self.actors)
  if datatype in ["all", "party", "commands"]:
   party.write_commands(self.rom, self.text, self.commands)
  if datatype in ["all", "combat", "monsters"]:
   # Causes a slight data misalignment, even with no changes.
   combat.write_monsters(self.rom, self.text, self.monsters)
  if datatype in ["all", "world", "mapnames"]:
   world.write_map_names(self.rom, self.text, self.map_names)
  if datatype in ["all", "world", "maps"]:
   world.write_maps(self.rom, self.maps, include_triggers)
  if datatype in ["all", "world", "tilemaps"]:
   world.write_tilemaps(self.rom, self.tilemaps)
  if datatype in ["all", "world", "overworld"]:
   world.write_overworld(self.rom, self.overworld)
  # if datatype in ["all", "world", "launchers"]:
   # Causes a slight data misalignment, even with no changes.
   # world.write_launchers(self.rom, self.launchers)
 
 def display(self, entity):
  result = ""
  if type(entity) == list:
   for index, entry in enumerate(entity):
    result += "{}: {}\n".format(self.text.hex(index), entry.name)
  else:
   result = entity.display(self)
  return result
 

