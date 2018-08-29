import re

from Code import Code
from SymbolTable import SymbolTable

class Parser:
  l_regex = re.compile('\((.*)\)') 
  a_regex = re.compile('@(\w*)')

  def __init__(self, filepath):
    self.file = open(filepath, 'r')
    self.advance()

  def hasMoreCommands(self):
    pos = self.file.tell()
    nextLine = self.file.readline()
    self.file.seek(pos)
    return not (nextLine == '')

  def advance(self):
    nextLineRaw = self.file.readline()
    comment_index = nextLineRaw.find('//')
    if (comment_index != -1):
      nextLineRaw = nextLineRaw[0:comment_index]
    nextLine = nextLineRaw.strip()
    if nextLine == "":
      self.advance()
    else:
      self.current_line = nextLine

  def commandType(self):
    if (self.a_regex.match(self.current_line)):
      return 'A_COMMAND'
    elif (self.l_regex.match(self.current_line)):
      return 'L_COMMAND'
    else:
      return 'C_COMMAND'

  def symbol(self):
    command_type = self.commandType();
    if (command_type == 'A_COMMAND'):
      a_match = Parser.a_regex.match(self.current_line)
      if (a_match):
        return a_match.group(1)
    elif (command_type == 'L_COMMAND'):
      l_match = Parser.l_regex.match(self.current_line)
      if (l_match):
        return l_match.group(1)
    else:
      return None

  def dest(self):
    if (self.commandType() != 'C_COMMAND'):
      return None
    splitEq = self.current_line.split('=')
    if (len(splitEq) > 1):
      return splitEq[0]
    else:
      return None

  def comp(self):
    if (self.commandType() != 'C_COMMAND'):
      return None
    splitEq = self.current_line.split('=')
    splitSc = splitEq[-1].split(';')
    return splitSc[0]

  def jump(self):
    if (self.commandType() != 'C_COMMAND'):
      return None
    splitEq = self.current_line.split('=')
    splitSc = splitEq[-1].split(';')
    if (len(splitSc) > 1):
      return splitSc[1]
    else:
      return None
