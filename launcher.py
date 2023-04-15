# Launchers involve a few objects so I'll explain them up front:
#
# A Launcher is what was known in FF4kster as an "Event Call". It's something that
# checks some flag settings and then decides which event to launch as a result. For
# example, the tile at the entrance of Mist Village contains a launcher that checks
# whether the package has already been delivered; if that flag is unset, it will
# launch the event that delivers the package. Otherwise, no event is launched.
#
# Each launcher consists of a series of what I'm calling here Components. This is a
# list of flag settings (such as "Opening complete: ON", "Package delivered: OFF")
# and an event index. If the player steps on a tile corresponding to a particular
# launcher, it will go through each of its components in order looking for one whose
# flag settings match the current settings of those flags in RAM. As soon as it
# encounters one, it launches the event indexed by that component. If it goes
# through the entire list without finding one, no event is launched.
#
# To facilitate the programming of the above, I have also created an EventCondition
# object that simply pairs a flag index with a particular on/off state. That way I
# can refer to the conditions as a list of these EventCondition objects rather than
# having a list of flag indexes and a list of states and making sure they line up.

class EventCondition:

 def __init__(self, flag = 0, setting = False):
  self.flag = flag 
  self.setting = setting

class Component:

 def __init__(self):
  self.conditions = []

  # We initialize this to None rather than 0 because 0 is a valid event index, so
  # this makes it easier to check whether the event has been set yet or not.
  self.event = None

class Launcher:

 def __init__(self):
  self.components = []
 
 def read(self, rom, start, finish):
  offset = 0
  component = Component()

  # Go through the given segment of the rom byte by byte until we reach the end,
  # parsing each byte individually.
  while start + offset < finish:

   # Check whether the byte indicates a true condition, false condition, or event.
   match rom.data[start + offset]:

    # An FF byte is used as a separator between the conditions and the event index.
    case 0xFF:
     offset += 1
     component.event = rom.data[start + offset]

     # There can only be one event index, so once we've read one, we know we're done
     # with the component and can add it to the list.
     self.components.append(component)
     component = Component()

    # An FE byte indicates the next byte is a condition that has to be false for the
    # event to be launched.
    case 0xFE:
     offset += 1
     component.conditions.append(EventCondition(rom.data[start + offset], False))

    # Any other byte indicates a condition that has to be true for the even to be
    # launched.
    case _:
     component.conditions.append(EventCondition(rom.data[start + offset], True))

   # Then regardless we move on to the next byte.
   offset += 1

 def write(self, rom, address):
  result = []
  for component in self.components:
   
   # Not sure if it needs to be done this way or not, but FF4kster wrote all the
   # true conditions first followed by all the false conditions, so until I have
   # tested it more thoroughly, this is what I will default to doing here as well.
   for condition in component.conditions:
    if condition.setting:
     result.append(0xFE)
     result.append(condition.flag)
   for condition in component.conditions:
    if not condition.setting:
     result.append(condition.flag)
   result.append(0xFF)
   result.append(component.event)

  # Once all the components have been encoded we are left with a list of bytes we
  # can simply inject directly at the given address.
  rom.inject(address, result)

  # And update it to report where we left off.
  return address + len(result)

 def display(self, main):
  result = ""
  for component in self.components:
   if len(component.conditions) > 0:
    result += "If "
    for index, condition in enumerate(component.conditions):
     result += "flag {} ".format(main.text.hex(condition.flag))
     result += "is {} ".format("ON" if condition.setting else "OFF")
     if index < len(component.conditions) - 1:
      result += "and "
   elif len(self.components) > 1:
    result += "Otherwise "
   else:
    result += "Always "
   result += "launch event {}\n".format(main.text.hex(component.event))
  return result

 # This returns the number of bytes the launcher would take up if it were to be
 # written to the rom. This is mostly needed in order to determine if there is
 # enough space in the rom to write all the launchers.
 def length(self):

  # Start with 0 and add the length of each component.
  result = 0
  for component in self.components:

   # Each component needs at least two bytes for the flag index and FF separator.
   result += 2

   # To that we add the length of each condition.
   for condition in component.conditions:

    # True conditions take two bytes each (FE and the flag index).
    if condition.setting:
     result += 2

    # While false conditions only take one (the flag index alone).
    else:
     result += 1

  # Finally we return our sum.
  return result
