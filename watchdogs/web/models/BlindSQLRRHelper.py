# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Request Response Helper
# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-public-methods

from watchdogs.utils.Constants import EMPTY


class BlindSQLRRHelper(object):

  def __init__(self, originalEndpoint=EMPTY, invalidResponseLength=-1, databaseVersion=EMPTY,
               dataList=EMPTY, databaseName=EMPTY, tableList=EMPTY, tableName=EMPTY, columnName=EMPTY,
               queryKey=EMPTY, queryOperator=EMPTY, queryOperand=EMPTY, query=EMPTY, characterIndex=0,
               rowIndex=0):
    #type: (str, int, str, str, str, str, str, str, str, str, str, str, int, int) -> None
    super(BlindSQLRRHelper, self).__init__()
    self.__originalEndpoint = originalEndpoint
    self.__invalidResponseLength = invalidResponseLength
    self.__databaseVersion = databaseVersion
    self.__dataList = dataList
    self.__databaseName = databaseName
    self.__tableList = tableList
    self.__tableName = tableName
    self.__columnName = columnName
    self.__characterIndex = characterIndex
    self.__rowIndex = rowIndex
    self.__queryKey = queryKey
    self.__queryOperator = queryOperator
    self.__queryOperand = queryOperand
    self.__query = query
    self.__isCharacterCheck = False
    self.__isRowCheck = False
    self.__isRowCharacterCheck = False

  def getOriginalEndpoint(self):
    #type: () -> str
    return self.__originalEndpoint

  def setOriginalEndpoint(self, originalEndpoint):
    #type: (str) -> None
    self.__originalEndpoint = originalEndpoint

  def getInvalidResponseLength(self):
    #type: () -> int
    return self.__invalidResponseLength

  def setInvalidResponseLength(self, invalidResponseLength):
    #type: (int) -> None
    self.__invalidResponseLength = invalidResponseLength

  def getDatabaseVersion(self):
    #type: () -> str
    return self.__databaseVersion

  def setDatabaseVersion(self, databaseVersion):
    #type: (str) -> None
    self.__databaseVersion = databaseVersion

  def getDataList(self):
    #type: () -> str
    return self.__dataList

  def setDataList(self, dataList):
    #type: (str) -> None
    self.__dataList = dataList

  def getDatabaseName(self):
    #type: () -> str
    return self.__databaseName

  def setDatabaseName(self, databaseName):
    #type: (str) -> None
    self.__databaseName = databaseName

  def getTableList(self):
    #type: () -> str
    return self.__tableList

  def setTableList(self, tableList):
    #type: (str) -> None
    self.__tableList = tableList

  def getTableName(self):
    #type: () -> str
    return self.__tableName

  def setTableName(self, tableName):
    #type: (str) -> None
    self.__tableName = tableName

  def getColumnName(self):
    #type: () -> str
    return self.__columnName

  def setColumnName(self, columnName):
    #type: (str) -> None
    self.__columnName = columnName

  def getQueryKey(self):
    #type: () -> str
    return self.__queryKey

  def setQueryKey(self, queryKey):
    #type: (str) -> None
    self.__queryKey = queryKey

  def getQueryOperator(self):
    #type: () -> str
    return self.__queryOperator

  def setQueryOperator(self, queryOperator):
    #type: (str) -> None
    self.__queryOperator = queryOperator

  def getQueryOperand(self):
    #type: () -> str
    return self.__queryOperand

  def setQueryOperand(self, queryOperand):
    #type: (str) -> None
    self.__queryOperand = queryOperand

  def getQuery(self):
    #type: () -> str
    return self.__query

  def setQuery(self, query):
    #type: (str) -> None
    self.__query = query

  def getCharacterIndex(self):
    #type: () -> str
    return self.__characterIndex

  def setCharacterIndex(self, characterIndex):
    #type: (str) -> None
    self.__characterIndex = characterIndex

  def getRowIndex(self):
    #type: () -> str
    return self.__rowIndex

  def setRowIndex(self, rowIndex):
    #type: (str) -> None
    self.__rowIndex = rowIndex

  def isRowCheck(self):
    #type: () -> bool
    return self.__isRowCheck

  def setIsRowCheck(self, isRowCheck):
    #type: (bool) -> None
    self.__isRowCheck = isRowCheck
    if (isRowCheck):
      self.__isCharacterCheck = False
      self.__isRowCharacterCheck = False

  def isCharacterCheck(self):
    #type: () -> bool
    return self.__isCharacterCheck

  def setIsCharacterCheck(self, isCharacterCheck):
    #type: (bool) -> None
    self.__isCharacterCheck = isCharacterCheck
    if (isCharacterCheck):
      self.__isRowCheck = False
      self.__isRowCharacterCheck = False

  def isRowCharacterCheck(self):
    #type: () -> bool
    return self.__isRowCharacterCheck

  def setIsRowCharacterCheck(self, isRowCharacterCheck):
    #type: (bool) -> None
    self.__isRowCharacterCheck = isRowCharacterCheck
    if (isRowCharacterCheck):
      self.__isRowCheck = False
      self.__isCharacterCheck = False
