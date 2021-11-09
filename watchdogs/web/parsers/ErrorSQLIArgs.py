# author: WatchDogOblivion
# description: TODO
# WatchDogs Error SQLI Arguments

from watchdogs.base.models import Args
from watchdogs.utils.Constants import (DATABASE_TYPES, EMPTY, INJECTION_TYPES)


class ErrorSQLIArgs(Args):  # pylint: disable=too-many-instance-attributes

  VERSION = "Error SQL injection version: 1.0"

  def __init__(  # pylint: disable=too-many-arguments
      self, databaseType=DATABASE_TYPES[0], injectionType=INJECTION_TYPES[1], terminator="1'",
      wordDelimiter=" ", commentOut="--", ordering="ASC",
      extractString="<i>Conversion failed when converting"):
    #type: (str, str, str, str, str, str, str) -> None
    super(ErrorSQLIArgs, self).__init__()
    self.databaseType = databaseType
    self.injectionType = injectionType
    self.terminator = terminator
    self.wordDelimiter = wordDelimiter
    self.commentOut = commentOut
    self.ordering = ordering
    self.extractString = extractString

  def getVersion(self):  #type: () -> str
    return ErrorSQLIArgs.VERSION

  def addArguments(self):  #type: () -> ErrorSQLIArgs
    DT_HELP = "Database type. Options: MSSQL, MYSQL, ORACLE, PostgreSQL"
    TP_HELP = "SQL injection type. Options are SELECT, INSERT, UPDATE."
    T_HELP = "Pre-confirmed terminator that will allow SQL injection. Example: 1'"
    WD_HELP = "The characters used to separate words. The default is a regular empty space"
    CO_HELP = "The characters used to signify commenting out after the terminator. Default is: --"
    O_HELP = "Specify result ordering. ASC or DESC"
    ES_HELP = "The string to match against to pull values. Default is: '<i>Conversion failed when converting'"

    parser = self.getParser()

    optional = parser.add_argument_group("Optional SQL injection arguments")
    optional.add_argument("-dt", "--databaseType", help=DT_HELP, type=str, metavar=EMPTY,
                          default=DATABASE_TYPES[0])
    optional.add_argument("-it", "--injectionType", help=TP_HELP, type=str, metavar=EMPTY,
                          default=INJECTION_TYPES[1])
    optional.add_argument("-t", "--terminator", help=T_HELP, type=str, metavar=EMPTY, default="1'")
    optional.add_argument("-wd", "--word-delimiter", help=WD_HELP, type=str, metavar=EMPTY, default=" ")
    optional.add_argument("-co", "--comment-out", help=CO_HELP, type=str, metavar=EMPTY, default="--")
    optional.add_argument("-o", "--ordering", help=O_HELP, type=str, metavar=EMPTY, default="ASC")
    optional.add_argument("-es", "--extract-string", help=ES_HELP, type=str, metavar=EMPTY,
                          default="<i>Conversion failed when converting")

    return self
