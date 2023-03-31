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

  self.job_names = [
   "Dark Knight",
   "Dragoon",
   "Caller",
   "Sage",
   "Bard",
   "White Wizard",
   "Karate",
   "Black Mage",
   "White Mage",
   "Paladin",
   "Chief",
   "Summoner",
   "Ninja",
   "Lunar",
   "Brother",
   "Fiancee"
  ]

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
  
 def index_list(self, candidate, datatype):
  error = False
  datatype = datatype.lower()
  if datatype in ["stat", "stats"]:
   pass
  elif datatype in ["race", "races"]:
   pass
  elif datatype in ["element", "elements"]:
   pass
  elif datatype in ["persistent", "persistent status", "persistent statuses"]:
   pass
  elif datatype in ["temporary", "temoporary status", "temporary statuses"]:
   pass
  elif datatype in ["attribute", "attributes"]:
   pass
  elif datatype in ["hidden", "hidden status", "hidden statuses"]:
   pass
  elif datatype in ["system", "system status", "system statuses"]:
   pass
  elif datatype in ["job", "jobs"]:
   pass
  elif datatype in ["slot", "slots", "equip slot", "equip slots"]:
   pass
  elif datatype in ["target", "targets", "target type", "target types"]:
   pass
  elif datatype in ["effect", "effects", "spell effect", "spell effects"]:
   pass
  elif datatype in ["drop rate", "drop rates", "item drop rate", "item drop rates"]:
   pass
  else:
   print("Unknown data type")
   error = True
  if not error:
   