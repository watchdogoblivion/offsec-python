# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

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


class LocatorContainer(Common):

  def __init__(self):
    super(LocatorContainer, self).__init__()
    self._locatorKey = ''  #type: str
    self._locatorIndex = -1  #type: int

  def getLocatorKey(self):  #type: (LocatorContainer) -> str
    return getattr(self, "_locatorKey")

  def setLocatorKey(self, value):  #type: (LocatorContainer, str) -> None
    setattr(self, "_locatorKey", value)

  def getLocatorIndex(self):  #type: (LocatorContainer) -> int
    return getattr(self, "_locatorIndex")

  def setLocatorIndex(self, value):  #type: (LocatorContainer, int) -> None
    setattr(self, "_locatorIndex", value)


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
    self.rhost = FuzzLocator()  #type: FuzzLocator
    self.info = FuzzLocator()  #type: FuzzLocator
    self.headers = FuzzLocator()  #type: FuzzLocator
    self.body = FuzzLocator()  #type: FuzzLocator

  def getRhost(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "rhost")

  def setRhost(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "rhost", value)

  def getInfo(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "info")

  def setInfo(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "info", value)

  def getHeaders(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "headers")

  def setHeaders(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "headers", value)

  def getBody(self):  #type: (FuzzLocators) -> FuzzLocator
    return getattr(self, "body")

  def setBody(self, value):  #type: (FuzzLocators, FuzzLocator) -> None
    setattr(self, "body", value)


class FuzzHelper(LocatorContainer):

  def __init__(self):
    super(FuzzHelper, self).__init__()
    self._attrKey = ''  #type: str
    self._originalFuzz = None  #type: str

  def getAttrKey(self):  #type: (FuzzHelper) -> str
    return getattr(self, "_attrKey")

  def setAttrKey(self, value):  #type: (FuzzHelper, str) -> None
    setattr(self, "_attrKey", value)

  def getOriginalFuzz(self):  #type: (FuzzHelper) -> str
    return getattr(self, "_originalFuzz")

  def setOriginalFuzz(self, value):  #type: (FuzzHelper, str) -> None
    setattr(self, "_originalFuzz", value)
