# author: WatchDogOblivion
# description: TODO
# WatchDogs TFTP Arguments

from watchdogs.base.models import Args
from watchdogs.utils.Constants import (EMPTY)


class TFTPArgs(Args):  # pylint: disable=too-many-instance-attributes

  VERSION = "TFTP args version: 1.0"

  def __init__(  # pylint: disable=too-many-arguments
      self, remoteHost="10.11.1.111", remotePort=69, upload=False,
      downloadFile=r'\windows\System32\drivers\etc\hosts', downloadedFile=None, uploadFile='./test',
      uploadedFile=None, timeout=5):
    #type: (str, int, bool, str, str, str, str, int) -> None
    super(TFTPArgs, self).__init__()
    self.remoteHost = remoteHost
    self.remotePort = remotePort
    self.upload = upload
    self.downloadFile = downloadFile
    self.downloadedFile = downloadedFile
    self.uploadFile = uploadFile
    self.uploadedFile = uploadedFile
    self.timeout = timeout

  def getVersion(self):  #type: () -> str
    return TFTPArgs.VERSION

  def addArguments(self):  #type: () -> TFTPArgs
    RH_HELP = "Specify the remote host."
    RP_HELP = "Specify the TFTP port. The default is 69"
    U_HELP = "Specify whether to upload."
    DF_HELP = "Specify the name of the file to download from the remote host"
    DDF_HELP = "Specify what to name the file downloaded from the remote host"
    UF_HELP = "Specify the name of the file to upload to the remote host"
    UDF_HELP = "Specify what to name the file uploaded to the remote host"
    T_HELP = "Specify the TFTP timeout"

    parser = self.getParser()
    required = parser.add_argument_group("Required TFTP arguments")
    required.add_argument("-rh", "--remote-host", required=True, help=RH_HELP, type=str,
                          metavar="10.11.1.111")

    optional = parser.add_argument_group("Optional TFTP arguments")
    optional.add_argument("-rp", "--remote-port", help=RP_HELP, type=int, metavar=EMPTY, default=69)
    optional.add_argument("-u", "--upload", action="store_true", help=U_HELP)
    optional.add_argument("-df", "--download-file", help=DF_HELP, type=str, metavar=EMPTY,
                          default=r'\windows\System32\drivers\etc\hosts')
    optional.add_argument("-ddf", "--downloaded-file", help=DDF_HELP, type=str, metavar=EMPTY, default=None)
    optional.add_argument("-uf", "--upload-file", help=UF_HELP, type=str, metavar=EMPTY, default="./test")
    optional.add_argument("-udf", "--uploaded-file", help=UDF_HELP, type=str, metavar=EMPTY, default=None)
    optional.add_argument("-t", "--timeout", help=T_HELP, type=int, metavar=EMPTY, default=5)

    return self
