# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder Script

import traceback

from watchdogs.base.models.Common import Common
from watchdogs.io.models.FileEncoderArgs import FileEncoderArgs
from watchdogs.io.services.FileEncoderService import FileEncoderService


class FileEncoderScript(Common):

  def __init__(self, fileEncoderService=FileEncoderService()):
    super(FileEncoderScript, self).__init__()
    self.fileEncoderService = fileEncoderService  #type: FileEncoderService

  def run(self):  #type: (FileEncoderScript) -> None
    fEncoderArgs = FileEncoderArgs()
    fEncoderService = FileEncoderService()

    try:
      fEncoderService.readLines(fEncoderArgs)
      if fEncoderArgs.outputFile:
        fEncoderService.writeLines(fEncoderArgs.inputFile)
      else:
        fEncoderService.printLines()
    except ValueError as ve:
      print(ve)
      print(fEncoderArgs.parser.print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fEncoderArgs.parser.print_usage())