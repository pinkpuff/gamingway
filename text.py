class TextInterface:

 def __init__(self):
  self.ff4totext = {}
  for i in range(0x100):
   self.ff4totext[chr(i)] = "[{}]".format(self.hex(i))
  for i in range(0x42, 0x5C):
   self.ff4totext[chr(i)] = chr(i - 1)
  for i in range(0x5C, 0x76):
   self.ff4totext[chr(i)] = chr(i + 0x61 - 0x5C)
  self.ff4totext[chr(0x15)] = "#"
  self.ff4totext[chr(0x29)] = "[CLW]"
  self.ff4totext[chr(0x2A)] = "[ROD]"
  self.ff4totext[chr(0x2B)] = "[STF]"
  self.ff4totext[chr(0x2C)] = "[FEL]"
  self.ff4totext[chr(0x2D)] = "[SWD]"
  self.ff4totext[chr(0x2E)] = "[KNS]"
  self.ff4totext[chr(0x2F)] = "[SPR]"
  self.ff4totext[chr(0x30)] = "[DAG]"
  self.ff4totext[chr(0x31)] = "[KAT]"
  self.ff4totext[chr(0x32)] = "[SHU]"
  self.ff4totext[chr(0x33)] = "[BMR]"
  self.ff4totext[chr(0x34)] = "[AXE]"
  self.ff4totext[chr(0x35)] = "[WRN]"
  self.ff4totext[chr(0x36)] = "[HRP]"
  self.ff4totext[chr(0x37)] = "[BOW]"
  self.ff4totext[chr(0x38)] = "[ARO]"
  self.ff4totext[chr(0x39)] = "[HMR]"
  self.ff4totext[chr(0x3A)] = "[WHP]"
  self.ff4totext[chr(0x3B)] = "[SHL]"
  self.ff4totext[chr(0x3C)] = "[HAT]"
  self.ff4totext[chr(0x3D)] = "[ARM]"
  self.ff4totext[chr(0x3E)] = "[GLV]"
  self.ff4totext[chr(0x3F)] = "[BLK]"
  self.ff4totext[chr(0x40)] = "[WHT]"
  self.ff4totext[chr(0x41)] = "[SUM]"
  self.ff4totext[chr(0x79)] = "[TNT]"
  self.ff4totext[chr(0x7A)] = "[BTL]"
  self.ff4totext[chr(0x7B)] = "[ROB]"
  self.ff4totext[chr(0x7C)] = "[RNG]"
  self.ff4totext[chr(0x7D)] = "[CRY]"
  self.ff4totext[chr(0x7E)] = "[KEY]"
  self.ff4totext[chr(0x7F)] = "[TAL]"
  self.ff4totext[chr(0x80)] = "0"
  self.ff4totext[chr(0x81)] = "1"
  self.ff4totext[chr(0x82)] = "2"
  self.ff4totext[chr(0x83)] = "3"
  self.ff4totext[chr(0x84)] = "4"
  self.ff4totext[chr(0x85)] = "5"
  self.ff4totext[chr(0x86)] = "6"
  self.ff4totext[chr(0x87)] = "7"
  self.ff4totext[chr(0x88)] = "8"
  self.ff4totext[chr(0x89)] = "9"
  self.ff4totext[chr(0xC0)] = "'"
  self.ff4totext[chr(0xC1)] = "."
  self.ff4totext[chr(0xC2)] = "-"
  self.ff4totext[chr(0xC3)] = "_"
  self.ff4totext[chr(0xC4)] = "!"
  self.ff4totext[chr(0xC5)] = "?"
  self.ff4totext[chr(0xC6)] = "%"
  self.ff4totext[chr(0xC7)] = "/"
  self.ff4totext[chr(0xC8)] = ":"
  self.ff4totext[chr(0xC9)] = ","
  self.ff4totext[chr(0xFF)] = " "
  self.texttoff4 = {value: key for key, value in self.ff4totext.items()}

 def hex(self, number):
  return "{:02x}".format(number).upper()

 def asciitext(self, ff4string):
  # Takes a string of text in FF4 encoding and converts it to ASCII.
  result = ""
  for letter in ff4string:
   result += self.ff4totext[letter]
  return result

 def ff4text(self, asciistring):
   # Takes a string of ASCII text and converts it to FF4 encoding.
   result = ""
   codemode = False
   code = ""
   for letter in asciistring:
    # When converting ASCII text, we need to consider things between [] as a single symbol.
    if codemode:
     code += letter
     if letter == "]":
      codemode = False
      result += self.texttoff4[code]
    elif letter == "[":
     code = "["
     codemode = True
    else:
     result += self.texttoff4[letter]
   return result

 def from_bytes(self, bytelist):
  result = ""
  for byte in bytelist:
   result += chr(byte)
  return result

 def to_bytes(self, ff4string):
  result = []
  for letter in ff4string:
   result.append(ord(letter))
  return result

 def assign_symbol(self, code, symbol):
  # Assigns a new ascii symbol to a given hex code.
  # This is useful for displaying text in roms whose text encoding has
  # been altered.
  # 
  # Note that this will not automatically go through all the text in
  # any abstract game objects that have already been created and
  # replace the symbol. It is best to call this function BEFORE calling
  # read if you want the already read text to reflect the change.
  self.ff4totext.update({chr(code): symbol})
  self.texttoff4.update({symbol: chr(code)})
 
