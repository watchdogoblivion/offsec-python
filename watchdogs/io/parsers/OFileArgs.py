# author: WatchDogOblivion
# description: TODO
# WatchDogs Optional FileArgs

from watchdogs.io.parsers.FileArgs import FileArgs
from watchdogs.utils.Constants import (EMPTY)


class OFileArgs(FileArgs):

  def addArguments(self):  #type: () -> FileArgs
    IF_HELP = "Specify the input file to read from."
    OF_HELP = "Specify the output file to write to."

    parser = self.getParser()

    optional = parser.add_argument_group("Optional file arguments")
    optional.add_argument("-if", "--input-file", help=IF_HELP, type=str, metavar=EMPTY)
    optional.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)

    return self
