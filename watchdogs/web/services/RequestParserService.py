# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Parser Service

import re
from watchdogs.io.parsers import FileArgs

from watchdogs.base.models import AllArgs, Common
from watchdogs.web.models import WebFile
from watchdogs.web.parsers import RequestArgs
from watchdogs.web.models.Requests import Request
from watchdogs.utils.Constants import (EMPTY, LFN, LFR, LR, SPACE, CONTENT_DISPOSITION, CONTENT_TYPE,
                                       FILE_NAME, RB)


class RequestParserService(Common):

  BOUNDARY_REGEX = r'boundary=([-a-zA-Z0-9]*)(?:$| )'
  KEY_REGEX = r'([-a-zA-Z0-9]+):'
  VALUE_REGEX = r':(.*)'
  NAME_REGEX = r' name="([^"]*)'
  FILENAME_REGEX = r' filename="([^"]*)'

  def __init__(self, request=Request()):  #type: (Request) -> None
    super(RequestParserService, self).__init__()
    self.__request = request

  def getRequest(self):  #type: () -> Request
    return self.__request

  def setRequest(self, request):  #type: (Request) -> None
    self.__request = request

  def setBoundary(self, fileLine):  #type: (str) -> bool
    matchedBoundary = re.search(RequestParserService.BOUNDARY_REGEX, fileLine)
    if (matchedBoundary):
      self.__request.setRequestBoundary(matchedBoundary.group(1))
      return True
    return False

  def isLineFeed(self, string):  #type: (str) -> bool
    return string == LFN or string == LFR

  def setFields(self, fileLines):  #type: (str) -> None
    fileLinesLength = len(fileLines)
    index = 0
    request = self.__request
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

  def parseInfo(self, requestArgs):  #type: (RequestArgs) -> None
    request = self.__request
    rawInfo = request.getRawInfo()

    requestInfo = request.getRequestInfo()
    rawInfoSplit = rawInfo.rstrip().split(SPACE)

    requestInfo.setUrlHost(requestArgs.remoteHost)
    requestInfo.setMethod(rawInfoSplit[0])
    requestInfo.setEndpoint(rawInfoSplit[1])

    request.setRequestInfo(requestInfo)

  def parseHeaders(self):  #type: () -> None
    request = self.__request
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

  def getRawBodyFiltered(self):  #type: () -> list[str]
    request = self.__request
    rawBodyLines = request.getRawBody().split(LFN)
    requestBoundary = request.getRequestBoundary()
    filteredLines = []
    for rawBodyLine in rawBodyLines:
      if (rawBodyLine and not requestBoundary in rawBodyLine):
        filteredLines.append(rawBodyLine)
    return filteredLines

  def parseBody(self, requestArgs):  #type: (RequestArgs) -> None
    request = self.__request
    if (requestArgs.postFile):
      rawBodyLines = self.getRawBodyFiltered()
      rawBodyLinesLength = len(rawBodyLines)

      for lineIndex in range(rawBodyLinesLength):
        rawBodyLine = rawBodyLines[lineIndex]
        requestBody = request.getRequestBody()

        if (FILE_NAME in rawBodyLine):
          nameValue = re.search(RequestParserService.NAME_REGEX, rawBodyLine).group(1)
          fileNameValue = re.search(RequestParserService.FILENAME_REGEX, rawBodyLine).group(1)
          contentTypeValue = None
          nextLine = rawBodyLines[lineIndex + 1]
          if (CONTENT_TYPE in nextLine):
            contentTypeValue = re.search(RequestParserService.VALUE_REGEX, nextLine).group(1)
          webFile = (fileNameValue, open(requestArgs.postFile, RB), contentTypeValue)
          requestBody[nameValue] = WebFile(webFile)
        elif (CONTENT_DISPOSITION in rawBodyLine):
          nameValue = re.search(RequestParserService.NAME_REGEX, rawBodyLine).group(1)
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

  def parseFile(self, allArgs):  # type: (AllArgs) -> RequestParserService
    requestArgs = allArgs.getArgs(RequestArgs)
    inputFile = open(allArgs.getArgs(FileArgs).getInputFile(), LR)
    inptFileLines = inputFile.readlines()

    self.setFields(inptFileLines)
    self.parseInfo(requestArgs)
    self.parseHeaders()
    self.parseBody(requestArgs)

    return self