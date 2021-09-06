# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Args

from watchdogs.io.models import FileArgs
from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class CharacterConverterArgs(FileArgs, Common):

  VERSION = "1.0"

  def __init__(self):
    super(CharacterConverterArgs, self).__init__()
    self.oldChar = EMPTY  #type: str
    self.newChar = EMPTY  #type: str
    self.incrementLine = False  #type: bool
    self.incrementWord = False  #type: bool
    self.upper = False  #type: bool
    self.lower = False  #type: bool

    self.parseArgs()
    self.setArguments()

  def parseArgs(self):  #type: (CharacterConverterArgs) -> None
    OC_HELP = "Specify the character that will be replaced."
    NC_HELP = "Specify the character that will replace the old character."
    IL_HELP = "Specify if you want to increment the replaced character by line."
    IW_HELP = "Specify if you want to increment the replaced character by word."
    U_HELP = "Specify if you want to upper case all the characters."
    L_HELP = "Specify if you want to lower case all the characters."
    V_HELP = "Show version"
    VERSION = "Character Converter version: {}".format(CharacterConverterArgs.VERSION)

    parser = self.parser
    parser.add_argument("-oc", "--old-char", help=OC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-nc", "--new-char", help=NC_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-il", "--increment-line", action="store_true", help=IL_HELP)
    parser.add_argument("-iw", "--increment-word", action="store_true", help=IW_HELP)
    parser.add_argument("-u", "--upper", action="store_true", help=U_HELP)
    parser.add_argument("-l", "--lower", action="store_true", help=L_HELP)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    self.parsedArgs = parser.parse_args()