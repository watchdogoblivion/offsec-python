# author: WatchDogOblivion
# description: TODO
# WatchDogs Request

import copy
from collections import OrderedDict

from watchdogs.base.models import Common


class RequestInfo(Common):

  def __init__(self, urlHost=str(), method=str(), endpoint=str()):  #type: (str, str, str) -> None
    super(RequestInfo, self).__init__()
    self._urlHost = urlHost
    self._method = method
    self._endpoint = endpoint

  def getUrlHost(self):  #type: () -> str
    return self._urlHost

  def setUrlHost(self, urlHost):  #type: (str) -> None
    self._urlHost = urlHost

  def getMethod(self):  #type: () -> str
    return self._method

  def setMethod(self, method):  #type: (str) -> None
    self._method = method

  def getEndpoint(self):  #type: () -> str
    return self._endpoint

  def setEndpoint(self, endpoint):  #type: (str) -> None
    self._endpoint = endpoint


class Request(Common):

  def __init__(self, rawInfo=str(), rawHeaders=str(), rawBody=str(), requestInfo=RequestInfo(),
               requestUrl=str(), requestHeaders=OrderedDict(), requestBoundary=str(),
               requestBody=OrderedDict()):
    #type: (str, str, str, RequestInfo, str, OrderedDict, str, OrderedDict) -> None
    super(Request, self).__init__()
    self._rawInfo = rawInfo
    self._rawHeaders = rawHeaders
    self._rawBody = rawBody
    self.requestInfo = requestInfo
    self.requestUrl = requestUrl
    self.requestHeaders = requestHeaders
    self.requestBoundary = requestBoundary
    self.requestBody = requestBody
    self.originalRequestInfo = requestInfo
    self.originalRequestHeaders = requestHeaders
    self.originalRequestBody = requestBody

  def getRawInfo(self):  #type: () -> str
    return self._rawInfo

  def setRawInfo(self, rawInfo):  #type: (str) -> None
    self._rawInfo = rawInfo

  def getRawHeaders(self):  #type: () -> str
    return self._rawHeaders

  def setRawHeaders(self, rawHeaders):  #type: (str) -> None
    self._rawHeaders = rawHeaders

  def getRawBody(self):  #type: () -> str
    return self._rawBody

  def setRawBody(self, rawBody):  #type: (str) -> None
    self._rawBody = rawBody

  def getRequestInfo(self):  #type: () -> RequestInfo
    return copy.copy(self.requestInfo)

  def setRequestInfo(self, requestInfo):  #type: (RequestInfo) -> None
    self.requestInfo = requestInfo

  def getRequestUrl(self):  #type: () -> str
    return self.requestUrl

  def setRequestUrl(self, requestUrl):  #type: (str) -> None
    self.requestUrl = requestUrl

  def getRequestHeaders(self):  #type: () -> OrderedDict
    return OrderedDict(self.requestHeaders)

  def setRequestHeaders(self, requestHeaders):  #type: (OrderedDict) -> None
    self.requestHeaders = requestHeaders

  def getRequestBoundary(self):  #type: () -> str
    return self.requestBoundary

  def setRequestBoundary(self, requestBoundary):  #type: (str) -> None
    self.requestBoundary = requestBoundary

  def getRequestBody(self):  #type: () -> OrderedDict
    return OrderedDict(self.requestBody)

  def setRequestBody(self, requestBody):  #type: (OrderedDict) -> None
    self.requestBody = requestBody

  def getOriginalRequestInfo(self):  #type: () -> OrderedDict
    return self.originalRequestInfo

  def setOriginalRequestInfo(self, originalRequestInfo):  #type: (OrderedDict) -> None
    self.originalRequestInfo = originalRequestInfo

  def getOriginalRequestHeaders(self):  #type: () -> OrderedDict
    return self.originalRequestHeaders

  def setOriginalRequestHeaders(self, originalRequestHeaders):  #type: (OrderedDict) -> None
    self.originalRequestHeaders = originalRequestHeaders

  def getOriginalRequestBody(self):  #type: () -> OrderedDict
    return self.originalRequestBody

  def setOriginalRequestBody(self, originalRequestBody):  #type: (OrderedDict) -> None
    self.originalRequestBody = originalRequestBody

  def updateOriginalValues(self):  #type: () -> None
    self.originalRequestInfo = self.requestInfo
    self.originalRequestHeaders = self.requestHeaders
    self.originalRequestBody = self.requestBody

  def resetRequestValues(self):
    self.requestInfo = self.originalRequestInfo
    self.requestHeaders = self.originalRequestHeaders
    self.requestBody = self.originalRequestBody