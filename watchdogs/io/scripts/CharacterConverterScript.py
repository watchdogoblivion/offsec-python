# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Script

import traceback

from watchdogs.base.models import Common
from watchdogs.io.parsers import CharacterConverterArgs
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
    cConverterArgs = CharacterConverterArgs()
    cConverterService = CharacterConverterService()
    try:
      cConverterService.readLines(cConverterArgs)
      if cConverterArgs.outputFile:
        cConverterService.writeLines(cConverterArgs.outputFile)
      else:
        cConverterService.printLines()
    except ValueError as ve:
      print(ve)
      print(cConverterArgs.getParser().print_usage())
    except Exception:
      print(traceback.format_exc())
      print(cConverterArgs.getParser().print_usage())