# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder Script

import traceback

from watchdogs.base.models.Common import Common
from watchdogs.io.parsers import FileEncoderArgs
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
    fEncoderArgs = FileEncoderArgs()
    fEncoderService = FileEncoderService()
    try:
      fEncoderService.readLines(fEncoderArgs)
      if fEncoderArgs.outputFile:
        fEncoderService.writeLines(fEncoderArgs.getInputFile())
      else:
        fEncoderService.printLines()
    except ValueError as ve:
      print(ve)
      print(fEncoderArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fEncoderArgs.getParser().print_usage())