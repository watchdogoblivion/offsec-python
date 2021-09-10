# author: WatchDogOblivion
# description: TODO
# WatchDogs AllArgs

from typing import Type, Any

from watchdogs.utils.Constants import T
from watchdogs.base.models import Args


class AllArgs(object):

  def __init__(self, argsList=None):  #type: (list[Args]) -> None
    super(AllArgs, self).__init__()
    self.__argsList = argsList

  def getArgsList(self):  #type: () -> list[Args]
    return list(self.__argsList)

  def setArgsList(self, __args):  #type: (list[Args]) -> None
    self.__argsList = __args

  def getArgs(self, clazz):  #type: (Type[T]) -> T
    for arg in self.__argsList:
      if (type(arg) == clazz):
        return arg
    print("Args object not found")

  def addArgs(self, arg):  #type: (Args) -> None
    self.__argsList.append(arg)

  def removeArgs(self, arg):  #type: (Args) -> None
    self.__argsList.remove(arg)

  def mergeAndProcess(self):  #type: () -> AllArgs
    argsList = self.__argsList
    parser = None

    for argsIndex in range(len(argsList)):
      arg = argsList[argsIndex]
      if (argsIndex == 0):
        parser = arg.getParser()
        arg.defaultArguments(arg.getVersion())
      else:
        arg.setParser(parser)
      arg.addArguments()

    for arg in argsList:
      arg.parseArguments()
      arg.setArguments()

    return self