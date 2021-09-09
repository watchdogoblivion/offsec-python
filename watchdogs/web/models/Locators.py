# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class LocatorDatum(Common):

  def __init__(self):
    super(LocatorDatum, self).__init__()
    # self._locatorKey = EMPTY  #type: str
    self._indexOfSubstitute = -1  #type: int
    self._isInfo = False
    self._headerKey = EMPTY
    self._bodyKey = EMPTY

  def getIndexOfSubstitute(self):  #type: (LocatorDatum) -> int
    return getattr(self, "_indexOfSubstitute")

  def setIndexOfSubstitute(self, value):  #type: (LocatorDatum, int) -> None
    setattr(self, "_indexOfSubstitute", value)

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


class VariantLocator(Common):

  def __init__(self, locatorData=[], isInfo=False, isHeaders=False, isBody=False):
    #type: (list[LocatorDatum], bool,bool,bool) -> None
    super(VariantLocator, self).__init__()
    self._locatorData = locatorData
    self._isInfo = isInfo
    self._isHeaders = isHeaders
    self._isBody = isBody

  def getLocatorData(self):  #type: (VariantLocator) -> list[LocatorDatum]
    return getattr(self, "_locatorData")

  def setLocatorData(self, value):  #type: (VariantLocator, list[LocatorDatum]) -> None
    setattr(self, "_locatorData", value)

  def isInfo(self):  #type: () -> bool
    return self._isInfo

  def setIsInfo(self, isInfo):  #type: (bool) -> None
    self._isInfo = isInfo

  def isHeader(self):  #type: () -> bool
    return self._isHeaders

  def setIsHeader(self, isHeader):  #type: (bool) -> None
    self._isHeaders = isHeader

  def isBody(self):  #type: () -> bool
    return self._isBody

  def setIsBody(self, isBody):  #type: (bool) -> None
    self._isBody = isBody