# author: WatchDogOblivion
# description: TODO
# WatchDogs Encoding Viewer Service

import os
from watchdogs.io.models.EncodingViewerArgs import EncodingViewerArgs
from watchdogs.base.models.Common import Common
from watchdogs.io.services.FileService import FileService


class EncodingViewerService(FileService, Common):

  def __init__(self):
    super(EncodingViewerService, self).__init__()

  def writeEncoding(self, outputFile, osCommand):  #type: (EncodingViewerService, str, str) -> None
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    redirectToFile = " > {}".format(outputFile)
    os.system(osCommand + redirectToFile)

  def outputEncoding(self, encodingViewerArgs):  #type: (EncodingViewerService, EncodingViewerArgs) -> None
    encodings = EncodingViewerArgs.ENCODINGS
    encodeFrom = encodingViewerArgs.encodeFrom
    encodeTo = encodingViewerArgs.encodeTo
    inputFile = encodingViewerArgs.inputFile
    outputFile = encodingViewerArgs.outputFile

    osCommand = "iconv -f {} -t {}//translit {}"
    osCommand = osCommand.format(encodings[encodeFrom], encodings[encodeTo], inputFile)
    print("Command: {}".format(osCommand))
    if outputFile:
      self.writeEncoding(outputFile, osCommand)
    else:
      os.system(osCommand)