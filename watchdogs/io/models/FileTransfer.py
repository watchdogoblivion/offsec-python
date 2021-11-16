# author: WatchDogOblivion
# description: TODO
# WatchDogs File Transfer

from watchdogs.base.models import Common


class FileTransfer(Common):

  def __init__(self, uploadFile=None, uploadedFile=None, downloadFile=None, downloadedFile=None):
    #type: (str, str, str, str) -> None
    super(FileTransfer, self).__init__()
    self.__uploadFile = uploadFile
    self.__uploadedFile = uploadedFile
    self.__downloadFile = downloadFile
    self.__downloadedFile = downloadedFile

  def getUploadFile(self):  #type: () -> str
    return self.__uploadFile

  def setUploadFile(self, uploadFile):  #type: (str) -> None
    self.__uploadFile = uploadFile

  def getUploadedFile(self):  #type: () -> str
    return self.__uploadedFile

  def setUploadedFile(self, uploadedFile):  #type: (str) -> None
    self.__uploadedFile = uploadedFile

  def getDownloadFile(self):  #type: () -> str
    return self.__downloadFile

  def setDownloadFile(self, downloadFile):  #type: (str) -> None
    self.__downloadFile = downloadFile

  def getDownloadedFile(self):  #type: () -> str
    return self.__downloadedFile

  def setDownloadedFile(self, downloadedFile):  #type: (str) -> None
    self.__downloadedFile = downloadedFile
