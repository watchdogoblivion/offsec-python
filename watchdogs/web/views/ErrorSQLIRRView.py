# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQL Request Response View
# pylint: disable=too-few-public-methods

import sys

from watchdogs.base.models import AllArgs  # pylint: disable=unused-import
from watchdogs.web.models import ErrorSQLIRRHelper  # pylint: disable=unused-import
from watchdogs.web.models.Requests import Request # pylint: disable=unused-import
from watchdogs.web.services import ErrorSQLIRRService  # pylint: disable=unused-import
from watchdogs.web.webutils.ErrorSQLIRRQueries import QUERY_TYPES

class ErrorSQLIRRView(object):  # pylint: disable=too-few-public-methods

  def start(self, allArgs, request, errorSQLIRRService, helper):  # pylint: disable=too-many-branches,too-many-statements
    # type: (AllArgs, Request, ErrorSQLIRRService, ErrorSQLIRRHelper) -> None
    print("Options:\r\n")
    print("1: List server name")
    print("2: List version")
    print("3: List current database name")
    print("4: List all databases")
    print("5: List tables from database")
    print("6: List columns from a table")
    print("7: List row values for a column")
    print("Type 'exit' to exit")

    print("\r\n")

    selected = raw_input("Select an option (numerical value): ")  # type: ignore
    if (selected == "1"):
      helper.setQueryType(QUERY_TYPES[0])
      errorSQLIRRService.processSimpleRequest(allArgs, request, helper)
      print("Server name: {}".format(helper.getResponseView()))
    elif (selected == "2"):
      helper.setQueryType(QUERY_TYPES[1])
      errorSQLIRRService.processSimpleRequest(allArgs, request, helper)
      print("Database version: {}".format(helper.getResponseView()))
    elif (selected == "3"):
      helper.setQueryType(QUERY_TYPES[2])
      errorSQLIRRService.processSimpleRequest(allArgs, request, helper)
      print("Current database name: {}".format(helper.getResponseView()))
    elif (selected == "4"):
      helper.setQueryType(QUERY_TYPES[3])
      errorSQLIRRService.processComplexRequest(allArgs, request, helper)
      databases = "Databases:\n"
      for database in helper.getResponseView():
        databases += "  {}\n".format(database)
      print(databases)
    elif (selected == "5"):
      helper.setQueryType(QUERY_TYPES[4])
      helper.setDatabaseName(raw_input("Enter a database name: "))  # type: ignore
      errorSQLIRRService.processComplexRequest(allArgs, request, helper)
      tables = "Tables in {}:\n".format(helper.getDatabaseName())
      for table in helper.getResponseView():
        tables += "  {}\n".format(table)
      print(tables)
    elif (selected == "6"):
      helper.setQueryType(QUERY_TYPES[5])
      helper.setDatabaseName(raw_input("Enter a database name: "))  # type: ignore
      helper.setTableName(raw_input("Enter a table name: "))  # type: ignore
      errorSQLIRRService.processComplexRequest(allArgs, request, helper)
      columns = "Columns in {}.{}:\n".format(helper.getDatabaseName(), helper.getTableName())
      for column in helper.getResponseView():
        columns += "  {}\n".format(column)
      print(columns)
    elif (selected == "7"):
      helper.setDatabaseName(raw_input("Enter a database name: "))  # type: ignore
      helper.setTableName(raw_input("Enter a table name: "))  # type: ignore
      helper.setColumnName(raw_input("Enter a column name: "))  # type: ignore
      helper.setOrderBy(raw_input("Optional - Enter column name to order by: "))  # type: ignore

      orderByColumn = helper.getOrderBy()
      if (not orderByColumn):
        helper.setQueryType(QUERY_TYPES[5])
        helper.setQueryOffset(0)
        errorSQLIRRService.processSimpleRequest(allArgs, request, helper)
        helper.setOrderBy(helper.getResponseView())
      else:
        helper.setOrderBy(orderByColumn)
      helper.setQueryType(QUERY_TYPES[6])
      errorSQLIRRService.processComplexRequest(allArgs, request, helper)
      rows = "Row values for {} in {}.{}:\n"
      rows = rows.format(helper.getColumnName(), helper.getDatabaseName(), helper.getTableName())
      for row in helper.getResponseView():
        rows += "  {}\n".format(row)
      print(rows)
    elif (str(selected).lower() == "exit"):
      sys.exit()

    self.start(allArgs, request, errorSQLIRRService, helper)
