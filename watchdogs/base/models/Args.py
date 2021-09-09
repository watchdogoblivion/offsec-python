# author: WatchDogOblivion
# description: TODO
# WatchDogs Args

import argparse
from argparse import ArgumentParser, Namespace

from watchdogs.utils import StringUtility


class Args(object):

  def __init__(self, parser=None, parsedArgs=None):  #type: (ArgumentParser, Namespace) -> None
    super(Args, self).__init__()
    self.__parser = parser
    self.__parsedArgs = parsedArgs

    self.defaultArgs()

  def getParser(self):  #type: () -> ArgumentParser
    return self.__parser

  def setParser(self, __parser):  #type: (ArgumentParser) -> None
    self.__parser = __parser

  def getParsedArgs(self):  #type: () -> Namespace
    return self.__parsedArgs

  def setParsedArgs(self, __parsedArgs):  #type: (Namespace) -> None
    self.__parsedArgs = __parsedArgs

  def defaultArgs(self):  #type: () -> None
    """
        Create another method to add to the argparser
        You can override this method to override the help functionality.
    """
    H_HELP = "Show this help message"

    self.__parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    self.__parser.add_argument("-h", "--help", action="help", help=H_HELP)

  def setArguments(self):  #type: () -> None
    parsedArgsDict = vars(self.__parsedArgs)
    for parsedArgsKey in parsedArgsDict:
      setattr(self, StringUtility.toCamelCase(parsedArgsKey), parsedArgsDict[parsedArgsKey])