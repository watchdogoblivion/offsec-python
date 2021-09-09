# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import re
import copy
import requests
from bs4 import BeautifulSoup
from typing import Any, Callable
from collections import OrderedDict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from watchdogs.utils import Cast
from watchdogs.base.models import Common
from watchdogs.web.models import FileFuzzer
from watchdogs.web.parsers import FileFuzzerArgs
from watchdogs.web.models.WebFile import WebFile
from watchdogs.web.models.Locators import (VariantLocator, LocatorDatum)
from watchdogs.utils.Constants import (EMPTY, LFN, LFR, SPACE, CONTENT_DISPOSITION, CONTENT_TYPE, FILE_NAME,
                                       RB, FUZZ, SONE, REGEX_SUB, LR, LFRN, HTTP, HTTP_PROTOCOL,
                                       HTTPS_PROTOCOL, HTTPS, HTML_PARSER, CONTENT_LENGTH, UTF8)


class FileFuzzerService(Common):

  VERSION = "1.0"

  BOUNDARY_REGEX = r'boundary=([-a-zA-Z0-9]*)(?:$| )'
  KEY_REGEX = r'([-a-zA-Z0-9]+):'
  VALUE_REGEX = r':(.*)'
  NAME_REGEX = r' name="([^"]*)'
  FILENAME_REGEX = r' filename="([^"]*)'
  UNNUMBERED_REGEX = r'(?:FUZZ)($|[^0-9])'
  NUMBERED_REGEX = r'FUZZ([0-9]+)'
  DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1"

  def __init__(self, fileFuzzer=FileFuzzer()):  #type: (FileFuzzer) -> None
    super(FileFuzzerService, self).__init__()
    self.__fileFuzzer = fileFuzzer

  def setBoundary(self, fileLine):  #type: (str) -> bool
    matchedBoundary = re.search(FileFuzzerService.BOUNDARY_REGEX, fileLine)
    if (matchedBoundary):
      self.__fileFuzzer.getRequest().setRequestBoundary(matchedBoundary.group(1))
      return True
    return False

  def isLineFeed(self, string):  #type: (str) -> bool
    return string == LFN or string == LFR

  def setFields(self, fileLines):  #type: (str) -> None
    fileLinesLength = len(fileLines)
    index = 0
    request = self.__fileFuzzer.getRequest()
    rawValue = EMPTY
    isBody = False
    boundarySet = False

    while (index < fileLinesLength):
      fileLine = fileLines[index]
      isLastIndex = index + 1 == fileLinesLength

      if (not boundarySet):
        boundarySet = self.setBoundary(fileLine)
      if (index == 0):
        request.setRawInfo(fileLine)
        index += 1
        continue
      elif ((self.isLineFeed(fileLine) and not isBody) or (isLastIndex and not isBody)):
        isBody = True
        request.setRawHeaders(rawValue)
        rawValue = EMPTY
      elif (isLastIndex):
        rawValue += fileLine + LFN
        request.setRawBody(rawValue)
        index += 1

      rawValue += fileLine + LFN
      index += 1

  def parseInfo(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    request = self.__fileFuzzer.getRequest()
    rawInfo = request.getRawInfo()

    requestInfo = request.getRequestInfo()
    rawInfoSplit = rawInfo.rstrip().split(SPACE)

    requestInfo.setUrlHost(fileFuzzerArgs.remoteHost)
    requestInfo.setMethod(rawInfoSplit[0])
    requestInfo.setEndpoint(rawInfoSplit[1])

    request.setRequestInfo(requestInfo)

  def parseHeaders(self):  #type: () -> None
    request = self.__fileFuzzer.getRequest()
    requestHeaders = request.getRequestHeaders()
    rawHeadersSplit = request.getRawHeaders().rstrip().split(LFN)

    for rawHeader in rawHeadersSplit:
      matchedKey = re.search(FileFuzzerService.KEY_REGEX, rawHeader)
      if (not matchedKey):
        continue

      matchedValue = re.search(FileFuzzerService.VALUE_REGEX, rawHeader)
      if (not matchedValue):
        continue

      headerKey = matchedKey.group(1)
      headerValue = matchedValue.group(1).strip()
      requestHeaders[headerKey] = headerValue

    request.setRequestHeaders(requestHeaders)

  def getRawBodyFiltered(self):  #type: () -> list[str]
    request = self.__fileFuzzer.getRequest()
    rawBodyLines = request.getRawBody().split(LFN)
    requestBoundary = request.getRequestBoundary()
    filteredLines = []
    for rawBodyLine in rawBodyLines:
      if (rawBodyLine and not requestBoundary in rawBodyLine):
        filteredLines.append(rawBodyLine)
    return filteredLines

  def parseBody(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    request = self.__fileFuzzer.getRequest()
    if (fileFuzzerArgs.postFile):
      rawBodyLines = self.getRawBodyFiltered()
      rawBodyLinesLength = len(rawBodyLines)

      for lineIndex in range(rawBodyLinesLength):
        rawBodyLine = rawBodyLines[lineIndex]
        requestBody = request.getRequestBody()

        if (FILE_NAME in rawBodyLine):
          nameValue = re.search(FileFuzzerService.NAME_REGEX, rawBodyLine).group(1)
          fileNameValue = re.search(FileFuzzerService.FILENAME_REGEX, rawBodyLine).group(1)
          contentTypeValue = None
          nextLine = rawBodyLines[lineIndex + 1]
          if (CONTENT_TYPE in nextLine):
            contentTypeValue = re.search(FileFuzzerService.VALUE_REGEX, nextLine).group(1)
          webFile = (fileNameValue, open(fileFuzzerArgs.postFile, RB), contentTypeValue)
          requestBody[nameValue] = WebFile(webFile)
        elif (CONTENT_DISPOSITION in rawBodyLine):
          nameValue = re.search(FileFuzzerService.NAME_REGEX, rawBodyLine).group(1)
          dispositionValue = EMPTY
          nextIndex = lineIndex + 1
          while (True):
            dispositionValue += rawBodyLines[nextIndex]
            nextLine = EMPTY
            nextIndex += 1
            if (nextIndex < rawBodyLinesLength):
              nextLine = rawBodyLines[nextIndex]
            if (nextIndex == rawBodyLinesLength or CONTENT_DISPOSITION in nextLine):
              requestBody[nameValue] = dispositionValue
              break
        request.setRequestBody(requestBody)
      if (not request.getRequestBody()):
        print(
            "Could not parse the post file specified. Please ensure that the -pf flag is being used with"
            " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
            " flag to send JSON or standard form data.")
        exit()
    else:
      request.setRequestBody(request.getRawBody())

  def getIndiciesOfSubstitutes(self, *fuzzWords):  # type: (str) -> list[int]
    stringIndicies = []
    for fuzzWord in fuzzWords:
      if fuzzWord:
        stringIndicies += re.findall(FileFuzzerService.NUMBERED_REGEX, fuzzWord)
    indiciesOfSubstitutes = map(int, stringIndicies)
    return indiciesOfSubstitutes

  def getUnnumberedFuzz(self, *fuzzWords):  # type: (str) -> str
    for fuzzWord in fuzzWords:
      unnumberedArray = re.findall(FileFuzzerService.UNNUMBERED_REGEX, fuzzWord)
      if unnumberedArray:
        if (len(unnumberedArray) > 1):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        return fuzzWord

  def handleUnnumbered(self, unnumberedFuzz, indiciesOfSubstitutes, requestObject, setNewValue,
                       requestKey=None):
    #type: (str, list[int], Any, Callable, str) -> None
    if unnumberedFuzz:
      UNNUMBERED_REGEX = FileFuzzerService.UNNUMBERED_REGEX
      newValue = re.sub(UNNUMBERED_REGEX, FUZZ + SONE + REGEX_SUB, unnumberedFuzz)
      indiciesOfSubstitutes.append(1)
      if (type(requestObject) == OrderedDict and requestKey):
        requestObject[requestKey] = newValue
      else:
        setNewValue(newValue)

  def updateLocatorData(self, indiciesOfSubstitutes, existingIndicies, variantLocator, requestKey=None):
    #type: (list[int], list, VariantLocator, str) -> None
    if (len(indiciesOfSubstitutes) > 0):
      for indexOfSubstitute in indiciesOfSubstitutes:
        if (indexOfSubstitute in existingIndicies):
          print(FileFuzzerService.DUPLICATE_MESSAGE)
        locatorDatum = LocatorDatum()
        locatorDatum.setIndexOfSubstitute(indexOfSubstitute)

        if (variantLocator.isInfo()):
          locatorDatum.setIsInfo(True)
        elif (variantLocator.isHeader()):
          locatorDatum.setHeaderKey(requestKey)
        elif (variantLocator.isBody()):
          locatorDatum.setBodyKey(requestKey)

        variantLocator.getLocatorData().append(locatorDatum)
        existingIndicies.append(locatorDatum.getIndexOfSubstitute())

  def updateFuzzLocators(self):  # type: () -> None
    fileFuzzer = self.__fileFuzzer
    request = fileFuzzer.getRequest()
    fuzzLocators = fileFuzzer.rebaseLocators()
    indiciesOfSubstitutes = []
    existingIndicies = []
    request = self.__fileFuzzer.getRequest()

    for fuzzLocator in fuzzLocators:
      if (fuzzLocator.isInfo()):
        requestInfo = request.getRequestInfo()

        urlHost = requestInfo.getUrlHost()
        indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(urlHost)
        unnumberedFuzz = self.getUnnumberedFuzz(urlHost)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestInfo, requestInfo.setUrlHost)

        endpoint = requestInfo.getEndpoint()
        indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(endpoint)
        unnumberedFuzz = self.getUnnumberedFuzz(endpoint)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestInfo, requestInfo.setEndpoint)

        self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, fuzzLocator)
        request.setRequestInfo(requestInfo)
      elif (fuzzLocator.isHeader()):
        requestHeaders = request.getRequestHeaders()

        requestHeaderItems = OrderedDict(requestHeaders).items()
        for requestHeaderKey, requestHeaderValue in requestHeaderItems:
          fuzzWord = requestHeaderValue
          indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fuzzWord)
          unnumberedFuzz = self.getUnnumberedFuzz(fuzzWord)
          self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestHeaders, None, requestHeaderKey)
          self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, fuzzLocator, requestHeaderKey)
          request.setRequestHeaders(requestHeaders)
      elif (fuzzLocator.isBody()):
        requestBody = request.getRequestBody()

        requestBodyItems = OrderedDict(requestBody).items()
        for requestBodyKey, requestBodyValue in requestBodyItems:
          fuzzWord = fileName = contentType = EMPTY
          webFile = None
          if (type(requestBodyValue) == WebFile):
            webFile = Cast._to(WebFile, requestBodyValue)
            fileName = webFile.getFileName()
            contentType = webFile.getContentType()
          elif (type(requestBodyValue) == str):
            fuzzWord = requestBodyValue

          if (fuzzWord):
            indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fuzzWord, fileName, contentType)
            unnumberedFuzz = self.getUnnumberedFuzz(fuzzWord, fileName, contentType)
            self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBody, None, requestBodyKey)

          if (webFile):
            indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fileName)
            unnumberedFuzz = self.getUnnumberedFuzz(fileName)
            self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBody, webFile.setFileName)

            indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(contentType)
            unnumberedFuzz = self.getUnnumberedFuzz(contentType)
            self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBody, webFile.setContentType)

          self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, fuzzLocator, requestBodyKey)
          request.setRequestBody(requestBody)

  def parseFile(self, fileFuzzerArgs):  # type: (FileFuzzerArgs) -> None
    inputFile = open(fileFuzzerArgs.getInputFile(), LR)
    inptFileLines = inputFile.readlines()

    self.setFields(inptFileLines)
    self.parseInfo(fileFuzzerArgs)
    self.parseHeaders()
    self.parseBody(fileFuzzerArgs)
    self.updateFuzzLocators()

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

  def getAllVariantsLocatorData(self):  # type: () -> list[LocatorDatum]
    variantLocators = self.__fileFuzzer.getVariantLocators()
    allVariantsLocatorData = []

    for variantLocator in variantLocators:
      allVariantsLocatorData += variantLocator.getLocatorData()

    return allVariantsLocatorData

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
    if (fileFuzzerArgs.showSubstitutes):
      responseString += " - Fuzz text: {}".format(self.__fileFuzzer.getFuzzSubstitutes())
    if (fileFuzzerArgs.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def sendRequest(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    request = self.__fileFuzzer.getRequest()
    requestInfo = request.getRequestInfo()
    requestHeaders = request.getRequestHeaders()
    requestBody = self.getRequestBody(fileFuzzerArgs)
    requestUrl = self.parseUrl(requestInfo.getUrlHost(), fileFuzzerArgs.secure, requestInfo.getEndpoint())
    request.setRequestUrl(requestUrl)

    req = requests.Request(requestInfo.getMethod(), requestUrl, headers=requestHeaders, data=requestBody)
    prepared = req.prepare()
    session = requests.Session()
    session.proxies = self.getProxies(fileFuzzerArgs)
    session.verify = not fileFuzzerArgs.disableVerification
    response = session.send(prepared, timeout=fileFuzzerArgs.readTimeout)
    self.handleResponse(response, fileFuzzerArgs)

  def swapFuzz(self, fuzzSubstitutes, variantsLocatorData):  #type: (list[str], list[LocatorDatum]) -> None
    request = self.__fileFuzzer.getRequest()

    for locatorDatum in variantsLocatorData:
      indexOfSubstitute = locatorDatum.getIndexOfSubstitute()
      fuzzWord = FUZZ + str(indexOfSubstitute)
      substitute = fuzzSubstitutes[indexOfSubstitute - 1].rstrip()

      if (locatorDatum.isInfo()):
        #Info
        requestInfo = request.getRequestInfo()

        newEndpointValue = str(requestInfo.getEndpoint()).replace(fuzzWord, substitute)
        requestInfo.setEndpoint(newEndpointValue)

        newUrlValue = str(requestInfo.getUrlHost()).replace(fuzzWord, substitute)
        requestInfo.setUrlHost(newUrlValue)

        request.setRequestInfo(requestInfo)
      elif (locatorDatum.getHeaderKey()):
        #Headers
        headerKey = locatorDatum.getHeaderKey()
        headers = request.getRequestHeaders()
        headerValue = headers[headerKey]
        headers[headerKey] = str(headerValue).replace(fuzzWord, substitute)
        request.setRequestHeaders(headers)
      elif (locatorDatum.getBodyKey()):
        #Body
        bodyKey = locatorDatum.getBodyKey()
        requestBody = request.getRequestBody()
        bodyValue = requestBody[bodyKey]
        if (isinstance(bodyValue, WebFile)):
          webFile = copy.copy(Cast._to(WebFile, bodyValue))
          fileName = webFile.getFileName()
          contentType = webFile.getContentType()
          if (fuzzWord in fileName):
            newValue = fileName.replace(fuzzWord, substitute)
            webFile.setFileName(newValue)
          elif (fuzzWord in contentType):
            newValue = contentType.replace(fuzzWord, substitute)
            webFile.setContentType(newValue)
          requestBody[bodyKey] = webFile
        elif (isinstance(bodyValue, str)):
          requestBody[bodyKey] = str(bodyValue).replace(fuzzWord, substitute)
        request.setRequestBody(requestBody)

  def fuzzRequest(self, fileFuzzerArgs, allVariantsLocatorData):
    #type: (FileFuzzerArgs, list[LocatorDatum]) -> None
    request = self.__fileFuzzer.getRequest()
    request.updateOriginalValues()
    fuzzSubstitutesFile = open(fileFuzzerArgs.substitutesFile, LR)
    fuzzSubstitutesLines = fuzzSubstitutesFile.readlines()

    for fuzzSubstitutesLine in fuzzSubstitutesLines:
      fuzzSubstitutes = fuzzSubstitutesLine.split(fileFuzzerArgs.substitutesDelimiter)
      self.swapFuzz(fuzzSubstitutes, allVariantsLocatorData)
      self.sendRequest(fileFuzzerArgs)
      request.resetRequestValues()

  def processRequest(self, fileFuzzerArgs):  #type: (FileFuzzerArgs) -> None
    allVariantsLocatorData = self.getAllVariantsLocatorData()
    if (len(allVariantsLocatorData) > 0):
      print("Fuzzing Request")
      self.fuzzRequest(fileFuzzerArgs, allVariantsLocatorData)
    else:
      print("Sending Request")
      self.sendRequest(fileFuzzerArgs)