# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Service

from watchdogs.base.models import Common
from watchdogs.io.services.FileService import FileService
from watchdogs.io.models.CharacterConverterArgs import CharacterConverterArgs
from watchdogs.utils.Constants import (LR, SPACE)


class CharacterConverterService(FileService, Common):

  def __init__(self):
    super(CharacterConverterService, self).__init__()

  def readLines(self, characterConverterArgs):
    #type: (CharacterConverterService, CharacterConverterArgs) -> None
    openedFile = open(characterConverterArgs.inputFile, LR)
    fileLines = openedFile.readlines()
    increment = 1
    linesRead = []
    oldChar = characterConverterArgs.oldChar
    newChar = characterConverterArgs.newChar
    incrementWord = characterConverterArgs.incrementWord

    for line in fileLines:
      if (characterConverterArgs.incrementLine and newChar):
        if (line.find(oldChar) > -1):
          line = line.replace(oldChar, "{}{}".format(str(increment), newChar))
          increment += 1
      elif (incrementWord and newChar):
        line = self.swapAndIncrementWord(characterConverterArgs, line, increment)
      else:
        line = line.replace(oldChar, newChar)

      if (characterConverterArgs.upper):
        line = line.upper()
      elif (characterConverterArgs.lower):
        line = line.lower()

      linesRead.append(line)
    self.file.lines = linesRead

  def swapAndIncrementWord(self, characterConverterArgs, line, increment):
    #type: (CharacterConverterService, CharacterConverterArgs, str, int) -> None
    oldChar = characterConverterArgs.oldChar
    newChar = characterConverterArgs.newChar
    words = line.split(SPACE)
    wordsLength = len(words)
    for wordIndex in range(wordsLength):
      word = words[wordIndex]
      if (word.find(oldChar) > -1):
        words[wordIndex] = word.replace(oldChar, "{}{}".format(str(increment), newChar))
        increment += 1
    line = SPACE.join(words)
    return line