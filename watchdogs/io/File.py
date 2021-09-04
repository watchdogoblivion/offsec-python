# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter

import os;
from argparse import ArgumentParser, Namespace;

from watchdogs.utils import StringUtility;
from watchdogs.utils.Constants import *;

class File(object):
    
    def __init__(self):
        super(File, self).__init__();
        self.inputFile = EMPTY #type: str
        self.outputFile = EMPTY #type: str
        self.lines = [] #type: list[str]
        self.parser = None #type: ArgumentParser
        self.args = None #type: Namespace
    
    def parseArgs(self):#type: (File) -> None
        """
        Override Method
            Example:
                self.parser = argparse.ArgumentParser(add_help=False);
                parser = self.parser;
                required = parser.add_argument_group("Required arguments");
                required.add_argument("-if", "--input-file", required=True, help="Specify the input file to read from", type=str, metavar="");
                parser.add_argument("-of", "--output-file", help="Specify the output file to write to", type=str, metavar="");
                parser.add_argument("-v", "--version", action="version", help="version", version="Character Converter version: {}".format(WFile.VERSION));
                parser.add_argument("-h", "--help", action="help", help="Help");
                self.args = parser.parse_args();
        """;

    def setArguments(self):#type: (File) -> None
        args = self.args;
        vargs = vars(args);
        for varg in vargs:
            setattr(self, StringUtility.toCamel(varg), vargs[varg]);
    
    def writeLines(self):#type: (File) -> None
        if not os.path.isfile(self.outputFile):
            print("File does not exist. Creating file in order to perform write operation.");
        openedFile = open(self.outputFile, "w");
        openedFile.writelines(self.lines);
        openedFile.close();

    def printLines(self):#type: (File) -> None
        lines = self.lines;
        length = len(lines);
        for i in range(length):
            print(lines[i].replace(LFN,EMPTY)); 