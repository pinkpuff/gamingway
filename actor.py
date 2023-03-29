# This can be seen as an "instance" of a character. For example, while Tellah is a
# Character, the Tellah you meet in the Watery Pass, the Tellah that joins you on
# your way up Mount Ordeals, and the Tellah that rejoins you at the top of Mount
# Ordeals after remembering all his spells are all different Actors.
class Actor:

 def __init__(self):

  # Actors don't all have their own name strings; they simply hold an index into a
  # list of names.
  self.name_index = 0

  # In addition to the usual party of five characters, there is an additional
  # "shadow" party that can store up to five characters for the purposes of having
  # them return to the regular party at some future time. When an actor leaves the
  # party, it can either go into a specific shadow party slot (overwriting whatever
  # data was in that slot, if any), or it can be discarded, in which case that
  # character's stats and progression are all completely discarded. Likewise, when
  # adding an actor to the party, its data can either be read from a character's
  # initial stats, or from a specific shadow party slot.

  # If this flag is set, the actor's stats are read from the initial stats of the
  # character referenced by the load slot. If it is unset, the load slot instead
  # references a shadow slot from which to read the actor's stats.
  self.initialize = False

  # If this flag is set, the actor's stats are stored in the shadow slot specified
  # by the store slot when leaving the party. If it is unset, the stats are
  # discarded.
  self.store = False

  # The initial character index or shadow party slot from which to load the actor's
  # stats when joining the party.
  self.load_slot = 0

  # The shadow party slot in which to store the actor's stats when leaving the
  # party.
  self.store_slot = 0

  # The index of the levelup data used by this actor.
  self.level_link = 0

  # The battle menu commands for the actor. Even two actors that correspond to the
  # same character can have different command menus. This is how Tellah loses his
  # "Recall" command, for example.
  self.commands = [0, 0, 0, 0, 0]

  # The items the actor starts equipped with. For example, the Kain that joins you
  # at the start of the game has different items equipped from the Kain that joins
  # you after the Giant of Babil sequence.
  self.equipped = [0, 0, 0, 0, 0]

  # The ammo count for the items equipped in the actor's right and left hand
  # respectively. This usually only matters for arrows.
  self.ammo = [0, 0]
  
 # Read the actor's name index from the rom.
 def read_name(self, rom, address):
  self.name_index = rom.data[address]
 
 # Write the actor's name index back to the rom.
 def write_name(self, rom, address):
  rom.data[address] = self.name_index
  
 # Read the actor's stat loading information from the rom.
 def read_loading(self, rom, address):
  self.load_slot = rom.data[address] % 0x80
  self.initialize = rom.flag(address, 7)
 
 # Write the character's stat loading information back to the rom.
 def write_loading(self, rom, address):
  rom.data[address] = self.load_slot
  rom.setbit(address, 7, self.initialize)
  
 # Read the actor's stat storing information from the rom.
 def read_storing(self, rom, address):
  self.store_slot = rom.data[address] % 0x80
  self.store = rom.flag(address, 7)
 
 # Write the actor's stat storing information back to the rom.
 def write_storing(self, rom, address):
  rom.data[address] = self.store_slot
  rom.setbit(address, 7, self.store)

 # Read the actor's command list from the rom.
 def read_commands(self, rom, address):
  for index in range(5):
   self.commands[index] = rom.data[address + index]
 
 # Write the actor's command list back to the rom.
 def write_commands(self, rom, address):
  for index in range(5):
   rom.data[address + index] = self.commands[index]
 
 # Read the actor's initial equipment from the rom.
 def read_equipped(self, rom, address):
  self.equipped[2] = rom.data[address]
  self.equipped[3] = rom.data[address + 1]
  self.equipped[4] = rom.data[address + 2]
  self.equipped[0] = rom.data[address + 3]
  self.ammo[0] = rom.data[address + 4]
  self.equipped[1] = rom.data[address + 5]
  self.ammo[1] = rom.data[address + 6]

 # Write the actor's initial equipment back to the rom. 
 def write_equipped(self, rom, address):
  rom.data[address] = self.equipped[2]
  rom.data[address + 1] = self.equipped[3]
  rom.data[address + 2] = self.equipped[4]
  rom.data[address + 3] = self.equipped[0]
  rom.data[address + 4] = self.ammo[0]
  rom.data[address + 5] = self.equipped[1]
  rom.data[address + 6] = self.ammo[1]

 # Return a string containing the actor's information.
 # For now it's just returning the command list for the sake of returning something.
 def display(self, main):
  result = ""
  for command in self.commands:
   result += "[{}] ".format(main.text.hex(command))
  return result
