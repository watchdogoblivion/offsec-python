# author: WatchDogOblivion
# description: TODO
# WatchDogs Encoding Viewer Service

import os
from watchdogs.io.parsers import EncodingViewerArgs
from watchdogs.base.models.Common import Common
from watchdogs.io.services.FileService import FileService


class EncodingViewerService(FileService, Common):

  def __init__(self):  #type: () -> None
    super(EncodingViewerService, self).__init__()

  def writeEncoding(self, outputFile, osCommand):  #type: (str, str) -> None
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    redirectToFile = " > {}".format(outputFile)
    os.system(osCommand + redirectToFile)

  def outputEncoding(self, encodingViewerArgs):  #type: (EncodingViewerArgs) -> None
    encodings = EncodingViewerArgs.ENCODINGS
    encodeFrom = encodingViewerArgs.getEncodeFrom()
    encodeTo = encodingViewerArgs.getEncodeTo()
    inputFile = encodingViewerArgs.getInputFile()
    outputFile = encodingViewerArgs.getOutputFile()

    osCommand = "iconv -f {} -t {}//translit {}"
    osCommand = osCommand.format(encodings[encodeFrom], encodings[encodeTo], inputFile)
    print("Command: {}".format(osCommand))
    if outputFile:
      self.writeEncoding(outputFile, osCommand)
    else:
      os.system(osCommand)