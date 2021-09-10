# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Service

from watchdogs.io.parsers.FileArgs import FileArgs
from watchdogs.base.models import Common, AllArgs
from watchdogs.io.services.FileService import FileService
from watchdogs.io.parsers import OracleCredConverterArgs
from watchdogs.utils.Constants import (EMPTY, FS, LR)


class OracleCredConverterService(FileService, Common):

  def __init__(self):  #type: () -> None
    super(OracleCredConverterService, self).__init__()

  def readLines(self, allArgs):  #type: (AllArgs) -> None
    oracleCredConverterArgs = allArgs.getArgs(OracleCredConverterArgs)
    openedFile = open(allArgs.getArgs(FileArgs).getInputFile(), LR)
    fileLines = openedFile.readlines()
    delimiter = FS
    conversion = oracleCredConverterArgs.getConversion()
    linesRead = []

    for fileLine in fileLines:
      line = EMPTY
      fileLineWords = fileLine.split(delimiter)
      if (conversion == OracleCredConverterArgs.UU):
        line = "{}{}{}".format(fileLineWords[0].upper(), delimiter, fileLineWords[1].upper())
      if (conversion == OracleCredConverterArgs.UL):
        line = "{}{}{}".format(fileLineWords[0].upper(), delimiter, fileLineWords[1].lower())
      if (conversion == OracleCredConverterArgs.LU):
        line = "{}{}{}".format(fileLineWords[0].lower(), delimiter, fileLineWords[1].upper())
      if (conversion == OracleCredConverterArgs.LL):
        line = "{}{}{}".format(fileLineWords[0].lower(), delimiter, fileLineWords[1].lower())

      linesRead.append(line)
    self.getFile().setLines(linesRead)