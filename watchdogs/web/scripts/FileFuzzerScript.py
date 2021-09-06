# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer Controller

import traceback

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY, COLON)
from watchdogs.web.models.FileFuzzerArgs import FileFuzzerArgs
from watchdogs.web.services.FileFuzzerService import FileFuzzerService


class FileFuzzerScript(Common):

  def __init__(self, fileFuzzerService=FileFuzzerService()):
    super(FileFuzzerScript, self).__init__()
    self.fileFuzzerService = fileFuzzerService  #type: FileFuzzerService

  def run(self):  #type: (FileFuzzerScript) -> None
    fFArgs = FileFuzzerArgs()
    fFService = FileFuzzerService()
    try:
      fFService.parseFile(fFArgs)
      fFService.processRequest(fFArgs)
    except ValueError as ve:
      print(ve)
      print(fFArgs.parser.print_usage())
    except Exception:
      print(traceback.format_exc())
      print(fFArgs.parser.print_usage())
