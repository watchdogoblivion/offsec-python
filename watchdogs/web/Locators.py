# author: WatchDogOblivion
# description: TODO
# WatchDogs Locators

from watchdogs.base import Common;

class LocatorContainer(Common):

    def __init__(self):
        super(LocatorContainer, self).__init__();
        self._locatorKey = '';
        self._locatorIndex = -1;

    def getLocatorKey(self):#type: (LocatorContainer) -> str
        return getattr(self, "_locatorKey");

    def setLocatorKey(self, value):#type: (LocatorContainer, str) -> None
        setattr(self, "_locatorKey", value);

    def getLocatorIndex(self):#type: (LocatorContainer) -> int
        return getattr(self, "_locatorIndex");

    def setLocatorIndex(self, value):#type: (LocatorContainer, int) -> None
        setattr(self, "_locatorIndex", value);

class FuzzLocator(Common):

    def __init__(self):
        super(FuzzLocator, self).__init__();
        self._locatorContainers = [];

    def getLocatorContainers(self):#type: (FuzzLocator) -> list[LocatorContainer]
        return getattr(self, "_locatorContainers");

    def setLocatorContainers(self, value):#type: (FuzzLocator, list[LocatorContainer]) -> None
        setattr(self, "_locatorContainers", value);

class FuzzLocators(Common):

    def __init__(self):
        super(FuzzLocators, self).__init__();
        self.rhost = FuzzLocator();
        self.info = FuzzLocator();
        self.headers = FuzzLocator();
        self.body = FuzzLocator();

    def getRhost(self):#type: (FuzzLocators) -> FuzzLocator
        return getattr(self, "rhost");

    def setRhost(self, value):#type: (FuzzLocators, FuzzLocator) -> None
        setattr(self, "rhost", value);

    def getInfo(self):#type: (FuzzLocators) -> FuzzLocator
        return getattr(self, "info");

    def setInfo(self, value):#type: (FuzzLocators, FuzzLocator) -> None
        setattr(self, "info", value);

    def getHeaders(self):#type: (FuzzLocators) -> FuzzLocator
        return getattr(self, "headers");

    def setHeaders(self, value):#type: (FuzzLocators, FuzzLocator) -> None
        setattr(self, "headers", value);

    def getBody(self):#type: (FuzzLocators) -> FuzzLocator
        return getattr(self, "body");

    def setBody(self, value):#type: (FuzzLocators, FuzzLocator) -> None
        setattr(self, "body", value);

class FuzzHelper(LocatorContainer):
    def __init__(self):
        super(FuzzHelper, self).__init__();
        self._attrKey = '';
        self._originalFuzz = None;

    def getAttrKey(self):#type: (FuzzHelper) -> str
        return getattr(self, "_attrKey");

    def setAttrKey(self, value):#type: (FuzzHelper, str) -> None
        setattr(self, "_attrKey", value);

    def getOriginalFuzz(self):#type: (FuzzHelper) -> str
        return getattr(self, "_originalFuzz");

    def setOriginalFuzz(self, value):#type: (FuzzHelper, str) -> None
        setattr(self, "_originalFuzz", value);