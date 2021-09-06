# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Args

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models.Common import Common
from watchdogs.utils.Constants import (EMPTY, LFN)


class OracleCredConverterArgs(FileArgs, Common):

  VERSION = "1.0"

  UU = "uu"
  UL = "ul"
  LU = "lu"
  LL = "ll"

  def __init__(self):
    super(OracleCredConverterArgs, self).__init__()
    self.conversion = EMPTY  #type: str

    self.parseArgs()
    self.setArguments()

  def getConversions(self):  #type: (OracleCredConverterArgs) -> str
    uppered = "uppered"
    lowered = "lowered"
    base = "  {}   : First word {} and second word {}{}"
    conversions = "Conversion types:{}".format(LFN)

    conversions += base.format(OracleCredConverterArgs.UU, uppered, uppered, LFN)
    conversions += base.format(OracleCredConverterArgs.UL, uppered, lowered, LFN)
    conversions += base.format(OracleCredConverterArgs.LU, lowered, uppered, LFN)
    conversions += base.format(OracleCredConverterArgs.LL, lowered, lowered, LFN)
    return conversions

  def parseArgs(self):  #type: (OracleCredConverterArgs) -> None
    C_HELP = "Specify the conversion type."
    LC_HELP = "Conversion types."
    V_HELP = "Show version"
    CONVERSIONS = self.getConversions()
    VERSION = " Oracle Credentials Converter version: {}".format(OracleCredConverterArgs.VERSION)

    parser = self.parser
    parser.add_argument("-c", "--conversion", help=C_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-lc", "--list-conversions", action="version", help=LC_HELP, version=CONVERSIONS)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    self.parsedArgs = parser.parse_args()