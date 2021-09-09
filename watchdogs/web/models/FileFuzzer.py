# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

from watchdogs.base.models import Common
from watchdogs.web.models.Requests import Request
from watchdogs.web.models.Locators import VariantLocator


class FileFuzzer(Common):

  def __init__(self, request=Request(), variantLocators=[]):
    #type: (Request, list[VariantLocator]) -> None

    super(FileFuzzer, self).__init__()
    self.__request = request
    self.__variantLocators = variantLocators

  def getRequest(self):  #type: () -> Request
    return self.__request

  def setRequest(self, request):  #type: (Request) -> None
    self.__request = request

  def getVariantLocators(self):  #type: () -> list[VariantLocator]
    return self.__variantLocators

  def setVariantLocators(self, variantLocators):  #type: (list[VariantLocator]) -> None
    self.__variantLocators = variantLocators

  def rebaseLocators(self):  #type() -> list[FuzzLocator]
    self.__variantLocators.append(VariantLocator(isInfo=True))
    self.__variantLocators.append(VariantLocator(isHeaders=True))
    self.__variantLocators.append(VariantLocator(isBody=True))
    return self.__variantLocators