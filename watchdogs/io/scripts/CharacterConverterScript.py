# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Script

import traceback

from watchdogs.base.models import Common, AllArgs
from watchdogs.io.models.File import File
from watchdogs.io.parsers import CharacterConverterArgs, FileArgs
from watchdogs.io.services.CharacterConverterService import CharacterConverterService


class CharacterConverterScript(Common):

  def __init__(self, characterConverterService=CharacterConverterService()):
    #type: (CharacterConverterService) -> None
    super(CharacterConverterScript, self).__init__()
    self.__characterConverterService = characterConverterService

  def getCharacterConverterService(self):
    #type: () -> CharacterConverterService
    return self.__characterConverterService

  def setCharacterConverterService(self, characterConverterService):
    #type: (CharacterConverterService) -> None
    self.__characterConverterService = characterConverterService

  def run(self):  #type: (CharacterConverterScript) -> None
    allArgs = AllArgs([CharacterConverterArgs(), FileArgs()]).processAllArguments()
    cConverterArgs = allArgs.getArgs(CharacterConverterArgs)
    cConverterService = self.__characterConverterService
    file = File()
    try:
      cConverterService.readLines(allArgs, file)
      if allArgs.getArgs(FileArgs).outputFile:
        cConverterService.writeLines(allArgs, file)
      else:
        cConverterService.printLines(file)
    except ValueError as ve:
      print(ve)
      print(cConverterArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(cConverterArgs.getParser().print_usage())