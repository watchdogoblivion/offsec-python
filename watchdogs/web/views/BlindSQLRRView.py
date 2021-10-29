# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Request Response View
# pylint: disable=too-few-public-methods

import sys

from watchdogs.base.models import AllArgs  # pylint: disable=unused-import
from watchdogs.web.models import BlindSQLRRHelper  # pylint: disable=unused-import
from watchdogs.web.models.Requests import Request  # pylint: disable=unused-import
from watchdogs.web.services.BlindSQLRRService import ERROR_STRING, BlindSQLRRService  # pylint: disable=unused-import
from watchdogs.utils.Constants import (SQL_COLUMN_NAME, SQL_SCHEMA_NAME, SQL_SCHEMATA, SQL_TABLE_NAME,
                                       SQL_TABLES)


class BlindSQLRRView(object):

  def start(self, allArgs, request, blindSQLRRService, helper):# pylint: disable=too-many-branches,too-many-statements
    # type: (AllArgs, Request, BlindSQLRRService, BlindSQLRRHelper) -> None
    print("Options:\r\n")
    print("1: List database version")
    print("2: List current database name")
    print("3: List all databases")
    print("4: List tables from database")
    print("5: List columns from a table")
    print("6: List row values for a column")
    print("Type 'exit' to exit")

    print("\r\n")

    selected = raw_input("Select an option (numerical value): ") # type: ignore

    if (selected == "1"):
      blindSQLRRService.setDataBaseVersion(allArgs, request, helper)
      if (not (helper.getDatabaseVersion() == ERROR_STRING)):
        print("Database version: {}".format(helper.getDatabaseVersion()))
      else:
        helper.setDatabaseVersion(None)
    elif (selected == "2"):
      blindSQLRRService.setCurrentDatabase(allArgs, request, helper)
      if (not (helper.getDatabaseName() == ERROR_STRING)):
        print("Current database name: {}".format(helper.getDatabaseName()))
      else:
        helper.setDatabaseName(None)
    elif (selected == "3"):
      helper.setTableName(SQL_SCHEMATA)
      helper.setColumnName(SQL_SCHEMA_NAME)
      blindSQLRRService.setDataList(allArgs, request, helper)
      databases = "Databases:\n"
      for database in helper.getDataList():
        databases += "  {}\n".format(database)
      print(databases)
    elif (selected == "4"):
      helper.setDatabaseName(raw_input("Enter a database name: ")) # type: ignore
      helper.setTableName(SQL_TABLES)
      helper.setColumnName(SQL_TABLE_NAME)
      blindSQLRRService.setDataList(allArgs, request, helper)
      if (helper.getDataList() and ERROR_STRING not in helper.getDataList()):
        tables = "Tables in {}:\n".format(helper.getDatabaseName())
        for table in helper.getDataList():
          tables += "  {}\n".format(table)
        print(tables)
    elif (selected == "5"):
      helper.setDatabaseName(raw_input("Enter a database name: ")) # type: ignore
      helper.setTableName(raw_input("Enter a table name: ")) # type: ignore
      helper.setColumnName(SQL_COLUMN_NAME)
      blindSQLRRService.setDataList(allArgs, request, helper)
      if (helper.getDataList() and ERROR_STRING not in helper.getDataList()):
        columns = "Columns in {}.{}:\n".format(helper.getDatabaseName(), helper.getTableName())
        for column in helper.getDataList():
          columns += "  {}\n".format(column)
        print(columns)
    elif (selected == "6"):
      helper.setDatabaseName(raw_input("Enter a database name: ")) # type: ignore
      helper.setTableName(raw_input("Enter a table name: ")) # type: ignore
      helper.setColumnName(raw_input("Enter a column name: ")) # type: ignore
      blindSQLRRService.setDataList(allArgs, request, helper)
      if (helper.getDataList() and ERROR_STRING not in helper.getDataList()):
        rows = "Row values for {} in {}.{}:\n"
        rows = rows.format(helper.getColumnName(), helper.getDatabaseName(), helper.getTableName())
        for row in helper.getDataList():
          rows += "  {}\n".format(row)
        print(rows)
    elif (str(selected).lower() == "exit"):
      sys.exit()

    self.start(allArgs, request, blindSQLRRService, helper)
