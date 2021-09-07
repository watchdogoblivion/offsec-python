# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

# from collections import OrderedDict

from watchdogs.base.models import Common
from watchdogs.web.models.Requests import Request
from watchdogs.web.models.Locators import FuzzLocators


class FileFuzzer(Common):

  def __init__(self, request=Request(), fuzzLocators=FuzzLocators(), fuzzValuesString=str()):
    #type: (Request, FuzzLocators, str) -> None

    super(FileFuzzer, self).__init__()
    self.__request = request
    self.__fuzzLocators = fuzzLocators
    self.__fuzzValuesString = fuzzValuesString

  def getRequest(self):  #type: () -> Request
    return self.__request

  def setRequest(self, request):  #type: (Request) -> None
    self.__request = request

  def getFuzzLocators(self):  #type: () -> FuzzLocators
    return self.__fuzzLocators

  def setFuzzLocators(self, fuzzLocators):  #type: (FuzzLocators) -> None
    self.__fuzzLocators = fuzzLocators

  def getFuzzValuesString(self):  #type: () -> str
    return self.__fuzzValuesString

  def setFuzzValuesString(self, fuzzValuesString):  #type: (str) -> None
    self.__fuzzValuesString = fuzzValuesString