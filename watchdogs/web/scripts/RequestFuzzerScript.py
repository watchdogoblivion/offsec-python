# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Fuzzer Script

import traceback

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import Common, AllArgs
from watchdogs.web.models import RequestFuzzer
from watchdogs.web.parsers import RequestArgs, FuzzerArgs
from watchdogs.web.services import RequestParserService, RequestResponseFuzzerService


class RequestFuzzerScript(Common):

  def __init__(self, requestParserService=RequestParserService(),
               requestResponseFuzzerService=RequestResponseFuzzerService()):
    #type: (RequestParserService, RequestResponseFuzzerService) -> None
    super(RequestFuzzerScript, self).__init__()
    self.__requestParserService = requestParserService
    self.__requestResponseFuzzerService = requestResponseFuzzerService

  def getRequestParserService(self):  #type: () -> RequestParserService
    return self.__requestParserService

  def setRequestParserService(self, requestParserService):  #type: (RequestParserService) -> None
    self.__requestParserService = requestParserService

  def getRequestResponseFuzzerService(self):  #type: () -> RequestResponseFuzzerService
    return self.__requestResponseFuzzerService

  def setRequestResponseFuzzerService(
      self, requestResponseFuzzerService):  #type: (RequestResponseFuzzerService) -> None
    self.__requestResponseFuzzerService = requestResponseFuzzerService

  def run(self):  #type: () -> None
    allArgs = AllArgs([FuzzerArgs(), RequestArgs(), FileArgs()]).mergeAndProcess()
    fuzzerArgs = allArgs.getArgs(FuzzerArgs)
    try:
      request = self.__requestParserService.parseFile(allArgs)
      self.__requestResponseFuzzerService.processRequest(allArgs, RequestFuzzer(request=request))
    except ValueError as ve:
      print(ve)
      print(fuzzerArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fuzzerArgs.getParser().print_usage())