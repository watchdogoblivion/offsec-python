# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter

import argparse

from watchdogs.io import File
from watchdogs.utils.Constants import (EMPTY, LR, SPACE)


class CharacterConverter(File):

  VERSION = "1.0"

  def __init__(self):
    super(CharacterConverter, self).__init__()
    self.oldChar = EMPTY  #type: str
    self.newChar = EMPTY  #type: str
    self.incrementLine = False  #type: bool
    self.incrementWord = False  #type: bool
    self.upper = False  #type: bool
    self.lower = False  #type: bool

  def parseArgs(self):  #type: (CharacterConverter) -> None
    IF_HELP = "Specify the input file to read from."
    OF_HELP = "Specify the output file to write to."
    OC_HELP = "Specify the character that will be replaced."
    NC_HELP = "Specify the character that will replace the old character."
    IL_HELP = "Specify if you want to increment the replaced character by line."
    IW_HELP = "Specify if you want to increment the replaced character by word."
    U_HELP = "Specify if you want to upper case all the characters."
    L_HELP = "Specify if you want to lower case all the characters."
    V_HELP = "Show version"
    H_HELP = "Show this help message"
    VERSION = "Character Converter version: {}".format(CharacterConverter.VERSION)

    self.parser = argparse.ArgumentParser(add_help=False)
    parser = self.parser
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-oc", "--old-char", help=OC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-nc", "--new-char", help=NC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-il", "--increment-line", action="store_true", help=IL_HELP)
    parser.add_argument("-iw", "--increment-word", action="store_true", help=IW_HELP)
    parser.add_argument("-u", "--upper", action="store_true", help=U_HELP)
    parser.add_argument("-l", "--lower", action="store_true", help=L_HELP)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    parser.add_argument("-h", "--help", action="help", help=H_HELP)
    self.parsedArgs = parser.parse_args()

  def readLines(self):  #type: (CharacterConverter) -> None
    openedFile = open(self.inputFile, LR)
    fileLines = openedFile.readlines()
    increment = 1
    linesRead = []
    oldChar = self.oldChar
    newChar = self.newChar
    incrementWord = self.incrementWord

    for line in fileLines:
      if (self.incrementLine and newChar):
        if (line.find(oldChar) > -1):
          line = line.replace(oldChar, "{}{}".format(str(increment), newChar))
          increment += 1
      elif (incrementWord and newChar):
        line = self.swapAndIncrementWord(line, increment)
      else:
        line = line.replace(oldChar, newChar)

      if (self.upper):
        line = line.upper()
      elif (self.lower):
        line = line.lower()

      linesRead.append(line)
    self.lines = linesRead

  def swapAndIncrementWord(self, line, increment):  #type: (CharacterConverter, str, int) -> None
    oldChar = self.oldChar
    newChar = self.newChar
    words = line.split(SPACE)
    wordsLength = len(words)
    for wordIndex in range(wordsLength):
      word = words[wordIndex]
      if (word.find(oldChar) > -1):
        words[wordIndex] = word.replace(oldChar, "{}{}".format(str(increment), newChar))
        increment += 1
    line = SPACE.join(words)
    return line
