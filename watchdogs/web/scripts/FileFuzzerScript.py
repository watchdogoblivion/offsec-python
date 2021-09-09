# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer Controller

import traceback

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY, COLON)
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
    fFuzzerArgs = FileFuzzerArgs()
    fFuzzerService = self.__fileFuzzerService
    try:
      fFuzzerService.parseFile(fFuzzerArgs)
      fFuzzerService.processRequest(fFuzzerArgs)
    except ValueError as ve:
      print(ve)
      print(fFuzzerArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fFuzzerArgs.getParser().print_usage())
