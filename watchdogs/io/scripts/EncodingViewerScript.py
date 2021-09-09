# author: WatchDogOblivion
# description: TODO
# WatchDogs Encoding Viewer Script

import traceback

from watchdogs.base.models.Common import Common
from watchdogs.io.parsers import EncodingViewerArgs
from watchdogs.io.services.EncodingViewerService import EncodingViewerService


class EncodingViewerScript(Common):

  def __init__(self, encodingViewerService=EncodingViewerService()):
    #type: (EncodingViewerService) -> None
    super(EncodingViewerScript, self).__init__()
    self.__encodingViewerService = encodingViewerService

  def getEncodingViewerService(self):
    #type: () -> EncodingViewerService
    return self.__encodingViewerService

  def setEncodingViewerService(self, __encodingViewerService):
    #type: (EncodingViewerService) -> None
    self.__encodingViewerService = __encodingViewerService

  def run(self):  #type: (EncodingViewerScript) -> None
    eViewerArgs = EncodingViewerArgs()
    eViewerService = EncodingViewerService()
    try:
      eViewerService.outputEncoding(eViewerArgs)
    except ValueError as ve:
      print(ve)
      print(eViewerArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(eViewerArgs.getParser().print_usage())