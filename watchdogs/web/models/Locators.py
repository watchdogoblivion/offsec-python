# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class LocatorContainer(Common):

  def __init__(self):
    super(LocatorContainer, self).__init__()
    self._locatorKey = EMPTY  #type: str
    self._fuzzWordIndex = -1  #type: int

  def getLocatorKey(self):  #type: (LocatorContainer) -> str
    return getattr(self, "_locatorKey")

  def setLocatorKey(self, value):  #type: (LocatorContainer, str) -> None
    setattr(self, "_locatorKey", value)

  def getFuzzWordIndex(self):  #type: (LocatorContainer) -> int
    return getattr(self, "_fuzzWordIndex")

  def setFuzzWordIndex(self, value):  #type: (LocatorContainer, int) -> None
    setattr(self, "_fuzzWordIndex", value)


class FuzzLocator(Common):

  def __init__(self):
    super(FuzzLocator, self).__init__()
    self._locatorContainers = []  #type: list[LocatorContainer]

  def getLocatorContainers(self):  #type: (FuzzLocator) -> list[LocatorContainer]
    return getattr(self, "_locatorContainers")

  def setLocatorContainers(self, value):  #type: (FuzzLocator, list[LocatorContainer]) -> None
    setattr(self, "_locatorContainers", value)


class FuzzLocators(Common):

  def __init__(self):
    super(FuzzLocators, self).__init__()
    self.remoteHost = FuzzLocator()  #type: FuzzLocator
    self.requestInfo = FuzzLocator()  #type: FuzzLocator
    self.requestHeaders = FuzzLocator()  #type: FuzzLocator
    self.requestBody = FuzzLocator()  #type: FuzzLocator

  def getRemoteHost(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "remoteHost")

  def setRemoteHost(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "remoteHost", value)

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
    self._originalAttrValue = None  #type: str

  def getAttrKey(self):  #type: (FuzzHelper) -> str
    return getattr(self, "_attrKey")

  def setAttrKey(self, value):  #type: (FuzzHelper, str) -> None
    setattr(self, "_attrKey", value)

  def getOriginalAttrValue(self):  #type: (FuzzHelper) -> str
    return getattr(self, "_originalAttrValue")

  def setOriginalAttrValue(self, value):  #type: (FuzzHelper, str) -> None
    setattr(self, "_originalAttrValue", value)
