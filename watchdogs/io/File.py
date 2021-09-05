# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter

import os
from argparse import ArgumentParser, Namespace

from watchdogs.utils import StringUtility
from watchdogs.utils.Constants import (EMPTY, LFN, LW)


class File(object):

  def __init__(self):
    super(File, self).__init__()
    self.inputFile = EMPTY  #type: str
    self.outputFile = EMPTY  #type: str
    self.lines = []  #type: list[str]
    self.parser = None  #type: ArgumentParser
    self.parsedArgs = None  #type: Namespace

  def parseArgs(self):  #type: (File) -> None
    """
      Override Method
        Example:
          IF_HELP = "Specify the input file to read from."
          OF_HELP = "Specify the output file to write to."
          V_HELP = "Show version"
          H_HELP = "Show this help message"
          VERSION = "File version: {}".format(File.VERSION)

          self.parser = argparse.ArgumentParser(add_help=False);
          parser = self.parser;
          required = parser.add_argument_group("Required arguments");
          required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar=EMPTY)
          parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)
          parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
          parser.add_argument("-h", "--help", action="help", help=H_HELP)
          self.parsedArgs = parser.parse_args();
    """

  def setArguments(self):  #type: (File) -> None
    parsedArgsDict = vars(self.parsedArgs)
    for parsedArgsKey in parsedArgsDict:
      setattr(self, StringUtility.toCamelCase(parsedArgsKey), parsedArgsDict[parsedArgsKey])

  def writeLines(self):  #type: (File) -> None
    outputFile = self.outputFile
    if not os.path.isfile(outputFile):
      print("File does not exist. Creating file in order to perform write operation.")
    openedFile = open(outputFile, LW)
    openedFile.writelines(self.lines)
    openedFile.close()

  def printLines(self):  #type: (File) -> None
    lines = self.lines
    for line in lines:
      print(line.replace(LFN, EMPTY))
