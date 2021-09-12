# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Parser Service

import re
from collections import OrderedDict

from watchdogs.io.parsers import FileArgs
from watchdogs.base.models import AllArgs, Common
from watchdogs.web.models import WebFile
from watchdogs.web.parsers import RequestArgs
from watchdogs.web.models.Requests import Request
from watchdogs.utils.Constants import (EMPTY, HTTP, LFN, LFR, LR, SPACE, CONTENT_DISPOSITION, CONTENT_TYPE,
                                       FILE_NAME, RB)


class RequestParserService(Common):

  BOUNDARY_REGEX = r'boundary=([-a-zA-Z0-9]*)(?:$| )'
  KEY_REGEX = r'([-a-zA-Z0-9]+):'
  VALUE_REGEX = r':(.*)'
  NAME_REGEX = r' name="([^"]*)'
  FILENAME_REGEX = r' filename="([^"]*)'

  def __init__(self):  #type: () -> None
    super(RequestParserService, self).__init__()

  def setBoundary(self, request, fileLine):  #type: (Request, str) -> bool
    matchedBoundary = re.search(RequestParserService.BOUNDARY_REGEX, fileLine)
    if (matchedBoundary):
      request.setRequestBoundary(matchedBoundary.group(1))
      return True
    return False

  def isLineFeed(self, string):  #type: (str) -> bool
    return string == LFN or string == LFR

  def setFields(self, request, fileLines):  #type: (Request, str) -> None
    fileLinesLength = len(fileLines)
    index = 0
    rawValue = EMPTY
    isBody = False
    boundarySet = False

    while (index < fileLinesLength):
      fileLine = fileLines[index]
      isLastIndex = index + 1 == fileLinesLength

      if (not boundarySet):
        boundarySet = self.setBoundary(request, fileLine)
      if (index == 0):
        if (HTTP.upper() not in fileLine):
          print("Please check file format and ensure that the first line contains the method,"
                " endpoint and protocol.")
          raise Exception("Illegal file format")
        request.setRawInfo(fileLine.strip())
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

  def parseInfo(self, requestArgs, request):  #type: (RequestArgs, Request) -> None
    rawInfo = request.getRawInfo()

    requestInfo = request.getRequestInfo()
    rawInfoSplit = rawInfo.rstrip().split(SPACE)

    requestInfo.setUrlHost(requestArgs.remoteHost)
    requestInfo.setMethod(rawInfoSplit[0])
    requestInfo.setEndpoint(rawInfoSplit[1])

    request.setRequestInfo(requestInfo)

  def parseHeaders(self, request):  #type: (Request) -> None
    requestHeaders = request.getRequestHeaders()
    rawHeadersSplit = request.getRawHeaders().rstrip().split(LFN)

    for rawHeader in rawHeadersSplit:
      matchedKey = re.search(RequestParserService.KEY_REGEX, rawHeader)
      if (not matchedKey):
        continue

      matchedValue = re.search(RequestParserService.VALUE_REGEX, rawHeader)
      if (not matchedValue):
        continue

      headerKey = matchedKey.group(1)
      headerValue = matchedValue.group(1).strip()
      requestHeaders[headerKey] = headerValue

    request.setRequestHeaders(requestHeaders)

  def getRawBodyFiltered(self, request):  #type: (Request) -> list[str]
    rawBodyLines = request.getRawBody().split(LFN)
    requestBoundary = request.getRequestBoundary()
    filteredLines = []
    for rawBodyLine in rawBodyLines:
      if (rawBodyLine and not requestBoundary in rawBodyLine):
        filteredLines.append(rawBodyLine)
    return filteredLines

  def addWebFile(self, rawBodyLines, lineIndex, requestArgs, requestBody):
    #type: (list[str], int, RequestArgs, OrderedDict) -> None
    rawBodyLine = rawBodyLines[lineIndex]
    nameValue = re.search(RequestParserService.NAME_REGEX, rawBodyLine).group(1)
    fileNameValue = re.search(RequestParserService.FILENAME_REGEX, rawBodyLine).group(1)
    contentTypeValue = None
    nextLine = rawBodyLines[lineIndex + 1]
    if (CONTENT_TYPE in nextLine):
      contentTypeValue = re.search(RequestParserService.VALUE_REGEX, nextLine).group(1)
    webFile = (fileNameValue, open(requestArgs.postFile, RB), contentTypeValue)
    requestBody[nameValue] = WebFile(webFile)

  def addDispositionValues(self, rawBodyLines, lineIndex, requestBody):
    #type: (list[str], int, OrderedDict) -> None
    rawBodyLine = rawBodyLines[lineIndex]
    nameValue = re.search(RequestParserService.NAME_REGEX, rawBodyLine).group(1)
    dispositionValue = EMPTY
    nextIndex = lineIndex + 1
    rawBodyLinesLength = len(rawBodyLines)
    while (True):
      dispositionValue += rawBodyLines[nextIndex] + LFN
      nextLine = EMPTY
      nextIndex += 1
      if (nextIndex < rawBodyLinesLength):
        nextLine = rawBodyLines[nextIndex]
      if (nextIndex == rawBodyLinesLength or CONTENT_DISPOSITION in nextLine):
        requestBody[nameValue] = dispositionValue.rstrip()
        break

  def parseBody(self, requestArgs, request):  #type: (RequestArgs, Request) -> None
    if (requestArgs.postFile):
      rawBodyLines = self.getRawBodyFiltered(request)
      rawBodyLinesLength = len(rawBodyLines)

      for lineIndex in range(rawBodyLinesLength):
        rawBodyLine = rawBodyLines[lineIndex]
        requestBody = request.getRequestBodyDict()

        if (FILE_NAME in rawBodyLine):
          self.addWebFile(rawBodyLines, lineIndex, requestArgs, requestBody)
        elif (CONTENT_DISPOSITION in rawBodyLine):
          self.addDispositionValues(rawBodyLines, lineIndex, requestBody)
        request.setRequestBodyDict(requestBody)

      if (not request.getRequestBodyDict()):
        print(
            "Could not parse the post file specified. Please ensure that the -pf flag is being used with"
            " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
            " flag to send JSON or standard form data.")
        exit()
    else:
      request.setRequestBodyString(request.getRawBody())

  def parseFile(self, allArgs):  # type: (AllArgs) -> Request
    requestArgs = allArgs.getArgs(RequestArgs)
    inputFile = open(allArgs.getArgs(FileArgs).getInputFile(), LR)
    inptFileLines = inputFile.readlines()

    request = Request()
    self.setFields(request, inptFileLines)
    self.parseInfo(requestArgs, request)
    self.parseHeaders(request)
    self.parseBody(requestArgs, request)

    return request