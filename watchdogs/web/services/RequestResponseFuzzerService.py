# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Response Fuzzer Service

import re
import copy
import requests
from typing import Any, Callable
from collections import OrderedDict

from watchdogs.utils import Cast
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
          locatorDatum.setHeaderKey(requestKey)
        elif (variantLocator.isBody()):
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

  def updateBodyLocator(self, request, existingIndicies, variantLocator):
    # type: (Request, list[int], list[VariantLocator]) -> None
    requestBody = request.getRequestBody()

    requestBodyItems = OrderedDict(requestBody).items()
    for requestBodyKey, requestBodyValue in requestBodyItems:
      fuzzWord = fileName = contentType = EMPTY
      webFile = None
      if (isinstance(requestBodyValue, WebFile)):
        webFile = Cast._to(WebFile, requestBodyValue)
        fileName = webFile.getFileName()
        contentType = webFile.getContentType()
      elif (isinstance(requestBodyValue, str)):
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

      self.updateLocatorData(indiciesOfSubstitutes, existingIndicies, variantLocator, requestBodyKey)
      request.setRequestBody(requestBody)

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
        self.updateBodyLocator(request, existingIndicies, variantLocator)

  def getAllVariantsLocatorData(self, requestFuzzer):  # type: (RequestFuzzer) -> list[LocatorDatum]
    variantLocators = requestFuzzer.getVariantLocators()
    allVariantsLocatorData = []

    for variantLocator in variantLocators:
      allVariantsLocatorData += variantLocator.getLocatorData()

    return allVariantsLocatorData

  def swapFuzz(self, requestFuzzer, variantsLocatorData):
    #type: (RequestFuzzer, list[LocatorDatum]) -> None
    fuzzSubstitutes = requestFuzzer.getFuzzSubstitutes()
    request = requestFuzzer.getRequest()

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

  def fuzzRequest(self, allArgs, requestFuzzer, allVariantsLocatorData):
    #type: (AllArgs, RequestFuzzer, list[LocatorDatum]) -> None
    fuzzerArgs = allArgs.getArgs(FuzzerArgs)
    request = requestFuzzer.getRequest()
    request.updateOriginalValues()
    fuzzSubstitutesFile = open(fuzzerArgs.substitutesFile, LR)
    fuzzSubstitutesLines = fuzzSubstitutesFile.readlines()

    for fuzzSubstitutesLine in fuzzSubstitutesLines:
      fuzzSubstitutes = fuzzSubstitutesLine.split(fuzzerArgs.substitutesDelimiter)
      requestFuzzer.setFuzzSubstitutes(fuzzSubstitutes)
      self.swapFuzz(requestFuzzer, allVariantsLocatorData)
      response = self.sendRequest(allArgs, request)
      self.handleResponse(allArgs, requestFuzzer, response)
      request.resetRequestValues()

  def processRequest(self, allArgs, requestFuzzer):  #type: (AllArgs, RequestFuzzer) -> None
    self.updateVariantLocators(requestFuzzer)
    allVariantsLocatorData = self.getAllVariantsLocatorData(requestFuzzer)
    if (len(allVariantsLocatorData) > 0):
      print("Fuzzing Request")
      self.fuzzRequest(allArgs, requestFuzzer, allVariantsLocatorData)
    else:
      print("Sending Request")
      response = self.sendRequest(allArgs, requestFuzzer.getRequest())
      self.handleResponse(allArgs, requestFuzzer, response)