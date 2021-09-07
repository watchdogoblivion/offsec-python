# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import re
from watchdogs import web
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from watchdogs.utils import Cast
from watchdogs.web.models import AVI
from watchdogs.base.models import Common
from watchdogs.web.models import FileFuzzer
from watchdogs.web.parsers import FileFuzzerArgs
from watchdogs.web.models.WebFile import WebFile
from watchdogs.web.models.Requests import RequestInfo
from watchdogs.web.models.Locators import (FuzzHelper, FuzzLocator, LocatorContainer)
from watchdogs.utils.Constants import (EMPTY, COLON, EQUAL, SEMI_COLON, LFN, BOUNDARY, DASH, SPACE,
                                       CONTENT_DISPOSITION, CONTENT_TYPE, FILE_NAME, DOUBLE_QUOTE, NAME, RB,
                                       FUZZ, SONE, REGEX_SUB, LR, LFRN, HTTP, HTTP_PROTOCOL, HTTPS_PROTOCOL,
                                       HTTPS, HTML_PARSER, CONTENT_LENGTH, UTF8)


class FileFuzzerService(Common):

  VERSION = "1.0"
  BOUNDLESS_REGEX = r'(?:FUZZ)($|[^0-9])'
  BOUND_REGEX = r'FUZZ([0-9]+)'
  DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1"

  def __init__(self, fileFuzzer=FileFuzzer()):  #type: (FileFuzzer) -> None
    super(FileFuzzerService, self).__init__()
    self.__fileFuzzer = fileFuzzer

  def setBoundary(self, fileLine, boundaryString):  #type: (str,str) -> None
    request = self.__fileFuzzer.getRequest()
    equalsIndex = fileLine.find(EQUAL, fileLine.find(boundaryString))
    semiColonIndex = fileLine.find(SEMI_COLON, equalsIndex)
    lineFeedIndex = fileLine.find(LFN)
    if (semiColonIndex > -1):
      request.setRequestBoundary(fileLine[equalsIndex + 1:semiColonIndex])
    elif (lineFeedIndex > -1):
      request.setRequestBoundary(fileLine[equalsIndex + 1:lineFeedIndex])
    else:
      request.setRequestBoundary(fileLine[equalsIndex + 1:])

  def setFields(self, fileLines):  #type: (str) -> None
    request = self.__fileFuzzer.getRequest()
    rawValue = EMPTY
    isBody = False
    fileLinesLength = len(fileLines)
    index = 0

    while (index < fileLinesLength):
      fileLine = fileLines[index].rstrip()
      boundaryString = BOUNDARY + EQUAL + DASH + DASH
      if (boundaryString in fileLine):
        self.setBoundary(fileLine, boundaryString)
      if (index == 0):
        request.setRawInfo(fileLine)
        index += 1
        continue
      elif ((fileLine == EMPTY and not isBody) or (index + 1 == fileLinesLength and not isBody)):
        isBody = True
        request.setRawHeaders(rawValue)
        rawValue = EMPTY
      elif (index + 1 == fileLinesLength):
        rawValue += fileLine + LFN
        request.setRawBody(rawValue)
        index += 1
        break

      rawValue += fileLine + LFN
      index += 1

  def parseInfo(self):  #type: () -> None
    rawInfo = self.__fileFuzzer.getRequest().getRawInfo()
    requestInfo = self.__fileFuzzer.getRequest().getRequestInfo()
    rawInfoSplit = rawInfo.rstrip().split(SPACE)

    requestInfo.setMethod(rawInfoSplit[0])
    requestInfo.setEndpoint(rawInfoSplit[1])

  def parseHeaders(self):  #type: () -> None
    request = self.__fileFuzzer.getRequest()
    requestHeaders = request.getRequestHeaders()

    rawHeaders = request.getRawHeaders()
    rawHeadersSplit = rawHeaders.rstrip().split(LFN)

    for rawHeader in rawHeadersSplit:
      colonIndex = rawHeader.find(COLON)
      headerKey = rawHeader[0:colonIndex]
      headerValue = rawHeader[colonIndex + 1:].strip()
      requestHeaders[headerKey] = headerValue
    request.setRequestHeaders(requestHeaders)

  def parseBody(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    request = self.__fileFuzzer.getRequest()
    if (fileFuzzerArgs.postFile):
      rawBodyLines = [
          (l) for l in request.getRawBody().split(LFN) if l and not request.getRequestBoundary() in l
      ]
      rawBodyLinesLength = len(rawBodyLines)

      for lineIndex in range(rawBodyLinesLength):
        cd = CONTENT_DISPOSITION + COLON
        ct = CONTENT_TYPE + COLON
        fn = FILE_NAME + EQUAL + DOUBLE_QUOTE
        n = NAME + EQUAL + DOUBLE_QUOTE
        rawBodyLine = rawBodyLines[lineIndex]
        startName = rawBodyLine.find(DOUBLE_QUOTE, rawBodyLine.find(n))
        endName = rawBodyLine.find(DOUBLE_QUOTE, startName + 1)
        requestBody = request.getRequestBody()

        if (fn in rawBodyLine):
          name = rawBodyLine[startName + 1:endName]
          startFileName = rawBodyLine.find(DOUBLE_QUOTE, rawBodyLine.find(fn))
          endFileName = rawBodyLine.find(DOUBLE_QUOTE, startFileName + 1)
          fileName = rawBodyLine[startFileName + 1:endFileName]
          contentTypeValue = None
          if (ct in rawBodyLines[lineIndex + 1]):
            contentType = rawBodyLines[lineIndex + 1]
            contentTypeValue = contentType[contentType.find(COLON) + 1:]
          webFile = (fileName, open(fileFuzzerArgs.postFile, RB), contentTypeValue)
          requestBody[name] = WebFile(webFile)
        elif (cd in rawBodyLine):
          name = rawBodyLine[startName + 1:endName]
          rawValue = EMPTY
          i = lineIndex + 1
          while (True):
            rawValue += rawBodyLines[i]
            nextLine = EMPTY
            if (i + 1 < rawBodyLinesLength):
              nextLine = rawBodyLines[i + 1]
            if (i + 1 == rawBodyLinesLength or cd in nextLine):
              requestBody[name] = rawValue
              break
        request.setRequestBody(requestBody)
      if (not request.getRequestBody()):
        print(
            "Could not parse thw post file specified. Please ensure that the -pf flag is being used with"
            " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
            " flag to send JSON or standard form data.")
        exit()
    else:
      request.setRequestBody(request.getRawBody())

  def getFuzzIndicies(self, *fuzzWords):  # type: (str) -> list[int]
    boundRegex = FileFuzzerService.BOUND_REGEX
    fuzzWordsIndicies = []
    for fuzzWord in fuzzWords:
      if fuzzWord:
        fuzzWordsIndicies += re.findall(boundRegex, fuzzWord)
    return fuzzWordsIndicies

  def getBoundlessFuzz(self, *fuzzWords):  # type: (str) -> str
    boundlessRegex = FileFuzzerService.BOUNDLESS_REGEX
    for fuzzWord in fuzzWords:
      boundlessArray = re.findall(boundlessRegex, fuzzWord)
      if (boundlessArray):
        if (len(boundlessArray) > 1):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        return fuzzWord

  def handleBoundless(self, boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey, aVI=None):
    #type: (str, list[int], str | OrderedDict, str, AVI) -> None
    request = self.__fileFuzzer.getRequest()
    if (boundlessFuzz):
      boundlessRegex = FileFuzzerService.BOUNDLESS_REGEX
      newValue = re.sub(boundlessRegex, FUZZ + SONE + REGEX_SUB, boundlessFuzz)
      fuzzWordsIndicies.append(SONE)
      if (type(attrValue) == str):
        setattr(request, attrKey, newValue)
      elif (type(attrValue) == RequestInfo):
        Cast._to(RequestInfo, attrValue).setEndpoint(newValue)
      elif (aVI):
        aVIKey = aVI.getAVIKey()
        aVIValue = aVI.getAVIValue()
        fileName = aVI.getFileName()
        contentType = aVI.getContentType()
        if (type(aVIValue) == WebFile):
          webFile = Cast._to(WebFile, aVIValue)
          if (fileName == boundlessFuzz):
            webFile.setFileName(newValue)
          if (contentType == boundlessFuzz):
            webFile.setContentType(newValue)
        elif (type(aVIValue) == str):
          attrValue[aVIKey] = newValue

  def manageLocatorValues(self, fuzzWordsIndicies, existingIndicies, locatorKey, locator):
    #type: (list[int], list[int], str, FuzzLocator) -> None
    if (len(fuzzWordsIndicies) > 0):
      for fuzzWordIndex in fuzzWordsIndicies:
        if (fuzzWordIndex in existingIndicies):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        container = LocatorContainer()
        container.setLocatorKey(locatorKey)
        container.setFuzzWordIndex(fuzzWordIndex)
        locator.getLocatorContainers().append(container)
        existingIndicies.append(container.getFuzzWordIndex())

  def updateFuzzLocator(self, *attrKeys):  # type: (str) -> None
    fileFuzzer = self.__fileFuzzer
    request = fileFuzzer.getRequest()
    locators = fileFuzzer.getFuzzLocators()
    existingIndicies = []

    for attrKey in attrKeys:
      attrValue = getattr(request, attrKey)
      locator = Cast._to(FuzzLocator, getattr(locators, attrKey))
      if (type(attrValue) == str):
        fuzzWordsIndicies = self.getFuzzIndicies(attrValue)
        boundlessFuzz = self.getBoundlessFuzz(attrValue)
        self.handleBoundless(boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey)
        self.manageLocatorValues(fuzzWordsIndicies, existingIndicies, attrKey, locator)
      elif (type(attrValue) == RequestInfo):
        endpoint = Cast._to(RequestInfo, attrValue).getEndpoint()
        fuzzWordsIndicies = self.getFuzzIndicies(endpoint)
        boundlessFuzz = self.getBoundlessFuzz(endpoint)
        self.handleBoundless(boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey)
        self.manageLocatorValues(fuzzWordsIndicies, existingIndicies, attrKey, locator)
      elif (type(attrValue) == OrderedDict):
        aVI = OrderedDict(attrValue).items()
        for aVIKey, aVIValue in aVI:
          fuzzWord = fileName = contentType = EMPTY
          if (type(aVIValue) == WebFile):
            webFile = Cast._to(WebFile, aVIValue)
            fileName = webFile.getFileName()
            contentType = webFile.getContentType()
          elif (type(aVIValue) == str):
            fuzzWord = aVIValue
          fuzzWordsIndicies = self.getFuzzIndicies(fuzzWord, fileName, contentType)
          boundlessFuzz = self.getBoundlessFuzz(fuzzWord, fileName, contentType)
          aVI = AVI(aVIKey, aVIValue, fileName, contentType)
          self.handleBoundless(boundlessFuzz, fuzzWordsIndicies, attrValue, None, aVI)
          self.manageLocatorValues(fuzzWordsIndicies, existingIndicies, aVIKey, locator)

  def parseFile(self, fileFuzzerArgs):
    # type: (FileFuzzerArgs) -> None
    inputFile = open(fileFuzzerArgs.inputFile, LR)
    inptFileLines = inputFile.readlines()

    self.__fileFuzzer.getRequest().setUrlHost(fileFuzzerArgs.remoteHost)
    self.setFields(inptFileLines)
    self.parseInfo()
    self.parseHeaders()
    self.parseBody(fileFuzzerArgs)
    attrKeys = ["urlHost", "requestInfo", "requestHeaders", "requestBody"]
    self.updateFuzzLocator(*attrKeys)

  def printRequest(self):  # type: () -> None
    request = self.__fileFuzzer.getRequest()
    format = '{}: {}'

    info = []
    for infoKey, infoValue in request.getRequestInfo().__dict__:
      info.append(format.format(infoKey, infoValue))

    headers = []
    for headersKey, headersValue in request.getRequestHeaders().__dict__:
      headers.append(format.format(headersKey, headersValue))

    body = []
    if (type(request.getRequestBody()) == str):
      body.append(request.getRequestBody())
    else:
      for k, v in request.getRequestBody().items():
        body.append(format.format(k, v))

    print('{}{}{}{}{}{}{}{}{}{}{}'.format(LFRN, '-----------Request Start-----------',
                                          LFRN, LFRN.join(info), LFRN, LFRN.join(headers), LFRN,
                                          LFRN.join(body), LFRN, '----------- Request End ------------',
                                          LFRN))

  def getAllLocatorsContainers(self):  # type: () -> int
    locators = self.__fileFuzzer.getFuzzLocators()
    rhostContainers = locators.getRemoteHost().getLocatorContainers()
    infoContainers = locators.getRequestInfo().getLocatorContainers()
    headersContainers = locators.getRequestHeaders().getLocatorContainers()
    bodyContainers = locators.getRequestBody().getLocatorContainers()
    return rhostContainers + infoContainers + headersContainers + bodyContainers

  def getFuzzHelpers(self):  # type: () -> list
    fileFuzzer = self.__fileFuzzer
    request = self.__fileFuzzer.getRequest()
    locators = vars(fileFuzzer.getFuzzLocators())
    fuzzHelpers = []
    for locatorField in locators:
      locator = Cast._to(FuzzLocator, locators[locatorField])
      containers = locator.getLocatorContainers()
      for container in containers:
        fuzzHelper = FuzzHelper()
        fuzzHelper.setFuzzWordIndex(int(container.getFuzzWordIndex()))
        fuzzHelper.setAttrKey(locatorField)
        fuzzHelper.setLocatorKey(container.getLocatorKey())
        attrValue = getattr(request, locatorField)
        if (type(attrValue) == str):
          fuzzHelper.setOriginalAttrValue(attrValue)
        elif (type(attrValue) == RequestInfo):
          fuzzHelper.setOriginalAttrValue(Cast._to(RequestInfo, attrValue).getEndpoint())
        else:
          fuzzHelper.setOriginalAttrValue(attrValue[fuzzHelper.getLocatorKey()])
        fuzzHelpers.append(fuzzHelper)
    return fuzzHelpers

  def parseUrl(self, host, secure, endpoint=EMPTY):  #type: (str, bool, str) -> str
    standardProtocol = HTTP
    if (standardProtocol in host):
      return "{}{}".format(host, endpoint)
    else:
      protocol = HTTP_PROTOCOL
      if (secure):
        protocol = HTTPS_PROTOCOL
      return "{}{}{}".format(protocol, host, endpoint)

  def getRequestBody(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> OrderedDict | str
    request = self.__fileFuzzer.getRequest()
    requestBodyDict = request.getRequestBody()
    if (fileFuzzerArgs.postFile):
      for requestBodyKey in requestBodyDict:
        requestBodyValue = requestBodyDict[requestBodyKey]
        if (type(requestBodyValue) == WebFile):
          requestBodyDict[requestBodyKey] = Cast._to(WebFile, requestBodyValue).getWebFile()
      return MultipartEncoder(fields=requestBodyDict, boundary=request.getRequestBoundary())
    return requestBodyDict

  def getProxies(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> dict
    proxies = {}
    if (fileFuzzerArgs.httpProxy):
      proxies[HTTP] = self.parseUrl(fileFuzzerArgs.httpProxy, False)
    elif (fileFuzzerArgs.httpsProxy):
      proxies[HTTPS] = self.parseUrl(fileFuzzerArgs.httpsProxy, True)
    return proxies

  def handleResponse(self, response, fileFuzzerArgs):
    #type: (requests.models.Response, FileFuzzerArgs) -> None
    responseSoup = BeautifulSoup(response.text, HTML_PARSER).prettify().rstrip()
    responseStatus = response.status_code
    responseLength = EMPTY
    try:
      responseLength = response.headers.get(CONTENT_LENGTH)
    except:
      print("An exception occurred trying to retrieve header {}".format(CONTENT_LENGTH))

    if (fileFuzzerArgs.filterLength and responseLength in fileFuzzerArgs.filterLength):
      return
    if (fileFuzzerArgs.filterStatus and not str(responseStatus) in fileFuzzerArgs.filterStatus):
      return
    if (fileFuzzerArgs.filterIn and not fileFuzzerArgs.filterIn.lower() in responseSoup.lower()):
      return
    if (fileFuzzerArgs.filterOut and fileFuzzerArgs.filterOut.lower() in responseSoup.lower()):
      return

    responseString = "Response status: {} - Response length: {}".format(responseStatus, responseLength)
    if (fileFuzzerArgs.showFuzz):
      responseString += " - Fuzz text: {}".format(self.__fileFuzzer.getFuzzValuesString())
    if (fileFuzzerArgs.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def sendRequest(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    request = self.__fileFuzzer.getRequest()
    urlHost = request.getUrlHost()
    requestInfo = request.getRequestInfo()
    requestHeaders = request.getRequestHeaders()
    requestBody = self.getRequestBody(fileFuzzerArgs)
    requestUrl = self.parseUrl(urlHost, fileFuzzerArgs.secure, requestInfo.getEndpoint())
    request.setRequestUrl(requestUrl)

    req = requests.Request(requestInfo.getMethod(), requestUrl, headers=requestHeaders, data=requestBody)
    prepared = req.prepare()
    session = requests.Session()
    session.proxies = self.getProxies(fileFuzzerArgs)
    session.verify = not fileFuzzerArgs.disableVerification
    response = session.send(prepared, timeout=fileFuzzerArgs.readTimeout)
    self.handleResponse(response, fileFuzzerArgs)

  def swapFuzz(self, fuzzValues, fuzzHelpers):
    #type: (list[str], list[FuzzHelper]) -> None
    request = self.__fileFuzzer.getRequest()
    for fuzzHelper in fuzzHelpers:
      fuzzWordIndex = fuzzHelper.getFuzzWordIndex()
      fuzzWord = FUZZ + str(fuzzWordIndex)
      fuzzValue = fuzzValues[fuzzWordIndex - 1].rstrip()
      attrKey = fuzzHelper.getAttrKey()
      attrValue = getattr(request, attrKey)
      if (type(attrValue) == str):
        setattr(request, attrKey, str(attrValue).replace(fuzzWord, fuzzValue))
        continue
      elif (type(attrValue) == RequestInfo):
        requestInfo = Cast._to(RequestInfo, attrValue)
        requestInfo.setEndpoint(requestInfo.getEndpoint().replace(fuzzWord, fuzzValue))
      elif (type(attrValue) == OrderedDict):
        locatorKey = fuzzHelper.getLocatorKey()
        requestValue = attrValue[locatorKey]
        if (isinstance(requestValue, WebFile)):
          webFile = Cast._to(WebFile, requestValue)
          fileName = webFile.getFileName()
          contentType = webFile.getContentType()
          if (fuzzWord in fileName):
            newValue = fileName.replace(fuzzWord, fuzzValue)
            webFile.setFileName(newValue)
          elif (fuzzWord in contentType):
            newValue = contentType.replace(fuzzWord, fuzzValue)
            webFile.setContentType(newValue)
        elif (isinstance(requestValue, str)):
          attrValue[locatorKey] = str(requestValue).replace(fuzzWord, fuzzValue)

  def swapBack(self, fuzzHelpers):  #type: (list[FuzzHelper]) -> None
    request = self.__fileFuzzer.getRequest()
    for fuzzHelper in fuzzHelpers:
      attrKey = fuzzHelper.getAttrKey()
      currentAttrValue = getattr(request, attrKey)
      originalAttrValue = fuzzHelper.getOriginalAttrValue()
      if (type(currentAttrValue) == str):
        setattr(request, attrKey, originalAttrValue)
        continue
      elif (type(currentAttrValue) == RequestInfo):
        requestInfo = Cast._to(RequestInfo, currentAttrValue)
        requestInfo.setEndpoint(originalAttrValue)
      elif (type(currentAttrValue) == OrderedDict):
        locatorKey = fuzzHelper.getLocatorKey()
        currentAttrValue[locatorKey] = originalAttrValue

  def fuzzRequest(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    fuzzValuesFile = open(fileFuzzerArgs.fuzzFile, LR)
    fuzzValuesLines = fuzzValuesFile.readlines()
    fuzzHelpers = self.getFuzzHelpers()
    fuzzDelimiter = fileFuzzerArgs.fuzzDelimiter

    if (len(fuzzHelpers) <= 0):
      print("No FUZZ keyword located. Sending normal request.")
      self.sendRequest(fileFuzzerArgs)
    else:
      for fuzzValuesLine in fuzzValuesLines:
        self.FuzzValuesString = fuzzValuesLine.rstrip()
        fuzzValues = fuzzValuesLine.split(fuzzDelimiter)
        self.swapFuzz(fuzzValues, fuzzHelpers)
        self.sendRequest(fileFuzzerArgs)
        self.swapBack(fuzzHelpers)

  def processRequest(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    if (len(self.getAllLocatorsContainers()) > 0):
      print("Fuzzing Request")
      self.fuzzRequest(fileFuzzerArgs)
    else:
      print("Sending Request")
      self.sendRequest(fileFuzzerArgs)