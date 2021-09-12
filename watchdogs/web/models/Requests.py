# author: WatchDogOblivion
# description: TODO
# WatchDogs Request

import copy
from collections import OrderedDict

from watchdogs.utils.Constants import EMPTY
from watchdogs.base.models import Common


class RequestInfo(Common):

  def __init__(self, urlHost=EMPTY, method=EMPTY, endpoint=EMPTY):  #type: (str, str, str) -> None
    super(RequestInfo, self).__init__()
    self.__urlHost = urlHost
    self.__method = method
    self.__endpoint = endpoint

  def getUrlHost(self):  #type: () -> str
    return self.__urlHost

  def setUrlHost(self, urlHost):  #type: (str) -> None
    self.__urlHost = urlHost

  def getMethod(self):  #type: () -> str
    return self.__method

  def setMethod(self, method):  #type: (str) -> None
    self.__method = method

  def getEndpoint(self):  #type: () -> str
    return self.__endpoint

  def setEndpoint(self, endpoint):  #type: (str) -> None
    self.__endpoint = endpoint


class Request(Common):

  def __init__(self, rawInfo=EMPTY, rawHeaders=EMPTY, rawBody=EMPTY, requestInfo=None, requestUrl=EMPTY,
               requestHeaders=None, requestBoundary=EMPTY, requestBodyDict=None, requestBodyString=None):
    #type: (str, str, str, RequestInfo, str, OrderedDict, str, OrderedDict, str) -> None
    super(Request, self).__init__()
    self.__rawInfo = rawInfo
    self.__rawHeaders = rawHeaders
    self.__rawBody = rawBody
    self.__requestInfo = requestInfo
    self.__requestUrl = requestUrl
    self.__requestHeaders = requestHeaders
    self.__requestBoundary = requestBoundary
    self.__requestBodyDict = requestBodyDict
    self.__requestBodyString = requestBodyString
    self.__originalRequestInfo = requestInfo
    self.__originalRequestHeaders = requestHeaders
    self.__originalRequestBodyDict = requestBodyDict
    self.__originalRequestBodyString = requestBodyString

  def getRawInfo(self):  #type: () -> str
    return self.__rawInfo

  def setRawInfo(self, rawInfo):  #type: (str) -> None
    self.__rawInfo = rawInfo

  def getRawHeaders(self):  #type: () -> str
    return self.__rawHeaders

  def setRawHeaders(self, rawHeaders):  #type: (str) -> None
    self.__rawHeaders = rawHeaders

  def getRawBody(self):  #type: () -> str
    return self.__rawBody

  def setRawBody(self, rawBody):  #type: (str) -> None
    self.__rawBody = rawBody

  def getRequestInfo(self):  #type: () -> RequestInfo
    if (not self.__requestInfo):
      return RequestInfo()
    return copy.copy(self.__requestInfo)

  def setRequestInfo(self, requestInfo):  #type: (RequestInfo) -> None
    self.__requestInfo = requestInfo

  def getRequestUrl(self):  #type: () -> str
    return self.__requestUrl

  def setRequestUrl(self, requestUrl):  #type: (str) -> None
    self.__requestUrl = requestUrl

  def getRequestHeaders(self):  #type: () -> OrderedDict
    if (not self.__requestHeaders):
      return OrderedDict()
    return OrderedDict(self.__requestHeaders)

  def setRequestHeaders(self, requestHeaders):  #type: (OrderedDict) -> None
    self.__requestHeaders = requestHeaders

  def getRequestBoundary(self):  #type: () -> str
    return self.__requestBoundary

  def setRequestBoundary(self, requestBoundary):  #type: (str) -> None
    self.__requestBoundary = requestBoundary

  def getRequestBodyDict(self):  #type: () -> OrderedDict
    if (not self.__requestBodyDict):
      return OrderedDict()
    return OrderedDict(self.__requestBodyDict)

  def setRequestBodyDict(self, requestBodyDict):  #type: (OrderedDict) -> None
    self.__requestBodyDict = requestBodyDict

  def getRequestBodyString(self):  #type: () -> str
    return self.__requestBodyString

  def setRequestBodyString(self, requestBodyString):  #type: (str) -> None
    self.__requestBodyString = requestBodyString

  def getOriginalRequestInfo(self):  #type: () -> OrderedDict
    return self.__originalRequestInfo

  def setOriginalRequestInfo(self, originalRequestInfo):  #type: (OrderedDict) -> None
    self.__originalRequestInfo = originalRequestInfo

  def getOriginalRequestHeaders(self):  #type: () -> OrderedDict
    return self.__originalRequestHeaders

  def setOriginalRequestHeaders(self, originalRequestHeaders):  #type: (OrderedDict) -> None
    self.__originalRequestHeaders = originalRequestHeaders

  def getOriginalRequestBodyDict(self):  #type: () -> OrderedDict
    return self.__originalRequestBodyDict

  def setOriginalRequestBodyDict(self, originalRequestBodyDict):  #type: (OrderedDict) -> None
    self.__originalRequestBodyDict = originalRequestBodyDict

  def getOriginalRequestBodyString(self):  #type: () -> str
    return self.__originalRequestBodyString

  def setOriginalRequestBodyString(self, originalRequestBodyString):  #type: (str) -> None
    self.__originalRequestBodyString = originalRequestBodyString

  def updateOriginalValues(self):  #type: () -> None
    self.__originalRequestInfo = self.__requestInfo
    self.__originalRequestHeaders = self.__requestHeaders
    self.__originalRequestBodyDict = self.__requestBodyDict
    self.__originalRequestBodyString = self.__requestBodyString

  def resetRequestValues(self):  #type: () -> None
    self.__requestInfo = self.__originalRequestInfo
    self.__requestHeaders = self.__originalRequestHeaders
    self.__requestBodyDict = self.__originalRequestBodyDict
    self.__requestBodyString = self.__originalRequestBodyString