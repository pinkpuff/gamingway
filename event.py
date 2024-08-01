class Instruction:

 def __init__(self, code = 0, parameters = None):
  self.code = code
  if parameters == None:
   self.parameters = []
  else:
   self.parameters = parameters
 
 def display(self, main):
  result = main.config.instruction_names[self.code]
  if len(self.parameters) > 0:
   for parameter in self.parameters:
    result += "{:02X} ".format(parameter)
  return result

class Event:

 def __init__(self):
  self.has_branch = False
  self.script = []
  self.branch = []
 
 def read(self, rom, config, address):
  offset = address
  instruction = rom.data[offset]
  while instruction != 0xFF:
   parameters = []
   count = config.parameter_count[instruction]
   offset += 1
   if count > 0:
    for index in range(count):
     parameters.append(rom.data[offset + index])
    offset += count
   self.script.append(Instruction(instruction, parameters))
   instruction = rom.data[offset]
 
 def display(self, main):
  result = ""
  for instruction in self.script:
   result += instruction.display(main) + "\n"
  return result