# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer Arguments

import argparse

from watchdogs.io.models import FileArgs
from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY, COLON)


class FileFuzzerArgs(FileArgs, Common):

  VERSION = "1.0"

  def __init__(self):
    super(FileFuzzerArgs, self).__init__()
    self.requestFields = []  #type: list[str]
    self.remoteHost = EMPTY  #type: str
    self.secure = False  #type: bool
    self.postFile = EMPTY  #type: str
    self.fuzzFile = EMPTY  #type: str
    self.fuzzDelimiter = COLON  #type: str
    self.httpProxy = EMPTY  #type: str
    self.httpsProxy = EMPTY  #type: str
    self.disableVerification = False  #type: bool
    self.readTimeout = None  #type: int
    self.filterLength = EMPTY  #type: str
    self.filterStatus = EMPTY  #type: str
    self.filterIn = EMPTY  #type: str
    self.filterOut = EMPTY  #type: str
    self.showResponse = False  #type: bool
    self.showFuzz = False  #type: bool

    self.parseArgs()
    self.setArguments()

  def parseArgs(self):  #type: (FileFuzzerArgs) -> None
    RH_HELP = "Explictly specify the remote host."
    IF_HELP = (
        "Specify the input file to read from.\nWhen executing POST, always ensure there is a new line"
        "feed separating the body from the headers.\nIf fuzzing, the file must include exactly 1 'FUZZ' keyword."
    )
    S_HELP = "Specifies https."
    OF_HELP = "Specify the output file to write to."
    PF_HELP = (
        "Specify a file to send in a POST request. This flag is for file uploads only and should not be"
        "used for other POST requests")
    FF_HELP = "Specify a file to fuzz with. If this is not specified, no fuzzing will occur"
    FD_HELP = "Specify the delimiter used to separate the words in the fuzz file"
    HP_HELP = "Specify a proxy."
    SP_HELP = "Specify an ssl proxy"
    DV_HELP = "For https proxies, this flag will disable cert verification."
    RT_HELP = "Specify the requests read time out."
    FL_HELP = "Filter OUT fuzzed responses by coma separated lengths"
    FS_HELP = "Filter IN fuzzed responses by coma separated status codes"
    FI_HELP = "Filters in and keeps the responses with the specified text"
    FO_HELP = "Filters out and removes the responses with the specified text"
    SR_HELP = "Shows the response body"
    SF_HELP = "Shows the fuzz text used in the request"
    V_HELP = "Show version"
    H_HELP = "Show this help message"
    VERSION = "File Fuzzer version: {}".format(FileFuzzerArgs.VERSION)

    self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    parser = self.parser
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-rh", "--remote-host", required=True, help=RH_HELP, type=str, metavar="127.0.0.1")
    required.add_argument("-if", "--input-file", required=True, help=IF_HELP, type=str, metavar="request.txt")
    parser.add_argument("-s", "--secure", action="store_true", help=S_HELP)
    parser.add_argument("-of", "--output-file", help=OF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-pf", "--post-file", help=PF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-ff", "--fuzz-file", help=FF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fd", "--fuzz-delimiter", help=FD_HELP, type=str, metavar=EMPTY, default=COLON)
    parser.add_argument("-hp", "--http-proxy", help=HP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sp", "--https-proxy", help=SP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-dv", "--disable-verification", action="store_true", help=DV_HELP, default=False)
    parser.add_argument("-rt", "--read-timeout", help=RT_HELP, type=int, metavar=EMPTY, default=None)
    parser.add_argument("-fl", "--filter-length", help=FL_HELP, type=str, metavar=EMPTY, default=EMPTY)
    parser.add_argument("-fs", "--filter-status", help=FS_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fi", "--filter-in", help=FI_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fo", "--filter-out", help=FO_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sr", "--show-response", action="store_true", help=SR_HELP)
    parser.add_argument("-sf", "--show-fuzz", action="store_true", help=SF_HELP)
    parser.add_argument("-v", "--version", action="version", help=V_HELP, version=VERSION)
    parser.add_argument("-h", "--help", action="help", help=H_HELP)
    self.parsedArgs = parser.parse_args()
