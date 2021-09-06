# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Service

from watchdogs.base.models.Common import Common
from watchdogs.io.services.FileService import FileService
from watchdogs.io.parsers import OracleCredConverterArgs
from watchdogs.utils.Constants import (EMPTY, FS, LR)


class OracleCredConverterService(FileService, Common):

  def __init__(self):
    super(OracleCredConverterService, self).__init__()
    self.conversion = EMPTY  #type: str

  def readLines(self, oracleCredConverterArgs):
    #type: (OracleCredConverterService, OracleCredConverterArgs) -> None
    openedFile = open(oracleCredConverterArgs.inputFile, LR)
    fileLines = openedFile.readlines()
    delimiter = FS
    conversion = oracleCredConverterArgs.conversion
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
    self.file.lines = linesRead