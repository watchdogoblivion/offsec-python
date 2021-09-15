# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Fuzzer Arguments

from watchdogs.base.models.Args import Args
from watchdogs.utils.Constants import (EMPTY, COLON)


class FuzzerArgs(Args):

  VERSION = "Fuzzer version: 1.0"

  def __init__(self, substitutesFile=EMPTY, substitutesDelimiter=COLON, showSubstitutes=False, poolSize=10,
               groupSize=1):
    #type: (str, str, bool, int, int) -> None
    super(FuzzerArgs, self).__init__()
    self.substitutesFile = substitutesFile
    self.substitutesDelimiter = substitutesDelimiter
    self.showSubstitutes = showSubstitutes
    self.poolSize = poolSize
    self.groupSize = groupSize

  def getVersion(self):  #type: () -> str
    return FuzzerArgs.VERSION

  def addArguments(self):  #type: () -> FuzzerArgs
    SF_HELP = ("Specify the file which contains the words that will be used as substitutions for the 'FUZZ'"
               " words.\nIf this is not specified, no fuzzing will occur.\nIMPORTANT: When enabling fuzzing"
               " ensure there is a blank line separating the headers and the body")
    SD_HELP = ("Specify the delimiter used to separate the words in the substitutes file."
               "\nThe default is a colon")
    SS_HELP = "Shows the fuzz substituted text used"
    PS_HELP = "Specify the multi processing pool size. The default size is 10"
    GS_HELP = ("Specify the size of the data groups, that are submitted into a single processing pool.\n"
               "The default group size is 1")

    parser = self.getParser()
    parser.add_argument("-sf", "--substitutes-file", help=SF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sd", "--substitutes-delimiter", help=SD_HELP, type=str, metavar=EMPTY,
                        default=COLON)
    parser.add_argument("-ss", "--show-substitutes", action="store_true", help=SS_HELP)
    parser.add_argument("-ps", "--pool-size", help=PS_HELP, type=int, metavar=EMPTY, default=10)
    parser.add_argument("-gs", "--group-size", help=GS_HELP, type=int, metavar=EMPTY, default=1)

    return self