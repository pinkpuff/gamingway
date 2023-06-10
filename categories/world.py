from tilemap import TileMap
from map import Map
from launcher import Launcher

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

  # Like the encounter rates, the triggers are categorically part of the Map object,
  # but are stored elsewhere. This passes the pointer to the map's trigger reader.
  map.read_triggers(rom, rom.TRIGGER_POINTERS_START + index * 2)
 
 # And finally, return the list.
 return maps

# This writes the Map data back to the rom.
def write_maps(rom, maps):

 # This is for tracking where we left off in writing trigger data.
 trigger_address = rom.TRIGGER_DATA_START
 
 # We simply loop through the list of Maps and write each one using the Map object's
 # "write" method.
 for index, map in enumerate(maps):
  map.write(rom, rom.MAP_DATA_START + index * 13)
  
  # The encounter rates are stored in a separate area of the rom, but they seem like
  # they should be categorically part of the Map object, so we still include them
  # here but write them separately from the built-in "write" method so that we don't
  # have to pass it several different addresses.
  map.write_encounter_rate(rom, rom.ENCOUNTER_RATES_START + index)

  # Like the encounter rates, the triggers are categorically part of the Map object,
  # but are stored elsewhere. The trigger list is a variable length record so we
  # need to make sure there's enough room before we write anything.
  if trigger_address + len(map.triggers) * 5 > rom.TRIGGER_DATA_END:
   print("ERROR: Not enough room for triggers.")
   print("** Map {}".format(index))
  else:
   trigger_address = map.write_triggers(rom, trigger_address)
   
   # The next map's trigger pointer should point to where this map's trigger data
   # left off.
   if index < len(maps) - 1:
    next_pointer = rom.TRIGGER_POINTERS_START + (index + 1) * 2
    rom.write_wide(next_pointer, trigger_address - rom.TRIGGER_DATA_START)

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

# This reads the list of event launchers from the rom.
def read_launchers(rom):
 launchers = []

 # Launchers are a variable length record with a pointer table. However, each
 # launcher doesn't seem to have a terminator like an 0xFF or 0x00 byte or anything,
 # so I'm not exactly sure how the game itself knows "where to stop" when it's
 # reading launchers. For now I'm just using the FF4kster strategy of reading the
 # next launcher's pointer and assuming that where the next launcher begins is
 # where this launcher ends.
 for index in range(rom.TOTAL_LAUNCHERS):
  start = rom.read_wide(rom.LAUNCHER_POINTERS_START + index * 2)
  start += rom.LAUNCHER_DATA_START
  finish = rom.read_wide(rom.LAUNCHER_POINTERS_START + (index + 1) * 2)
  finish += rom.LAUNCHER_DATA_START
  launcher = Launcher()
  launchers.append(launcher)
  launcher.read(rom, start, finish)
 return launchers

# This writes the list of event launchers back to the rom.
def write_launchers(rom, launchers):

 # Since the list of launchers is variable length, we need to first determine if
 # there is enough room for all the launcher data.
 needed = 0
 for launcher in launchers:
  needed += launcher.length()
 
 # Then if there isn't enough room, we don't write anything and produce an error.
 if needed > rom.LAUNCHER_ROOM:
  print("ERROR: Not enough room for event launchers.")
 
 # Otherwise, we proceed.
 else:
  
  # Loop through the list, writing each one and updating the pointers as we go.
  address = rom.LAUNCHER_DATA_START
  for index, launcher in enumerate(launchers):

   # First create the pointer.
   pointer = address - rom.LAUNCHER_DATA_START
   rom.write_wide(rom.LAUNCHER_POINTERS_START, pointer)

   # Then write the launcher data.
   # Since launchers are a variable length record, the writing routine returns the
   # address it left off at so that we can accurately track where we are.
   address = launcher.write(rom, address)

  # Finally, add the final pointer to the address where the last launcher left off.
  # This has to do with the way we're reading them, using the pointer to the next
  # launcher to determine the ending of the current one. Thus we only read 0xFF
  # launchers despite there being 0x100 pointers, since we need an "ending" pointer
  # for the last launcher in order for this to work.
  pointer = address - rom.LAUNCHER_DATA_START
  rom.write_wide(rom.LAUNCHER_POINTERS_START, pointer)
