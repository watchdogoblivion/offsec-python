# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Args

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class CharacterConverterArgs(FileArgs, Common):

  VERSION = "1.0"

  def __init__(self, oldChar=EMPTY, newChar=EMPTY, incrementLine=False, incrementWord=False, upper=False,
               lower=False):
    #type: (str, str, bool, bool, bool, bool) -> None
    super(CharacterConverterArgs, self).__init__()
    self.oldChar = oldChar
    self.newChar = newChar
    self.incrementLine = incrementLine
    self.incrementWord = incrementWord
    self.upper = upper
    self.lower = lower

    self.parseArgs()
    self.setArguments()

  def getOldChar(self):  #type: () -> str
    return self.oldChar

  def setOldChar(self, oldChar):  #type: (str) -> None
    self.oldChar = oldChar

  def getNewChar(self):  #type: () -> str
    return self.newChar

  def setNewChar(self, newChar):  #type: (str) -> None
    self.newChar = newChar

  def isIncrementLine(self):  #type: () -> bool
    return self.incrementLine

  def setIncrementLine(self, incrementLine):  #type: (bool) -> None
    self.incrementLine = incrementLine

  def isIncrementWord(self):  #type: () -> bool
    return self.incrementWord

  def setIncrementWord(self, incrementWord):  #type: (bool) -> None
    self.incrementWord = incrementWord

  def isUpper(self):  #type: () -> bool
    return self.upper

  def setUpper(self, upper):  #type: (bool) -> None
    self.upper = upper

  def isLower(self):  #type: () -> bool
    return self.lower

  def setLower(self, lower):  #type: (bool) -> None
    self.lower = lower

  def parseArgs(self):  #type: () -> None
    OC_HELP = "Specify the character that will be replaced."
    NC_HELP = "Specify the character that will replace the old character."
    IL_HELP = "Specify if you want to increment the replaced character by line."
    IW_HELP = "Specify if you want to increment the replaced character by word."
    U_HELP = "Specify if you want to upper case all the characters."
    L_HELP = "Specify if you want to lower case all the characters."
    V_HELP = "Show version"
    VERSION = "Character Converter version: {}".format(CharacterConverterArgs.VERSION)

    parser = self.getParser()
    parser.add_argument("-oc", "--old-char", help=OC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-nc", "--new-char", help=NC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-il", "--increment-line", action="store_true", help=IL_HELP)
    parser.add_argument("-iw", "--increment-word", action="store_true", help=IW_HELP)
    parser.add_argument("-u", "--upper", action="store_true", help=U_HELP)
    parser.add_argument("-l", "--lower", action="store_true", help=L_HELP)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    self.setParsedArgs(parser.parse_args())