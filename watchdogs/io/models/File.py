# author: WatchDogOblivion
# description: TODO
# WatchDogs File

from watchdogs.base.models import Common


class File(Common):

  def __init__(self, lines=[]):  #type: (list[str]) -> None
    super(File, self).__init__()
    self.__lines = lines

  def getLines(self):  #type: () -> list[str]
    return self.__lines

  def setLines(self, lines):  #type: (list[str]) -> None
    self.__lines = lines