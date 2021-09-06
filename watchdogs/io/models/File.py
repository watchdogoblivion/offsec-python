# author: WatchDogOblivion
# description: TODO
# WatchDogs File

from watchdogs.base.models import Common


class File(Common):

  def __init__(self):
    super(File, self).__init__()
    self.lines = []  #type: list[str]