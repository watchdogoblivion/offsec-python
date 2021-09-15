# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Args

from watchdogs.base.models.Args import Args
from watchdogs.utils.Constants import (EMPTY, LFN)


class OracleCredConverterArgs(Args):

  VERSION = "Oracle Credentials Converter version: 1.0"

  UU = "uu"
  UL = "ul"
  LU = "lu"
  LL = "ll"

  def __init__(self, conversion=EMPTY):  #type: (str) -> None
    super(OracleCredConverterArgs, self).__init__()
    self.conversion = conversion

  def getConversion(self):  #type: () -> str
    return self.conversion

  def setConversion(self, conversion):  #type: (str) -> None
    self.conversion = conversion

  def getConversions(self):  #type: () -> str
    uppered = "uppered"
    lowered = "lowered"
    base = "  {}   : First word {} and second word {}{}"
    conversions = "Conversion types:{}".format(LFN)

    conversions += base.format(OracleCredConverterArgs.UU, uppered, uppered, LFN)
    conversions += base.format(OracleCredConverterArgs.UL, uppered, lowered, LFN)
    conversions += base.format(OracleCredConverterArgs.LU, lowered, uppered, LFN)
    conversions += base.format(OracleCredConverterArgs.LL, lowered, lowered, LFN)
    return conversions

  def getVersion(self):  #type: () -> str
    return OracleCredConverterArgs.VERSION

  def addArguments(self):  #type: () -> OracleCredConverterArgs
    C_HELP = "Specify the conversion type."
    LC_HELP = "Conversion types."
    CONVERSIONS = self.getConversions()

    parser = self.getParser()
    parser.add_argument("-c", "--conversion", help=C_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-lc", "--list-conversions", action="version", help=LC_HELP, version=CONVERSIONS)

    return self