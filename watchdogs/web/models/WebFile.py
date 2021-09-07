# author: WatchDogOblivion
# description: TODO
# WatchDogs Web File

from typing import IO

from watchdogs.base.models import Common


class WebFile(Common):

  def __init__(self, webFile=(None, None, None)):  #type: (tuple[str, IO, str]) -> None
    super(WebFile, self).__init__()
    self.__webFile = webFile
    self.__fileName = webFile[0]
    self.__content = webFile[1]
    self.__contentType = webFile[2]

  def getWebFile(self):  #type: () -> tuple[str, IO, str]
    return self.__webFile

  def setWebFile(self, webFile):  #type: (tuple[str, IO, str]) -> None
    self.__webFile = webFile
    self.__fileName = webFile[0]
    self.__content = webFile[1]
    self.__contentType = webFile[2]

  def getFileName(self):  #type: () -> str
    return self.__fileName

  def setFileName(self, fileName):  #type: (str) -> None
    self.__fileName = fileName
    webFile = self.__webFile
    self.__webFile = (fileName, webFile[1], webFile[2])

  def getContent(self):  #type: () -> IO
    return self.__content

  def setContent(self, content):  #type: (IO) -> None
    self.__content = content
    webFile = self.__webFile
    self.__webFile = (webFile[0], content, webFile[2])

  def getContentType(self):  #type: () -> str
    return self.__contentType

  def setContentType(self, contentType):  #type: (str) -> None
    self.__contentType = contentType
    webFile = self.__webFile
    self.__webFile = (webFile[0], webFile[1], contentType)