# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQLI Request Response Helper
# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-public-methods

from watchdogs.utils.Constants import EMPTY


class ErrorSQLIRRHelper(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes

  def __init__(  # pylint: disable=too-many-arguments
      self, originalRequestBodyString=EMPTY, invalidResponseLength=-1, databaseName=EMPTY, tableName=EMPTY,
      columnName=EMPTY, query=EMPTY, ordering="ASC"):
    #type: (str, int, str, str, str, str, str) -> None
    super(ErrorSQLIRRHelper, self).__init__()
    self.__originalRequestBodyString = originalRequestBodyString
    self.__invalidResponseLength = invalidResponseLength
    self.__databaseName = databaseName
    self.__tableName = tableName
    self.__columnName = columnName
    self.__query = query
    self.__queryType = None
    self.__queryOffset = None
    self.__orderBy = None
    self.__ordering = ordering
    self.__count = None
    self.__responseView = None

  def getOriginalRequestBodyString(self):
    #type: () -> str
    return self.__originalRequestBodyString

  def setOriginalRequestBodyString(self, originalRequestBodyString):
    #type: (str) -> None
    self.__originalRequestBodyString = originalRequestBodyString

  def getInvalidResponseLength(self):
    #type: () -> int
    return self.__invalidResponseLength

  def setInvalidResponseLength(self, invalidResponseLength):
    #type: (int) -> None
    self.__invalidResponseLength = invalidResponseLength

  def getDatabaseName(self):
    #type: () -> str
    return self.__databaseName

  def setDatabaseName(self, databaseName):
    #type: (str) -> None
    self.__databaseName = databaseName

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

  def getQuery(self):
    #type: () -> str
    return self.__query

  def setQuery(self, query):
    #type: (str) -> None
    self.__query = query

  def getQueryType(self):
    #type: () -> str
    return self.__queryType

  def setQueryType(self, queryType):
    #type: (str) -> None
    self.__queryType = queryType

  def getOrdering(self):
    #type: () -> str
    return self.__ordering

  def setOrdering(self, ordering):
    #type: (str) -> None
    self.__ordering = ordering

  def getQueryOffset(self):
    #type: () -> str
    return self.__queryOffset

  def setQueryOffset(self, queryOffset):
    #type: (str) -> None
    self.__queryOffset = queryOffset

  def getOrderBy(self):
    #type: () -> str
    return self.__orderBy

  def setOrderBy(self, orderBy):
    #type: (str) -> None
    self.__orderBy = orderBy

  def getCount(self):
    #type: () -> str
    return self.__count

  def setCount(self, count):
    #type: (str) -> None
    self.__count = count

  def getResponseView(self):
    #type: () -> str | list
    return self.__responseView

  def setResponseView(self, responseView):
    #type: (str | list) -> None
    self.__responseView = responseView
