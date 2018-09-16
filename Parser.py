import re

from Code import Code
from SymbolTable import SymbolTable

def stripComment(line):
  comment_index = line.find('//')
  if (comment_index != -1):
    return line[0:comment_index]
  else:
    return line

class Parser:
  l_regex = re.compile('\((.*)\)') 
  a_regex = re.compile('@(\w*)')

  def __init__(self, filepath):
    self.file = open(filepath, 'r')
    self.is_last_command = False
    self.advance()

  def hasMoreCommands(self):
    if self.is_last_command:
      return False
    pos = self.file.tell()
    nextLine = self.file.readline()
    self.file.seek(pos)
    if nextLine == '':
      self.is_last_command = True
    return True

  def advance(self):
    # Read line
    nextLineRaw = self.file.readline()
    if nextLineRaw == '':
      self.current_line == ''
      return

    # Strip characters after //, then strip whitespace
    self.current_line = stripComment(nextLineRaw).strip()

    if self.current_line == '':
      self.advance()

  def commandType(self):
    print(self.current_line)
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
