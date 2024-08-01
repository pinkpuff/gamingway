class Configuration:

 def __init__(self):
  # Labels for common data types
  self.stat_names = [
   "STR",
   "AGI",
   "VIT",
   "WIS",
   "WIL"
  ]

  self.race_names = [
   "Dragon",
   "Machine",
   "Reptile",
   "Spirit",
   "Giant",
   "Slime",
   "Mage",
   "Undead"
  ]

  self.element_names = [
   "Fire",
   "Ice",
   "Bolt",
   "Shadow",
   "Holy",
   "Air",
   "Absorb",
   "Immune"
  ]

  self.persistent_status_names = [
   "Poison",
   "Blind",
   "Mute",
   "Pig",
   "Mini",
   "Frog",
   "Petrify",
   "KO"
  ]

  self.temporary_status_names = [
   "Calcify 1",
   "Calcify 2",
   "Berserk",
   "Charm",
   "Sleep",
   "Stun",
   "Float",
   "Curse"
  ]

  self.hidden_status_names = [
   "Count",
   "Airborne",
   "Twincasting",
   "Charging",
   "Defending",
   "Stop",
   "Egg",
   "Magnetize"
  ]

  self.system_status_names = [
   "Critical",
   "Covered",
   "Blink 1",
   "Blink 2",
   "Barrier",
   "Reflect",
   "Sap",
   "Hidden"
  ]

  # self.job_names = [
   # "Dark Knight",
   # "Dragoon",
   # "Caller",
   # "Sage",
   # "Bard",
   # "White Wizard",
   # "Karate",
   # "Black Mage",
   # "White Mage",
   # "Paladin",
   # "Chief",
   # "Summoner",
   # "Ninja",
   # "Lunar",
   # "Brother",
   # "Fiancee"
  # ]

  self.equip_slots = [
   "Hand", 
   "Head", 
   "Body", 
   "Arms"
  ]
  
  self.target_types = [
   "Self",
   "Single (ally)",
   "All allies",
   "Split (ally)",
   "Single enemy",
   "Single (enemy)",
   "All enemies",
   "Split (enemy)"
  ]

  self.spell_effects = [
   "Damage",
   "Damage, Sap",
   "Recover HP",
   "Single-digit HP",
   "Drain HP",
   "Drain MP",
   "Add status to living creatures",
   "Add immobilizing status",
   "Add Blink",
   "Add Reflect",
   "Remove KO",
   "Remove statuses",
   "Add form-changing status",
   "Increase physical defense",
   "Increase magic defense",
   "Modify speed",
   "Remove positive statuses",
   "Add Stop",
   "Scan",
   "Flee battle",
   "Damage based on caster's HP",
   "Recover MP",
   "Fully heal HP/MP",
   "Damage, Poison",
   "Damage, status to living creatures",
   "damage, immobilizing status",
   "Sylph",
   "Odin",
   "Add Count (A)",
   "Add Count (B)",
   "Damage based on target's Max HP",
   "Add Calcify",
   "Gaze",
   "Bluster",
   "Slap",
   "Blast",
   "Hug",
   "Explode",
   "Reaction",
   "Recover 1/10 target's HP",
   "Damage, status",
   "Spawn a monster",
   "Remove positive status",
   "Damage based on physical attack power",
   "Recover 1/3 target's HP",
   "Trigger a reaction",
   "Increment invincibility counter",
   "Decrement invincibility counter",
   "Revive monster",
   "Suicide, bring in next monster",
   "End battle",
   "Search",
   "Hatch",
   "Something happens to adult Rydia"
  ]
  self.spell_effects += ["(unknown)"] * (0x80 - len(self.spell_effects))

  self.drop_rates = [
   "0%",
   "5%",
   "25%",
   "100%"
  ]
  
  self.facings = [
   "up",
   "right",
   "down",
   "left"
  ]
  
  self.placement_movements = [
   "moves up",
   "moves right",
   "moves down",
   "moves left",
   "faces up",
   "faces right",
   "faces down",
   "faces left",
   "becomes (in)visible",
   "leaps over",
   "spins",
   "hops",
   "waves in",
   "waves out",
   "bows head",
   "lies down"
  ]
  
  self.self_movements = [
   "move up",
   "move right",
   "move down",
   "move left",
   "face up",
   "face right",
   "face down",
   "face left",
   "become invisible",
   "become visible",
   "wave in",
   "wave out",
   "bow head",
   "lie down",
   "start/stop turning",
   "start/stop spinning"
  ]

  self.instruction_names = []
  for index in range(0xC0):
   instruction = "Placement {} ".format(int(index / 0x10))
   instruction += self.placement_movements[index % 0x10]
   self.instruction_names.append(instruction)
  for index in range(0xC0, 0xD0):
   instruction = "You " + self.self_movements[index % 0x10]
   self.instruction_names.append(instruction)
  self.instruction_names += [
   "Start/stop shaking",
   "Flash screen",
   "Blur screen",
   "Space travel",
   "Fat chocobo",
   "Open next door",
   "Jolt screen",
   "Start/stop running",
   "Fade out",
   "Namingway",
   "Screen fade",
   "Toggle status: ",
   "Pay GP: ",
   "Change leader: ",
   "Heal HP: ",
   "Heal MP: ",
   "Get item: ",
   "Lose item: ",
   "Learn spell: ",
   "Remove status: ",
   "Add status: ",
   "Get GP: ",
   "Lose GP: ",
   "Hire actor: ",
   "Lose actor: ",
   "Pause: ",
   "Fade in: ",
   "Repeat: ",
   "Battle: ",
   "Shop: ",
   "Message parameter: ",
   "Local message: ",
   "Bank 1 (lo) message: ",
   "Bank 1 (hi) message: ",
   "Set flag: ",
   "Clear flag: ",
   "Activate NPC: ",
   "Deactivate NPC: ",
   "Bank 3 message: ",
   "Select item: ",
   "Choose Yes/No",
   "Tint screen: ",
   "Play song: ",
   "Play SFX: ",
   "Conditional: ",
   "Play VFX: ",
   "Teleport: ",
   "END EVENT"
  ]
  
  self.parameter_count = {}
  for index in range(0x100):
   if index <= 0xDA:
    self.parameter_count[index] = 0
   else:
    self.parameter_count[index] = 1
  self.parameter_count[0xFF] = 0
  self.parameter_count[0xE2] = 2
  self.parameter_count[0xEB] = 2
  self.parameter_count[0xFC] = 2
  self.parameter_count[0xFE] = 4

  self.attribute_names = self.element_names 
  self.attribute_names += self.persistent_status_names
  self.attribute_names += self.temporary_status_names
  
 def index_list(self, candidate, datatype):
  error = False
  datatype = datatype.lower()
  if datatype in ["stat", "stats"]:
   typelist = self.stat_names
  elif datatype in ["race", "races"]:
   typelist = self.race_names
  elif datatype in ["element", "elements"]:
   typelist = self.element_names
  elif datatype in ["persistent", "persistent status", "persistent statuses"]:
   typelist = self.persistent_status_names
  elif datatype in ["temporary", "temoporary status", "temporary statuses"]:
   typelist = self.temporary_status_names
  elif datatype in ["attribute", "attributes"]:
   typelist = self.attribute_names
  elif datatype in ["hidden", "hidden status", "hidden statuses"]:
   typelist = self.hidden_status_names
  elif datatype in ["system", "system status", "system statuses"]:
   typelist = self.system_status_names
  elif datatype in ["job", "jobs"]:
   typelist = self.job_names
  elif datatype in ["slot", "slots", "equip slot", "equip slots"]:
   typelist = self.equip_slots
  elif datatype in ["target", "targets", "target type", "target types"]:
   typelist = self.target_types
  elif datatype in ["effect", "effects", "spell effect", "spell effects"]:
   typelist = self.spell_effects
  elif datatype in ["drop rate", "drop rates", "item drop rate", "item drop rates"]:
   typelist = self.drop_rates
  else:
   print("Unknown data type")
   error = True
  if not error:
   if type(candidate) == str:
    if candidate.lower() in [x.lower() for x in typelist]:
     flaglist = [typelist.index(candidate)]
    else:
     error = True
   elif type(candidate) == int:
    if candidate < len(typelist):
     flaglist = [candidate]
    else:
     error = True
   elif type(candidate) == list:
    flaglist = []
    for item in candidate:
     if type(item) == str:
      if item.lower() in [x.lower() for x in typelist]:
       flaglist.append(typelist.index(item))
      else:
       error = True
     elif type(item) == int:
      if item < len(typelist):
       flaglist.append(item)
      else:
       error = True
     else:
      error = True
   else:
    error = True
   if error:
    print("Unknown data type")
   else:
    return flaglist

