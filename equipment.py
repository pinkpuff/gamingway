from item import Item
from common import FlagSet, StatBuff

# This represents an item that can be equipped onto characters. It acts as the
# parent class for both Weapons and Armors, and encodes all the information that is
# common to both.
class Equipment(Item):

 def __init__(self):
  super().__init__()

  # If a character is wearing any equipment at all that has this flag set, and you
  # are on a map that also has its "magnetic" flag set, the character will have the
  # "Magnetized" status in all battles spawned by that map.
  self.magnetic = False

  # Attributes refer to the element and status flags. For weapons, this indicates
  # what properties your physical attacks will have; for armors, it indicates what
  # elements and statuses you resist.
  # Rather than each equipment having its own independent set of flags, it instead
  # has an index into a global list of attribute tables that indicates which of
  # those tables it uses.
  self.attributes = 0

  # For weapons, this indicates the monster races your attacks will deal more damage
  # to. For armors, it indicates the monster races that will deal less damage to you
  # with their physical attacks.
  self.races = FlagSet()

  # This indicates what stats the equipment boosts and by how much.
  self.statbuff = StatBuff()

  # This indicates which jobs can use the equipment. Note that much like attributes,
  # each equipment does not get its own independent set of flags, but rather
  # references an index into a list of equip tables.
  self.equips = 0

