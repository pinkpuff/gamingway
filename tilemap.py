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

