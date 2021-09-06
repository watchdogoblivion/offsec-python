# author: WatchDogOblivion
# description: TODO
# WatchDogs Encoding Viewer Script

import traceback

from watchdogs.base.models.Common import Common
from watchdogs.io.models.EncodingViewerArgs import EncodingViewerArgs
from watchdogs.io.services.EncodingViewerService import EncodingViewerService


class EncodingViewerScript(Common):

  def __init__(self, encodingViewerService=EncodingViewerService()):
    super(EncodingViewerScript, self).__init__()
    self.encodingViewerService = encodingViewerService  #type: EncodingViewerService

  def run(self):  #type: (EncodingViewerScript) -> None
    eViewerArgs = EncodingViewerArgs()
    eViewerService = EncodingViewerService()
    try:
      eViewerService.outputEncoding(eViewerArgs)
    except ValueError as ve:
      print(ve)
      print(eViewerArgs.parser.print_usage())
    except Exception:
      print(traceback.format_exc())
      print(eViewerArgs.parser.print_usage())