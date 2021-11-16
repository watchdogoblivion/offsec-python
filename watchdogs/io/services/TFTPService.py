# author: WatchDogOblivion
# description: TODO
# WatchDogs TFTP Service

import tftpy
from tftpy.TftpShared import TftpException

from watchdogs.base.models import AllArgs, Common  # pylint: disable=unused-import
from watchdogs.io.models import FileTransfer
from watchdogs.io.parsers import TFTPArgs, OFileArgs
from watchdogs.utils.StringUtility import StringUtility
from watchdogs.utils.Constants import (LR)

ERROR_CODES = [256]


class TFTPService(Common):

  @staticmethod
  def transferFile(allArgs, fileTransfer):
    #type: (AllArgs, FileTransfer) -> None
    tFTPArgs = allArgs.getArgs(TFTPArgs)
    try:
      client = tftpy.TftpClient(tFTPArgs.remoteHost, tFTPArgs.remotePort)
      if (tFTPArgs.upload):
        print(fileTransfer.getUploadFile(), fileTransfer.getUploadedFile())
        client.upload(fileTransfer.getUploadedFile(), fileTransfer.getUploadFile(), timeout=tFTPArgs.timeout)
      else:
        print(fileTransfer.getDownloadFile(), fileTransfer.getDownloadedFile())
        client.download(fileTransfer.getDownloadFile(), fileTransfer.getDownloadedFile(),
                        timeout=tFTPArgs.timeout)
    except TftpException as tftpe:
      error = "errorcode = "
      if (error in str(tftpe)):
        for errorCode in ERROR_CODES:
          error += str(errorCode)
          if (str(256) in error):
            print('File not found on remote server')
      else:
        print(tftpe)

  def delegate(self, allArgs, localFile=None, remoteFile=None):
    #type: (AllArgs, str, str) -> None
    tFTPArgs = allArgs.getArgs(TFTPArgs)
    fileTransfer = FileTransfer()
    if (tFTPArgs.upload):
      if (remoteFile is None):
        remoteFile = localFile
        remoteFile = StringUtility.getFileName(remoteFile)
      fileTransfer.setUploadFile(localFile.rstrip())
      fileTransfer.setUploadedFile(remoteFile.rstrip())
      self.transferFile(allArgs, fileTransfer)
    else:
      if (localFile is None):
        localFile = remoteFile
        localFile = StringUtility.getFileName(localFile, "_")
      fileTransfer.setDownloadFile(remoteFile.rstrip())
      fileTransfer.setDownloadedFile(localFile.rstrip())
      self.transferFile(allArgs, fileTransfer)

  def process(self, allArgs):
    #type: (AllArgs) -> None
    fileArgs = allArgs.getArgs(OFileArgs)
    tFTPArgs = allArgs.getArgs(TFTPArgs)
    inputFile = fileArgs.inputFile

    if (inputFile):
      lines = open(inputFile, LR).readlines()
      for line in lines:
        if (tFTPArgs.upload):
          self.delegate(allArgs, localFile=line)
        else:
          self.delegate(allArgs, remoteFile=line)
    else:
      if (tFTPArgs.upload):
        self.delegate(allArgs, tFTPArgs.uploadFile, tFTPArgs.uploadedFile)
      else:
        self.delegate(allArgs, tFTPArgs.downloadedFile, tFTPArgs.downloadFile)
