class EventCondition:

 def __init__(self, flag = 0, setting = False):
  self.flag = flag 
  self.setting = setting

class Component:

 def __init__(self):
  self.conditions = []
  self.event = 0

class Launcher:

 def __init__(self):
  self.components = []
 
 def read(self, rom, start, finish):
  pass
