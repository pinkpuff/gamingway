from equipment import Equipment

# This represents an item that can be equipped onto a character to boost their
# attack stats. 
class Weapon(Equipment):

 def __init__(self):

  # It has all the stats an Equipment has.
  super().__init__()

  # This flag indicates whether or not the weapon can be thrown using Dart.
  self.throwable = False

  # This flag indicates whether the weapon ignores the usual penalties for attacking
  # from the back row.
  self.ranged = False

  # I have no idea what the function of this flag is. The reason it's called
  # "litarrow" and not simply "mystery flag" like many of the others is because
  # there are already a few "mystery flags" in the weapon record, and because in
  # vanilla, there is exactly one weapon that has this flag set: the Lit Arrow.
  self.litarrow = False

  # Technically another mystery flag, but this one seems to be off on all weapons in
  # vanilla. I have no idea if setting it has any effect on gameplay.
  self.unused_property = False

  # This flag seems to be set on hammers, but I'm not convinced that the game
  # actually checks it. My understanding is that anything that needs to check types
  # of weapons such as hammers, harps, bows, etc, seems to have hard coded item
  # index ranges and doesn't actually check the flag settings.
  self.hammer_flag = False

  # As above but for axe type weapons.
  self.axe_flag = False

  # My understanding is that a character wielding a weapon with this flag cannot
  # deal critical hits. 
  self.nerf_crits = False

  # The bonus the weapon gives to the character's physical attack power.
  self.attack = 0
  
  # The bonus the weapon gives to the character's physical hit rate.
  self.hit = 0

  # I have no idea what this flag does, if anything.
  self.mystery_flag = False

  # This is the index of the spell this weapon will cast if it is selected from the
  # character's equipped items in battle. 
  self.casts_spell = 0

  # I have no idea what this flag does either, if anything.
  self.mystery_flag2 = False

  # If this flag is set, the weapon will be consumed when used. This is generally
  # meant for arrows but there's no reason it couldn't theoretically be set on an
  # otherwise normal weapon if you wanted to do that.
  self.consumable = False

  # Throwable weapons also have this flag set. I don't think it does anything and
  # all the "work" is done by the first throwable flag above.
  self.throwable2 = False

  # This is the type of graphic used by the weapon when you attack with it. For
  # example, does it look like a spear, knife, harp, etc.
  self.sprite = 0

  # This is the index into the list of palettes that determines the colors of the
  # weapon when animating the user's physical attack.
  self.palette = 0

  # This determines the type of animation used by the weapon. For example, is it
  # "swung" over the head like a knife or sword? Is it "pulled" like a harp or bow?
  # As usual, this is determined by an index into a list of weapon swing animations.
  self.swing = 0

  # This is the animation that appears on the target when you hit with the weapon.
  # For example, the swords' slashing effect, the impact animations of the hammers,
  # notes of the harp, etc.
  self.slash = 0

  # This is the animation used by the weapon's "item cast" spell. Normally this will
  # match the animation used by the spell itself, but there's no reason you couldn't
  # have a different spell's animation if you felt like doing that.
  self.casts_visual = 0

  # This is the spell power of the weapon's "item cast" spell. It ignores the user's
  # spell power and uses this value instead. This is currently not being read from
  # the rom yet.
  self.casts_power = 0

 # Read the main item information from the rom.
 def read(self, rom, address):
  self.magnetic = rom.flag(address, 7)
  self.throwable = rom.flag(address, 6)
  self.ranged = rom.flag(address, 5)
  self.litarrow = rom.flag(address, 4)
  self.unused_property = rom.flag(address, 3)
  self.hammer_flag = rom.flag(address, 2)
  self.axe_flag = rom.flag(address, 1)
  self.nerf_crits = rom.flag(address, 0)
  self.attack = rom.data[address + 1]
  self.hit = rom.data[address + 2] % 0x80
  self.mystery_flag = rom.flag(address + 2, 7)
  self.casts_spell = rom.data[address + 3]
  self.attributes = rom.data[address + 4]
  self.races.read(rom, address + 5)
  self.equips = rom.data[address + 6] % 0x20
  self.mystery_flag2 = rom.flag(address + 6, 5)
  self.consumable = rom.flag(address + 6, 6)
  self.bow_flag = rom.flag(address + 6, 7)
  self.statbuff.read(rom, address + 7)
 
 # Write the main item information back to the rom.
 def write(self, rom, address):
  rom.data[address] = 0
  rom.setbit(address, 7, self.magnetic)
  rom.setbit(address, 6, self.throwable)
  rom.setbit(address, 5, self.ranged)
  rom.setbit(address, 4, self.litarrow)
  rom.setbit(address, 3, self.unused_property)
  rom.setbit(address, 2, self.hammer_flag)
  rom.setbit(address, 1, self.axe_flag)
  rom.setbit(address, 0, self.nerf_crits)
  rom.data[address + 1] = self.attack
  rom.data[address + 2] = self.hit % 0x80
  rom.setbit(address + 2, 7, self.mystery_flag)
  rom.data[address + 3] = self.casts_spell
  rom.data[address + 4] = self.attributes
  self.races.write(rom, address + 5)
  rom.data[address + 6] = self.equips % 0x20
  rom.setbit(address + 6, 5, self.mystery_flag2)
  rom.setbit(address + 6, 6, self.consumable)
  rom.setbit(address + 6, 7, self.bow_flag)
  self.statbuff.write(rom, address + 7)
 
 # Read the item's animation information from the rom.
 def read_visuals(self, rom, address):
  self.palette = rom.data[address]
  self.sprite = rom.data[address + 1]
  self.slash = rom.data[address + 2]
  self.swing = rom.data[address + 3]
  
 # Write the item's animation information back to the rom.
 def write_visuals(self, rom, address):
  rom.data[address] = self.palette
  rom.data[address + 1] = self.sprite
  rom.data[address + 2] = self.slash
  rom.data[address + 3] = self.swing

 # Return a string containing the weapon's information.
 def display(self, main):
  result = ""
  result += "Name: {}\n".format(self.name)
  result += "Attack:     {}\n".format(self.attack)
  result += "Hit:        {}\n".format(self.hit)
  result += "Mystery1:   {}\n".format(self.mystery_flag)
  if len(main.spells) > self.casts_spell:
   casts = main.spells[self.casts_spell].name
  else:
   casts = text.hex(self.casts_spell)
  result += "Casts:      {}\n".format(casts)
  attributes = "[{}] ".format(main.text.hex(self.attributes))
  if len(main.attributes) > 0:
   attributes += main.attributes[self.attributes].display(main)
  result += "Attributes: {}\n".format(attributes)
  result += "Races:      {}\n".format(self.races.display(main))
  equips = "[{}] ".format(main.text.hex(self.equips))
  if len(main.equips) > 0:
   equips += main.equips[self.equips].display(main)
  result += "Equips:     {}\n".format(equips)
  result += "Mystery2:   {}\n".format(self.mystery_flag2)
  result += "Magnetic:   {}\n".format(self.magnetic)
  result += self.statbuff.display(main)
  properties = ""
  if self.throwable:
   properties += "Throwable  "
  if self.ranged:
   properties += "Ranged  "
  if self.litarrow:
   properties += "LitArrow  "
  if self.unused_property:
   properties += "Unknown  "
  if self.hammer_flag:
   properties += "Hammer  "
  if self.axe_flag:
   properties += "Axe  "
  if self.nerf_crits:
   properties += "Uncrit  "
  if self.consumable:
   properties += "Consumable  "
  if self.bow_flag:
   properties += "Bow  "
  if len(properties) > 0:
   result += "\n" + properties
  return result

