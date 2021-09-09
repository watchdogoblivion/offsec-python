# author: WatchDogOblivion
# description: TODO
# WatchDogs Character Converter Service

from watchdogs.base.models import Common
from watchdogs.io.services.FileService import FileService
from watchdogs.io.parsers import CharacterConverterArgs
from watchdogs.utils.Constants import (LR, SPACE)


class CharacterConverterService(FileService, Common):

  def __init__(self):  #type: () -> None
    super(CharacterConverterService, self).__init__()

  def readLines(self, characterConverterArgs):  #type: (CharacterConverterArgs) -> None
    openedFile = open(characterConverterArgs.getInputFile(), LR)
    fileLines = openedFile.readlines()
    increment = 1
    linesRead = []
    oldChar = characterConverterArgs.getOldChar()
    newChar = characterConverterArgs.getNewChar()
    incrementWord = characterConverterArgs.isIncrementWord()

    for line in fileLines:
      if (characterConverterArgs.isIncrementLine() and newChar):
        if (line.find(oldChar) > -1):
          line = line.replace(oldChar, "{}{}".format(str(increment), newChar))
          increment += 1
      elif (incrementWord and newChar):
        line = self.swapAndIncrementWord(characterConverterArgs, line, increment)
      else:
        line = line.replace(oldChar, newChar)

      if (characterConverterArgs.isUpper()):
        line = line.upper()
      elif (characterConverterArgs.isLower()):
        line = line.lower()

      linesRead.append(line)
    self.getFile().setLines(linesRead)

  def swapAndIncrementWord(self, characterConverterArgs, line, increment):
    #type: (CharacterConverterArgs, str, int) -> None
    oldChar = characterConverterArgs.getOldChar()
    newChar = characterConverterArgs.getNewChar()
    words = line.split(SPACE)
    wordsLength = len(words)
    for wordIndex in range(wordsLength):
      word = words[wordIndex]
      if (word.find(oldChar) > -1):
        words[wordIndex] = word.replace(oldChar, "{}{}".format(str(increment), newChar))
        increment += 1
    line = SPACE.join(words)
    return line