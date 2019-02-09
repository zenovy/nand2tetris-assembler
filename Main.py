from Parser import Parser
from SymbolTable import SymbolTable
from Code import Code

import sys
import math

def divTill(num, width):
  bin = []
  while (num > 0):
    bin += str(num % 2)
    num = math.floor(num / 2)
  bin.reverse()
  binstr = ''.join(bin)
  diff = width - len(bin)
  for _ in range(diff):
    binstr = '0' + binstr
  return binstr

lc = 0
new_address_counter = 16
compiled_lines = []

filename = sys.argv[1]

# First Pass
p = Parser(filename)
st = SymbolTable()
while p.hasMoreCommands():
  if p.commandType() == "L_COMMAND":
    symbol = p.symbol()
    if not st.contains(symbol):
      st.addEntry(symbol, lc)
  else:
    lc += 1
  p.advance()

# Second Pass
p = Parser(filename)
while (p.hasMoreCommands()):
  print("\nInput: '{0}'".format(p.current_line))
  print("CommandType: {0}".format(p.commandType()))
  if p.commandType() == "C_COMMAND":
    dest = p.dest()
    comp = p.comp()
    jump = p.jump()
    instruction = "111{0}{1}{2}".format(Code.comp(comp), Code.dest(dest), Code.jump(jump))
    print(instruction)
    compiled_lines.append(instruction)
  else:
    symbol = p.symbol()
    # print("Symbol: {0}".format(symbol))
    if p.commandType() == "A_COMMAND":
      address = ""
      if symbol.isdigit():
        address = symbol
      elif st.contains(symbol):
        address = st.getAddress(symbol)
      else:
        st.addEntry(symbol, new_address_counter)
        address = new_address_counter
        new_address_counter += 1
      bin_address = divTill(int(address), 15)
      instruction = "0{0}".format(bin_address)
      print(instruction)
      compiled_lines.append(instruction)
  p.advance()

new_file = filename.rstrip('asm').rstrip('.') + '.hack'
with open(new_file, 'w') as file:
  file.write('\n'.join(compiled_lines))
