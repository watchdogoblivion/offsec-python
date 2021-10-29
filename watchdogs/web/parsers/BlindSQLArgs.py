# author: WatchDogOblivion
# description: TODO
# WatchDogs Blind SQL Arguments

from watchdogs.base.models import Args
from watchdogs.utils.Constants import (EMPTY)


class BlindSQLArgs(Args):

  VERSION = "Blind SQL version: 1.0"

  def __init__(self, terminator="admin'", wordDelimiter=" ", commentOut="--", threadPoolSize=10,
               processPoolSize=10):
    #type: (str, str, str, int, int) -> None
    super(BlindSQLArgs, self).__init__()
    self.terminator = terminator
    self.wordDelimiter = wordDelimiter
    self.commentOut = commentOut
    self.threadPoolSize = threadPoolSize
    self.processPoolSize = processPoolSize

  def getVersion(self):  #type: () -> str
    return BlindSQLArgs.VERSION

  def addArguments(self):  #type: () -> BlindSQLArgs
    T_HELP = "Pre-confirmed terminator that will allow SQL injection. Example: admin'"
    WD_HELP = "The characters used to separate words. The default is a regular empty space"
    CO_HELP = "The characters used to signify commenting out after the terminator. Default is: --"
    TPS_HELP = "Specify the thread pool size. The default size is 10"
    PPS_HELP = "Specify the multi processing pool size. The default size is 10"

    parser = self.getParser()

    optional = parser.add_argument_group("Optional blind SQL arguments")
    optional.add_argument("-t", "--terminator", help=T_HELP, type=str, metavar=EMPTY, default="admin'")
    optional.add_argument("-wd", "--word-delimiter", help=WD_HELP, type=str, metavar=EMPTY, default=" ")
    optional.add_argument("-co", "--comment-out", help=CO_HELP, type=str, metavar=EMPTY, default="--")
    optional.add_argument("-tps", "--thread-pool-size", help=TPS_HELP, type=int, metavar=EMPTY, default=10)
    optional.add_argument("-pps", "--process-pool-size", help=PPS_HELP, type=int, metavar=EMPTY, default=10)

    return self
