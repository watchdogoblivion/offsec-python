# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from watchdogs.utils import Cast
from watchdogs.web.models import AVI
from watchdogs.base.models import Common
from watchdogs.web.models import FileFuzzer
from watchdogs.web.parsers import FileFuzzerArgs
from watchdogs.web.models.Locators import (FuzzHelper, FuzzLocator, LocatorContainer)
from watchdogs.utils.Constants import (EMPTY, COLON, EQUAL, SEMI_COLON, LFN, BOUNDARY, DASH, SPACE, METHOD,
                                       ENDPOINT, CONTENT_DISPOSITION, CONTENT_TYPE, FILE_NAME, DOUBLE_QUOTE,
                                       NAME, RB, FUZZ, SONE, REGEX_SUB, LR, LFRN, HTTP, HTTP_PROTOCOL,
                                       HTTPS_PROTOCOL, HTTPS, HTML_PARSER, CONTENT_LENGTH, UTF8)


class FileFuzzerService(Common):

  VERSION = "1.0"
  BOUNDLESS_REGEX = r'(?:FUZZ)($|[^0-9])'
  BOUND_REGEX = r'FUZZ([0-9]+)'
  DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1"

  def __init__(self, fileFuzzer=FileFuzzer()):
    super(FileFuzzerService, self).__init__()
    self.fileFuzzer = fileFuzzer  #type: FileFuzzer

  def setBoundary(self, fileLine, boundaryString):  #type: (str,str) -> None
    fileFuzzer = self.fileFuzzer
    equalsIndex = fileLine.find(EQUAL, fileLine.find(boundaryString))
    semiColonIndex = fileLine.find(SEMI_COLON, equalsIndex)
    lineFeedIndex = fileLine.find(LFN)
    if (semiColonIndex > -1):
      fileFuzzer.requestBoundary = fileLine[equalsIndex + 1:semiColonIndex]
    elif (lineFeedIndex > -1):
      fileFuzzer.requestBoundary = fileLine[equalsIndex + 1:lineFeedIndex]
    else:
      fileFuzzer.requestBoundary = fileLine[equalsIndex + 1:]

  def setFields(self, fileLines):  #type: (FileFuzzerService,str) -> None
    fileFuzzer = self.fileFuzzer
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
        fileFuzzer.raw_info = fileLine
        index += 1
        continue
      elif ((fileLine == EMPTY and not isBody) or (index + 1 == fileLinesLength and not isBody)):
        isBody = True
        fileFuzzer.raw_headers = rawValue
        rawValue = EMPTY
      elif (index + 1 == fileLinesLength):
        rawValue += fileLine + LFN
        fileFuzzer.raw_body = rawValue
        index += 1
        break

      rawValue += fileLine + LFN
      index += 1

  def parseInfo(self):  #type: (FileFuzzerService) -> None
    fileFuzzer = self.fileFuzzer
    rawInfo = fileFuzzer.raw_info.rstrip().split(SPACE)
    fileFuzzer.requestInfo[METHOD] = rawInfo[0]
    fileFuzzer.requestInfo[ENDPOINT] = rawInfo[1]

  def parseHeaders(self):  #type: (FileFuzzerService) -> None
    fileFuzzer = self.fileFuzzer
    rawHeaders = fileFuzzer.raw_headers.rstrip().split(LFN)
    for rawHeader in rawHeaders:
      colonIndex = rawHeader.find(COLON)
      fileFuzzer.requestHeaders[rawHeader[0:colonIndex]] = rawHeader[colonIndex + 1:].strip()

  def parseBody(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> None
    fileFuzzer = self.fileFuzzer
    if (fileFuzzerArgs.postFile):
      rawBodyLines = [(l) for l in fileFuzzer.raw_body.split(LFN) if l and not fileFuzzer.requestBoundary in l
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

        if (fn in rawBodyLine):
          name = rawBodyLine[startName + 1:endName]
          startFileName = rawBodyLine.find(DOUBLE_QUOTE, rawBodyLine.find(fn))
          endFileName = rawBodyLine.find(DOUBLE_QUOTE, startFileName + 1)
          fileName = rawBodyLine[startFileName + 1:endFileName]
          if (ct in rawBodyLines[lineIndex + 1]):
            contentType = rawBodyLines[lineIndex + 1]
            contentTypeValue = contentType[contentType.find(COLON) + 1:]
          fileFuzzer.requestBody[name] = (fileName, open(fileFuzzerArgs.postFile, RB), contentTypeValue)
        elif (cd in rawBodyLine):
          name = rawBodyLine[startName + 1:endName]
          rawValue = EMPTY
          i = lineIndex + 1
          nextLine = rawBodyLines[i]
          while (True):
            rawValue += nextLine
            if (i + 1 == rawBodyLinesLength or cd in rawBodyLines[i + 1]):
              fileFuzzer.requestBody[name] = rawValue
              break
            nextLine += rawBodyLines[i + 1]
      if (not fileFuzzer.requestBody):
        print(
            "Could not parse thw post file specified. Please ensure that the -pf flag is being used with"
            " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
            " flag to send JSON or standard form data.")
        exit()
    else:
      fileFuzzer.requestBody = fileFuzzer.raw_body

  def getFuzzIndicies(self, *fuzzWords):  # type: (FileFuzzerService, str) -> list[int]
    boundRegex = FileFuzzerService.BOUND_REGEX
    fuzzWordsIndicies = []
    for fuzzWord in fuzzWords:
      if fuzzWord:
        fuzzWordsIndicies += re.findall(boundRegex, fuzzWord)
    return fuzzWordsIndicies

  def getBoundlessFuzz(self, *fuzzWords):  # type: (FileFuzzerService, str) -> str
    boundlessRegex = FileFuzzerService.BOUNDLESS_REGEX
    for fuzzWord in fuzzWords:
      boundlessArray = re.findall(boundlessRegex, fuzzWord)
      if (boundlessArray):
        if (len(boundlessArray) > 1):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        return fuzzWord

  def handleBoundless(self, boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey, aVI=None):
    #type: (FileFuzzerService, str, list[int], str | OrderedDict, str, AVI) -> None
    fileFuzzer = self.fileFuzzer
    if (boundlessFuzz):
      boundlessRegex = FileFuzzerService.BOUNDLESS_REGEX
      newValue = re.sub(boundlessRegex, FUZZ + SONE + REGEX_SUB, boundlessFuzz)
      fuzzWordsIndicies.append(SONE)
      if (type(attrValue) == str):
        setattr(fileFuzzer, attrKey, newValue)
      elif (aVI):
        aVIKey = aVI.getAVIKey()
        aVIValue = aVI.getAVIValue()
        fileName = aVI.getFileName()
        contentType = aVI.getContentType()
        if (type(aVIValue) == tuple):
          newFile = None
          if (fileName == boundlessFuzz):
            newFile = (newValue, aVIValue[1], contentType)
          if (contentType == boundlessFuzz):
            newFile = (fileName, aVIValue[1], newValue)
          if (newFile):
            attrValue[aVIKey] = newFile
        elif (type(aVIValue) == str):
          attrValue[aVIKey] = newValue

  def manageLocatorValues(self, fuzzWordsIndicies, existingIndicies, locatorKey, locator):
    #type: (FileFuzzerService, list[int], list[int], str, FuzzLocator) -> None
    if (len(fuzzWordsIndicies) > 0):
      for fuzzWordIndex in fuzzWordsIndicies:
        if (fuzzWordIndex in existingIndicies):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        container = LocatorContainer()
        container.setLocatorKey(locatorKey)
        container.setFuzzWordIndex(fuzzWordIndex)
        locator.getLocatorContainers().append(container)
        existingIndicies.append(container.getFuzzWordIndex())

  def updateFuzzLocator(self, *attrKeys):  # type: (FileFuzzerService, str) -> None
    fileFuzzer = self.fileFuzzer
    locators = fileFuzzer.fuzzLocators
    existingIndicies = []

    for attrKey in attrKeys:
      attrValue = getattr(fileFuzzer, attrKey)
      locator = Cast._from(getattr(locators, attrKey), FuzzLocator)
      if (type(attrValue) == str):
        fuzzWordsIndicies = self.getFuzzIndicies(attrValue)
        boundlessFuzz = self.getBoundlessFuzz(attrValue)
        self.handleBoundless(boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey)
        self.manageLocatorValues(fuzzWordsIndicies, existingIndicies, attrKey, locator)
      elif (type(attrValue) == OrderedDict):
        aVI = OrderedDict(attrValue).items()
        for aVIKey, aVIValue in aVI:
          fuzzWord = fileName = contentType = EMPTY
          if (type(aVIValue) == tuple):
            fileName = aVIValue[0]
            contentType = aVIValue[2]
          elif (type(aVIValue) == str):
            fuzzWord = aVIValue
          fuzzWordsIndicies = self.getFuzzIndicies(fuzzWord, fileName, contentType)
          boundlessFuzz = self.getBoundlessFuzz(fuzzWord, fileName, contentType)
          aVI = AVI(aVIKey, aVIValue, fileName, contentType)
          self.handleBoundless(boundlessFuzz, fuzzWordsIndicies, attrValue, None, aVI)
          self.manageLocatorValues(fuzzWordsIndicies, existingIndicies, aVIKey, locator)

  def parseFile(self, fileFuzzerArgs):
    # type: (FileFuzzerService, FileFuzzerArgs) -> None
    inputFile = open(fileFuzzerArgs.inputFile, LR)
    fileLines = inputFile.readlines()

    self.fileFuzzer.remoteHost = fileFuzzerArgs.remoteHost
    self.setFields(fileLines)
    self.parseInfo()
    self.parseHeaders()
    self.parseBody(fileFuzzerArgs)
    attrKeys = ["remoteHost", "requestInfo", "requestHeaders", "requestBody"]
    self.updateFuzzLocator(*attrKeys)

  def printRequest(self):  # type: (FileFuzzerService) -> None
    fileFuzzer = self.fileFuzzer
    format = '{}: {}'

    info = []
    for infoKey, infoValue in fileFuzzer.requestInfo.items():
      info.append(format.format(infoKey, infoValue))

    headers = []
    for headersKey, headersValue in fileFuzzer.requestHeaders.items():
      headers.append(format.format(headersKey, headersValue))

    body = []
    if (type(fileFuzzer.requestBody) == str):
      body.append(fileFuzzer.requestBody)
    else:
      for k, v in fileFuzzer.requestBody.items():
        body.append(format.format(k, v))

    print('{}{}{}{}{}{}{}{}{}{}{}'.format(LFRN, '-----------Request Start-----------',
                                          LFRN, LFRN.join(info), LFRN, LFRN.join(headers), LFRN,
                                          LFRN.join(body), LFRN, '----------- Request End ------------',
                                          LFRN))

  def getAllLocatorsContainers(self):  # type: (FileFuzzerService) -> int
    locators = self.fileFuzzer.fuzzLocators
    rhostContainers = locators.getRemoteHost().getLocatorContainers()
    infoContainers = locators.getRequestInfo().getLocatorContainers()
    headersContainers = locators.getRequestHeaders().getLocatorContainers()
    bodyContainers = locators.getRequestBody().getLocatorContainers()
    return rhostContainers + infoContainers + headersContainers + bodyContainers

  def getFuzzHelpers(self):  # type: (FileFuzzerService) -> list
    fileFuzzer = self.fileFuzzer
    locators = vars(fileFuzzer.fuzzLocators)
    fuzzHelpers = []
    for locatorField in locators:
      locator = Cast._from(locators[locatorField], FuzzLocator)
      containers = locator.getLocatorContainers()
      for container in containers:
        fuzzHelper = FuzzHelper()
        fuzzHelper.setFuzzWordIndex(int(container.getFuzzWordIndex()))
        fuzzHelper.setAttrKey(locatorField)
        fuzzHelper.setLocatorKey(container.getLocatorKey())
        attrValue = getattr(fileFuzzer, locatorField)
        if (type(attrValue) == str):
          fuzzHelper.setOriginalAttrValue(attrValue)
        else:
          fuzzHelper.setOriginalAttrValue(attrValue[fuzzHelper.getLocatorKey()])
        fuzzHelpers.append(fuzzHelper)
    return fuzzHelpers

  def parseUrl(self, host, secure, endpoint=EMPTY):  #type: (FileFuzzerService, str, bool, str) -> str
    standardProtocol = HTTP
    if (standardProtocol in host):
      return "{}{}".format(host, endpoint)
    else:
      protocol = HTTP_PROTOCOL
      if (secure):
        protocol = HTTPS_PROTOCOL
      return "{}{}{}".format(protocol, host, endpoint)

  def getRequestBody(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> OrderedDict | str
    fileFuzzer = self.fileFuzzer
    if (fileFuzzerArgs.postFile):
      return MultipartEncoder(fields=fileFuzzer.requestBody, boundary=fileFuzzer.requestBoundary)
    return fileFuzzer.requestBody

  def getProxies(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> dict
    proxies = {}
    if (fileFuzzerArgs.httpProxy):
      proxies[HTTP] = self.parseUrl(fileFuzzerArgs.httpProxy, False)
    elif (fileFuzzerArgs.httpsProxy):
      proxies[HTTPS] = self.parseUrl(fileFuzzerArgs.httpsProxy, True)
    return proxies

  def handleResponse(self, response, fileFuzzerArgs):
    #type: (FileFuzzerService, requests.models.Response, FileFuzzerArgs) -> None
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
      responseString += " - Fuzz text: {}".format(self.fileFuzzer.FuzzValuesString)
    if (fileFuzzerArgs.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def sendRequest(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> None
    fileFuzzer = self.fileFuzzer
    requestHost = fileFuzzer.remoteHost
    requestInfo = fileFuzzer.requestInfo
    requestHeaders = fileFuzzer.requestHeaders
    requestBody = self.getRequestBody(fileFuzzerArgs)
    requestUrl = self.parseUrl(requestHost, fileFuzzerArgs.secure, requestInfo[ENDPOINT])
    fileFuzzer.requestUrl = requestUrl

    req = requests.Request(requestInfo[METHOD], requestUrl, headers=requestHeaders, data=requestBody)
    prepared = req.prepare()
    session = requests.Session()
    session.proxies = self.getProxies(fileFuzzerArgs)
    session.verify = not fileFuzzerArgs.disableVerification
    response = session.send(prepared, timeout=fileFuzzerArgs.readTimeout)
    self.handleResponse(response, fileFuzzerArgs)

  def swapFuzz(self, fuzzValues, fuzzHelpers):
    #type: (FileFuzzerService, list[str], list[FuzzHelper]) -> None
    fileFuzzer = self.fileFuzzer
    for fuzzHelper in fuzzHelpers:
      fuzzWordIndex = fuzzHelper.getFuzzWordIndex()
      fuzzWord = FUZZ + str(fuzzWordIndex)
      fuzzValue = fuzzValues[fuzzWordIndex - 1].rstrip()
      attrKey = fuzzHelper.getAttrKey()
      attrValue = getattr(fileFuzzer, attrKey)
      if (type(attrValue) == str):
        setattr(fileFuzzer, attrKey, str(attrValue).replace(fuzzWord, fuzzValue))
        continue
      locatorKey = fuzzHelper.getLocatorKey()
      requestValue = attrValue[locatorKey]
      if (isinstance(requestValue, tuple)):
        fileName = str(requestValue[0])
        content = requestValue[1]
        contentType = str(requestValue[2])
        if (fuzzWord in fileName):
          newValue = fileName.replace(fuzzWord, fuzzValue)
          attrValue[locatorKey] = (newValue, content, contentType)
        elif (fuzzWord in contentType):
          newValue = contentType.replace(fuzzWord, fuzzValue)
          attrValue[locatorKey] = (fileName, content, newValue)
      elif (isinstance(requestValue, str)):
        attrValue[locatorKey] = str(requestValue).replace(fuzzWord, fuzzValue)

  def swapBack(self, fuzzHelpers):  #type: (FileFuzzerService, list[FuzzHelper]) -> None
    fileFuzzer = self.fileFuzzer
    for fuzzHelper in fuzzHelpers:
      attrKey = fuzzHelper.getAttrKey()
      currentAttrValue = getattr(fileFuzzer, attrKey)
      originalAttrValue = fuzzHelper.getOriginalAttrValue()
      if (type(currentAttrValue) == str):
        setattr(fileFuzzer, attrKey, originalAttrValue)
        continue
      locatorKey = fuzzHelper.getLocatorKey()
      currentAttrValue[locatorKey] = originalAttrValue

  def fuzzRequest(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> None
    fuzzValuesFile = open(fileFuzzerArgs.fuzzFile, "r")
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

  def processRequest(self, fileFuzzerArgs):  #type: (FileFuzzerService, FileFuzzerArgs) -> None
    if (len(self.getAllLocatorsContainers()) > 0):
      print("Fuzzing Request")
      self.fuzzRequest(fileFuzzerArgs)
    else:
      print("Sending Request")
      self.sendRequest(fileFuzzerArgs)
