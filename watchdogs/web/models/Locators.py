# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)


class LocatorDatum(Common):

  def __init__(self, indexOfSubstitute=-1, isInfo=False, headerKey=EMPTY, bodyKey=EMPTY):
    #type: (int, bool, str, str) -> None
    super(LocatorDatum, self).__init__()
    self.__indexOfSubstitute = indexOfSubstitute
    self.__isInfo = isInfo
    self.__headerKey = headerKey
    self.__bodyKey = bodyKey

  def getIndexOfSubstitute(self):  #type: () -> int
    return self.__indexOfSubstitute

  def setIndexOfSubstitute(self, indexOfSubstitute):  #type: (int) -> None
    self.__indexOfSubstitute = indexOfSubstitute

  def isInfo(self):  #type: () -> bool
    return self.__isInfo

  def setIsInfo(self, isInfo):  #type: (bool) -> None
    self.__isInfo = isInfo

  def getHeaderKey(self):  #type: () -> str
    return self.__headerKey

  def setHeaderKey(self, headerKey):  #type: (str) -> None
    self.__headerKey = headerKey

  def getBodyKey(self):  #type: () -> str
    return self.__bodyKey

  def setBodyKey(self, bodyKey):  #type: (str) -> None
    self.__bodyKey = bodyKey


class VariantLocator(Common):

  def __init__(self, locatorData=None, isInfo=False, isHeaders=False, isBody=False):
    #type: (list[LocatorDatum], bool,bool,bool) -> None
    super(VariantLocator, self).__init__()
    self.__locatorData = locatorData
    self.__isInfo = isInfo
    self.__isHeaders = isHeaders
    self.__isBody = isBody

  def getLocatorData(self):  #type: () -> list[LocatorDatum]
    if(not self.__locatorData):
      return []
    return list(self.__locatorData)

  def setLocatorData(self, locatorData):  #type: (list[LocatorDatum]) -> None
    self.__locatorData = locatorData

  def isInfo(self):  #type: () -> bool
    return self.__isInfo

  def setIsInfo(self, isInfo):  #type: (bool) -> None
    self.__isInfo = isInfo

  def isHeader(self):  #type: () -> bool
    return self.__isHeaders

  def setIsHeader(self, isHeader):  #type: (bool) -> None
    self.__isHeaders = isHeader

  def isBody(self):  #type: () -> bool
    return self.__isBody

  def setIsBody(self, isBody):  #type: (bool) -> None
    self.__isBody = isBody