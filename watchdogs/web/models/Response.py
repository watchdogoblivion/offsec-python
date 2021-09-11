# author: WatchDogOblivion
# description: TODO
# WatchDogs Response

import requests
from bs4 import BeautifulSoup

from watchdogs.base.models import Common
from watchdogs.utils.Constants import EMPTY


class Response(Common):

  def __init__(self, response=None, responseSoup=EMPTY, responseStatus=EMPTY, responseLength=EMPTY):
    #type: (requests.models.Response, BeautifulSoup, int, str) -> None
    super(Response, self).__init__()
    self.__response = response
    self.__responseSoup = responseSoup
    self.__responseStatus = responseStatus
    self.__responseLength = responseLength

  def getResponse(self):  #type: () -> requests.models.Response
    return self.__response

  def setResponse(self, response):  #type: (requests.models.Response) -> None
    self.__response = response

  def getResponseSoup(self):  #type: () -> BeautifulSoup
    return self.__responseSoup

  def setResponseSoup(self, responseSoup):  #type: (BeautifulSoup) -> None
    self.__responseSoup = responseSoup

  def getResponseStatus(self):  #type: () -> int
    return self.__responseStatus

  def setResponseStatus(self, responseStatus):  #type: (int) -> None
    self.__responseStatus = responseStatus

  def getResponseLength(self):  #type: () -> str
    return self.__responseLength

  def setResponseLength(self, responseLength):  #type: (str) -> None
    self.__responseLength = responseLength