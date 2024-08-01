from event import Event

def read_events(rom, config):
 oldaddress = None
 events = []
 for index in range(rom.TOTAL_EVENTS):
  event = Event()
  events.append(event)
  pointer = rom.EVENT_POINTERS_START + index * 2
  address = rom.read_wide(pointer) + rom.EVENT_POINTER_BONUS
  if address != oldaddress:
   event.read(rom, config, address)
   oldaddress = address
 return events