# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder

import urllib
import base64
import argparse
from collections import OrderedDict

from watchdogs.io import File
from watchdogs.utils.Constants import (LFN, EMPTY, FS, LR)


class FileEncoder(File):

  VERSION = "1.0"
  V1 = "v1"; V2 = "v2"; V3 = "v3"

  URL_ENCODING_OPTIONS = OrderedDict([
      (V1, "Encodes everything except forward slash '/'"),
      (V2, "Encodes everything. Spaces turn to '+'"),
      (V3, "Encodes everything. Spaces turn to %20 and forward slashes to %2F"),
  ])

  def __init__(self):
    super(FileEncoder, self).__init__()
    self.b64Encode = False  #type: bool
    self.urlEncode = None  #type: str

  def getEncodingOptions(self):  #type: (FileEncoder) -> None
    options = FileEncoder.URL_ENCODING_OPTIONS
    optionsString = "Encoding options:" + LFN
    for optionsKey, optionsValue in options.items():
      optionsString += "  {}) {}{}".format(optionsKey, optionsValue, LFN)
    return optionsString

  def parseArgs(self):  #type: (FileEncoder) -> None
    IF_HELP = "Specify the input file to read from."
    OF_HELP = "Specify the output file to write to."
    BE_HELP = "Specify if you want to perform base64 encoding. Enabled by default"
    UE_HELP = "Specify if you want to perform url encoding. Look at flag -uo/ue-options for arguments"
    UO_HELP = "Show url encoding options"
    V_HELP = "Show version"
    H_HELP = "Show this help message"
    ENCODINGS = "{}".format(self.getEncodingOptions())
    VERSION = "Character Converter version: {}".format(FileEncoder.VERSION)

    self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    parser = self.parser
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-be", "--b64-encode", action="store_true", help=BE_HELP, default=False)
    parser.add_argument("-ue", "--url-encode", help=UE_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-uo", "--ue-options", action="version", help=UO_HELP, version=ENCODINGS)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    parser.add_argument("-h", "--help", action="help", help=H_HELP)
    self.parsedArgs = parser.parse_args()

  def readLines(self):  #type: (FileEncoder) -> None
    openedFile = open(self.inputFile, LR)
    lines = openedFile.readlines()
    linesLength = len(lines)
    encodedLines = []

    for index in range(linesLength):
      encoded = lines[index].rstrip()
      urlEncode = self.urlEncode

      if (self.b64Encode):
        encoded = base64.b64encode(encoded)

      if (urlEncode == FileEncoder.V1):
        encoded = urllib.quote(encoded)
      elif (urlEncode == FileEncoder.V2):
        encoded = urllib.quote_plus(encoded)
      elif (urlEncode == FileEncoder.V3):
        encoded = str(urllib.quote(encoded)).replace(FS, "%2F")

      if (index + 1 == linesLength):
        encodedLines.append(encoded)
      else:
        encodedLines.append(encoded + LFN)

    self.lines = encodedLines
