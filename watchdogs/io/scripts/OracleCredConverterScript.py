# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Script

import traceback

from watchdogs.base.models import Common, AllArgs
from watchdogs.io.models.File import File
from watchdogs.io.parsers import OracleCredConverterArgs, FileArgs
from watchdogs.io.services.OracleCredConverterService import OracleCredConverterService


class OracleCredConverterScript(Common):

  def __init__(self, oracleCredConverterService=OracleCredConverterService()):
    #type: (OracleCredConverterService) -> None
    super(OracleCredConverterScript, self).__init__()
    self.__oracleCredConverterService = oracleCredConverterService

  def getOracleCredConverterService(self):
    #type: () -> OracleCredConverterService
    return self.__oracleCredConverterService

  def setOracleCredConverterService(self, __oracleCredConverterService):
    #type: (OracleCredConverterService) -> None
    self.__oracleCredConverterService = __oracleCredConverterService

  def run(self):  #type: (OracleCredConverterScript) -> None
    allArgs = AllArgs([OracleCredConverterArgs(), FileArgs()]).processAllArguments()
    oracleCredConverterArgs = allArgs.getArgs(OracleCredConverterArgs)
    oCredConverterService = OracleCredConverterService()
    file = File()
    try:
      oCredConverterService.readLines(allArgs, file)
      if allArgs.getArgs(FileArgs).outputFile:
        oCredConverterService.writeLines(allArgs, file)
      else:
        oCredConverterService.printLines(file)
    except ValueError as ve:
      print(ve)
      print(oracleCredConverterArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(oracleCredConverterArgs.getParser().print_usage())