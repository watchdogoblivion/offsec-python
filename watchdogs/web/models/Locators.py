# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

from typing import Any

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class LocatorContainer(Common):

  def __init__(self):
    super(LocatorContainer, self).__init__()
    self._locatorKey = EMPTY  #type: str
    self._fuzzWordIndex = -1  #type: int
    self._isInfo = False
    self._headerKey = EMPTY
    self._bodyKey = EMPTY

  def getLocatorKey(self):  #type: (LocatorContainer) -> str
    return getattr(self, "_locatorKey")

  def setLocatorKey(self, value):  #type: (LocatorContainer, str) -> None
    setattr(self, "_locatorKey", value)

  def getFuzzWordIndex(self):  #type: (LocatorContainer) -> int
    return getattr(self, "_fuzzWordIndex")

  def setFuzzWordIndex(self, value):  #type: (LocatorContainer, int) -> None
    setattr(self, "_fuzzWordIndex", value)

  def isInfo(self):  #type: () -> bool
    return self._isInfo

  def setIsInfo(self, isInfo):  #type: (bool) -> None
    self._isInfo = isInfo

  def getHeaderKey(self):  #type: () -> str
    return self._headerKey

  def setHeaderKey(self, headerKey):  #type: (str) -> None
    self._headerKey = headerKey

  def getBodyKey(self):  #type: () -> str
    return self._bodyKey

  def setBodyKey(self, bodyKey):  #type: (str) -> None
    self._bodyKey = bodyKey


class FuzzLocator(Common):

  def __init__(self, locatorContainers=[], isInfo=False, isHeaders=False, isBody=False):
    #type: (list[LocatorContainer], bool,bool,bool) -> None
    super(FuzzLocator, self).__init__()
    self._locatorContainers = locatorContainers
    self._isInfo = isInfo
    self._isHeader = isHeaders
    self._isBody = isBody

  def getLocatorContainers(self):  #type: (FuzzLocator) -> list[LocatorContainer]
    return getattr(self, "_locatorContainers")

  def setLocatorContainers(self, value):  #type: (FuzzLocator, list[LocatorContainer]) -> None
    setattr(self, "_locatorContainers", value)

  def isInfo(self):  #type: () -> bool
    return self._isInfo

  def setIsInfo(self, isInfo):  #type: (bool) -> None
    self._isInfo = isInfo

  def isHeader(self):  #type: () -> bool
    return self._isHeader

  def setIsHeader(self, isHeader):  #type: (bool) -> None
    self._isHeader = isHeader

  def isBody(self):  #type: () -> bool
    return self._isBody

  def setIsBody(self, isBody):  #type: (bool) -> None
    self._isBody = isBody


class FuzzLocators(Common):

  def __init__(self, requestInfo=FuzzLocator(isInfo=True), requestHeaders=FuzzLocator(isHeaders=True),
               requestBody=FuzzLocator(isBody=True)):
    #type: (FuzzLocator, FuzzLocator, FuzzLocator) -> None
    super(FuzzLocators, self).__init__()
    self.requestInfo = requestInfo
    self.requestHeaders = requestHeaders
    self.requestBody = requestBody

  def getUrlHost(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "urlHost")

  def setUrlHost(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "urlHost", value)

  def getRequestInfo(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "requestInfo")

  def setRequestInfo(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "requestInfo", value)

  def getRequestHeaders(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "requestHeaders")

  def setRequestHeaders(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "requestHeaders", value)

  def getRequestBody(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "requestBody")

  def setRequestBody(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "requestBody", value)


class FuzzHelper(LocatorContainer):

  def __init__(self):
    super(FuzzHelper, self).__init__()
    self._attrKey = EMPTY  #type: str

  def getAttrKey(self):  #type: (FuzzHelper) -> str
    return getattr(self, "_attrKey")

  def setAttrKey(self, value):  #type: (FuzzHelper, str) -> None
    setattr(self, "_attrKey", value)