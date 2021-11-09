# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQL Request Response Script

import traceback

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import Common, AllArgs
from watchdogs.web.views import ErrorSQLIRRView
from watchdogs.web.models import ErrorSQLIRRHelper
from watchdogs.web.parsers import ErrorSQLIArgs, RequestArgs
from watchdogs.web.services import ErrorSQLIRRService, RequestParserService

class ErrorSQLIRRScript(Common):

  def __init__(self, requestParserService=RequestParserService(), errorSQLIRRService=ErrorSQLIRRService()):
    #type: (RequestParserService, ErrorSQLIRRService) -> None
    super(ErrorSQLIRRScript, self).__init__()
    self.__requestParserService = requestParserService
    self.__errorSQLIRRService = errorSQLIRRService

  def getRequestParserService(self):  #type: () -> RequestParserService
    return self.__requestParserService

  def setRequestParserService(self, requestParserService):  #type: (RequestParserService) -> None
    self.__requestParserService = requestParserService

  def geterrorSQLIRRService(self):  #type: () -> ErrorSQLIRRService
    return self.__errorSQLIRRService

  def seterrorSQLIRRService(self, errorSQLIRRService):  #type: (ErrorSQLIRRService) -> None
    self.__errorSQLIRRService = errorSQLIRRService

  def run(self):  # pylint: disable=no-self-use
    #type: () -> None
    allArgs = AllArgs([ErrorSQLIArgs(), RequestArgs(), FileArgs()]).mergeAndProcess()
    errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
    try:
      request = RequestParserService().parseFile(allArgs)
      errorSQLIRRService = ErrorSQLIRRService()
      originalRequestBodyString = request.getRequestBodyString()
      invalidResponseLength = errorSQLIRRService.getInvalidResponseLength(allArgs, request)
      helper = ErrorSQLIRRHelper(originalRequestBodyString, invalidResponseLength)
      ErrorSQLIRRView().start(allArgs, request, errorSQLIRRService, helper)
    except ValueError:
      print(traceback.format_exc())
      print(errorSQLIArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(errorSQLIArgs.getParser().print_usage())
