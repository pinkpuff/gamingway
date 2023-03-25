# This represents the actual grid of tiles that compose a map. The reason this is
# its own separate class and not part of the Map itself is because multiple Maps
# can share the same TileMap, in which case the shared TileMap is only stored once
# and simply pointed to by the various Maps that use it.
class TileMap:

 def __init__(self):

  # The "tiles" variable represents a 2D array of tile indexes.
  self.tiles = []
 
 # This reads the RLE encoded tile data for a single TileMap from the rom, starting
 # at the specified address, and continuing until 0x400 tiles have been read.
 # During the tile reading process, the tiles are read into a 1D array which is
 # then converted to a 32x32 2D array.
 def read(self, rom, address):
  tiles = []
  offset = 0

  # Continue reading tiles until 0x400 of them have been read.
  while len(tiles) < 0x400:

   # There are 0x80 tiles in a tileset; the high bit is used to indicate a run.
   tile = rom.data[address + offset] % 0x80
   runlength = 1

   # If the high bit is set, it means we have a run of several tiles. The following
   # byte indicates how many "extra" tiles beyond the first.
   if rom.flag(address + offset, 7):
    offset += 1

    # For some reason, runlength byte FF seems to represent 0xFF tiles, not 0x100.
    # Thus, a run byte of FF seems to be the same as FE?
    # In any case, without this cap, the data seems to be misread.
    runlength += min(rom.data[address + offset], 0xFE)

   # Regardless of whether or not there was a run, we add the tile(s) to the array.
   tiles += [tile] * runlength 
   offset += 1

  # Finally, once we've read a full map worth of tiles, we convert it to a 2D array.
  self.tiles = [[tiles[y * 32 + x] for x in range(32)] for y in range(32)]

 # This writes the 2D tile array back to the rom as an RLE encoded sequence.
 # Most of the work though is done by the "encode" method.
 def write(self, rom, address):
 
  # The encode method does the heavy lifting.
  encoding = self.encode()
  
  # We simply inject it directly into the appropriate place in the rom.
  rom.inject(address, encoding)
  
  # And return the new address based on how long the encoding was.
  return address + len(encoding)

 # This converts the TileMap object's 2D tiles array into a 1D array of tiles
 # using run-length encoding.
 def encode(self):
  result = []
  tiles = [tile for row in self.tiles for tile in row]

  # Then we iterate through the new 1D array, if there is any data to even look at.
  if len(self.tiles) > 0:
   runlength = 1

   # Examine each tile and either add it as a single tile if it doesn't match the
   # previous tile, or increment the run length if it does.
   for index, tile in enumerate(tiles):

    # If we're at the beginning of the list, we initialize the tile we're tracking
    # to be the current tile, and reset the runlength to 1.
    if index == 0:
     oldtile = tile
     runlength = 1

    # Otherwise, we handle it normally.
    else:
     
     # If the current tile matches the one we're already tracking, simply increase
     # the runlength.
     if tile == oldtile:
      runlength += 1
     
     # Otherwise, we write the tile we were tracking and start tracking the new one.
     else:
      
      # A single run can only be at most 0x100 tiles. If it needs to be longer than
      # that, we need to create multiple runs.
      while runlength >= 0x100:
       result.append(oldtile + 0x80)
       result.append(0xFF)
       runlength -= 0xFF

      # Now that we know the runlength is less than 0x100, we check whether it's a
      # single tile or a run. If it's a run, we need to set the high bit and 
      # include the runlength as the following byte (-1 since the runlength byte
      # only represents the number of "additional" repeats of the tile).
      if runlength > 1:
       result.append(oldtile + 0x80)
       result.append(runlength - 1)

      # Otherwise, it's a single tile. We still need to check whether it's 1 since
      # the above while loop could theoretically have reduced it to 0, in which case
      # we don't need to write anything further.
      # Since it's a single tile, all we need to do is write the tile index and
      # leave the high bit unset.
      elif runlength == 1:
       result.append(oldtile)
      
      # Finally, we reset the runlength to 1 and begin tracking the current tile.
      runlength = 1
      oldtile = tile

   # Once we've exhausted the full array of tiles, we might have a tile or run of
   # tiles left to write. Therefore, we need to process them the same way as above.
   while runlength >= 0x100:
    result.append(oldtile + 0x80)
    result.append(0xFF)
    runlength -= 0xFF
   if runlength > 1:
    result.append(oldtile + 0x80)
    result.append(runlength - 1)
   elif runlength == 1:
    result.append(oldtile)

  # And finally, return the constructed RLE encoded array of bytes.
  return result

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

# Read the list of map names from the rom.
def read_map_names(rom, text):

 # Start with a list of blanks.
 map_names = [""] * rom.TOTAL_MAP_NAMES
 address = rom.MAP_NAMES_START
 
 # Then read through the list of map names.
 # There's no pointer table; the names are just separated by 00 bytes.
 for index in range(rom.TOTAL_MAP_NAMES):
 
  # Start with a blank name, then read bytes one by one, adding the corresponding
  # symbols to the name until we read a 00 byte.
  name = ""
  while rom.data[address] > 0:
   name += chr(rom.data[address])
   address += 1
  
  # Finally, we convert the name to ascii to make it easier to work with.
  address += 1
  map_names[index] = text.asciitext(name)
  
 # And return the completed list.
 return map_names

# Write the map names back to the rom.
def write_map_names(rom, text, map_names):

 # Since this is variable-length data, we need to make sure there is enough room
 # before we write it in order to prevent data bleed.
 room_needed = 0
 for name in map_names:
  converted = text.ff4text(name)
  room_needed += len(converted) + 1
 
 # If there isn't enough room for all the map names, we don't write any of them.
 # We simply spit out an error message and return.
 if room_needed > rom.MAP_NAMES_ROOM:
  print("ERROR: Not enough room for map names.")
 
 # Otherwise, we do write the map names.
 else:
  address = rom.MAP_NAMES_START
  
  # Loop through each map name, converting it back from ASCII to FF4 text
  # encoding, and then injecting it into the rom.
  for name in map_names:
   converted = text.ff4text(name)
   rom.inject(address, text.to_bytes(converted))
   
   # Make sure we update the address as we go.
   address += len(converted)
   
   # The map names are terminated with a 00 byte.
   rom.data[address] = 0
   address += 1

# This reads the Map data from the rom and returns the resulting list.
def read_maps(rom):

 # Start with an empty list.
 maps = []
 
 # We simply loop through the list of Maps in the rom and use the Map object's
 # "read" method to parse the data.
 for index in range(rom.TOTAL_MAPS):
 
  # First, create a new map and add it to the list.
  map = Map()
  maps.append(map)
  
  # Then read the data from the rom.
  # Map data is a fixed length record so there's no pointer table.
  map.read(rom, rom.MAP_DATA_START + index * 13)

  # The encounter rates are stored in a separate area of the rom, but they seem like
  # they should be categorically part of the Map object, so we still include them
  # here but write them separately from the built-in "write" method so that we don't
  # have to pass it several different addresses.
  map.read_encounter_rate(rom, rom.ENCOUNTER_RATES_START + index)
 
 # And finally, return the list.
 return maps

# This writes the Map data back to the rom.
def write_maps(rom, maps):

 # We simply loop through the list of Maps and write each one using the Map object's
 # "write" method.
 for index, map in enumerate(maps):
  map.write(rom, rom.MAP_DATA_START + index * 13)
  
  # The encounter rates are stored in a separate area of the rom, but they seem like
  # they should be categorically part of the Map object, so we still include them
  # here but write them separately from the built-in "write" method so that we don't
  # have to pass it several different addresses.
  map.write_encounter_rate(rom, rom.ENCOUNTER_RATES_START + index)

# This reads the list of TileMaps from the rom.
def read_tilemaps(rom):

 # The "oldaddress" variable is there to track the previous TileMap's pointer
 # because when a TileMap has no data, it seems to use the previous TileMap's
 # pointer, not a pointer to where the previous TileMap's data left off.
 oldaddress = None
 tilemaps = []
 
 # We simply loop through the TileMap pointer table, computing the pointers and
 # adding the TileMaps to the list. The TileMap object's built-in "read" method is
 # used to read the actual TileMap data from the address pointed to by the pointer.
 for index in range(rom.TOTAL_OVERWORLD_TILEMAPS):
 
  # Create a new TileMap and add it to the list.
  tilemap = TileMap()
  tilemaps.append(tilemap)
  
  # Read the next pointer and compute the address from it.
  pointer = rom.TILEMAP_POINTERS_START + index * 2
  address = rom.read_wide(pointer) + rom.TILEMAP_OVERWORLD_BONUS
  
  # When the tilemap has no data it uses the same pointer as the previous tilemap.
  # Therefore, we only read data for the map if its pointer is different from the
  # previous one.
  if address != oldaddress:
   tilemap.read(rom, address)
   oldaddress = address

 # And finally we return the list.
 return tilemaps

# This writes the list of tilemaps back to the rom.
def write_tilemaps(rom, tilemaps):

 # The "oldaddress" variable is there to track the previous TileMap's pointer
 # because when a TileMap has no data, it seems to use the previous TileMap's pointer,
 # even if the previous map had data. Thus we can't simply use the address where we
 # left off writing, as that would be ahead of where it should be.
 address = rom.TILEMAP_DATA_START
 oldaddress = address
 
 # Mostly we just loop through the list and use the TileMap object's "write"
 # method to write it back, but we also need to update the pointer table.
 for index, tilemap in enumerate(tilemaps):
 
  # If the TileMap has no data, we write the PREVIOUS TileMap's pointer (not the
  # pointer to the address where we left off writing TileMap data).
  if len(tilemap.tiles) == 0:
   pointer = oldaddress - rom.TILEMAP_OVERWORLD_BONUS
   
  # If it DOES have data, we write the pointer to where we left off writing TileMap
  # data. We also update the "oldaddress" to be the pointer we just wrote.
  else:
   pointer = address - rom.TILEMAP_OVERWORLD_BONUS
   oldaddress = address
  
  # Now we actually write the pointer we decided on above.
  rom.write_wide(rom.TILEMAP_POINTERS_START + index * 2, pointer)
  
  # And write the actual TileMap data itself, updating the address where we leave
  # off in the process.
  address = tilemap.write(rom, address)

# This reads the RLE-encoded overworld tile data and returns it as an array.
def read_overworld(rom):

 # The array itself is one-dimensional but it represents a 256x256 grid.
 tilemap = TileMap()
 address = rom.OVERWORLD_DATA_START
 tiles = []

 # The overworld is stored as 256 "rows" of 256 tiles, all RLE encoded, with a
 # pointer table indicating where each row starts. Each RLE encoded row is also
 # terminated with an FF byte.
 for row in range(0x100):

  # Create the row in the tilemap.
  tilemap.tiles.append([])

  # Read the current byte.
  tile = rom.data[address]
  address += 1

  # If it's an FF byte, that means the row is done. Otherwise, we process it as a
  # tile.
  while tile < 0xFF:

   # Start with a runlength of 1; we'll increase it later if needed.
   runlength = 1

   # There are several special tiles which represent a sequence of four specific 
   # tiles, so we check for one of those first.
   if tile == 0x00 or tile == 0x10 or tile == 0x20 or tile == 0x30:

    # In each case, the tile sequence is the initial tile followed by a specific
    # sequence of tiles defined by the formula below.
    # For these, we don't care about the runlength; they each represent a run of
    # exactly four specific tiles.
    tilemap.tiles[row].append(tile)
    suffix = (tile >> 4) * 3
    for index in range(3):
     tilemap.tiles[row].append(0x70 + suffix + index)

   # If it wasn't one of the special tiles, we see if it's a single tile or a run.
   else:

    # If the high bit is set, it's a run; the next byte tells us how many "extra"
    # tiles beyond the first. For example, 81 03 would represent a run of four
    # tile 01's.
    if tile >= 0x80:
     runlength += rom.data[address]
     address += 1
     for index in range(runlength):
      tilemap.tiles[row].append(tile % 0x80)
    
    # Otherwise, it's a single tile and we can simply add it to the list directly.
    else:
     tilemap.tiles[row].append(tile)

   # Now we can read the next tile and check if it's FF and so on.
   tile = rom.data[address]
   address += 1
 
 # And finally return the fully parsed tilemap.
 return tilemap
 
# This writes the 2D array of overworld tiles back to the rom data as a list
# of 256-tile-wide RLE-encoded rows, along with the appropriate pointers.
def write_overworld(rom, tilemap):
 address = rom.OVERWORLD_DATA_START
 
 # We go row by row and write each line along with its pointer.
 for row in range(0x100):
  
  # First we compute the pointer.
  # The "address" variable is not reset on each loop so it tracks where we left
  # off writing tiles, which is exactly where the next pointer should point.
  pointer = address - rom.OVERWORLD_DATA_START
  rom.write_wide(rom.OVERWORLD_POINTERS_START + row * 2, pointer)
  
  # When tracking a run of tiles, oldtile is the tile index and runlength is
  # how many we've seen so far. The chunk variable is used for writing the four
  # tile wide "chunks" that are encoded in a single byte in the RLE.
  oldtile = None
  runlength = 1
  chunk = 0
  
  # Now we are ready to RLE-encode the row.
  for tile in tilemap.tiles[row]:
   
   # If we see a copy of the tile we're already tracking a run of, we simply
   # increment the length of the run.
   if tile == oldtile:
    runlength += 1
    
   # Otherwise, we have a few more checks to make.
   else:
   
    # First check if there was an existing run that needs to be written.
    if oldtile != None:
     if runlength > 1:
      rom.data[address] = oldtile + 0x80
      rom.data[address + 1] = runlength - 1
      address += 2
     else:
      rom.data[address] = oldtile
      address += 1
    
    # Then, regardless of whether there was a run or not, we check if the
    # current tile is part of a chunk of four. If we've written such a tile
    # three or fewer tiles ago, we don't process the current tile just yet.
    if chunk > 0:
     chunk -= 1
    
    # If we're not already processing a special tile chunk, we see if the
    # current tile is the start of one. If so, we write the tile but don't
    # start a run. Instead we signal that the next three tiles are to be
    # ignored as part of the chunk.
    elif tile == 0x00 or tile == 0x10 or tile == 0x20 or tile == 0x30:
     oldtile = None
     rom.data[address] = tile
     address += 1
     chunk = 3

    # It's not a special tile or a continuation of a run, so we start a new run.
    else:
     oldtile = tile
     runlength = 1

  # We're done the row so we just make sure we write the existing run, if any.
  if oldtile != None:
   if runlength > 1:
    rom.data[address] = oldtile + 0x80
    rom.data[address + 1] = runlength - 1
    address += 2
   else:
    rom.data[address] = oldtile
    address += 1
    
  # Then terminate the row with an FF byte.
  rom.data[address] = 0xFF
  address += 1
