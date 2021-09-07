# author: WatchDogOblivion
# description: TODO
# WatchDogs Request

from collections import OrderedDict

from watchdogs.base.models import Common


class RequestInfo(Common):

  def __init__(self, method=str(), endpoint=str()):  #type: (str, str) -> None
    super(RequestInfo, self).__init__()
    self._method = method
    self._endpoint = endpoint

  def getMethod(self):  #type: () -> str
    return self._method

  def setMethod(self, method):  #type: (str) -> None
    self._method = method

  def getEndpoint(self):  #type: () -> str
    return self._endpoint

  def setEndpoint(self, endpoint):  #type: (str) -> None
    self._endpoint = endpoint


class Request(Common):

  def __init__(self, rawInfo=str(), rawHeaders=str(), rawBody=str(), urlHost=str(), requestInfo=RequestInfo(),
               requestUrl=str(), requestHeaders=OrderedDict(), requestBoundary=str(),
               requestBody=OrderedDict()):
    #type: (str, str, str, str, RequestInfo, str, OrderedDict, str, OrderedDict) -> None
    super(Request, self).__init__()
    self._rawInfo = rawInfo
    self._rawHeaders = rawHeaders
    self._rawBody = rawBody
    self.urlHost = urlHost
    self.requestInfo = requestInfo
    self.requestUrl = requestUrl
    self.requestHeaders = requestHeaders
    self.requestBoundary = requestBoundary
    self.requestBody = requestBody

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

  def getUrlHost(self):  #type: () -> str
    return self.urlHost

  def setUrlHost(self, urlHost):  #type: (str) -> None
    self.urlHost = urlHost

  def getRequestInfo(self):  #type: () -> RequestInfo
    return self.requestInfo

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