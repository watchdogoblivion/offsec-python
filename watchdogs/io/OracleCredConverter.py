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
        self.conversion = EMPTY #type: str

    def getConversions(self):#type: (OracleCredConverter) -> str
        uppered = "uppered";
        lowered = "lowered";
        base = "  {}   : First word {} and second word {}{}";
        conversions = "Conversion types:{}".format(LFN);

        conversions += base.format(OracleCredConverter.UU,uppered,uppered,LFN);
        conversions += base.format(OracleCredConverter.UL,uppered,lowered,LFN);
        conversions += base.format(OracleCredConverter.LU,lowered,uppered,LFN);
        conversions += base.format(OracleCredConverter.LL,lowered,lowered,LFN);
        return conversions;

    def parseArgs(self):#type: (OracleCredConverter) -> None
        IF_HELP = "Specify the input file to read from.";
        OF_HELP = "Specify the output file to write to.";
        C_HELP = "Specify the conversion type.";
        LC_HELP = "Conversion types.";
        V_HELP = "Show version";
        H_HELP = "Show this help message";
        CONVERSIONS = self.getConversions();
        VERSION = " Oracle Credentials Converter version: {}".format(OracleCredConverter.VERSION);

        self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar=EMPTY);
        parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY);
        parser.add_argument("-c", "--conversion", help=C_HELP, type=str, metavar=EMPTY);
        parser.add_argument("-lc", "--list-conversions", action="version", help=LC_HELP, version=CONVERSIONS);
        parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION);
        parser.add_argument("-h", "--help", action="help", help=H_HELP);
        self.args = parser.parse_args();

    def readLines(self):#type: (OracleCredConverter) -> None
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