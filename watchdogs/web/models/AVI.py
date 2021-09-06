# author: WatchDogOblivion
# description: TODO
# WatchDogs AVI

from watchdogs.base import Common


class AVI(Common):

  def __init__(self, aVIKey=None, aVIValue=None, fileName=None, contentType=None):
    super(AVI, self).__init__()
    self._aVIKey = aVIKey  #type: str
    self._aVIValue = aVIValue  #type: str | tuple
    self._fileName = fileName  #type: str
    self._contentType = contentType  #type: str

  def getAVIKey(self):  #type: (AVI) -> str
    return getattr(self, "_aVIKey")

  def setAVIKey(self, value):  #type: (AVI, str) -> None
    setattr(self, "_aVIKey", value)

  def getAVIValue(self):  #type: (AVI) -> str | tuple
    return getattr(self, "_aVIValue")

  def setAVIValue(self, value):  #type: (AVI, str | tuple) -> None
    setattr(self, "_aVIValue", value)

  def getFileName(self):  #type: (AVI) -> str
    return getattr(self, "_fileName")

  def setFileName(self, value):  #type: (AVI, str) -> None
    setattr(self, "_fileName", value)

  def getContentType(self):  #type: (AVI) -> str
    return getattr(self, "_contentType")

  def setContentType(self, value):  #type: (AVI, str) -> None
    setattr(self, "_contentType", value)