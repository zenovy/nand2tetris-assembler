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
st = SymbolTable()
while (p.hasMoreCommands()):
  # print("Input: '{0}'".format(p.current_line))
  # print("CommandType: {0}".format(p.commandType()))
  if p.commandType() == "C_COMMAND":
    dest = p.dest()
    comp = p.comp()
    jump = p.jump()
    print("111{0}{1}{2}".format(Code.comp(comp), Code.dest(dest), Code.jump(jump)))
  else :
    symbol = p.symbol()
    # print("Symbol: {0}".format(symbol))
    if p.commandType() == "A_COMMAND":
      if st.contains(symbol):
        address = st.getAddress(symbol)
        bin_address = divTill(int(address), 15)
        print("0{0}".format(bin_address))
      else:
        if symbol.isdigit():
          bin_address = divTill(int(symbol), 15)
          print("0{0}".format(bin_address))
        else:
          st.addEntry(symbol, new_address_counter)
          bin_address = divTill(int(new_address_counter), 15)
          new_address_counter += 1
          print("0{0}".format(bin_address))
  p.advance()

