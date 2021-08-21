# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder

import urllib;
import base64;
import argparse;
from collections import OrderedDict;

from watchdogs.io import File;
from watchdogs.utils.Constants import *;

class FileEncoder(File):

    VERSION = "1.0";
    URL_ENCODING_OPTIONS = OrderedDict([
        ("v1","Encodes everything except forward slash '/'"),
        ("v2","Encodes everything. Spaces turn to '+'"),
        ("v3","Encodes everything. Spaces turn to %20 and forward slashes to %2F"),
    ]);

    def __init__(self):
        super(FileEncoder, self).__init__();
        self.b64Encode = False;
        self.urlEncode = None;
    
    def getEncodingOptions(self):
        options = FileEncoder.URL_ENCODING_OPTIONS;
        optionsString = "Encoding options:"+LFN;
        for k,v in options.items():
            optionsString += "  {}) {}{}".format(k,v,LFN);
        return optionsString;

    def parseArgs(self):
        self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        required.add_argument("-if", "--input-file", required=True, help="Specify the input file to read from.", type=str, metavar=EMPTY);
        parser.add_argument("-of", "--output-file", help="Specify the output file to write to.", type=str, metavar=EMPTY);
        parser.add_argument("-be", "--b64-encode", action="store_true", help="Specify if you want to perform base64 encoding. Enabled by default", default=False);
        parser.add_argument("-ue", "--url-encode", help="Specify if you want to perform url encoding. Look at flag -uo/ue-options for arguments");
        parser.add_argument("-uo", "--ue-options", action="version", help="Show url encoding options", version="{}".format(self.getEncodingOptions()));
        parser.add_argument("-v", "--version", action="version", help="Show version", version="Character Converter version: {}".format(FileEncoder.VERSION));
        parser.add_argument("-h", "--help", action="help", help="Show this help message");
        self.args = parser.parse_args();

        
    def readLines(self):
        openedFile = open(self.inputFile, "r");
        lines = openedFile.readlines();
        length = len(lines);

        for i in range(length):
            encoded = lines[i].rstrip();
            urlEncode = self.urlEncode;
            
            if(self.b64Encode):
                encoded = base64.b64encode(encoded);

            if(urlEncode == "v1"):
                encoded = urllib.quote(encoded);
            elif(urlEncode == "v2"):
                encoded = urllib.quote_plus(encoded);
            elif(urlEncode == "v3"):
                encoded = encoded = urllib.quote(encoded).replace(FS,"%2F");
            
            if(i + 1 == length):
                lines[i] = encoded;
            else:
                lines[i] = encoded+LFN;
            
        self.lines = lines;