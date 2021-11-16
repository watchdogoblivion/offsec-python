# author: WatchDogOblivion
# description: TODO
# WatchDogs TFTP Script

import traceback

from watchdogs.base.models import AllArgs, Common
from watchdogs.io.parsers import OFileArgs, TFTPArgs
from watchdogs.io.services import TFTPService


class TFTPScript(Common):

  def __init__(self, tFTPService=TFTPService()):
    #type: (TFTPScript) -> None
    super(TFTPScript, self).__init__()
    self.__tFTPService = tFTPService

  def getTFTPService(self):  #type: () -> TFTPService
    return self.__tFTPService

  def setTFTPService(self, tFTPService):  #type: (TFTPService) -> None
    self.__tFTPService = tFTPService

  def run(self):  #type: () -> None
    allArgs = AllArgs([TFTPArgs(), OFileArgs()]).mergeAndProcess()
    sMTPArgs = allArgs.getArgs(TFTPArgs)
    try:
      self.__tFTPService.process(allArgs)
    except ValueError:
      print(traceback.format_exc())
      print(sMTPArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(sMTPArgs.getParser().print_usage())
