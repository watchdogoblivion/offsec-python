# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter Script

import traceback

from watchdogs.base.models.Common import Common
from watchdogs.io.parsers import OracleCredConverterArgs
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
    oracleCredConverterArgs = OracleCredConverterArgs()
    oCredConverterService = OracleCredConverterService()
    try:
      oCredConverterService.readLines(oracleCredConverterArgs)
      if oracleCredConverterArgs.outputFile:
        oCredConverterService.writeLines(oracleCredConverterArgs.outputFile)
      else:
        oCredConverterService.printLines()
    except ValueError as ve:
      print(ve)
      print(oracleCredConverterArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(oracleCredConverterArgs.getParser().print_usage())