# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer Controller

import traceback

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import Common, AllArgs
from watchdogs.web.parsers import FileFuzzerArgs
from watchdogs.web.services.FileFuzzerService import FileFuzzerService


class FileFuzzerScript(Common):

  def __init__(self, fileFuzzerService=FileFuzzerService()):  #type: (FileFuzzerService) -> None
    super(FileFuzzerScript, self).__init__()
    self.__fileFuzzerService = fileFuzzerService

  def getFileFuzzerService(self):  #type: () -> FileFuzzerService
    return self.__fileFuzzerService

  def setFileFuzzerService(self, fileFuzzerService):  #type: (FileFuzzerService) -> None
    self.__fileFuzzerService = fileFuzzerService

  def run(self):  #type: () -> None
    allArgs = AllArgs([FileFuzzerArgs(), FileArgs()]).mergeAndProcess()
    fFuzzerArgs = allArgs.getArgs(FileFuzzerArgs)
    fFuzzerService = self.__fileFuzzerService
    try:
      fFuzzerService.parseFile(allArgs)
      fFuzzerService.processRequest(allArgs)
    except ValueError as ve:
      print(ve)
      print(fFuzzerArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fFuzzerArgs.getParser().print_usage())
