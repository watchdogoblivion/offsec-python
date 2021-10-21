# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Arguments

from watchdogs.base.models import Args
from watchdogs.utils.Constants import (EMPTY)


class RequestArgs(Args):

  VERSION = "Request version: 1.0"

  def __init__(self, remoteHost=EMPTY, secure=False, postFile=EMPTY, multiPart=False, httpProxy=EMPTY,
               httpsProxy=EMPTY, disableVerification=False, readTimeout=None, filterLength=EMPTY,
               filterStatus=EMPTY, filterIn=EMPTY, filterOut=EMPTY, showResponse=False):
    #type: (str, bool, str, bool, str, str, bool, int, str, str, str, str, bool) -> None
    super(RequestArgs, self).__init__()
    self.remoteHost = remoteHost
    self.secure = secure
    self.postFile = postFile
    self.multiPart = multiPart
    self.httpProxy = httpProxy
    self.httpsProxy = httpsProxy
    self.disableVerification = disableVerification
    self.readTimeout = readTimeout
    self.filterLength = filterLength
    self.filterStatus = filterStatus
    self.filterIn = filterIn
    self.filterOut = filterOut
    self.showResponse = showResponse

  def getVersion(self):  #type: () -> str
    return RequestArgs.VERSION

  def addArguments(self):  #type: () -> RequestArgs
    RH_HELP = "Explictly specify the remote host."
    S_HELP = "Specifies https."
    PF_HELP = ("Specify a file to send in a POST request."
               "\nThis flag is for file uploads only and should not be used for other POST requests")
    MP_HELP = ("Specify this when the request is sending multipart data")
    HP_HELP = "Specify a proxy."
    SP_HELP = "Specify an ssl proxy"
    DV_HELP = "For https proxies, this flag will disable cert verification."
    RT_HELP = "Specify the requests read time out."
    FL_HELP = "Filter OUT responses by coma separated lengths"
    FS_HELP = "Filter IN responses by coma separated status codes"
    FI_HELP = "Filters in and keeps the responses with the specified text"
    FO_HELP = "Filters out and removes the responses with the specified text"
    SR_HELP = "Shows the response body"

    parser = self.getParser()
    required = parser.add_argument_group("Required request arguments")
    required.add_argument("-rh", "--remote-host", required=True, help=RH_HELP, type=str, metavar="127.0.0.1")
    parser.add_argument("-s", "--secure", action="store_true", help=S_HELP)
    parser.add_argument("-pf", "--post-file", help=PF_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-mp", "--multi-part", action="store_true", help=MP_HELP)
    parser.add_argument("-hp", "--http-proxy", help=HP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sp", "--https-proxy", help=SP_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-dv", "--disable-verification", action="store_true", help=DV_HELP, default=False)
    parser.add_argument("-rt", "--read-timeout", help=RT_HELP, type=int, metavar=EMPTY, default=None)
    parser.add_argument("-fl", "--filter-length", help=FL_HELP, type=str, metavar=EMPTY, default=EMPTY)
    parser.add_argument("-fs", "--filter-status", help=FS_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fi", "--filter-in", help=FI_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-fo", "--filter-out", help=FO_HELP, type=str, metavar=EMPTY)
    parser.add_argument("-sr", "--show-response", action="store_true", help=SR_HELP)

    return self