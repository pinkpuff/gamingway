# A job is mostly a collection of spellbooks and equips.
# There are separate spellbooks for the menu and for combat.
# While these are normally the same, there is nothing in the
# code ensuring that they correspond to each other.
class Job:
 
 def __init__(self):
  self.name = ""
  
  # Combat spellbooks
  self.white = 0
  self.black = 0
  self.summon = 0
  
  # Menu spellbooks
  self.menu_white = 0
  self.menu_black = 0
  self.menu_summon = 0
 
 # Read the Job from the given address.
 def read(self, rom, address):
  pass
 
 # Read the spell name from the given address.
 # The spell names are stored separately from the rest of the spell data, so we use
 # a separate reading function so that we don't get confused passing a bunch of
 # different addresses to one function.
 def read_name(self, rom, address, text):
 
  # We simply pass the raw byte sequence to the text converter.
  bytelist = rom.data[address:address + rom.JOB_NAME_WIDTH]

  # The name is cropped on the right to facilitate printing and constructing
  # strings, but it will be padded back out when it gets written back to the rom.
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()

 # Returns a string containing the main information about the Job.
 def display(self, main):
  result = self.name
  return result.name