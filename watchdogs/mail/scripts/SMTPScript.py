# author: WatchDogOblivion
# description: TODO
# WatchDogs SMTP Script

import traceback

from watchdogs.base.models import AllArgs, Common
from watchdogs.mail.parsers import SMTPArgs
from watchdogs.mail.services import SMTPService

class SMTPScript(Common):

  def __init__(self, sMTPService=SMTPService()):
    #type: (SMTPScript) -> None
    super(SMTPScript, self).__init__()
    self.__sMTPService = sMTPService

  def getSMTPService(self):  #type: () -> SMTPService
    return self.__sMTPService

  def setSMTPService(self, sMTPService):  #type: (SMTPService) -> None
    self.__sMTPService = sMTPService

  def run(self):  #type: () -> None
    allArgs = AllArgs([SMTPArgs()]).mergeAndProcess()
    sMTPArgs = allArgs.getArgs(SMTPArgs)
    try:
      self.__sMTPService.sendEmail(allArgs)
    except ValueError:
      print(traceback.format_exc())
      print(sMTPArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(sMTPArgs.getParser().print_usage())
