from trigger import EventCallTrigger
from trigger import TeleportTrigger
from trigger import TreasureTrigger

# This refers to an entire town or dungeon floor, including its associated
# metadata such as whether it's magnetic, whether you can use Warp or Exit,
# what music plays, etc. It does NOT contain the layout of tiles (at least
# not directly; it instead contains an index referencing one of the TileMaps).
class Map:

 def __init__(self):

  # Triggers are essentially tiles which activate some kind of effect when the
  # player steps on them or interacts with them. Treasures, events, and teleports
  # can all be caused by interacting with a trigger tile on a map. Each map has a
  # list of Trigger objects that encode this information.
  self.triggers = []
  
  # Each map also has associated with it a set of messages or dialogues that can be
  # referenced by NPCs or events in that map. The point of doing it this way is so
  # that you can have one NPC event that simply says "Display map message 3" or
  # something similar and then you can reuse that same NPC event in every map while
  # having the actual dialogue spoken be different for different maps.
  self.messages = []
  
  # The backdrop refers to the battle background that will be used for any combat
  # encounters that happen within the map.
  self.backdrop = 0
  
  # These indicate whether the "Warp" spell and "Exit" spell respectively can be
  # used on this map.
  self.warpable = False
  self.exitable = False
  
  # Some maps have an "alternate version" of a battle background, such as the Sylph
  # Cave background being an alternate version of the Cave of Summons background.
  # This flag indicates whether or not to use the alternate version, if it exists.
  self.alternate_backdrop = False
  
  # When this flag is set, it applies the Magnetized status to all allies in
  # battles spawned from this map.
  self.magnetic = False
  
  # The tilemap doesn't represent the actual array of tiles but rather indicates
  # the INDEX of which TileMap to use for this map. This allows multiple maps to use
  # the same layout of tiles, trigger tile locations, etc, but have different NPCs,
  # messages, and different effects for the triggers.
  self.tilemap = 0
  
  # The tileset likewise indicates the index of which set of tiles to use. For
  # example, the castle tileset is different from the town tileset, which is
  # different from the cavern tileset, and so on.
  self.tileset = 0
  
  # A layout is an arrangement of NPCs. It indicates which NPCs are present and at
  # what locations within the map. There is a separate list of these layouts, and
  # this variable indicates which of those NPC layouts is used by this map.
  self.layout = 0
  
  # When displaying the map, sometimes the camera is positioned in such a way that
  # it shows some area outside the defined TileMap. This indicates which tile to
  # fill that area with.
  self.border_tile = 0
  
  # I'm not entirely certain what this means; I just copied it directly from
  # FF4kster. I suspect if this flag is set, the tiles outside the area defined by
  # the TileMap are considered solid, even if the border tile above would normally
  # be non-solid.
  self.solid_border = False
  
  # This indicates which set of colors to use for the tileset.
  self.palette = 0
  
  # This indicates which set of colors to use for this map's NPCs. Even maps with
  # the same NPC layout can have differently colored NPCs. There are two entries in
  # this list; some NPCs use palette 1 and some use palette 2. I think this just
  # depends on which sprite the NPC uses; some sprites are tied to palette 1 while
  # others are tied to palette 2.
  self.npc_palettes = [0, 0]
  
  # The BGM track that normally plays on this map.
  self.music = 0
  
  # Some maps show another map in the background. For exmaple, in the upper levels
  # of the Watery Pass, you can see a small river below the chasm, or in the Town
  # of Summons you can see previous floors through the empty areas of the map. I
  # think it's also used to achieve certain other effects like the Mist Cave's mist.
  # I think this is a tileset index as opposed to a map index but I have yet to
  # verify that.
  self.background = 0
  
  # This indicates that the background map above should be displayed in a semi-
  # transparent way, such as the aforementioned mist effect.
  self.translucent = False
  
  # I think these indicate whether the background map uses the parallax style
  # scrolling in each direction or whether it's simply "glued" to the position of
  # the map's main tileset as it scrolls.
  self.scroll_vertical = False
  self.scroll_horizontal = False
  
  # I haven't investigated yet what this flag represents, if anything.
  self.mystery_bit = False
  
  # Some background maps scroll automatically, even while the main map stays still.
  # Examples include the Mist Cave's mist or the water in the town maps. I'm not yet
  # sure which numbers indicate which direction.
  self.move_direction = 0
  
  # This indicates the speed of the background map's automatic scroll.
  self.move_speed = 0
  
  # This flag seems to be set on maps used in the ending sequence, but beyond that,
  # I'm not really sure what else it does, if anything.
  self.ending = False
  
  # Map names are not stored directly but rather as an index in a list of names. I
  # suspect this is because a lot of maps are simply "B1", "F2", etc, and not many
  # have unique names; indeed, many don't have names at all.
  self.name_index = 0
  
  # This takes a bit of explaining but it's important. This number is tracked by
  # each map to indicate how many treasures exist on this map AND MAPS "BEFORE" IT
  # in the same world (overworld/undermoon). I'm not sure why this is tracked
  # manually and not dynamically computed based on the triggers, but here we are.
  # In any case, if this number does not accurately match the actual treasure count,
  # it can cause glitches like being able to get treasures by talking to doors etc.
  # A function will be provided for gamingway to automatically compute the treasure
  # indexes for all the maps, but as the original game also contains the occasional
  # error in this number, calling that function will cause a data mismatch even if
  # you haven't made any changes to any maps (though it will likely be a change for
  # the better on balance as it will FIX existing glitches as opposed to introducing
  # new ones).
  self.treasure_index = 0
  
  # This indicates how often you fight random battles on this map when stepping on
  # tiles that have random encounters enabled.
  self.encounter_rate = 0
  
  # There is a list of encounter tables somewhere; this indicates which of those
  # tables is used for random encounters generated by this map.
  self.encounter_set = 0

 def read(self, rom, address):
  self.backdrop = rom.data[address] % 0x10
  self.warpable = rom.flag(address, 4)
  self.exitable = rom.flag(address, 5)
  self.alternate_backdrop = rom.flag(address, 6)
  self.magnetic = rom.flag(address, 7)
  self.tilemap = rom.data[address + 1]
  self.tileset = rom.data[address + 2]
  self.layout = rom.data[address + 3]
  self.border_tile = rom.data[address + 4] % 0x80
  self.solid_border = rom.flag(address + 4, 7)
  self.palette = rom.data[address + 5]
  self.npc_palettes[0] = rom.data[address + 6] % 0x10
  self.npc_palettes[1] = rom.data[address + 6] >> 4
  self.music = rom.data[address + 7]
  self.background = rom.data[address + 8]
  self.translucent = rom.flag(address + 9, 0)
  self.scroll_vertical = rom.flag(address + 9, 1)
  self.scroll_horizontal = rom.flag(address + 9, 2)
  self.mystery_bit = rom.flag(address + 9, 3)
  self.move_direction = (rom.data[address + 9] >> 4) % 4
  self.move_speed = (rom.data[address + 9] >> 6)
  self.unknown = rom.data[address + 10] % 0x80
  self.ending = rom.flag(address + 10, 7)
  self.name_index = rom.data[address + 11] 
  self.treasure_index = rom.data[address + 12]
 
 def write(self, rom, address):
  rom.data[address] = self.backdrop % 0x10
  rom.setbit(address, 4, self.warpable)
  rom.setbit(address, 5, self.exitable)
  rom.setbit(address, 6, self.alternate_backdrop)
  rom.setbit(address, 7, self.magnetic)
  rom.data[address + 1] = self.tilemap
  rom.data[address + 2] = self.tileset
  rom.data[address + 3] = self.layout
  rom.data[address + 4] = self.border_tile % 0x80
  rom.setbit(address + 4, 7, self.solid_border)
  rom.data[address + 5] = self.palette
  rom.data[address + 6] = self.npc_palettes[0] + self.npc_palettes[1] * 0x10
  rom.data[address + 7] = self.music
  rom.data[address + 8] = self.background
  rom.data[address + 9] = 0
  rom.setbit(address + 9, 0, self.translucent)
  rom.setbit(address + 9, 1, self.scroll_vertical)
  rom.setbit(address + 9, 2, self.scroll_horizontal)
  rom.setbit(address + 9, 3, self.mystery_bit)
  rom.data[address + 9] += (self.move_direction % 4) << 4
  rom.data[address + 9] += (self.move_speed % 4) << 6
  rom.data[address + 10] = self.unknown % 0x80
  rom.setbit(address + 10, 7, self.ending)
  rom.data[address + 11] = self.name_index 
  rom.data[address + 12] = self.treasure_index
 
 def read_encounter_rate(self, rom, address):
  self.encounter_rate = rom.data[address]
 
 def write_encounter_rate(self, rom, address):
  rom.data[address] = self.encounter_rate

 def read_triggers(self, rom, address):
  start = rom.read_wide(address) + rom.TRIGGER_POINTER_BONUS
  finish = rom.read_wide(address + 2) + rom.TRIGGER_POINTER_BONUS
  self.triggers = []
  while start < finish:
   match rom.data[start + 2]:
    case 0xFF:
     trigger = EventCallTrigger()
     trigger.type = "eventcall"
    case 0xFE:
     trigger = TreasureTrigger()
     trigger.type = "treasure"
    case _:
     trigger = TeleportTrigger()
     trigger.type = "teleport"
   trigger.read(rom, start)
   self.triggers.append(trigger)
   start += 5
 
 # Returns a string representing the map information.
 def display(self, main):
  result = ""
  
  # Produce an error if the name index is out of bounds.
  if self.name_index > len(main.map_names):
   print("ERROR: Name index {} / {}".format(self.name_index, len(main.map_names)))

  # Otherwise, simply return the map name for now.
  # I will likely flesh this out later to show more information, but for now I just
  # need to be able to know which map is which.
  else:
   result = main.map_names[self.name_index]
   
  # And return the resulting string.
  return result

