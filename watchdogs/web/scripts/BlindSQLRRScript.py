# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Request Response Script

import traceback

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import Common, AllArgs
from watchdogs.web.views import BlindSQLRRView
from watchdogs.web.models import BlindSQLRRHelper
from watchdogs.web.parsers import BlindSQLArgs, RequestArgs
from watchdogs.web.services import BlindSQLRRService, RequestParserService


class BlindSQLRRScript(Common):

  def __init__(self, requestParserService=RequestParserService(), blindSQLRRService=BlindSQLRRService()):
    #type: (RequestParserService, BlindSQLRRService) -> None
    super(BlindSQLRRScript, self).__init__()
    self.__requestParserService = requestParserService
    self.__blindSQLRRService = blindSQLRRService

  def getRequestParserService(self):  #type: () -> RequestParserService
    return self.__requestParserService

  def setRequestParserService(self, requestParserService):  #type: (RequestParserService) -> None
    self.__requestParserService = requestParserService

  def getBlindSQLRRService(self):  #type: () -> BlindSQLRRService
    return self.__blindSQLRRService

  def setBlindSQLRRService(self, blindSQLRRService):  #type: (BlindSQLRRService) -> None
    self.__blindSQLRRService = blindSQLRRService

  def run(self):  #type: () -> None
    allArgs = AllArgs([BlindSQLArgs(), RequestArgs(), FileArgs()]).mergeAndProcess()
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    try:
      request = RequestParserService().parseFile(allArgs)
      blindSQLRRService = BlindSQLRRService()
      originalEndpoint = request.getRequestInfo().getEndpoint()
      invalidResponseLength = blindSQLRRService.getInvalidResponseLength(allArgs, request)
      helper = BlindSQLRRHelper(originalEndpoint, invalidResponseLength)
      BlindSQLRRView().start(allArgs, request, blindSQLRRService, helper)
    except ValueError:
      print(traceback.format_exc())
      print(blindSQLArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(blindSQLArgs.getParser().print_usage())
