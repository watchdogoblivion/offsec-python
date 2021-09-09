# author: WatchDogOblivion
# description: TODO
# WatchDogs File Service

import os

from watchdogs.io.models.File import File
from watchdogs.utils.Constants import (EMPTY, LFN, LW)


class FileService(object):

  def __init__(self, file=File()):  #type: (File) -> None
    super(FileService, self).__init__()
    self.__file = file

  def getFile(self):  #type: () -> File
    return self.__file

  def setFile(self, file):  #type: (File) -> None
    self.__file = file

  def writeLines(self, outputFile):  #type: (str) -> None
    file = self.__file
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    openedFile = open(outputFile, LW)
    openedFile.writelines(file.getLines())
    openedFile.close()

  def printLines(self):  #type: (FileService) -> None
    file = self.__file
    for line in file.getLines():
      print(line.replace(LFN, EMPTY))