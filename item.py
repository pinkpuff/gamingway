# An Item is anything that can appear in the player's inventory.
# There are several Item subtypes based on what properties they have in the rom:
#  * Tool      = Something that can't be equipped or used in battle. It has no
#                corresponding class because it doesn't have any information or
#                functionality beyond that of the parent Item class.
#  * Supply    = Something that can't be equipped but can be used in battle.
#  * Equipment = Something that can be equipped onto characters.
# Equipment has two further subtypes:
#     * Weapon = Something that affects your attack damage, hit, and attributes.
#     * Armor  = Something that affects your physical and magical defense and evade
#                as well as your defense attributes (elemental/status resistances)
class Item:

 def __init__(self):

  # The item's name in ASCII. 
  # Special symbols are encoded using a three-letter code enclosed in square 
  # brackets (e.g. [HRP] or [SWD]). For a full list of codes, see config.py.
  self.name = ""

  # The price of the item.
  # Prices in FF4 are encoded in a compressed way that doesn't allow you to simply
  # have any arbitrary number be a price. If the high bit is unset, the remaining
  # bits are multiplied by 10 to arrive at the price; if it is set, the remaining
  # bits are multiplied by 1000. That means you can have a price of 50 but not 55.
  # Likewise, you can have a price of 5000, but not 5123.
  # This variable represents the "decompressed" price, and you can technically
  # change it to any number you like while editing, but be aware that when writing
  # it back to the rom, it will compress the number as outlined above into the
  # nearest price. So for example, if you set the price to 5123, it will end up as
  # a price of 5000.
  self.price = 0

  # This does not encode a description string directly, but rather the index in a
  # table of descriptions. Most items have no description, and the ones that do
  # can often have identical ones, such as "Restores HP" on all the Cure potion
  # variants, so I imagine it's being done this way to conserve space.
  self.description = 0
 
 # Read the item name from the rom. The other information is stored in different
 # places, so there are different functions for reading each of them in order to
 # avoid making a single read function that's cluttered with a bunch of different
 # addresses.
 def read_name(self, rom, address, text):

  # We use the text module's byte conversion function to parse the item name.
  bytelist = rom.data[address:address + rom.ITEM_NAME_WIDTH]

  # The name is cropped on the right to facilitate displaying and renaming but it
  # will be padded back out when we go to write it back to the rom.
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 # Write the name back to the rom.
 def write_name(self, rom, address, text):

  # First we convert it back from ASCII to FF4 text encoding.
  newname = text.ff4text(self.name)

  # Then we make sure it's exactly 9 letters long. If the given name was longer, we
  # crop it off at 9; if it's shorter, we pad it out to 9 with space characters.
  newname = newname.ljust(rom.ITEM_NAME_WIDTH, text.ff4text(" "))

  # And finally we inject the converted name into the appropriate place in the rom.
  rom.inject(address, text.to_bytes(newname))
 
 # Return a string that contains the item's information.
 # For now, it just displays the name, as that's all that's being read currently,
 # but in future it will also display the price and description.
 def display(self, main):
  return "Name: {}".format(self.name)

