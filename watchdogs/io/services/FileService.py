# author: WatchDogOblivion
# description: TODO
# WatchDogs File Service

import os

from watchdogs.base.models import AllArgs
from watchdogs.io.parsers.FileArgs import FileArgs
from watchdogs.io.models.File import File
from watchdogs.utils.Constants import (EMPTY, LFN, LW)


class FileService(object):

  def __init__(self):  #type: () -> None
    super(FileService, self).__init__()

  def writeLines(self, allArgs, file):  #type: (AllArgs, File) -> None
    outputFile = allArgs.getArgs(FileArgs).outputFile
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    openedFile = open(outputFile, LW)
    openedFile.writelines(file.getLines())
    openedFile.close()

  def printLines(self, file):  #type: (File) -> None
    for line in file.getLines():
      print(line.replace(LFN, EMPTY))