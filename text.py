class TextInterface:

 def __init__(self):
  
  # This array converts symbols in the FF4 text encoding into ASCII.
  self.ff4totext = {}
  
  # We start by populating the array with the hex representation of each symbol.
  for i in range(0x100):
   self.ff4totext[chr(i)] = "[{}]".format(self.hex(i))
  
  # Then we replace the capital letters with their ASCII equivalents.
  for i in range(0x42, 0x5C):
   self.ff4totext[chr(i)] = chr(i - 1)
  
  # And likewise the lowercase letters.
  for i in range(0x5C, 0x76):
   self.ff4totext[chr(i)] = chr(i + 0x61 - 0x5C)
  
  # Then we take care of some individual symbols. Punctuation is straightforward
  # enough, but some symbols are unique to FF4 and do not have ASCII equivalents.
  # For these, we use three letters enclosed in square brackets to reperesent a
  # single symbol. This improves readability without bloating the length too much.
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
  
  # Then we use that array to create the inverse array, which converts ASCII text
  # back into FF4 encoded text.
  self.texttoff4 = {value: key for key, value in self.ff4totext.items()}

 # This returns a string representation of a hex value, including one leading 0 for
 # single-digit values.
 def hex(self, number):
  return "{:02x}".format(number).upper()

 # This takes a string of text in FF4 encoding and converts it to ASCII.
 def asciitext(self, ff4string):
  result = ""
  
  # Since FF4 encoding uses one byte per symbol, we can simply use the array to
  # construct the string byte by byte.
  for letter in ff4string:
   result += self.ff4totext[letter]
  
  # And finally return it.
  return result

 # This takes a string of ASCII text and converts it to FF4 encoding.
 def ff4text(self, asciistring):
  result = ""
  codemode = False
  code = ""

  # When converting ASCII text, we need to consider things between [] as a single
  # symbol. Thus, if we read a "[", we change to a special "code-reading mode"
  # until we read a "]". Then the code is looked up and the proper symbol added to
  # the resulting string and we return back to "letter-reading mode".
  for letter in asciistring:
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

 # Assigns a new ascii symbol to a given hex code.
 # This is useful for displaying text in roms whose text encoding has been altered.
 # Note that this will not automatically go through all the text in all the
 # abstract game objects that have already been created and replace the symbol. It
 # is best to call this function BEFORE calling read if you want the already read
 # text to reflect the change.
 def assign_symbol(self, code, symbol):
  self.ff4totext.update({chr(code): symbol})
  self.texttoff4.update({symbol: chr(code)})
 
