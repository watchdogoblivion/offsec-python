# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder Service

import urllib
import base64
from watchdogs.io.models import FileEncoderArgs
from watchdogs.base.models.Common import Common
from watchdogs.io.services.FileService import FileService
from watchdogs.utils.Constants import (LFN, FS, LR, V1, V2, V3)


class FileEncoderService(FileService, Common):

  def __init__(self):
    super(FileEncoderService, self).__init__()

  def readLines(self, fileEncoderArgs):  #type: (FileEncoderService, FileEncoderArgs) -> None
    openedFile = open(fileEncoderArgs.inputFile, LR)
    lines = openedFile.readlines()
    linesLength = len(lines)
    encodedLines = []

    for index in range(linesLength):
      encoded = lines[index].rstrip()
      urlEncode = fileEncoderArgs.urlEncode

      if (fileEncoderArgs.b64Encode):
        encoded = base64.b64encode(encoded)

      if (urlEncode == V1):
        encoded = urllib.quote(encoded)
      elif (urlEncode == V2):
        encoded = urllib.quote_plus(encoded)
      elif (urlEncode == V3):
        encoded = str(urllib.quote(encoded)).replace(FS, "%2F")

      if (index + 1 == linesLength):
        encodedLines.append(encoded)
      else:
        encodedLines.append(encoded + LFN)

    self.file.lines = encodedLines