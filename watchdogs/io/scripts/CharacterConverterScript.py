# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Script

import traceback

from watchdogs.base.models import Common
from watchdogs.io.models.CharacterConverterArgs import CharacterConverterArgs
from watchdogs.io.services.CharacterConverterService import CharacterConverterService


class CharacterConverterScript(Common):

  def __init__(self, characterConverterService=CharacterConverterService()):
    super(CharacterConverterScript, self).__init__()
    self.characterConverterService = characterConverterService  #type: CharacterConverterService

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
      print(cConverterArgs.parser.print_usage())
    except Exception:
      print(traceback.format_exc())
      print(cConverterArgs.parser.print_usage())