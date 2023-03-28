# This represents a spell that can be cast in battle.
# The same object will likely be used for "monster abilities" like ColdMist and
# Reaction and such but for now, only the 6-letter-name player spells are being
# read.
class Spell:
 
 def __init__(self):
  
  # The name of the spell in ASCII. Symbols like magic orbs use the corresponding
  # three letter code in square brackets (e.g. [BLK], [WHT], [SUM]). See text.py
  # for the full list of codes.
  self.name = ""
  
  # This is how long between inputting the command and the spell resolving. Slower
  # spells have a higher delay value.
  self.delay = 0
  
  # There are eight target types. This indicates which of the eight the spell uses.
  # The target types are enumerated in config.py.
  self.target = 0
  
  # The specific function of the spell's power depends on its effect type, but in
  # general, the higher this number is, the "stronger" the spell is. So damage
  # spells with higher power will deal more damage; healing spells with higher
  # power will heal more, etc. Some spell effects don't use it at all though.
  self.power = 0
  
  # This indicates the chance of the spell succeeding when cast. Even if a given
  # target isn't immune to the spell's effect, it still has a chance of failing.
  # For many (most?) spells, the chance of it failing is either 0 or close enough
  # to it that you don't have to consider it, especially since I think the caster's
  # spell power gets added to this number before making the check. However, I think
  # the target's magic evade is also subtracted from it (or otherwise reduces it
  # somehow) so sometimes you might see, for example, a spell from a late game
  # monster appear to do nothing; this could be because it missed due to your
  # character's magic evasion.
  self.hit = 0
  
  # This flag is set for spells that are usable on bosses. If the flag is unset,
  # monsters that have the Boss flag set will be immune to the spell.
  self.hitsboss = True
  
  # This indicates which spell effect the spell has. There is a large list of
  # effects, and this number represents the index in that list. See config.py for
  # the full list of spell effects.
  self.effect = 0
  
  # When this flag is set, if the spell deals damage, it will deal a lot more than
  # if this flag is unset. Most, if not all, of the vanilla damage spells have it
  # set, so if you set it, it will do the kind of damage you would probably expect.
  # I'm not sure what effect it has, if any, on non-damage spells.
  self.damaging = False
  
  # An attribute table is a set of flag settings for all the game's attribute
  # flags. These are things like "fire", "ice", etc, but also statuses like "mute",
  # "blind", "charm", etc. There is a list of these attribute tables in the rom and
  # things like spells and equipment use an index in this list rather than each one
  # having their own independent attribute table. So for example, say attribute
  # table 3 has the "ice" flag set and all other flags unset, then any spell or 
  # equipment that uses attribute index 3 will be considered to have the "ice" flag
  # and no other flags set. The meaning of having particular attribute flags set or
  # unset depends on what effect the spell has. For example, the "Add status"
  # effect will try to add all the statuses in the given attribute table whose 
  # flags are set. In contrast, the "Remove status" effect will try to remove all 
  # statuses from the target whose corresponding attribute flags are UNSET in the
  # spell's attribute table.
  self.attributes = 0
  
  # This flag indicates whether or not a player unit hit with the spell will show
  # the "impact" animation (the one that looks like they're getting hit).
  self.impact = False
  
  # This is the MP cost of the spell. The byte that encodes this uses the high bit
  # for something else so it physically can't be any higher than 128, but I think
  # putting it higher than 99 might cause some strange behaviour when the game
  # tries to display the MP cost, since it only expects a two digit number.
  self.mp = 0
  
  # This flag indicates whether or not the spell is bounced by reflect.
  self.reflectable = False

  # These are the spell's animation data. They indicate which animation it uses and
  # what colors and what sound effect.
  self.palette = 0
  self.sprites = 0
  self.visual1 = 0
  self.visual2 = 0
  self.sound = 0
 
 # Read the main spell data from the rom at the given address.
 def read(self, rom, address):
  self.delay = rom.data[address] % 0x20
  self.target = rom.data[address] >> 5
  self.power = rom.data[address + 1]
  self.hit = rom.data[address + 2] % 0x80
  self.hitsboss = not rom.flag(address + 2, 7)
  self.effect = rom.data[address + 3] % 0x80
  self.damaging = not rom.flag(address + 3, 7)
  self.attributes = rom.data[address + 4] % 0x80
  self.impact = rom.flag(address + 4, 7)
  self.mp = rom.data[address + 5] % 0x80
  self.reflectable = not rom.flag(address + 5, 7)
 
 # Write the main spell data back to the rom at the given address.
 def write(self, rom, address):
  rom.data[address] = self.delay + (self.target << 5)
  rom.data[address + 1] = self.power
  rom.data[address + 2] = self.hit % 0x80
  rom.setbit(address + 2, 7, not self.hitsboss)
  rom.data[address + 3] = self.effect % 0x80
  rom.setbit(address + 3, 7, not self.damaging)
  rom.data[address + 4] = self.attributes % 0x80
  rom.setbit(address + 4, 7, self.impact)
  rom.data[address + 5] = self.mp % 0x80
  rom.setbit(address + 5, 7, not self.reflectable)
 
 # Read the spell name from the given address.
 # The spell names are stored separately from the rest of the spell data, so we use
 # a separate reading function so that we don't get confused passing a bunch of
 # different addresses to one function.
 def read_name(self, rom, address, text):

  # We simply pass the raw byte sequence to the text converter.
  bytelist = rom.data[address:address + rom.SPELL_NAME_WIDTH]

  # The name is cropped on the right to facilitate printing and constructing
  # strings, but it will be padded back out when it gets written back to the rom.
  self.name = text.asciitext(text.from_bytes(bytelist)).rstrip()
 
 # Write the spell name back to the rom.
 def write_name(self, rom, address, text):

  # Pad the name back out to the appropriate width first.
  newname = text.ff4text(self.name)
  newname = newname.ljust(rom.SPELL_NAME_WIDTH, text.ff4text(" "))

  # Then convert it and put it back into the rom.
  rom.inject(address, text.to_bytes(newname))

 # Read the spell visual effect information from the rom.
 # As with the names, these are stored in a separate place in the rom, so we use a
 # separate function to read them in order to reduce confusion.
 def read_visuals(self, rom, address):
  self.palette = rom.data[address]
  self.sprites = rom.data[address + 1]
  self.visual1 = rom.data[address + 2]
  self.visual2 = rom.data[address + 3]
  
 # Write the spell visual effect information back to the rom.
 def write_visuals(self, rom, address):
  rom.data[address] = self.palette
  rom.data[address + 1] = self.sprites
  rom.data[address + 2] = self.visual1
  rom.data[address + 3] = self.visual2
 
 # Read the spell's sound effect from the rom.
 # As with the visual data and names, the sound effects are stored separately, so we
 # use a separate function to read them.
 def read_sound(self, rom, address):
  self.sound = rom.data[address]
 
 # Write the spell's sound effect back to the rom.
 def write_sound(self, rom, address):
  rom.data[address] = self.sound
 
 # Returns a string containing the spell's visual effect information.
 def display_visuals(self, main):
  result  = "Palette: {}, ".format(main.text.hex(self.palette))
  result += "Sprites: {}, ".format(main.text.hex(self.sprites))
  result += "Visual1: {}, ".format(main.text.hex(self.visual1))
  result += "Visual2: {}, ".format(main.text.hex(self.visual2))
  result += "Sound:   {}".format(main.text.hex(self.sound))
  return result
 
 # Returns a string containing the main information about the spell.
 def display(self, main):
  result  = "Name: {}\n".format(self.name)
  result += "MP:     {}\n".format(self.mp)
  result += "Effect: {}\n".format(main.config.spell_effects[self.effect])
  result += "Target: {}\n".format(main.config.target_types[self.target])
  result += "Hit:    {}%\n".format(self.hit)
  result += "Power:  {}\n".format(self.power)
  result += "Delay:  {}\n".format(self.delay)
  result += "Attributes: [{}] ".format(main.text.hex(self.attributes))
  if len(main.attributes) > 0:
   if self.effect in [8, 9, 17, 28, 29]:
    result += main.attributes[self.attributes].display_alternate(main)
   elif self.effect == 11:
    result += main.attributes[self.attributes].display_inverted(main)
   else:
    result += main.attributes[self.attributes].display(main)
  properties = ""
  if self.reflectable:
   properties += "Reflectable"
  if self.hitsboss:
   if len(properties) > 0:
    properties += ", "
   properties += "Hits bosses"
  if self.damaging:
   if len(properties) > 0:
    properties += ", "
   properties += "Deals damage"
  if self.impact:
   if len(properties) > 0:
    properties += ", "
   properties += "Impact"
  if len(properties) > 0:
   result += "\n" + properties
  return result

