# author: WatchDogOblivion
# description: TODO
# WatchDogs Args

from watchdogs.external import argparse
from watchdogs.external.argparse import ArgumentParser, Namespace

from watchdogs.utils import StringUtility

SHARED_PARSER = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)


class Args(object):

  def __init__(self, parser=SHARED_PARSER, parsedArgs=None):
    #type: (ArgumentParser, Namespace | tuple[Namespace,list[str]]) -> None
    super(Args, self).__init__()
    self.__parser = parser
    self.__parsedArgs = parsedArgs

  def getParser(self):  #type: () -> ArgumentParser
    return self.__parser

  def setParser(self, __parser):  #type: (ArgumentParser) -> None
    self.__parser = __parser

  def getParsedArgs(self):  #type: () -> Namespace
    return self.__parsedArgs

  def setParsedArgs(self, __parsedArgs):  #type: (Namespace) -> None
    self.__parsedArgs = __parsedArgs

  def __str__(self):  #type: () -> str
    return str(vars(self))

  def __repr__(self):  #type: () -> str
    return str(vars(self))

  def getVersion(self):  #type: () -> str
    """Override this method to specify a version for the module"""
    return "No version specified"

  def defaultArguments(self, version):  #type: (str) -> None
    """
        You can override this method to override the help functionality.
    """
    V_HELP = "Show version"
    H_HELP = "Show this help message"
    self.__parser.add_argument("-v", "--version", action="version", help=V_HELP, version=version)
    self.__parser.add_argument("-h", "--help", action="help", help=H_HELP)

  def addArguments(self):  #type: () ->  Args
    """
      Override and use this method to add arguments to the arg parser. It will be reused 
      in the combineArguments method to gather all the arguments needed into a single object
    """
    return self

  def parseArguments(self, parseKnownOnly=True):  #type: (bool) -> None
    if (parseKnownOnly):
      self.__parsedArgs = self.__parser.parse_known_args()[0]
    else:
      self.__parsedArgs = self.__parser.parse_args()

  def setArguments(self):  #type: () -> None
    parsedArgsDict = vars(self.__parsedArgs)
    for parsedArgsKey in parsedArgsDict:
      setattr(self, StringUtility.toCamelCase(parsedArgsKey), parsedArgsDict[parsedArgsKey])