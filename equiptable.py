from common import FlagSet

# An EquipTable is essentially a list of flags indicating which jobs have permission
# to use a certain piece of equipment. Since many equipments share the same set of
# jobs that can equip them, this saves space relative to giving each equipment its 
# own individual full set of flags.
class EquipTable(FlagSet):

 def __init__(self):

  # An EquipTable is essentially a FlagSet with two bytes.
  super().__init__(2)
 
 # Read the flag settings from the rom.
 def read(self, rom, address):

  # We simply defer to the parent function but pass it an array of two bytes.
  super().from_bytes(rom.data[address:address + 2])
 
 # Write the flag settings back to the rom.
 def write(self, rom, address):

  # We use the parent function to encode the flags into a pair of bytes, which we
  # inject directly into the rom at the appropriate place.
  rom.inject(address, super().to_bytes())
 
 # Return a string which shows a list of the jobs whose flags are set, separated by
 # commas.
 def display(self, main):
  result = ""
  for index, flag in enumerate(self.flags):
   if flag:
    if len(result) > 0:
     result += ", "
    result += main.config.job_names[index]
  return result

