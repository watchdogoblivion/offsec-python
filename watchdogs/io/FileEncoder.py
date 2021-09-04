# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder

import urllib
import base64
import argparse
from collections import OrderedDict

from watchdogs.io import File
from watchdogs.utils.Constants import *


class FileEncoder(File):

  VERSION = "1.0"
  URL_ENCODING_OPTIONS = OrderedDict([
      ("v1", "Encodes everything except forward slash '/'"),
      ("v2", "Encodes everything. Spaces turn to '+'"),
      ("v3", "Encodes everything. Spaces turn to %20 and forward slashes to %2F"),
  ])

  def __init__(self):
    super(FileEncoder, self).__init__()
    self.b64Encode = False  #type: bool
    self.urlEncode = None  #type: str

  def getEncodingOptions(self):  #type: (FileEncoder) -> None
    options = FileEncoder.URL_ENCODING_OPTIONS
    optionsString = "Encoding options:" + LFN
    for k, v in options.items():
      optionsString += "  {}) {}{}".format(k, v, LFN)
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
    self.args = parser.parse_args()

  def readLines(self):  #type: (FileEncoder) -> None
    openedFile = open(self.inputFile, "r")
    lines = openedFile.readlines()
    length = len(lines)

    for i in range(length):
      encoded = lines[i].rstrip()
      urlEncode = self.urlEncode

      if (self.b64Encode):
        encoded = base64.b64encode(encoded)

      if (urlEncode == "v1"):
        encoded = urllib.quote(encoded)
      elif (urlEncode == "v2"):
        encoded = urllib.quote_plus(encoded)
      elif (urlEncode == "v3"):
        encoded = encoded = urllib.quote(encoded).replace(FS, "%2F")

      if (i + 1 == length):
        lines[i] = encoded
      else:
        lines[i] = encoded + LFN

    self.lines = lines
