# author: WatchDogOblivion
# description: TODO
# WatchDogs File Encoder Script

from collections import OrderedDict

from watchdogs.base.models.Args import Args
from watchdogs.utils.Constants import (LFN, EMPTY, V1, V2, V3)


class FileEncoderArgs(Args):

  VERSION = "Character Converter version: 1.0"

  URL_ENCODING_OPTIONS = OrderedDict([
      (V1, "Encodes everything except forward slash '/'"),
      (V2, "Encodes everything. Spaces turn to '+'"),
      (V3, "Encodes everything. Spaces turn to %20 and forward slashes to %2F"),
  ])

  def __init__(self, b64Encode=False, urlEncode=None):  #type: (bool, str) -> None
    super(FileEncoderArgs, self).__init__()
    self.b64Encode = b64Encode
    self.urlEncode = urlEncode

  def isB64Encode(self):  #type: () -> bool
    return self.b64Encode

  def setB64Encode(self, b64Encode):  #type: (bool) -> None
    self.b64Encode = b64Encode

  def getUrlEncode(self):  #type: () -> str
    return self.urlEncode

  def setUrlEncode(self, urlEncode):  #type: (str) -> None
    self.urlEncode = urlEncode

  def getEncodingOptions(self):  #type: () -> None
    options = FileEncoderArgs.URL_ENCODING_OPTIONS
    optionsString = "Encoding options:" + LFN
    for optionsKey, optionsValue in options.items():
      optionsString += "  {}) {}{}".format(optionsKey, optionsValue, LFN)
    return optionsString

  def getVersion(self):  #type: () -> str
    return FileEncoderArgs.VERSION

  def addArguments(self):  #type: () -> FileEncoderArgs
    BE_HELP = "Specify if you want to perform base64 encoding. Enabled by default"
    UE_HELP = "Specify if you want to perform url encoding. Look at flag -uo/ue-options for arguments"
    UO_HELP = "Show url encoding options"
    ENCODINGS = "{}".format(self.getEncodingOptions())

    parser = self.getParser()
    parser.add_argument("-be", "--b64-encode", action="store_true", help=BE_HELP, default=False)
    parser.add_argument("-ue", "--url-encode", help=UE_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-uo", "--ue-options", action="version", help=UO_HELP, version=ENCODINGS)

    return self