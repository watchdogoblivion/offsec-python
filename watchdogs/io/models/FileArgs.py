# author: WatchDogOblivion
# description: TODO
# WatchDogs FileArgs

from watchdogs.base.models.Args import Args
from watchdogs.utils.Constants import (EMPTY)


class FileArgs(Args):

  def __init__(self):
    super(FileArgs, self).__init__()
    self.inputFile = EMPTY  #type: str
    self.outputFile = EMPTY  #type: str
    self.lines = []  #type: list[str]

    self.fileArgs()

  def fileArgs(self):  #type: (FileArgs) -> None
    IF_HELP = "Specify the input file to read from."
    OF_HELP = "Specify the output file to write to."

    parser = self.parser
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)