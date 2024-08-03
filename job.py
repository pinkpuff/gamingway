# A job is mostly a collection of spellbooks and equips.
# There are separate spellbooks for the menu and for combat.
# While these are normally the same, there is nothing in the
# code ensuring that they correspond to each other.
class Job:
 
 def __init__(self):
  self.name = ""
  
  # Combat spellbooks
  # 0xFF indicates no spellbook assignment.
  self.white = 0xFF
  self.black = 0xFF
  self.summon = 0xFF
  
  # Menu spellbooks
  self.menu_white = 0xFF
  self.menu_black = 0xFF
  self.menu_summon = 0xFF
 
 # Read the Job from the given address.
 def read(self, rom, address):
  pass

 # Read the main job information.
 # In this case, it's only the battle spell menus.
 def read(self, rom, address):
  self.white = rom.data[address]
  self.black = rom.data[address + 1]
  self.summon = rom.data[address + 2]

 # Write the main job information.
 def write(self, rom, address):
  rom.data[address] = self.white
  rom.data[address + 1] = self.black
  rom.data[address + 2] = self.summon

 # Read the in-menu spell assignments.
 def read_menu(self, rom, address):
  self.menu_white = rom.data[address]
  self.menu_black = rom.data[address + 1]
  self.menu_summon = rom.data[address + 2]

 # Write the in-menu spell assignements.
 def write_menu(self, rom, address):
  rom.data[address] = self.menu_white
  rom.data[address + 1] = self.menu_black
  rom.data[address + 2] = self.menu_summon
 
 # Read the job name from the given address.
 # The job names are stored separately from the rest of the job data, so we use
 # a separate reading function so that we don't get confused passing a bunch of
 # different addresses to one function.
 def read_name(self, rom, address, text):
 
  # We simply pass the raw byte sequence to the text converter.
  bytelist = rom.data[address:address + rom.JOB_NAME_WIDTH]

  # The name is cropped on the right to facilitate printing and constructing
  # strings, but it will be padded back out when it gets written back to the rom.
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()

 # Write the job name back to the rom.
 def write_name(self, rom, address, text):

  # Pad the name back out to the appropriate width first.
  newname = text.ff4text(self.name)
  newname = newname.ljust(rom.JOB_NAME_WIDTH, text.ff4text(" "))

  # Then convert it and put it back into the rom.
  rom.inject(address, text.to_bytes(newname))

 # Returns a string containing the main information about the Job.
 def display(self, main):
  result = self.name
  result += " [{:02X}]".format(self.white)
  result += " [{:02X}]".format(self.black)
  result += " [{:02X}]".format(self.summon)
  return result
