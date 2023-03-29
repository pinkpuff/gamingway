import rom
import config
import common
import text
import magic
import gear
import party
import combat
import world

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
   self.set_spell_constants()
  if datatype in ["all", "magic", "spellbooks"]:
   self.spellbooks = magic.read_spellbooks(self.rom, self.spells)
   self.set_spellbook_constants()
  if datatype in ["all", "gear", "equips"]:
   self.equips = gear.read_equips(self.rom)
  if datatype in ["all", "gear", "items"]:
   self.items = gear.read_items(self.rom, self.text)
   self.set_item_constants()
  if datatype in ["all", "party", "characters"]:
   self.characters = party.read_characters(self.rom)
   self.set_character_constants()
  if datatype in ["all", "party", "actors"]:
   self.actors = party.read_actors(self.rom)
  if datatype in ["all", "combat", "monsters"]:
   self.monsters = combat.read_monsters(self.rom, self.text)
  if datatype in ["all", "world", "mapnames"]:
   self.map_names = world.read_map_names(self.rom, self.text)
  if datatype in ["all", "world", "maps"]:
   self.maps = world.read_maps(self.rom)
  if datatype in ["all", "world", "tilemaps"]:
   self.tilemaps = world.read_tilemaps(self.rom)
  if datatype in ["all", "world", "overworld"]:
   self.overworld = world.read_overworld(self.rom)
 
 # Writes all the data of the specified type from the abstract game objects and 
 # converts it into the raw bytes. If no type is specified, it defaults to writing 
 # ALL game data. If you wish to write multiple types of data without writing all of
 # them, call this method multiple times with different arguments.
 def write(self, datatype = "all"):

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
   party.write_characters(self.rom, self.characters)
  if datatype in ["all", "combat", "monsters"]:
   # Causes a slight data misalignment, even with no changes.
   combat.write_monsters(self.rom, self.text, self.monsters)
  if datatype in ["all", "world", "mapnames"]:
   world.write_map_names(self.rom, self.text, self.map_names)
  if datatype in ["all", "world", "maps"]:
   world.write_maps(self.rom, self.maps)
  if datatype in ["all", "world", "tilemaps"]:
   world.write_tilemaps(self.rom, self.tilemaps)
  if datatype in ["all", "world", "overworld"]:
   world.write_overworld(self.rom, self.overworld)
 
 def display(self, entity):
  result = ""
  if type(entity) == list:
   for index, entry in enumerate(entity):
    result += "{}: {}\n".format(self.text.hex(index), entry.name)
  else:
   result = entity.display(self)
  return result
 
 # Creates aliases for the player spells.
 def set_spell_constants(self):

  # The names are used from vanilla where possible.
  # Punctuation, spell orbs, and other symbols are omitted.
  # In the case of "dummy" or otherwise unnamed spells, 
  # the Free Enterprise naming convention is used.
  if len(self.spells) > 0:
   self.NO_SPELL = self.spells[0]
  if len(self.spells) > 1:
   self.HOLD_SPELL = self.spells[1]
  if len(self.spells) > 2:
   self.MUTE_SPELL = self.spells[2]
  if len(self.spells) > 3:
   self.CHARM_SPELL = self.spells[3]
  if len(self.spells) > 4:
   self.BLINK_SPELL = self.spells[4]
  if len(self.spells) > 5:
   self.ARMOR_SPELL = self.spells[5]
  if len(self.spells) > 6:
   self.SHELL_SPELL = self.spells[6]
  if len(self.spells) > 7:
   self.SLOW_SPELL = self.spells[7]
  if len(self.spells) > 8:
   self.FAST_SPELL = self.spells[8]
  if len(self.spells) > 9:
   self.BERSK_SPELL = self.spells[9]
  if len(self.spells) > 10:
   self.WALL_SPELL = self.spells[10]
  if len(self.spells) > 11:
   self.WHITE_SPELL = self.spells[11]
  if len(self.spells) > 12:
   self.DISPL_SPELL = self.spells[12]
  if len(self.spells) > 13:
   self.PEEP_SPELL = self.spells[13]
  if len(self.spells) > 14:
   self.CURE1_SPELL = self.spells[14]
  if len(self.spells) > 15:
   self.CURE2_SPELL = self.spells[15]
  if len(self.spells) > 16:
   self.CURE3_SPELL = self.spells[16]
  if len(self.spells) > 17:
   self.CURE4_SPELL = self.spells[17]
  if len(self.spells) > 18:
   self.HEAL_SPELL = self.spells[18]
  if len(self.spells) > 19:
   self.LIFE1_SPELL = self.spells[19]
  if len(self.spells) > 20:
   self.LIFE2_SPELL = self.spells[20]
  if len(self.spells) > 21:
   self.SIZE_SPELL = self.spells[21]
  if len(self.spells) > 22:
   self.EXIT_SPELL = self.spells[22]
  if len(self.spells) > 23:
   self.SIGHT_SPELL = self.spells[23]
  if len(self.spells) > 24:
   self.FLOAT_SPELL = self.spells[24]
  if len(self.spells) > 25:
   self.TOAD_SPELL = self.spells[25]
  if len(self.spells) > 26:
   self.PIGGY_SPELL = self.spells[26]
  if len(self.spells) > 27:
   self.WARP_SPELL = self.spells[27]
  if len(self.spells) > 28:
   self.VENOM_SPELL = self.spells[28]
  if len(self.spells) > 29:
   self.FIRE1_SPELL = self.spells[29]
  if len(self.spells) > 30:
   self.FIRE2_SPELL = self.spells[30]
  if len(self.spells) > 31:
   self.FIRE3_SPELL = self.spells[31]
  if len(self.spells) > 32:
   self.ICE1_SPELL = self.spells[32]
  if len(self.spells) > 33:
   self.ICE2_SPELL = self.spells[33]
  if len(self.spells) > 34:
   self.ICE3_SPELL = self.spells[34]
  if len(self.spells) > 35:
   self.LIT1_SPELL = self.spells[35]
  if len(self.spells) > 36:
   self.LIT2_SPELL = self.spells[36]
  if len(self.spells) > 37:
   self.LIT3_SPELL = self.spells[37]
  if len(self.spells) > 38:
   self.VIRUS_SPELL = self.spells[38]
  if len(self.spells) > 39:
   self.WEAK_SPELL = self.spells[39]
  if len(self.spells) > 40:
   self.QUAKE_SPELL = self.spells[40]
  if len(self.spells) > 41:
   self.SLEEP_SPELL = self.spells[41]
  if len(self.spells) > 42:
   self.STONE_SPELL = self.spells[42]
  if len(self.spells) > 43:
   self.FATAL_SPELL = self.spells[43]
  if len(self.spells) > 44:
   self.STOP_SPELL = self.spells[44]
  if len(self.spells) > 45:
   self.DRAIN_SPELL = self.spells[45]
  if len(self.spells) > 46:
   self.PSYCH_SPELL = self.spells[46]
  if len(self.spells) > 47:
   self.METEO_SPELL = self.spells[47]
  if len(self.spells) > 48:
   self.NUKE_SPELL = self.spells[48]
  if len(self.spells) > 49:
   self.IMP_SPELL = self.spells[49]
  if len(self.spells) > 50:
   self.BOMB_SPELL = self.spells[50]
  if len(self.spells) > 51:
   self.COCKA_SPELL = self.spells[51]
  if len(self.spells) > 52:
   self.MAGE_SPELL = self.spells[52]
  if len(self.spells) > 53:
   self.CHOCB_SPELL = self.spells[53]
  if len(self.spells) > 54:
   self.SHIVA_SPELL = self.spells[54]
  if len(self.spells) > 55:
   self.INDRA_SPELL = self.spells[55]
  if len(self.spells) > 56:
   self.JINN_SPELL = self.spells[56]
  if len(self.spells) > 57:
   self.TITAN_SPELL = self.spells[57]
  if len(self.spells) > 58:
   self.MIST_SPELL = self.spells[58]
  if len(self.spells) > 59:
   self.SYLPH_SPELL = self.spells[59]
  if len(self.spells) > 60:
   self.ODIN_SPELL = self.spells[60]
  if len(self.spells) > 61:
   self.LEVIA_SPELL = self.spells[61]
  if len(self.spells) > 62:
   self.ASURA_SPELL = self.spells[62]
  if len(self.spells) > 63:
   self.BAHAM_SPELL = self.spells[63]
  if len(self.spells) > 64:
   self.COMET_SPELL = self.spells[64]
  if len(self.spells) > 65:
   self.FLARE_SPELL = self.spells[65]
  if len(self.spells) > 66:
   self.FLAME_SPELL = self.spells[66]
  if len(self.spells) > 67:
   self.FLOOD_SPELL = self.spells[67]
  if len(self.spells) > 68:
   self.BLITZ_SPELL = self.spells[68]
  if len(self.spells) > 69:
   self.SMOKE_SPELL = self.spells[69]
  if len(self.spells) > 70:
   self.PIN_SPELL = self.spells[70]
  if len(self.spells) > 71:
   self.IMAGE_SPELL = self.spells[71]

 # Creates aliases for the spellbooks.
 def set_spellbook_constants(self):
  if len(self.spellbooks) > 0:
   self.CECIL_WHITE = self.spellbooks[0]
  if len(self.spellbooks) > 1:
   self.KAIN_MAGIC = self.spellbooks[1]
  if len(self.spellbooks) > 2:
   self.RYDIA_WHITE = self.spellbooks[2]
  if len(self.spellbooks) > 3:
   self.RYDIA_BLACK = self.spellbooks[3]
  if len(self.spellbooks) > 4:
   self.RYDIA_CALL = self.spellbooks[4]
  if len(self.spellbooks) > 5:
   self.TELLAH_WHITE = self.spellbooks[5]
  if len(self.spellbooks) > 6:
   self.TELLAH_BLACK = self.spellbooks[6]
  if len(self.spellbooks) > 7:
   self.ROSA_WHITE = self.spellbooks[7]
  if len(self.spellbooks) > 8:
   self.PALOM_BLACK = self.spellbooks[8]
  if len(self.spellbooks) > 9:
   self.POROM_WHITE = self.spellbooks[9]
  if len(self.spellbooks) > 10:
   self.FUSOYA_WHITE = self.spellbooks[10]
  if len(self.spellbooks) > 11:
   self.FUSOYA_BLACK = self.spellbooks[11]
  if len(self.spellbooks) > 12:
   self.EDGE_NINJA = self.spellbooks[12]

 # Constants referencing particular items.
 def set_item_constants(self):

  # Names go by the FF2US original SNES translation where possible.
  # Punctuation symbols are skipped.
  # Names omit the initial symbol, but usually spell it out at the end, except where 
  # it's clearly unnecessary (e.g. it's not "spear spear" or "excalibur sword")
  # Some have aliases, especially those with shortened names like
  # "Excalbur"/"Excalibur".
  # Dummied consumables use the Free Enterprise naming conventions, with the
  # exception of the summon orbs. 
  if len(self.items) > 0x00:
   self.NOWEAPON = self.items[0x00]
  if len(self.items) > 0x01:
   self.FIRECLAW = self.items[0x01]
  if len(self.items) > 0x02:
   self.ICECLAW = self.items[0x02]
  if len(self.items) > 0x03:
   self.THUNDERCLAW = self.items[0x03]
  if len(self.items) > 0x04:
   self.CHARMCLAW = self.items[0x04]
  if len(self.items) > 0x05:
   self.POISONCLAW = self.items[0x05]
  if len(self.items) > 0x06:
   self.CATCLAW = self.items[0x06]
  if len(self.items) > 0x07:
   self.ROD = self.items[0x07]
  if len(self.items) > 0x08:
   self.ICEROD = self.items[0x08]
  if len(self.items) > 0x09:
   self.FLAMEROD = self.items[0x09]
  if len(self.items) > 0x0A:
   self.THUNDERROD = self.items[0x0A]
  if len(self.items) > 0x0B:
   self.CHANGEROD = self.items[0x0B]
  if len(self.items) > 0x0C: 
   self.CHARMROD = self.items[0x0C]
  if len(self.items) > 0x0D:
   self.STARDUSTROD = self.items[0x0D]
  if len(self.items) > 0x0E:
   self.LILITHROD = self.items[0x0E]
  if len(self.items) > 0x0F:
   self.STAFF = self.items[0x0F]
  if len(self.items) > 0x10:
   self.CURESTAFF = self.items[0x10]
  if len(self.items) > 0x11:
   self.SILVERSTAFF = self.items[0x11]
  if len(self.items) > 0x12:
   self.POWERSTAFF = self.items[0x12]
  if len(self.items) > 0x13:
   self.LUNARSTAFF = self.items[0x13]
  if len(self.items) > 0x14:
   self.LIFESTAFF = self.items[0x14]
  if len(self.items) > 0x15:
   self.SILENCESTAFF = self.items[0x15]
  if len(self.items) > 0x16:
   self.SHADOWSWORD = self.items[0x16]
  if len(self.items) > 0x17:
   self.DARKNESSSWORD = self.items[0x17]
  if len(self.items) > 0x18:
   self.BLACKSWORD = self.items[0x18]
  if len(self.items) > 0x19:
   self.LEGENDSWORD = self.items[0x19]
  if len(self.items) > 0x1A:
   self.LIGHTSWORD = self.items[0x1A]
  if len(self.items) > 0x1B:
   self.EXCALBUR, self.EXCALIBUR = self.items[0x1B], self.items[0x1B]
  if len(self.items) > 0x1C:
   self.FIRESWORD = self.items[0x1C]
  if len(self.items) > 0x1D:
   self.ICEBRAND = self.items[0x1D]
  if len(self.items) > 0x1E:
   self.DEFENSE = self.items[0x1E]
  if len(self.items) > 0x1F:
   self.DRAINSWORD = self.items[0x1F]
  if len(self.items) > 0x20:
   self.ANCIENTSWORD = self.items[0x20]
  if len(self.items) > 0x21:
   self.SLUMBERSWORD = self.items[0x21]
  if len(self.items) > 0x22:
   self.MEDUSASWORD = self.items[0x22]
  if len(self.items) > 0x23:
   self.SPEAR = self.items[0x23]
  if len(self.items) > 0x24:
   self.WINDSPEAR = self.items[0x24]
  if len(self.items) > 0x25:
   self.FLAMESPEAR = self.items[0x25]
  if len(self.items) > 0x26:
   self.BLIZZARDSPEAR = self.items[0x26]
  if len(self.items) > 0x27:
   self.DRAGOONSPEAR = self.items[0x27]
  if len(self.items) > 0x28:
   self.WHITESPEAR = self.items[0x28]
  if len(self.items) > 0x29:
   self.DRAINSPEAR = self.items[0x29]
  if len(self.items) > 0x2A:
   self.GUNGNIR = self.items[0x2A]
  if len(self.items) > 0x2B:
   self.SHORTBLADE = self.items[0x2B]
  if len(self.items) > 0x2C:
   self.MIDDLEBLADE = self.items[0x2C]
  if len(self.items) > 0x2D:
   self.LONGBLADE = self.items[0x2D]
  if len(self.items) > 0x2E:
   self.NINJABLADE = self.items[0x2E]
  if len(self.items) > 0x2F:
   self.MURASAME = self.items[0x2F]
  if len(self.items) > 0x30:
   self.MASAMUNE = self.items[0x30]
  if len(self.items) > 0x31:
   self.ASSASSIN = self.items[0x31]
  if len(self.items) > 0x32:
   self.MUTEDAGGER, self.MUTEKNIFE = self.items[0x32], self.items[0x32]
  if len(self.items) > 0x33:
   self.WHIP = self.items[0x33]
  if len(self.items) > 0x34:
   self.CHAINWHIP = self.items[0x34]
  if len(self.items) > 0x35:
   self.BLITZWHIP = self.items[0x35]
  if len(self.items) > 0x36:
   self.FLAMEWHIP = self.items[0x36]
  if len(self.items) > 0x37:
   self.DRAGONWHIP = self.items[0x37]
  if len(self.items) > 0x38:
   self.HANDAXE = self.items[0x38]
  if len(self.items) > 0x39:
   self.DWARFAXE = self.items[0x39]
  if len(self.items) > 0x3A:
   self.OGREAXE = self.items[0x3A]
  if len(self.items) > 0x3B:
   self.SILVERDAGGER, self.SILVERKNIFE = self.items[0x3B], self.items[0x3B]
  if len(self.items) > 0x3C:
   self.DANCINGDAGGER, self.DANCINGKNIFE = self.items[0x3C], self.items[0x3C]
  if len(self.items) > 0x3D:
   self.SILVERSWORD = self.items[0x3D]
  if len(self.items) > 0x3E:
   self.SPOON = self.items[0x3E]
  if len(self.items) > 0x3F:
   self.CRYSTALSWORD = self.items[0x3F]
  if len(self.items) > 0x40:
   self.SHURIKEN = self.items[0x40]
  if len(self.items) > 0x41:
   self.NINJASTAR = self.items[0x41]
  if len(self.items) > 0x42:
   self.BOOMRANG, self.BOOMERANG = self.items[0x42], self.items[0x42]
  if len(self.items) > 0x43:
   self.FULLMOON = self.items[0x43]
  if len(self.items) > 0x44:
   self.DREAMER = self.items[0x44]
  if len(self.items) > 0x45:
   self.CHARMHARP = self.items[0x45]
  if len(self.items) > 0x46:
   self.DUMMYSWORD = self.items[0x46]
  if len(self.items) > 0x47:
   self.POISONAXE = self.items[0x47]
  if len(self.items) > 0x48:
   self.RUNEAXE = self.items[0x48]
  if len(self.items) > 0x49:
   self.SILVERHAMMER = self.items[0x49]
  if len(self.items) > 0x4A:
   self.EARTHHAMMER = self.items[0x4A]
  if len(self.items) > 0x4B:
   self.WOODENHAMMER = self.items[0x4B]
  if len(self.items) > 0x4C:
   self.AVENGER = self.items[0x4C]
  if len(self.items) > 0x4D:
   self.SHORTBOW = self.items[0x4D]
  if len(self.items) > 0x4E:
   self.CROSSBOW = self.items[0x4E]
  if len(self.items) > 0x4F:
   self.GREATBOW = self.items[0x4F]
  if len(self.items) > 0x50:
   self.ARCHER, self.ARCHERBOW = self.items[0x50], self.items[0x50]
  if len(self.items) > 0x51:
   self.ELVENBOW = self.items[0x51]
  if len(self.items) > 0x52:
   self.SAMURAIBOW = self.items[0x52]
  if len(self.items) > 0x53:
   self.ARTEMISBOW = self.items[0x53]
  if len(self.items) > 0x54:
   self.IRONARROW = self.items[0x54]
  if len(self.items) > 0x55:
   self.WHITEARROW = self.items[0x55]
  if len(self.items) > 0x56:
   self.FIREARROW = self.items[0x56]
  if len(self.items) > 0x57:
   self.ICEARROW = self.items[0x57]
  if len(self.items) > 0x58:
   self.LITARROW = self.items[0x58]
  if len(self.items) > 0x59:
   self.DARKNESSARROW = self.items[0x59]
  if len(self.items) > 0x5A:
   self.POISONARROW = self.items[0x5A]
  if len(self.items) > 0x5B:
   self.MUTEARROW = self.items[0x5B]
  if len(self.items) > 0x5C:
   self.CHARMARROW = self.items[0x5C]
  if len(self.items) > 0x5D:
   self.SAMURAIARROW = self.items[0x5D]
  if len(self.items) > 0x5E:
   self.MEDUSAARROW = self.items[0x5E]
  if len(self.items) > 0x5F:
   self.ARTEMISARROW = self.items[0x5F]
  if len(self.items) > 0x60:
   self.NOARMOR = self.items[0x60]
  if len(self.items) > 0x61:
   self.IRONSHIELD = self.items[0x61]
  if len(self.items) > 0x62:
   self.SHADOWSHIELD = self.items[0x62]
  if len(self.items) > 0x63:
   self.BLACKSHIELD = self.items[0x63]
  if len(self.items) > 0x64:
   self.PALADINSHIELD = self.items[0x64]
  if len(self.items) > 0x65:
   self.SILVERSHIELD = self.items[0x65]
  if len(self.items) > 0x66:
   self.FIRESHIELD = self.items[0x66]
  if len(self.items) > 0x67:
   self.ICESHIELD = self.items[0x67]
  if len(self.items) > 0x68:
   self.DIAMONDSHIELD = self.items[0x68]
  if len(self.items) > 0x69:
   self.AEGIS, self.AEGISSHIELD = self.items[0x69], self.items[0x69]
  if len(self.items) > 0x6A:
   self.SAMURAISHIELD = self.items[0x6A]
  if len(self.items) > 0x6B:
   self.DRAGOONSHIELD = self.items[0x6B]
  if len(self.items) > 0x6C:
   self.CRYSTALSHIELD = self.items[0x6C]
  if len(self.items) > 0x6D:
   self.IRONHELM = self.items[0x6D]
  if len(self.items) > 0x6E:
   self.SHADOWHELM = self.items[0x6E]
  if len(self.items) > 0x6F:
   self.DARKNESSHELM = self.items[0x6F]
  if len(self.items) > 0x70:
   self.BLACKHELM = self.items[0x70]
  if len(self.items) > 0x71:
   self.PALADINHELM = self.items[0x71]
  if len(self.items) > 0x72:
   self.SILVERHELM = self.items[0x72]
  if len(self.items) > 0x73:
   self.DIAMONDHELM = self.items[0x73]
  if len(self.items) > 0x74:
   self.SAMURAIHELM = self.items[0x74]
  if len(self.items) > 0x75:
   self.DRAGOONHELM = self.items[0x75]
  if len(self.items) > 0x76:
   self.CRYSTALHELM = self.items[0x76]
  if len(self.items) > 0x77:
   self.CAP = self.items[0x77]
  if len(self.items) > 0x78:
   self.LEATHERHAT = self.items[0x78]
  if len(self.items) > 0x79:
   self.GAEAHAT = self.items[0x79]
  if len(self.items) > 0x7A:
   self.WIZARDHAT = self.items[0x7A]
  if len(self.items) > 0x7B:
   self.TIARA = self.items[0x7B]
  if len(self.items) > 0x7C:
   self.RIBBON = self.items[0x7C]
  if len(self.items) > 0x7D:
   self.HEADBAND = self.items[0x7D]
  if len(self.items) > 0x7E:
   self.BANDANNA = self.items[0x7E]
  if len(self.items) > 0x7F:
   self.NINJAHAT = self.items[0x7F]
  if len(self.items) > 0x80:
   self.GLASS, self.GLASSHELM = self.items[0x80], self.items[0x80]
   self.GLASSHAT, self.GLASSMASK = self.items[0x80], self.items[0x80]
  if len(self.items) > 0x81:
   self.IRONMAIL = self.items[0x81]
  if len(self.items) > 0x82:
   self.SHADOWMAIL = self.items[0x82]
  if len(self.items) > 0x83:
   self.DARKNESSMAIL = self.items[0x83]
  if len(self.items) > 0x84:
   self.BLACKMAIL = self.items[0x84]
  if len(self.items) > 0x85:
   self.PALADINMAIL = self.items[0x85]
  if len(self.items) > 0x86:
   self.SILVERMAIL = self.items[0x86]
  if len(self.items) > 0x87:
   self.FIREMAIL = self.items[0x87]
  if len(self.items) > 0x88:
   self.ICEMAIL = self.items[0x88]
  if len(self.items) > 0x89:
   self.DIAMONDMAIL = self.items[0x89]
  if len(self.items) > 0x8A:
   self.SAMURAIMAIL = self.items[0x8A]
  if len(self.items) > 0x8B:
   self.DRAGOONMAIL = self.items[0x8B]
  if len(self.items) > 0x8C:
   self.CRYSTALMAIL = self.items[0x8C]
  if len(self.items) > 0x8D:
   self.CLOTHROBE = self.items[0x8D]
  if len(self.items) > 0x8E:
   self.LEATHERROBE = self.items[0x8E]
  if len(self.items) > 0x8F:
   self.GAEAROBE = self.items[0x8F]
  if len(self.items) > 0x90:
   self.WIZARDROBE = self.items[0x90]
  if len(self.items) > 0x91:
   self.BLACKROBE = self.items[0x91]
  if len(self.items) > 0x92:
   self.SORCERERROBE = self.items[0x92]
  if len(self.items) > 0x93:
   self.WHITEROBE = self.items[0x93]
  if len(self.items) > 0x94:
   self.POWERROBE = self.items[0x94]
  if len(self.items) > 0x95:
   self.HEROINE, self.HEROINEROBE = self.items[0x95], self.items[0x95]
  if len(self.items) > 0x96:
   self.PRISONER, self.PRISONERROBE = self.items[0x96], self.items[0x96]
  if len(self.items) > 0x97:
   self.BARDROBE = self.items[0x97]
  if len(self.items) > 0x98:
   self.KARATEROBE = self.items[0x98]
  if len(self.items) > 0x99:
   self.BLBELT, self.BLACKBELT = self.items[0x99], self.items[0x99]
  if len(self.items) > 0x9A:
   self.ADAMANTARMOR, self.ADAMANTMAIL = self.items[0x9A], self.items[0x9A]
  if len(self.items) > 0x9B:
   self.NINJAROBE = self.items[0x9B]
  if len(self.items) > 0x9C:
   self.IRONGLOVE = self.items[0x9C]
  if len(self.items) > 0x9D:
   self.SHADOWGLOVE = self.items[0x9D]
  if len(self.items) > 0x9E:
   self.DARKNESSGLOVE = self.items[0x9E]
  if len(self.items) > 0x9F:
   self.BLACKGLOVE = self.items[0x9F]
  if len(self.items) > 0xA0:
   self.PALADINGLOVE = self.items[0xA0]
  if len(self.items) > 0xA1:
   self.SILVERGLOVE = self.items[0xA1]
  if len(self.items) > 0xA2:
   self.DIAMONDGLOVE = self.items[0xA2]
  if len(self.items) > 0xA3:
   self.ZEUSGLOVE = self.items[0xA3]
  if len(self.items) > 0xA4:
   self.SAMURAIGLOVE = self.items[0xA4]
  if len(self.items) > 0xA5:
   self.DRAGOONGLOVE = self.items[0xA5]
  if len(self.items) > 0xA6:
   self.CRYSTALGLOVE = self.items[0xA6]
  if len(self.items) > 0xA7:
   self.IRONRING = self.items[0xA7]
  if len(self.items) > 0xA8:
   self.RUBYRING = self.items[0xA8]
  if len(self.items) > 0xA9:
   self.SILVERRING = self.items[0xA9]
  if len(self.items) > 0xAA:
   self.STRENGTHRING = self.items[0xAA]
  if len(self.items) > 0xAB:
   self.RUNERING = self.items[0xAB]
  if len(self.items) > 0xAC:
   self.CRYSTALRING = self.items[0xAC]
  if len(self.items) > 0xAD:
   self.DIAMONDRING = self.items[0xAD]
  if len(self.items) > 0xAE:
   self.PROTECTRING = self.items[0xAE]
  if len(self.items) > 0xAF:
   self.CURSEDRING = self.items[0xAF]
  if len(self.items) > 0xB0:
   self.BOMB = self.items[0xB0]
  if len(self.items) > 0xB1:
   self.BIGBOMB = self.items[0xB1]
  if len(self.items) > 0xB2:
   self.NOTUS = self.items[0xB2]
  if len(self.items) > 0xB3:
   self.BOREAS = self.items[0xB3]
  if len(self.items) > 0xB4:
   self.THORRAGE = self.items[0xB4]
  if len(self.items) > 0xB5:
   self.ZEUSRAGE = self.items[0xB5]
  if len(self.items) > 0xB6:
   self.STARDUST = self.items[0xB6]
  if len(self.items) > 0xB7:
   self.SUCCUBUS = self.items[0xB7]
  if len(self.items) > 0xB8:
   self.VAMPIRE = self.items[0xB8]
  if len(self.items) > 0xB9:
   self.BACCHUS = self.items[0xB9]
  if len(self.items) > 0xBA:
   self.HERMES = self.items[0xBA]
  if len(self.items) > 0xBB:
   self.HRGLASS1, self.HOURGLASS1 = self.items[0xBB], self.items[0xBB]
  if len(self.items) > 0xBC:
   self.HRGLASS2, self.HOURGLASS2 = self.items[0xBC], self.items[0xBC]
  if len(self.items) > 0xBD:
   self.HRGLASS3, self.HOURGLASS3 = self.items[0xBD], self.items[0xBD]
  if len(self.items) > 0xBE:
   self.SILKWEB = self.items[0xBE]
  if len(self.items) > 0xBF:
   self.ILLUSION = self.items[0xBF]
  if len(self.items) > 0xC0:
   self.FIREBOMB = self.items[0xC0]
  if len(self.items) > 0xC1:
   self.BLIZZARD = self.items[0xC1]
  if len(self.items) > 0xC2:
   self.LITBOLT = self.items[0xC2]
  if len(self.items) > 0xC3:
   self.STARVEIL = self.items[0xC3]
  if len(self.items) > 0xC4:
   self.KAMIKAZE = self.items[0xC4]
  if len(self.items) > 0xC5:
   self.MOONVEIL = self.items[0xC5]
  if len(self.items) > 0xC6:
   self.MUTEBELL = self.items[0xC6]
  if len(self.items) > 0xC7:
   self.GAIADRUM = self.items[0xC7]
  if len(self.items) > 0xC8:
   self.CRYSTAL = self.items[0xC8]
  if len(self.items) > 0xC9:
   self.COFFIN = self.items[0xC9]
  if len(self.items) > 0xCA:
   self.GRIMOIRE = self.items[0xCA]
  if len(self.items) > 0xCB:
   self.BESTIARY = self.items[0xCB]
  if len(self.items) > 0xCC:
   self.ALARM = self.items[0xCC]
  if len(self.items) > 0xCD:
   self.UNIHORN = self.items[0xCD]
  if len(self.items) > 0xCE:
   self.CURE1 = self.items[0xCE]
  if len(self.items) > 0xCF:
   self.CURE2 = self.items[0xCF]
  if len(self.items) > 0xD0:
   self.CURE3 = self.items[0xD0]
  if len(self.items) > 0xD1:
   self.ETHER1 = self.items[0xD1]
  if len(self.items) > 0xD2:
   self.ETHER2 = self.items[0xD2]
  if len(self.items) > 0xD3:
   self.ELIXIR = self.items[0xD3]
  if len(self.items) > 0xD4:
   self.LIFE = self.items[0xD4]
  if len(self.items) > 0xD5:
   self.SOFT = self.items[0xD5]
  if len(self.items) > 0xD6:
   self.MAIDKISS = self.items[0xD6]
  if len(self.items) > 0xD7:
   self.MALLET = self.items[0xD7]
  if len(self.items) > 0xD8:
   self.DIETFOOD = self.items[0xD8]
  if len(self.items) > 0xD9:
   self.ECHONOTE = self.items[0xD9]
  if len(self.items) > 0xDA:
   self.EYEDROPS = self.items[0xDA]
  if len(self.items) > 0xDB:
   self.ANTIDOTE = self.items[0xDB]
  if len(self.items) > 0xDC:
   self.CROSS = self.items[0xDC]
  if len(self.items) > 0xDD:
   self.HEAL = self.items[0xDD]
  if len(self.items) > 0xDE:
   self.SIREN = self.items[0xDE]
  if len(self.items) > 0xDF:
   self.AUAPPLE, self.GOLDAPPLE = self.items[0xDF], self.items[0xDF]
  if len(self.items) > 0xE0:
   self.AGAPPLE, self.SILVERAPPLE = self.items[0xE0], self.items[0xE0]
  if len(self.items) > 0xE1:
   self.SOMADROP = self.items[0xE1]
  if len(self.items) > 0xE2:
   self.TENT = self.items[0xE2]
  if len(self.items) > 0xE3:
   self.CABIN = self.items[0xE3]
  if len(self.items) > 0xE4:
   self.EAGLEEYE = self.items[0xE4]
  if len(self.items) > 0xE5:
   self.EXIT = self.items[0xE5]
  # I'm not sure what item 0xE6 was in the original.
  if len(self.items) > 0xE7:
   self.IMPORB = self.items[0xE7]
  if len(self.items) > 0xE8:
   self.BOMBORB = self.items[0xE8]
  if len(self.items) > 0xE9:
   self.COCKATRICEORB, self.BIRDORB = self.items[0xE9], self.items[0xE9]
  if len(self.items) > 0xEA:
   self.MAGEORB = self.items[0xEA]
  if len(self.items) > 0xEB:
   self.CARROT = self.items[0xEB]
  if len(self.items) > 0xEC:
   self.PASS = self.items[0xEC]
  if len(self.items) > 0xED:
   self.WHISTLE = self.items[0xED]
  if len(self.items) > 0xEE:
   self.PACKAGE = self.items[0xEE]
  if len(self.items) > 0xEF:
   self.BARONKEY = self.items[0xEF]
  if len(self.items) > 0xF0:
   self.SANDRUBY = self.items[0xF0]
  if len(self.items) > 0xF1:
   self.EARTHCRYSTAL = self.items[0xF1]
  if len(self.items) > 0xF2:
   self.MAGMAKEY = self.items[0xF2]
  if len(self.items) > 0xF3:
   self.LUCAKEY = self.items[0xF3]
  if len(self.items) > 0xF4:
   self.TWINHARP = self.items[0xF4]
  if len(self.items) > 0xF5:
   self.DARKNESSCRYSTAL = self.items[0xF5]
  if len(self.items) > 0xF6:
   self.RATTAIL = self.items[0xF6]
  if len(self.items) > 0xF7:
   self.ADAMANT = self.items[0xF7]
  if len(self.items) > 0xF8:
   self.PAN = self.items[0xF8]
  if len(self.items) > 0xF9:
   self.PINKTAIL = self.items[0xF9]
  if len(self.items) > 0xFA:
   self.TOWERKEY = self.items[0xFA]
  if len(self.items) > 0xFB:
   self.DARKMATTER = self.items[0xFB]
  # Items 0xFC and 0xFD went unused in vanilla, so even though they have names and
  # uses in Free Enterprise, they remain unnamed here.
  if len(self.items) > 0xFE:
   self.SORT = self.items[0xFE]
  if len(self.items) > 0xFF:
   self.TRASHCAN = self.items[0xFF]

 # Constants referencing the characters.
 def set_character_constants(self):
  self.DKCECIL = self.characters[0]
  self.KAIN = self.characters[1]
  self.RYDIA = self.characters[2]
  self.TELLAH = self.characters[3]
  self.EDWARD = self.characters[4]
  self.ROSA = self.characters[5]
  self.YANG = self.characters[6]
  self.PALOM = self.characters[7]
  self.POROM = self.characters[8]
  self.PALADINCECIL = self.characters[9]
  self.CID = self.characters[10]
  self.EDGE = self.characters[11]
  self.FUSOYA = self.characters[12]
 
 # Constants referencing the maps.
 def set_map_constants(self):
  self.BARON_TOWN = self.maps[0]
  self.MIST_TOWN = self.maps[1]
  self.KAIPO_TOWN = self.maps[2]
  self.MYSIDIA_TOWN = self.maps[3]
  self.MYTHRIL_TOWN = self.maps[4]
  self.TOROIA_TOWN = self.maps[5]
  self.AGART_TOWN = self.maps[6]
  self.TOROIA_INN = self.maps[7]
  self.TOROIA_WEAPON_SHOP = self.maps[8]
  self.TOROIA_ARMOR_SHOP = self.maps[9]
  self.TOROIA_ITEM_SHOP = self.maps[10]
  self.BARON_INN = self.maps[11]
  self.BARON_EQUIPMENT_SHOP = self.maps[12]
  self.CIDS_HOUSE = self.maps[13]
  self.ROSAS_HOUSE = self.maps[14]
  self.RYDIAS_HOUSE = self.maps[15]
  self.KAIPO_INN = self.maps[16]
  self.KAIPO_CAFE = self.maps[17]
  self.KAIPO_HOSPITAL = self.maps[18]
  self.MYSIDIA_CAFE = self.maps[19]
  self.MYSIDIA_INN = self.maps[20]
  self.ORDEALS_MIRROR_ROOM = self.maps[21]
  self.HOUSE_OF_WISHES = self.maps[22]
  self.ROOM_OF_WISHES = self.maps[23]
  self.TOROIA_CAFE = self.maps[24]
  self.TOROIA_LOUNGE = self.maps[25]
  self.TOROIA_STAGE, self.SALOON_KING = self.maps[26], self.maps[26]
  # Map 27 is a glitch world
  self.TOROIA_STABLE_PORCH = self.maps[28]
  self.TOROIA_STABLE = self.maps[29]
  self.ASTRO_TOWER = self.maps[30]
  self.OBSERVATORY = self.maps[31]
  self.AGART_INN = self.maps[32]
  self.TOROIA_CHOCOBO_FOREST = self.maps[33]
  self.TOWN_WATER = self.maps[34]
  self.CASTLE_FLOOR = self.maps[35]
  self.BARON_CASTLE = self.maps[36]
  self.DAMCYAN_CASTLE = self.maps[37]
  self.FABUL_CASTLE = self.maps[38]
  self.TOROIA_CASTLE = self.maps[39]
  self.EBLAN_CASTLE = self.maps[40]
  self.DESERT_SAND = self.maps[41]
  self.BARON_LOBBY = self.maps[42]
  self.BARON_COURT = self.maps[43]
  self.BARON_THRONE_ROOM = self.maps[44]
  self.BARON_WEST_HALL = self.maps[45]
  self.BARON_EAST_HALL = self.maps[46]
  self.BARON_PRISON_HALL = self.maps[47]
  self.BARON_PRISON = self.maps[48]
  self.BARON_DORM = self.maps[49]
  self.BARON_WEST_TOWER_1F = self.maps[50]
  self.BARON_WEST_TOWER_2F = self.maps[51]
  self.BARON_WEST_TOWER_3F, self.CECILS_ROOM = self.maps[52], self.maps[52]
  self.BARON_EAST_TOWER_1F = self.maps[53]
  self.BARON_EAST_TOWER_2F = self.maps[54]
  self.BARON_EAST_TOWER_3F = self.maps[55]
  self.BARON_BASEMENT = self.maps[56]
  self.BARON_LOWER_THRONE, self.ODINS_ROOM = self.maps[57], self.maps[57]
  self.BARON_SEWER_ENTRANCE = self.maps[58]
  self.BARON_SEWER_B3 = self.maps[59]
  self.BARON_SEWER_B1 = self.maps[60]
  self.BARON_SEWER_CAMP = self.maps[61]
  self.BARON_SEWER_B2 = self.maps[62]
  self.DAMCYAN_1F = self.maps[63]
  self.DAMCYAN_2F = self.maps[64]
  self.DAMCYAN_3F, self.DAMCYAN_MAIN_HALL = self.maps[65], self.maps[65]
  self.DAMCYAN_PRISON = self.maps[66]
  self.DAMCYAN_TREASURY = self.maps[67]
  self.BARON_SEWER_PORCH = self.maps[68]
  self.AGART_WEAPON_SHOP = self.maps[69]
  self.AGART_ARMOR_SHOP = self.maps[70]
  self.FABUL_LOBBY = self.maps[71]
  self.FABUL_INTERSECTION = self.maps[72]
  self.FABUL_THRONE_ROOM = self.maps[73]
  self.FABUL_CRYSTAL_ROOM = self.maps[74]
  self.FABUL_EQUIPMENT_SHOP = self.maps[75]
  self.FABUL_INN = self.maps[76]
  self.FABUL_EAST_TOWER_1F, self.FABUL_DORM = self.maps[77], self.maps[77]
  self.FABUL_EAST_TOWER_2F, self.FABUL_CAFE = self.maps[78], self.maps[78]
  self.FABUL_EAST_TOWER_3F, self.FABUL_KINGS_ROOM = self.maps[79], self.maps[79]
  self.FABUL_WEST_TOWER_1F, self.FABUL_POTS_ROOM = self.maps[80], self.maps[80]
  self.FABUL_WEST_TOWER_2F, self.FABUL_HOSPITAL = self.maps[81], self.maps[81]
  self.FABUL_WEST_TOWER_3F, self.YANGS_ROOM = self.maps[82], self.maps[82]
  self.MIST_FOREST = self.maps[83]
  self.WATERY_PASS_CAMP = self.maps[84]
  self.TOROIA_LOBBY = self.maps[85]
  self.TOROIA_CLERICS_ROOM = self.maps[86]
  self.TOROIA_CRYSTAL_ROOM = self.maps[87]
  self.TOROIA_HOSPITAL = self.maps[88]
  self.TOROIA_INTERSECTION = self.maps[89]
  self.TOROIA_PRISON = self.maps[90]
  self.TOROIA_STORAGE_ROOM = self.maps[91]
  self.TOROIA_PUBLIC_TREASURY = self.maps[92]
  self.TOROIA_TREASURY = self.maps[93]
  self.EBLAN_MIDDLE_1F, self.EBLAN_LOBBY = self.maps[94], self.maps[94]
  self.EBLAN_MIDDLE_2F, self.EBLAN_COURT = self.maps[95], self.maps[95]
  self.EBLAN_THRONE_ROOM = self.maps[96]
  self.EBLAN_WEST_TOWER_1F = self.maps[97]
  self.EBLAN_WEST_TOWER_2F = self.maps[98]
  self.EBLAN_EAST_TOWER_1F = self.maps[99]
  self.EBLAN_EAST_TOWER_2F = self.maps[100]
  self.EBLAN_BASEMENT = self.maps[101]
  self.BARON_BLACK_SCHOOL = self.maps[102]
  self.BARON_WHITE_SCHOOL = self.maps[103]
  self.DESERT_BACKGROUND = self.maps[104]
  self.TRAINING_ROOM = self.maps[105]
  self.WATERFALL_BACKGROUND = self.maps[106]
  self.CASTLE_WATER = self.maps[107]
  self.MISTY_CAVE = self.maps[108]
  self.MIRROR_ROOM_BACKGROUND = self.maps[109]
  self.WATERY_PASS_BACKGROUND = self.maps[110]
  self.WATERY_PASS_1F = self.maps[111]
  self.WATERY_PASS_2F = self.maps[112]
  self.WATERY_PASS_3F = self.maps[113]
  self.WATERY_PASS_4F = self.maps[114]
  self.WATERY_PASS_5F = self.maps[115]
  self.WATERFALL_ENTRANCE = self.maps[116]
  self.WATERFALL_1F = self.maps[117]
  self.WATERFALL_2F = self.maps[118]
  self.ANTLION_CAVE_1F = self.maps[119]
  self.ANTLION_CAVE_2F = self.maps[120]
  self.ANTLION_NEST = self.maps[121]
  self.ANTLION_SAVE_ROOM = self.maps[122]
  self.ANTLION_CAVE_HARP_ROOM = self.maps[123]
  self.BLACK_BACKGROUND = self.maps[124]
  self.MIST_BACKGROUND = self.maps[125]
  self.MOUNT_HOBS_WEST = self.maps[126]
  self.MOUNT_HOBS_SUMMIT = self.maps[127]
  self.MOUNT_HOBS_EAST = self.maps[128]
  self.MOUNT_HOBS_SAVE_ROOM = self.maps[129]
  self.MOUNTAIN_BACKGROUND = self.maps[130]
  self.WATERY_PASS_WATERFALL = self.maps[131]
  self.MOUNT_ORDEALS_1F = self.maps[132]
  self.MOUNT_ORDEALS_2F = self.maps[133]
  self.MOUNT_ORDEALS_3F = self.maps[134]
  self.MOUNT_ORDEALS_SUMMIT = self.maps[135]
  self.MYSIDIA_CRYSTAL_ROOM = self.maps[136]
  self.MYSIDIA_SERPENT_ROAD = self.maps[137]
  self.BARON_CASTLE_COLLAPSING_HALL = self.maps[138]
  self.AGART_WELL = self.maps[139]
  self.CAVE_MAGNES_1F = self.maps[140]
  self.CAVE_MAGNES_2F = self.maps[141]
  self.CAVE_MAGNES_PIT_ROOM = self.maps[142]
  self.CAVE_MAGNES_3F = self.maps[143]
  self.CAVE_MAGNES_TORCH_ROOM = self.maps[144]
  self.CAVE_MAGNES_4F = self.maps[145]
  self.CAVE_MAGNES_SAVE_ROOM = self.maps[146]
  self.CAVE_MAGNES_5F = self.maps[147]
  self.CAVE_MAGNES_CRYSTAL_ROOM = self.maps[148]
  self.CAVE_MAGNES_BACKGROUND = self.maps[149]
  self.WATERY_PASS_CAMPSITE = self.maps[150]
  self.BARON_SERPENT_ROAD = self.maps[151]
  self.ZOT_1F = self.maps[152]
  self.ZOT_2F = self.maps[153]
  self.ZOT_3F = self.maps[154]
  # Map 155 seems to be just an empty black floor
  self.ZOT_4F = self.maps[156]
  self.ZOT_5F = self.maps[157]
  self.ZOT_6F = self.maps[158]
  self.ZOT_ROSA_ROOM = self.maps[159]
  self.ADAMANT_GROTTO = self.maps[160]
  self.CAVE_MAGNES_SAVE_ROOM = self.maps[161]
  self.ZOT_SAVE_ROOM = self.maps[162]
  self.GIANT_SEQUENCE_CIDS_AIRSHIP = self.maps[163]
  self.GIANT_SEQUENCE_TWINS_AIRSHIP = self.maps[164]
  self.GIANT_SEQUENCE_EDWARDS_AIRSHIP = self.maps[165]
  self.BABIL_SAVE_ROOM = self.maps[166]
  self.BABIL_B1 = self.maps[167]
  self.BABIL_B2 = self.maps[168]
  self.BABIL_B3 = self.maps[169]
  self.BABIL_B4 = self.maps[170]
  self.BABIL_CRYSTAL_ROOM = self.maps[171]
  self.BABIL_B5 = self.maps[172]
  self.SCROLLING_MOUNTAINS = self.maps[173]
  self.TUNNEL_BACKGROUND = self.maps[174]
  self.CRYSTAL_ROOM_BACKGROUND = self.maps[175]
  self.ENDING_CECILS_ROOM_A = self.maps[176]
  self.TRAINING_ROOM_1F = self.maps[177]
  self.TRAINING_ROOM_2F = self.maps[178]
  # Map 179 unknown
  # Map 180 unknown
  self.GIANT_MOUTH = self.maps[181]
  self.GIANT_NECK = self.maps[182]
  self.GIANT_CHEST = self.maps[183]
  # Map 184 unknown
  self.GIANT_STOMACH = self.maps[185]
  self.GIANT_PASSAGE = self.maps[186]
  # Map 187 unknown
  self.GIANT_LUNG = self.maps[188]
  self.GIANT_CPU = self.maps[189]
  self.GIANT_BACKGROUND = self.maps[190]
  # Map 191 unknown
  self.OPENING_AIRSHIP = self.maps[192]
  self.FABUL_PORT = self.maps[193]
  self.SAILING_SHIP = self.maps[194]
  self.DOCKED_AIRSHIP = self.maps[195]
  self.JOINED_AIRSHIPS = self.maps[196]
  self.EMPTY_AIRSHIP_A = self.maps[197]
  self.UNDERWORLD_AIRSHIP = self.maps[198]
  self.CAVE_EBLAN_ENTRANCE = self.maps[199]
  self.CAVE_EBLAN_TOWN = self.maps[200]
  self.CAVE_EBLAN_PASS_TO_BABIL = self.maps[201]
  self.CAVE_EBLAN_EXIT = self.maps[202]
  self.CAVE_EBLAN_INN = self.maps[203]
  self.CAVE_EBLAN_ARMORY = self.maps[204]
  self.CAVE_EBLAN_SAVE_ROOM = self.maps[205]
  self.CAVE_EBLAN_HOSPITAL = self.maps[206]
  self.CHOCOBO_FOREST_FABUL = self.maps[207]
  self.EMPTY_AIRSHIP_B = self.maps[208]
  self.CHOCOBO_FOREST_ORDEALS = self.maps[209]
  self.CHOCOBO_FOREST_BARON = self.maps[210]
  self.CHOCOBO_FOREST_TOROIA = self.maps[211]
  self.CHOCOBO_FOREST_ISLAND = self.maps[212]
  self.BARON_EMPTY_THRONE_ROOM = self.maps[213]
  self.EMPTY_AIRSHIP_C = self.maps[214]
  self.EMPTY_AIRSHIP_D = self.maps[215]
  self.EMPTY_AIRSHIP_E = self.maps[216]
  self.EMPTY_AIRSHIP_F = self.maps[217]
  self.TOWER_OF_WISHES_FINAL_BATTLE = self.maps[218]
  self.AIRSHIP_BACKGROUND = self.maps[219]
  self.LARGE_DOCK = self.maps[220]
  # Map 221 unknown
  # Map 222 unknown
  self.SMALL_DOCK = self.maps[223]
  self.MIST_INN = self.maps[224]
  self.MIST_WEAPON_SHOP = self.maps[225]
  self.MIST_ARMOR_SHOP = self.maps[226]
  self.KAIPO_WEAPONS_SHOP = self.maps[227]
  self.KAIPO_ARMOR_SHOP = self.maps[228]
  self.MYSIDIA_WEAPONS_SHOP = self.maps[229]
  self.MYSIDIA_ARMOR_SHOP = self.maps[230]
  self.MYSIDIA_ITEM_SHOP = self.maps[231]
  self.SILVERA_INN = self.maps[232]
  self.SILVERA_WEAPON_SHOP = self.maps[233]
  self.SILVERA_ARMOR_SHOP = self.maps[234]
  self.SILVERA_ITEM_SHOP = self.maps[235]
  self.BARON_ITEM_SHOP = self.maps[236]
  self.ENDING_TOWER_OF_WISHES = self.maps[237]
  self.ENDING_PALOM_FOREST = self.maps[238]
  self.ENDING_EBLAN_THRONE_ROOM = self.maps[239]
  self.ENDING_LAND_OF_SUMMONS = self.maps[240]
  self.ENDING_DAMCYAN = self.maps[241]
  self.ENDING_DWARF_CASTLE = self.maps[242]
  self.ENDING_MOUNT_ORDEALS = self.maps[243]
  self.ENDING_ASTRO_TOWER = self.maps[244]
  self.ENDING_CECILS_ROOM_B = self.maps[245]
  self.ENDING_BARON_THRONE_ROOM = self.maps[246]
  self.ENDING_FABUL_THRONE_ROOM = self.maps[247]
  # Map 248 unknown
  # Map 249 unknown
  # Map 250 unknown
  # Map 251 is the Overworld
  # Map 252 is the Underworld
  # Map 253 is the Moon surface
  # Map 254 is whatever map you're currently on
  # Map 255 is used for some kind of visual effect
