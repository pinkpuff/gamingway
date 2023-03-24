class TileMap:
 # This represents the actual grid of tiles that compose a map. The reason this is
 # its own separate class and not part of the Map itself is because multiple Maps
 # can share the same TileMap, in which case the shared TileMap is only stored once
 # and simply pointed to by the various Maps that use it.

 def __init__(self):
  # The "tiles" variable represents a 2D array of tile indexes.
  self.tiles = []
 
 def read(self, rom, address):
  # This reads the RLE encoded tile data for a single TileMap from the rom, starting
  # at the specified address, and continuing until 0x400 tiles have been read.
  # During the tile reading process, the tiles are read into a 1D array which is
  # then converted to a 32x32 2D array.
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

 def write(self, rom, address):
  # This writes the 2D tile array back to the rom as an RLE encoded sequence.
  # Most of the work though is done by the "encode" method.
  encoding = self.encode()
  rom.inject(address, encoding)
  return address + len(encoding)

 def encode(self):
  # This converts the TileMap object's 2D tiles array into a 1D array of tiles
  # using run-length encoding.
  result = []
  tiles = [tile for row in self.tiles for tile in row]
  # tiles = self.tiles
  if len(self.tiles) > 0:
   offset = 0
   runlength = 1
   for index, tile in enumerate(tiles):
    if index == 0:
     oldtile = tile
     runlength = 1
    else:
     if tile == oldtile:
      runlength += 1
     else:
      while runlength >= 0x100:
       result.append(oldtile + 0x80)
       result.append(0xFF)
       runlength -= 0xFF
      if runlength > 1:
       result.append(oldtile + 0x80)
       result.append(runlength - 1)
      elif runlength == 1:
       result.append(oldtile)
      runlength = 1
      oldtile = tile
   while runlength >= 0x100:
    result.append(oldtile + 0x80)
    result.append(0xFF)
    runlength -= 0xFF
   if runlength > 1:
    result.append(oldtile + 0x80)
    result.append(runlength - 1)
   elif runlength == 1:
    result.append(oldtile)
  return result

class Map:
 # This refers to an entire town or dungeon floor, including its associated
 # metadata such as whether it's magnetic, whether you can use Warp or Exit,
 # what music plays, etc. It does NOT contain the layout of tiles, at least
 # not directly. Rather, it contains an index of a TileMap object as defined
 # above.

 def __init__(self):
  self.triggers = []
  self.messages = []
  self.backdrop = 0
  self.warpable = False
  self.exitable = False
  self.alternate_backdrop = False
  self.magnetic = False
  self.tilemap = 0
  self.tileset = 0
  self.layout = 0
  self.border_tile = 0
  self.solid_border = False
  self.palette = 0
  self.npc_palettes = [0, 0]
  self.music = 0
  self.background = 0
  self.translucent = False
  self.scroll_vertical = False
  self.scroll_horizontal = False
  self.mystery_bit = False
  self.move_direction = 0
  self.move_speed = 0
  self.ending = False
  self.name_index = 0
  self.treasure_index = 0
  self.encounter_rate = 0
  self.encounter_set = 0  # Where is this read from?

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
 
 def display(self, main):
  result = ""
  if self.name_index > len(main.map_names):
   print("ERROR: Name index {} / {}".format(self.name_index, len(main.map_names)))
  else:
   result = main.map_names[self.name_index]
  return result

def read_map_names(rom, text):
 map_names = [""] * rom.TOTAL_MAP_NAMES
 address = rom.MAP_NAMES_START
 for index in range(rom.TOTAL_MAP_NAMES):
  name = ""
  while rom.data[address] > 0:
   name += chr(rom.data[address])
   address += 1
  address += 1
  map_names[index] = text.asciitext(name)
 return map_names

def write_map_names(rom, text, map_names):
 # Write the map names back to the rom.
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

def read_maps(rom):
 # This reads the Map data from the rom and returns the resulting list.
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

def write_maps(rom, maps):
 # This writes the Map data back to the rom.
 # We simply loop through the list of Maps and write each one using the Map object's
 # "write" method.
 for index, map in enumerate(maps):
  map.write(rom, rom.MAP_DATA_START + index * 13)
  
  # The encounter rates are stored in a separate area of the rom, but they seem like
  # they should be categorically part of the Map object, so we still include them
  # here but write them separately from the built-in "write" method so that we don't
  # have to pass it several different addresses.
  map.write_encounter_rate(rom, rom.ENCOUNTER_RATES_START + index)

def read_tilemaps(rom):
 # This reads the list of TileMaps from the rom.
 # The "oldaddress" variable is there to track the previous TileMap's pointer
 # because when a TileMap has no data, it seems to use the previous TileMap's pointer.
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

def write_tilemaps(rom, tilemaps):
 # This writes the list of tilemaps back to the rom.
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

def read_overworld(rom):
 # This reads the RLE-encoded overworld tile data and returns it as an array.
 # The array itself is one-dimensional but in practice it is 256x256.
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
    else:
     tilemap.tiles[row].append(tile)

   # Now we can read the next tile and check if it's FF and so on.
   tile = rom.data[address]
   address += 1
 
 # And finally return the fully parsed tilemap.
 return tilemap
 
def write_overworld(rom, tilemap):
 # This writes the 2D array of overworld tiles back to the rom data as a list
 # of 256-tile-wide RLE-encoded rows, along with the appropriate pointers.
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
