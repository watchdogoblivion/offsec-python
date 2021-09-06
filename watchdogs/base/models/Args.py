# author: WatchDogOblivion
# description: TODO
# WatchDogs Args

import argparse
from argparse import ArgumentParser, Namespace

from watchdogs.utils import StringUtility


class Args(object):

  def __init__(self):
    super(Args, self).__init__()
    self.parser = None  #type: ArgumentParser
    self.parsedArgs = None  #type: Namespace

    self.defaultArgs()

  def defaultArgs(self):  #type: (Args) -> None
    """
        Create another method to add to the argparser
        You can override this method to override the help functionality.
    """
    H_HELP = "Show this help message"

    self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    self.parser.add_argument("-h", "--help", action="help", help=H_HELP)

  def setArguments(self):  #type: (Args) -> None
    parsedArgsDict = vars(self.parsedArgs)
    for parsedArgsKey in parsedArgsDict:
      setattr(self, StringUtility.toCamelCase(parsedArgsKey), parsedArgsDict[parsedArgsKey])