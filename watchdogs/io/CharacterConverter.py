# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter

import argparse;

from watchdogs.io import File;
from watchdogs.utils.Constants import *;

class CharacterConverter(File):

    VERSION = "1.0";

    def __init__(self):
        super(CharacterConverter, self).__init__();
        self.oldChar = EMPTY;
        self.newChar = EMPTY;
        self.incrementLine = False;
        self.incrementWord = False;
        self.upper = False;
        self.lower = False;

    def parseArgs(self):
        self.parser = argparse.ArgumentParser(add_help=False);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        required.add_argument("-if", "--input-file", required=True, help="Specify the input file to read from.", type=str, metavar=EMPTY);
        parser.add_argument("-of", "--output-file", help="Specify the output file to write to.", type=str, metavar="");
        parser.add_argument("-oc", "--old-char", help="Specify the character that will be replaced.", type=str, metavar="");
        parser.add_argument("-nc", "--new-char", help="Specify the character that will replace the old character.", type=str, metavar="");
        parser.add_argument("-il", "--increment-line", action="store_true", help="Specify if you want to increment the replaced character by line.");
        parser.add_argument("-iw", "--increment-word", action="store_true", help="Specify if you want to increment the replaced character by word.");
        parser.add_argument("-u", "--upper", action="store_true", help="Specify if you want to upper case all the characters.");
        parser.add_argument("-l", "--lower", action="store_true", help="Specify if you want to lower case all the characters.");
        parser.add_argument("-v", "--version", action="version", help="Show version", version="Character Converter version: {}".format(CharacterConverter.VERSION));
        parser.add_argument("-h", "--help", action="help", help="Show this help message");
        self.args = parser.parse_args();
        
    def readLines(self):
        openedFile = open(self.inputFile, "r");
        lines = openedFile.readlines();
        length = len(lines);
        inc = 1;
        for i in range(length):
            line = lines[i];
            if(self.incrementLine and self.newChar):
                if(line.find(self.oldChar) > -1):
                    line = line.replace(self.oldChar, "{}{}".format(str(inc), self.newChar));
                    inc+=1;
            elif(self.incrementWord and self.newChar):
                words = line.split(SPACE);
                wlength = len(words);
                for w in range(wlength):
                    word = words[w];
                    if(word.find(self.oldChar) > -1):
                        words[w] = word.replace(self.oldChar, "{}{}".format(str(inc), self.newChar));
                        inc+=1;
                line = SPACE.join(words);
            else:
                line = line.replace(self.oldChar, self.newChar);

            if(self.upper):
                line = line.upper();
            elif(self.lower):
                line = line.lower();
            
            lines[i] = line;
        self.lines = lines;