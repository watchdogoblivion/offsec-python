# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import re
import argparse
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from watchdogs.io import File
from watchdogs.web.Locators import *
from watchdogs.utils import Cast
from watchdogs.utils.Constants import (EMPTY, COLON, EQUAL, SEMI_COLON, LFN, BOUNDARY, DASH, SPACE, METHOD,
                                       ENDPOINT, CONTENT_DISPOSITION, CONTENT_TYPE, FILE_NAME, DOUBLE_QUOTE,
                                       NAME, RB, FUZZ, SONE, REGEX_SUB, LR, HOST, INFO, HEADER, LS, BODY,
                                       LFRN, HTTP, HTTP_PROTOCOL, HTTPS_PROTOCOL, HTTPS, HTML_PARSER,
                                       CONTENT_LENGTH, T, UTF8)


class FileFuzzer(File, Common):

  VERSION = "1.0"
  BOUNDLESS_REGEX = r'(?:FUZZ)($|[^0-9])'
  BOUND_REGEX = r'FUZZ([0-9]+)'
  DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1"

  def __init__(self):
    super(FileFuzzer, self).__init__()
    self.requestFields = []  #type: list[str]
    self.remoteHost = EMPTY  #type: str
    self.secure = False  #type: bool
    self.raw_info = EMPTY  #type: str
    self.raw_headers = EMPTY  #type: str
    self.raw_body = EMPTY  #type: str
    self.requestInfo = OrderedDict()  #type: OrderedDict
    self.requestUrl = EMPTY  #type: str
    self.requestHeaders = OrderedDict()  #type: OrderedDict
    self.requestBoundary = EMPTY  #type: str
    self.requestBody = OrderedDict()  #type: OrderedDict
    self.postFile = EMPTY  #type: str
    self.fuzzLocators = FuzzLocators()  #type: FuzzLocators
    self.fuzzFile = EMPTY  #type: str
    self.fuzzDelimiter = COLON  #type: str
    self.httpProxy = EMPTY  #type: str
    self.httpsProxy = EMPTY  #type: str
    self.disableVerification = False  #type: bool
    self.readTimeout = None  #type: int
    self.filterLength = EMPTY  #type: str
    self.filterStatus = EMPTY  #type: str
    self.filterIn = EMPTY  #type: str
    self.filterOut = EMPTY  #type: str
    self.showResponse = False  #type: bool
    self.showFuzz = False  #type: bool
    self.FuzzValuesString = EMPTY  #type: str

  def __setattr__(self, name, value):  #type: (FileFuzzer, str, T) -> T
    super(FileFuzzer, self).__setattr__(name, value)

    requestFields = self.requestFields if hasattr(self, "requestFields") else None
    if (not requestFields == None) and (not name in requestFields):
      if name.find("raw_") > -1 or name.find("_raw") > -1:
        requestFields.append(name)

    return value

  def parseArgs(self):  #type: (FileFuzzer) -> None
    RH_HELP = "Explictly specify the remote host."
    IF_HELP = (
        "Specify the input file to read from.\nWhen executing POST, always ensure there is a new line"
        "feed separating the body from the headers.\nIf fuzzing, the file must include exactly 1 'FUZZ' keyword."
    )
    S_HELP = "Specifies https."
    OF_HELP = "Specify the output file to write to."
    PF_HELP = (
        "Specify a file to send in a POST request. This flag is for file uploads only and should not be"
        "used for other POST requests")
    FF_HELP = "Specify a file to fuzz with. If this is not specified, no fuzzing will occur"
    FD_HELP = "Specify the delimiter used to separate the words in the fuzz file"
    HP_HELP = "Specify a proxy."
    SP_HELP = "Specify an ssl proxy"
    DV_HELP = "For https proxies, this flag will disable cert verification."
    RT_HELP = "Specify the requests read time out."
    FL_HELP = "Filter OUT fuzzed responses by coma separated lengths"
    FS_HELP = "Filter IN fuzzed responses by coma separated status codes"
    FI_HELP = "Filters in and keeps the responses with the specified text"
    FO_HELP = "Filters out and removes the responses with the specified text"
    SR_HELP = "Shows the response body"
    SF_HELP = "Shows the fuzz text used in the request"
    V_HELP = "Show version"
    H_HELP = "Show this help message"
    VERSION = "File Fuzzer version: {}".format(FileFuzzer.VERSION)

    self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    parser = self.parser
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-rh", "--remote-host", required=True, help=RH_HELP, type=str, metavar="127.0.0.1")
    required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar="request.txt")
    parser.add_argument("-s", "--secure", action="store_true", help=S_HELP)
    parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-pf", "--post-file", help=PF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-ff", "--fuzz-file", help=FF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fd", "--fuzz-delimiter", help=FD_HELP, type=str, metavar=EMPTY, default=COLON)
    parser.add_argument("-hp", "--http-proxy", help=HP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sp", "--https-proxy", help=SP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-dv", "--disable-verification", action="store_true", help=DV_HELP, default=False)
    parser.add_argument("-rt", "--read-timeout", help=RT_HELP, type=int, metavar=EMPTY, default=None)
    parser.add_argument("-fl", "--filter-length", help=FL_HELP, type=str, metavar=EMPTY, default=EMPTY)
    parser.add_argument("-fs", "--filter-status", help=FS_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fi", "--filter-in", help=FI_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fo", "--filter-out", help=FO_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sr", "--show-response", action="store_true", help=SR_HELP)
    parser.add_argument("-sf", "--show-fuzz", action="store_true", help=SF_HELP)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    parser.add_argument("-h", "--help", action="help", help=H_HELP)
    self.parsedArgs = parser.parse_args()

  def setBoundary(self, line, boundaryString):  #type: (str,str) -> None
    equalsIndex = line.find(EQUAL, line.find(boundaryString))
    semiColonIndex = line.find(SEMI_COLON, equalsIndex)
    lineFeedIndex = line.find(LFN)
    if (semiColonIndex > -1):
      self.requestBoundary = line[equalsIndex + 1:semiColonIndex]
    elif (lineFeedIndex > -1):
      self.requestBoundary = line[equalsIndex + 1:lineFeedIndex]
    else:
      self.requestBoundary = line[equalsIndex + 1:]

  def setFields(self, fileLines):  #type: (FileFuzzer,str) -> None
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
        self.raw_info = fileLine
        index += 1
        continue
      elif ((fileLine == EMPTY and not isBody) or (index + 1 == fileLinesLength and not isBody)):
        isBody = True
        self.raw_headers = rawValue
        rawValue = EMPTY
      elif (index + 1 == fileLinesLength):
        rawValue += fileLine + LFN
        self.raw_body = rawValue
        index += 1
        break

      rawValue += fileLine + LFN
      index += 1

  def parseInfo(self):  #type: (FileFuzzer) -> None
    rawInfo = self.raw_info.rstrip().split(SPACE)
    self.requestInfo[METHOD] = rawInfo[0]
    self.requestInfo[ENDPOINT] = rawInfo[1]

  def parseHeaders(self):  #type: (FileFuzzer) -> None
    rawHeaders = self.raw_headers.rstrip().split(LFN)
    for rawHeader in rawHeaders:
      colonIndex = rawHeader.find(COLON)
      self.requestHeaders[rawHeader[0:colonIndex]] = rawHeader[colonIndex + 1:].strip()

  def parseBody(self):  #type: (FileFuzzer) -> None
    if (self.postFile):
      rawBodyLines = [(l) for l in self.raw_body.split(LFN) if l and not self.requestBoundary in l]
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
          self.requestBody[name] = (fileName, open(self.postFile, RB), contentTypeValue)
        elif (cd in rawBodyLine):
          name = rawBodyLine[startName + 1:endName]
          rawValue = EMPTY
          i = lineIndex + 1
          nextLine = rawBodyLines[i]
          while (True):
            rawValue += nextLine
            if (i + 1 == rawBodyLinesLength or cd in rawBodyLines[i + 1]):
              self.requestBody[name] = rawValue
              break
            nextLine += rawBodyLines[i + 1]
      if (not self.requestBody):
        print(
            "Could not parse thw post file specified. Please ensure that the -pf flag is being used with"
            " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
            " flag to send JSON or standard form data.")
        exit()
    else:
      self.requestBody = self.raw_body

  def getFuzzIndicies(self, *fuzzWords):  # type: (FileFuzzer, str) -> list[int]
    boundRegex = FileFuzzer.BOUND_REGEX
    fuzzWordsIndicies = []
    for fuzzWord in fuzzWords:
      if fuzzWord:
        fuzzWordsIndicies += re.findall(boundRegex, fuzzWord)
    return fuzzWordsIndicies

  def getBoundlessFuzz(self, *fuzzWords):  # type: (FileFuzzer, str) -> str
    boundlessRegex = FileFuzzer.BOUNDLESS_REGEX
    for fuzzWord in fuzzWords:
      boundlessArray = re.findall(boundlessRegex, fuzzWord)
      if (boundlessArray):
        if (len(boundlessArray) > 1):
          print(FileFuzzer.DUPLICATE_MESSAGE)
        return fuzzWord

  def handleBoundless(self, boundlessFuzz, fuzzWordsIndicies, attrValue, attrKey, aVI=None):
    #type: (FileFuzzer, str, list[int], str | OrderedDict, str, AVI) -> None
    if (boundlessFuzz):
      boundlessRegex = FileFuzzer.BOUNDLESS_REGEX
      newValue = re.sub(boundlessRegex, FUZZ + SONE + REGEX_SUB, boundlessFuzz)
      fuzzWordsIndicies.append(SONE)
      if (type(attrValue) == str):
        setattr(self, attrKey, newValue)
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
    #type: (FileFuzzer, list[int], list[int], str, FuzzLocator) -> None
    if (len(fuzzWordsIndicies) > 0):
      for fuzzWordIndex in fuzzWordsIndicies:
        if (fuzzWordIndex in existingIndicies):
          print(FileFuzzer.DUPLICATE_MESSAGE)
        container = LocatorContainer()
        container.setLocatorKey(locatorKey)
        container.setFuzzWordIndex(fuzzWordIndex)
        locator.getLocatorContainers().append(container)
        existingIndicies.append(container.getFuzzWordIndex())

  def updateFuzzLocator(self, *attrKeys):  # type: (FileFuzzer, str) -> None
    locators = self.fuzzLocators
    existingIndicies = []
    for attrKey in attrKeys:
      attrValue = getattr(self, attrKey)
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

  def parseFile(self):  # type: (FileFuzzer) -> None
    inputFile = open(self.inputFile, LR)
    fileLines = inputFile.readlines()

    self.setFields(fileLines)
    self.parseInfo()
    self.parseHeaders()
    self.parseBody()
    attrKeys = ["remoteHost", "requestInfo", "requestHeaders", "requestBody"]
    self.updateFuzzLocator(*attrKeys)

  def printRequest(self):  # type: (FileFuzzer) -> None
    format = '{}: {}'

    info = []
    for infoKey, infoValue in self.requestInfo.items():
      info.append(format.format(infoKey, infoValue))

    headers = []
    for headersKey, headersValue in self.requestHeaders.items():
      headers.append(format.format(headersKey, headersValue))

    body = []
    if (type(self.requestBody) == str):
      body.append(self.requestBody)
    else:
      for k, v in self.requestBody.items():
        body.append(format.format(k, v))

    print('{}{}{}{}{}{}{}{}{}{}{}'.format(LFRN, '-----------Request Start-----------',
                                          LFRN, LFRN.join(info), LFRN, LFRN.join(headers), LFRN,
                                          LFRN.join(body), LFRN, '----------- Request End ------------',
                                          LFRN))

  def getAllLocatorsContainers(self):  # type: (FileFuzzer) -> int
    locators = self.fuzzLocators
    rhostContainers = locators.getRemoteHost().getLocatorContainers()
    infoContainers = locators.getRequestInfo().getLocatorContainers()
    headersContainers = locators.getRequestHeaders().getLocatorContainers()
    bodyContainers = locators.getRequestBody().getLocatorContainers()
    return rhostContainers + infoContainers + headersContainers + bodyContainers

  def getFuzzHelpers(self):  # type: (FileFuzzer) -> list
    locators = vars(self.fuzzLocators)
    fuzzHelpers = []
    for locatorField in locators:
      locator = Cast._from(locators[locatorField], FuzzLocator)
      containers = locator.getLocatorContainers()
      for container in containers:
        fuzzHelper = FuzzHelper()
        fuzzHelper.setFuzzWordIndex(int(container.getFuzzWordIndex()))
        fuzzHelper.setAttrKey(locatorField)
        fuzzHelper.setLocatorKey(container.getLocatorKey())
        attrValue = getattr(self, locatorField)
        if (type(attrValue) == str):
          fuzzHelper.setOriginalAttrValue(attrValue)
        else:
          fuzzHelper.setOriginalAttrValue(attrValue[fuzzHelper.getLocatorKey()])
        fuzzHelpers.append(fuzzHelper)
    return fuzzHelpers

  def parseUrl(self, host, secure, endpoint=EMPTY):  #type: (FileFuzzer, str, bool, str) -> str
    standardProtocol = HTTP
    if (standardProtocol in host):
      return "{}{}".format(host, endpoint)
    else:
      protocol = HTTP_PROTOCOL
      if (secure):
        protocol = HTTPS_PROTOCOL
      return "{}{}{}".format(protocol, host, endpoint)

  def getRequestBody(self):  #type: (FileFuzzer) -> OrderedDict | str
    if (self.postFile):
      return MultipartEncoder(fields=self.requestBody, boundary=self.requestBoundary)
    return self.requestBody

  def getProxies(self):  #type: (FileFuzzer) -> dict
    proxies = {}
    if (self.httpProxy):
      proxies[HTTP] = self.parseUrl(self.httpProxy, False)
    elif (self.httpsProxy):
      proxies[HTTPS] = self.parseUrl(self.httpsProxy, True)
    return proxies

  def handleResponse(self, response):  #type: (FileFuzzer, requests.models.Response) -> None
    responseSoup = BeautifulSoup(response.text, HTML_PARSER).prettify().rstrip()
    responseStatus = response.status_code
    responseLength = EMPTY
    try:
      responseLength = response.headers.get(CONTENT_LENGTH)
    except:
      print("An exception occurred trying to retrieve header {}".format(CONTENT_LENGTH))

    if (self.filterLength and responseLength in self.filterLength):
      return
    if (self.filterStatus and not str(responseStatus) in self.filterStatus):
      return
    if (self.filterIn and not self.filterIn.lower() in responseSoup.lower()):
      return
    if (self.filterOut and self.filterOut.lower() in responseSoup.lower()):
      return

    responseString = "Response status: {} - Response length: {}".format(responseStatus, responseLength)
    if (self.showFuzz):
      responseString += " - Fuzz text: {}".format(self.FuzzValuesString)
    if (self.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def sendRequest(self):  #type: (FileFuzzer) -> None
    self.requestUrl = self.parseUrl(self.remoteHost, self.secure, self.requestInfo[ENDPOINT])

    req = requests.Request(self.requestInfo[METHOD], self.requestUrl, headers=self.requestHeaders,
                           data=self.getRequestBody())
    prepared = req.prepare()
    session = requests.Session()
    session.proxies = self.getProxies()
    session.verify = not self.disableVerification
    response = session.send(prepared, timeout=self.readTimeout)
    self.handleResponse(response)

  def swapFuzz(self, fuzzValues, fuzzHelpers):  #type: (FileFuzzer, list[str], list[FuzzHelper]) -> None
    for fuzzHelper in fuzzHelpers:
      fuzzWordIndex = fuzzHelper.getFuzzWordIndex()
      fuzzWord = FUZZ + str(fuzzWordIndex)
      fuzzValue = fuzzValues[fuzzWordIndex - 1].rstrip()
      attrKey = fuzzHelper.getAttrKey()
      attrValue = getattr(self, attrKey)
      if (type(attrValue) == str):
        setattr(self, attrKey, str(attrValue).replace(fuzzWord, fuzzValue))
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

  def swapBack(self, fuzzHelpers):  #type: (FileFuzzer, list[FuzzHelper]) -> None
    for fuzzHelper in fuzzHelpers:
      attrKey = fuzzHelper.getAttrKey()
      currentAttrValue = getattr(self, attrKey)
      originalAttrValue = fuzzHelper.getOriginalAttrValue()
      if (type(currentAttrValue) == str):
        setattr(self, attrKey, originalAttrValue)
        continue
      locatorKey = fuzzHelper.getLocatorKey()
      currentAttrValue[locatorKey] = originalAttrValue

  def fuzzRequest(self):  #type: (FileFuzzer) -> None
    fuzzValuesFile = open(self.fuzzFile, "r")
    fuzzValuesLines = fuzzValuesFile.readlines()
    fuzzHelpers = self.getFuzzHelpers()
    fuzzDelimiter = self.fuzzDelimiter

    if (len(fuzzHelpers) <= 0):
      print("No FUZZ keyword located. Sending normal request.")
      self.sendRequest()
    else:
      for fuzzValuesLine in fuzzValuesLines:
        self.FuzzValuesString = fuzzValuesLine.rstrip()
        fuzzValues = fuzzValuesLine.split(fuzzDelimiter)
        self.swapFuzz(fuzzValues, fuzzHelpers)
        self.sendRequest()
        self.swapBack(fuzzHelpers)

  def processRequest(self):  #type: (FileFuzzer) -> None
    if (len(self.getAllLocatorsContainers()) > 0):
      print("Fuzzing Request")
      self.fuzzRequest()
    else:
      print("Sending Request")
      self.sendRequest()
