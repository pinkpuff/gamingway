from item import Item
from spell import Spell

# This is a consumable item that can be used in battle.
class Supply(Item):

 def __init__(self, attribute_reference = []):
  super().__init__()

  # The "utility" essentially defines what the supply does when used in battle.
  # Since all the information is encoded in exactly the same way and same order as
  # it is in the spells, we simply use the spell object to encode it.
  self.utility = Spell()
  
 # Read the item's utility from the rom.
 def read(self, rom, address):
  self.utility.read(rom, address)

 # Write the item's utility back to the rom. 
 def write(self, rom, address):
  self.utility.write(rom, address)
 
 # Return a string that contains the supply's information.
 def display(self, main):
  self.utility.name = self.name
  return self.utility.display(main)

