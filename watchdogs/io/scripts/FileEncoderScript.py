# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder Script

import traceback

from watchdogs.base.models import Common, AllArgs
from watchdogs.io.models.File import File
from watchdogs.io.parsers import FileArgs, FileEncoderArgs
from watchdogs.io.services.FileEncoderService import FileEncoderService


class FileEncoderScript(Common):

  def __init__(self, fileEncoderService=FileEncoderService()):
    #type: (FileEncoderService) -> None
    super(FileEncoderScript, self).__init__()
    self.__fileEncoderService = fileEncoderService

  def get___fileEncoderService(self):
    #type: () -> FileEncoderService
    return self.__fileEncoderService

  def set___fileEncoderService(self, __fileEncoderService):
    #type: (FileEncoderService) -> None
    self.__fileEncoderService = __fileEncoderService

  def run(self):  #type: (FileEncoderScript) -> None
    allArgs = AllArgs([FileEncoderArgs(), FileArgs()]).processAllArguments()
    fEncoderArgs = allArgs.getArgs(FileEncoderArgs)
    fEncoderService = FileEncoderService()
    file = File()
    try:
      fEncoderService.readLines(allArgs, file)
      if allArgs.getArgs(FileArgs).outputFile:
        fEncoderService.writeLines(allArgs, file)
      else:
        fEncoderService.printLines(file)
    except ValueError as ve:
      print(ve)
      print(fEncoderArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fEncoderArgs.getParser().print_usage())