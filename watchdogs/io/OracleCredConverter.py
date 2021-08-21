# author: WatchDogOblivion
# description: TODO
# WatchDogs Oracle Credentials Converter a.k.a woraclecc

import argparse

from watchdogs.io import File;
from watchdogs.utils.Constants import *;

class OracleCredConverter(File):

    VERSION = "1.0";

    UU = "uu";
    UL = "ul";
    LU = "lu";
    LL = "ll";

    def __init__(self):
        self.conversion = EMPTY;

    def getConversions(self):
        conversions = "Conversion types:"+LFN;
        conversions += "  {}   : First word uppered and second word uppered{}".format(OracleCredConverter.UU,LFN);
        conversions += "  {}   : First word uppered and second word lowered{}".format(OracleCredConverter.UL,LFN);
        conversions += "  {}   : First word lowered and second word uppered{}".format(OracleCredConverter.LU,LFN);
        conversions += "  {}   : First word lowered and second word lowered".format(OracleCredConverter.LL,LFN);
        return conversions;

    def parseArgs(self):
        self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        required.add_argument("-if", "--input-file", required=True, help="Specify the input file to read from.", type=str, metavar=EMPTY);
        parser.add_argument("-of", "--output-file", help="Specify the output file to write to.", type=str, metavar=EMPTY);
        parser.add_argument("-c", "--conversion", help="Specify the conversion type.", type=str, metavar=EMPTY);
        parser.add_argument("-lc", "--list-conversions", action="version", help="Conversion types.", version=self.getConversions());
        parser.add_argument("-v", "--version", action="version", help="Show version", version=" Oracle Credentials Converter version: {}".format(OracleCredConverter.VERSION));
        parser.add_argument("-h", "--help", action="help", help="Show this help message");
        self.args = parser.parse_args();

    def readLines(self):
        openedFile = open(self.inputFile, "r");
        lines = openedFile.readlines();
        length = len(lines);
        for i in range(length):
            de = FS;
            line = EMPTY;
            splitLines = lines[i].split(de);
            if(self.conversion == OracleCredConverter.UU):
                line = "{}{}{}".format(splitLines[0].upper(), de, splitLines[1].upper());
            if(self.conversion == OracleCredConverter.UL):
                line = "{}{}{}".format(splitLines[0].upper(), de, splitLines[1].lower());
            if(self.conversion == OracleCredConverter.LU):
                line = "{}{}{}".format(splitLines[0].lower(), de, splitLines[1].upper());
            if(self.conversion == OracleCredConverter.LL):
                line = "{}{}{}".format(splitLines[0].lower(), de, splitLines[1].lower());
            
            lines[i] = line;
        self.lines = lines;