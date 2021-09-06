# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

from collections import OrderedDict

from watchdogs.base.models import Common
from watchdogs.utils.Constants import (EMPTY)
from watchdogs.web.models.Locators import FuzzLocators


class FileFuzzer(Common):

  def __init__(self):
    super(FileFuzzer, self).__init__()
    self.requestFields = []  #type: list[str]
    self.remoteHost = EMPTY  #type: str
    self.raw_info = EMPTY  #type: str
    self.raw_headers = EMPTY  #type: str
    self.raw_body = EMPTY  #type: str
    self.requestInfo = OrderedDict()  #type: OrderedDict
    self.requestUrl = EMPTY  #type: str
    self.requestHeaders = OrderedDict()  #type: OrderedDict
    self.requestBoundary = EMPTY  #type: str
    self.requestBody = OrderedDict()  #type: OrderedDict
    self.fuzzLocators = FuzzLocators()  #type: FuzzLocators
    self.FuzzValuesString = EMPTY  #type: str