# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Response Fuzzer Service


from __future__ import division
import re
import copy
import time
import requests
from typing import Any, Callable
from collections import OrderedDict
from pathos.multiprocessing import ProcessingPool

from watchdogs.utils import Cast, ListUtility
from watchdogs.base.models import AllArgs
from watchdogs.web.models.Requests import Request
from watchdogs.web.models import RequestFuzzer, Response
from watchdogs.web.models.WebFile import WebFile
from watchdogs.web.models.Locators import (VariantLocator, LocatorDatum)
from watchdogs.web.parsers import RequestArgs, FuzzerArgs
from watchdogs.web.services import RequestResponseService
from watchdogs.utils.Constants import (EMPTY, FUZZ, SONE, REGEX_SUB, LR, LFRN, UTF8)


class RequestResponseFuzzerService(RequestResponseService):

  UNNUMBERED_REGEX = r'(?:FUZZ)($|[^0-9])'
  NUMBERED_REGEX = r'FUZZ([0-9]+)'
  DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1"

  def __init__(self):  #type: () -> None
    super(RequestResponseFuzzerService, self).__init__()

  def getIndiciesOfSubstitutes(self, *fuzzWords):  # type: (str) -> list[int]
    stringIndicies = []
    for fuzzWord in fuzzWords:
      if fuzzWord:
        stringIndicies += re.findall(RequestResponseFuzzerService.NUMBERED_REGEX, fuzzWord)
    indiciesOfSubstitutes = map(int, stringIndicies)
    return indiciesOfSubstitutes

  def getUnnumberedFuzz(self, *fuzzWords):  # type: (str) -> str
    for fuzzWord in fuzzWords:
      unnumberedArray = re.findall(RequestResponseFuzzerService.UNNUMBERED_REGEX, fuzzWord)
      if unnumberedArray:
        if (len(unnumberedArray) > 1):
          print(RequestResponseFuzzerService.DUPLICATE_MESSAGE)
        return fuzzWord

  def handleUnnumbered(self, unnumberedFuzz, indiciesOfSubstitutes, requestObject, setNewValue,
                       requestKey=None):
    #type: (str, list[int], Any, Callable, str) -> None
    if unnumberedFuzz:
      UNNUMBERED_REGEX = RequestResponseFuzzerService.UNNUMBERED_REGEX
      newValue = re.sub(UNNUMBERED_REGEX, FUZZ + SONE + REGEX_SUB, unnumberedFuzz)
      indiciesOfSubstitutes.append(1)
      if (isinstance(requestObject, OrderedDict) and requestKey):
        requestObject[requestKey] = newValue
      else:
        setNewValue(newValue)

  def updateLocatorData(self, indiciesOfSubstitutes, existingIndicies, variantLocator, requestKey=None):
    #type: (list[int], list, VariantLocator, str) -> None
    if (len(indiciesOfSubstitutes) > 0):
      for indexOfSubstitute in indiciesOfSubstitutes:
        if (indexOfSubstitute in existingIndicies):
          print(RequestResponseFuzzerService.DUPLICATE_MESSAGE)
        locatorDatum = LocatorDatum()
        locatorDatum.setIndexOfSubstitute(indexOfSubstitute)

        if (variantLocator.isInfo()):
          locatorDatum.setIsInfo(True)
        elif (variantLocator.isHeader()):
          locatorDatum.setIsHeaders(True)
          locatorDatum.setHeaderKey(requestKey)
        elif (variantLocator.isBody()):
          locatorDatum.setIsBody(True)
          locatorDatum.setBodyKey(requestKey)

        locatorData = variantLocator.getLocatorData()
        locatorData.append(locatorDatum)
        variantLocator.setLocatorData(locatorData)
        existingIndicies.append(locatorDatum.getIndexOfSubstitute())

  def updateInfoLocator(self, request, existingIndicies, variantLocator):
    # type: (Request, list[int], list[VariantLocator]) -> None
    requestInfo = request.getRequestInfo()

    urlHost = requestInfo.getUrlHost()
    indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(urlHost)
    unnumberedFuzz = self.getUnnumberedFuzz(urlHost)
    self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestInfo, requestInfo.setUrlHost)

    endpoint = requestInfo.getEndpoint()
    indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(endpoint)
    unnumberedFuzz = self.getUnnumberedFuzz(endpoint)
    self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestInfo, requestInfo.setEndpoint)

    self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, variantLocator)
    request.setRequestInfo(requestInfo)

  def updateHeadersLocator(self, request, existingIndicies, variantLocator):
    # type: (Request, list[int], list[VariantLocator]) -> None
    requestHeaders = request.getRequestHeaders()

    requestHeaderItems = OrderedDict(requestHeaders).items()
    for requestHeaderKey, requestHeaderValue in requestHeaderItems:
      fuzzWord = requestHeaderValue
      indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fuzzWord)
      unnumberedFuzz = self.getUnnumberedFuzz(fuzzWord)
      self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestHeaders, None, requestHeaderKey)
      self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, variantLocator, requestHeaderKey)
      request.setRequestHeaders(requestHeaders)

  def updateStringBodyLocator(self, request, existingIndicies, variantLocator):
    # type: (Request, list[int], list[VariantLocator]) -> None
    requestBodyString = request.getRequestBodyString()
    indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(requestBodyString)
    unnumberedFuzz = self.getUnnumberedFuzz(requestBodyString)
    self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, request, request.setRequestBodyString)
    self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, variantLocator)
    request.setRequestBodyString(requestBodyString)

  def updateDictBodyLocator(self, request, existingIndicies, variantLocator):
    # type: (Request, list[int], VariantLocator) -> None
    requestBodyDict = request.getRequestBodyDict()
    requestBodyItems = requestBodyDict.items()
    for requestBodyKey, requestBodyValue in requestBodyItems:
      fuzzWord = fileName = content = contentType = EMPTY
      webFile = None
      if (isinstance(requestBodyValue, WebFile)):
        webFile = Cast._to(WebFile, requestBodyValue)
        fileName = webFile.getFileName()
        content = webFile.getContent()
        contentType = webFile.getContentType()
      elif (isinstance(requestBodyValue, str)):
        fuzzWord = requestBodyValue

      if (fuzzWord):
        indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fuzzWord)
        unnumberedFuzz = self.getUnnumberedFuzz(fuzzWord)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBodyDict, None, requestBodyKey)

      if (webFile):
        indiciesOfSubstitutes = self.getIndiciesOfSubstitutes(fileName)
        unnumberedFuzz = self.getUnnumberedFuzz(fileName)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBodyDict, webFile.setFileName)

        indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(content)
        unnumberedFuzz = self.getUnnumberedFuzz(content)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBodyDict, webFile.setContent)

        indiciesOfSubstitutes += self.getIndiciesOfSubstitutes(contentType)
        unnumberedFuzz = self.getUnnumberedFuzz(contentType)
        self.handleUnnumbered(unnumberedFuzz, indiciesOfSubstitutes, requestBodyDict, webFile.setContentType)

      self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, variantLocator, requestBodyKey)
      request.setRequestBodyDict(requestBodyDict)

  def updateVariantLocators(self, requestFuzzer):  # type: (RequestFuzzer) -> None
    variantLocators = requestFuzzer.rebaseLocators()
    request = requestFuzzer.getRequest()
    existingIndicies = []

    for variantLocator in variantLocators:
      if (variantLocator.isInfo()):
        self.updateInfoLocator(request, existingIndicies, variantLocator)
      elif (variantLocator.isHeader()):
        self.updateHeadersLocator(request, existingIndicies, variantLocator)
      elif (variantLocator.isBody()):
        if (request.getRequestBodyString()):
          self.updateStringBodyLocator(request, existingIndicies, variantLocator)
        elif (request.getRequestBodyDict()):
          self.updateDictBodyLocator(request, existingIndicies, variantLocator)

  def getAllVariantsLocatorData(self, requestFuzzer):  # type: (RequestFuzzer) -> list[LocatorDatum]
    variantLocators = requestFuzzer.getVariantLocators()
    allVariantsLocatorData = []

    for variantLocator in variantLocators:
      allVariantsLocatorData += variantLocator.getLocatorData()

    return allVariantsLocatorData

  def swapInfoFuzz(self, request, fuzzWord, substitute):
    #type: (Request, str, str) -> None
    requestInfo = request.getRequestInfo()

    newEndpointValue = requestInfo.getEndpoint().replace(fuzzWord, substitute)
    requestInfo.setEndpoint(newEndpointValue)

    newUrlValue = requestInfo.getUrlHost().replace(fuzzWord, substitute)
    requestInfo.setUrlHost(newUrlValue)

    request.setRequestInfo(requestInfo)

  def swapHeadersFuzz(self, request, locatorDatum, fuzzWord, substitute):
    #type: (Request, LocatorDatum, str, str) -> None
    headerKey = locatorDatum.getHeaderKey()
    headers = request.getRequestHeaders()
    headerValue = headers[headerKey]
    headers[headerKey] = str(headerValue).replace(fuzzWord, substitute)
    request.setRequestHeaders(headers)

  def swapBodyFuzz(self, request, locatorDatum, fuzzWord, substitute):
    #type: (Request, LocatorDatum, str, str) -> None
    if (request.getRequestBodyString()):
      requestBodyString = request.getRequestBodyString()
      newRequestBodyString = requestBodyString.replace(fuzzWord, substitute)
      request.setRequestBodyString(newRequestBodyString)
    elif (request.getRequestBodyDict()):
      bodyKey = locatorDatum.getBodyKey()
      requestBodyDict = request.getRequestBodyDict()
      bodyValue = requestBodyDict[bodyKey]
      if (isinstance(bodyValue, WebFile)):
        webFile = copy.copy(Cast._to(WebFile, bodyValue))
        fileName = webFile.getFileName()
        content = webFile.getContent()
        contentType = webFile.getContentType()
        if (fuzzWord in fileName):
          newValue = fileName.replace(fuzzWord, substitute)
          webFile.setFileName(newValue)
        elif (fuzzWord in content):
          newValue = str(content).replace(fuzzWord, substitute).encode()
          webFile.setContent(newValue)
        elif (fuzzWord in contentType):
          newValue = contentType.replace(fuzzWord, substitute)
          webFile.setContentType(newValue)
        requestBodyDict[bodyKey] = webFile
      elif (isinstance(bodyValue, str)):
        requestBodyDict[bodyKey] = str(bodyValue).replace(fuzzWord, substitute)
      request.setRequestBodyDict(requestBodyDict)

  def swapFuzz(self, request, fuzzSubstitutes, allLocatorData):
    #type: (Request, list[str], list[LocatorDatum]) -> None

    for locatorDatum in allLocatorData:
      indexOfSubstitute = locatorDatum.getIndexOfSubstitute()
      fuzzWord = FUZZ + str(indexOfSubstitute)
      substitute = fuzzSubstitutes[indexOfSubstitute - 1].rstrip()

      if (locatorDatum.isInfo()):
        self.swapInfoFuzz(request, fuzzWord, substitute)
      elif (locatorDatum.isHeaders()):
        self.swapHeadersFuzz(request, locatorDatum, fuzzWord, substitute)
      elif (locatorDatum.isBody()):
        self.swapBodyFuzz(request, locatorDatum, fuzzWord, substitute)

  def printResponse(self, allArgs, requestFuzzer, response):
    #type: (AllArgs, RequestFuzzer, Response) -> None
    fuzzerArgs = allArgs.getArgs(FuzzerArgs)
    requestArgs = allArgs.getArgs(RequestArgs)
    responseStatus = response.getResponseStatus()
    responseLength = response.getResponseLength()
    responseSoup = response.getResponseSoup()
    responseString = "Response status: {} - Response length: {}".format(responseStatus, responseLength)
    if (fuzzerArgs.showSubstitutes):
      responseString += " - Fuzz text: {}".format(requestFuzzer.getFuzzSubstitutes())
    if (requestArgs.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def handleResponse(self, allArgs, requestFuzzer, response):
    #type: (AllArgs, RequestFuzzer, requests.models.Response) -> None
    finalResponse = self.getFinalResponse(response)

    if (self.filterResponse(allArgs, finalResponse)):
      return

    self.printResponse(allArgs, requestFuzzer, finalResponse)

  def swapAndFuzzRequest(self, allArgs, requestFuzzer, allLocatorData, fuzzSubstitutesLines):
    #type: (AllArgs, RequestFuzzer, list[LocatorDatum], list[str]) -> None
    for fuzzSubstitutesLine in fuzzSubstitutesLines:
      fuzzerArgs = allArgs.getArgs(FuzzerArgs)
      request = copy.deepcopy(requestFuzzer.getRequest())
      request.updateOriginalValues()
      fuzzSubstitutes = fuzzSubstitutesLine.rstrip().split(fuzzerArgs.substitutesDelimiter)
      requestFuzzer.setFuzzSubstitutes(fuzzSubstitutes)
      self.swapFuzz(request, fuzzSubstitutes, allLocatorData)
      response = self.sendRequest(allArgs, request)
      if (not response == None):
        self.handleResponse(allArgs, requestFuzzer, response)
      request.resetRequestValues()

  def prepareFuzzRequests(self, allArgs, requestFuzzer, allLocatorData):
    #type: (AllArgs, RequestFuzzer, list[LocatorDatum]) -> None
    fuzzerArgs = allArgs.getArgs(FuzzerArgs)
    fuzzSubstitutesFile = open(fuzzerArgs.substitutesFile, LR)
    fuzzSubstitutesLines = fuzzSubstitutesFile.readlines()

    pool = ProcessingPool(fuzzerArgs.poolSize)
    groups = ListUtility.group(fuzzSubstitutesLines, fuzzerArgs.groupSize)
    substituesLength = len(groups)
    allArgsArray = []
    requestFuzzerArray = []
    allLocatorDataArray = []
    index = 0

    while index < substituesLength:
      allArgsArray.append(allArgs)
      requestFuzzerArray.append(requestFuzzer)
      allLocatorDataArray.append(allLocatorData)
      index += 1

    start = time.time()
    pool.map(self.swapAndFuzzRequest, allArgsArray, requestFuzzerArray, allLocatorDataArray, groups)
    end = time.time()
    totalTime = end - start
    if (totalTime > 60):
      print("Fuzzing completed. Total time: {} minutes".format(round(totalTime / 60, 2)))
    else:
      print("Fuzzing completed. Total time: {} seconds".format(totalTime))

  def processRequest(self, allArgs, requestFuzzer):  #type: (AllArgs, RequestFuzzer) -> None
    self.updateVariantLocators(requestFuzzer)
    allVariantsLocatorData = self.getAllVariantsLocatorData(requestFuzzer)
    if (len(allVariantsLocatorData) > 0):
      print("Fuzzing Request. Please wait...")
      self.prepareFuzzRequests(allArgs, requestFuzzer, allVariantsLocatorData)
    else:
      print("Sending Request")
      response = self.sendRequest(allArgs, requestFuzzer.getRequest())
      if (not response == None):
        self.handleResponse(allArgs, requestFuzzer, response)