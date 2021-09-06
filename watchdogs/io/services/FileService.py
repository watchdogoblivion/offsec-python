# author: WatchDogOblivion
# description: TODO
# WatchDogs File Service

import os

from watchdogs.io.models.File import File
from watchdogs.utils.Constants import (EMPTY, LFN, LW)


class FileService(object):

  def __init__(self, file=File()):
    super(FileService, self).__init__()
    self.file = file  #type: File

  def writeLines(self, outputFile):  #type: (FileService, str) -> None
    file = self.file
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    openedFile = open(outputFile, LW)
    openedFile.writelines(file.lines)
    openedFile.close()

  def printLines(self):  #type: (FileService) -> None
    file = self.file
    for line in file.lines:
      print(line.replace(LFN, EMPTY))