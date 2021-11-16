# author: WatchDogOblivion
# description: TODO
# WatchDogs String Utility

import re
from typing import Any # pylint: disable=unused-import

from watchdogs.utils.Constants import (EMPTY, USC)
from watchdogs.utils.Constants import (FS, BS) # pylint: disable=unused-import

class StringUtility(object):

  @staticmethod
  def strTobool(string, truthyArray=["yes", "y", "true", "t"]): # pylint: disable=dangerous-default-value
    #type: (str, list[str]) -> bool
    return string.lower() in truthyArray

  @staticmethod
  def toCamelCase(string, delimiter=USC):  #type: (str, str) -> str
    camelCasedString = EMPTY
    strings = string.split(delimiter)
    stringsLength = len(strings)
    for index in range(stringsLength):
      word = strings[index]
      if (index == 0):
        camelCasedString += word.lower()
      else:
        camelCasedString += word[0].upper() + word[1:].lower()
    return camelCasedString

  @staticmethod
  def sanitize(string, dict):  #type: (str, dict[str,str]) -> str
    sanitizedString = EMPTY
    for dictKey, dictValue in dict.items():
      sanitizedString = string.replace(dictKey, dictValue)
    return sanitizedString

  @staticmethod
  def naturalOrdering(string):  #type: (str) -> list
    specificationArray = []
    stringArray = re.split(r'(\d+)', string)
    for s in stringArray:
      if (s.isdigit()):
        specificationArray.append(int(s))
      else:
        specificationArray.append(s)
    return specificationArray

  @staticmethod
  def toHexFormat(string): #type:(str) -> str
    hexString = ""
    hexFormat = "0x{:02x}"
    for charachter in string:
      unicodeNumber = ord(charachter)
      hexString += hexFormat.format(unicodeNumber)
    return hexString

  @staticmethod
  def charsToHex(string, assembly=False):  #type:(str,bool)->str
    hexString = ""
    for charachter in string:
      unicodeNumber = ord(charachter)
      hexString += hex(unicodeNumber)
    if (assembly):
      hexString = hexString.replace("0x", "\\x")
    return hexString

  @staticmethod
  def charsToDeci(charString):  #type:(str) -> str
    newDelimiter = ":"
    decimalString = ""
    for character in charString:
      decimalString += str(ord(character)) + newDelimiter
    return decimalString.rstrip(newDelimiter)

  @staticmethod
  def hexToChars(hexString, delimiter="0x"):  #type:(str, str) -> str
    hexArray = hexString.split(delimiter)
    charsString = ""
    for hex in hexArray:
      if (hex):
        unicodeNumber = int(hex, 16)
        charsString += chr(unicodeNumber)
    return charsString

  @staticmethod
  def hexToDeci(hexString, delimiter="0x"):  #type:(str, str) -> str
    hexArray = hexString.split(delimiter)
    newDelimiter = ":"
    decimalString = ""
    for hex in hexArray:
      if (hex):
        unicodeNumber = int(hex, 16)
        decimalString += str(unicodeNumber) + newDelimiter
    return decimalString.rstrip(newDelimiter)

  @staticmethod
  def deciToChars(deciString, delimiter=":"):  #type:(str, str) -> str
    deciArray = deciString.split(delimiter)
    charsString = ""
    for decimal in deciArray:
      charsString += chr(int(decimal))
    return charsString

  @staticmethod
  def deciToHex(deciString, delimiter=":"):  #type:(str, str) -> str
    deciArray = deciString.split(delimiter)
    hexString = ""
    for decimal in deciArray:
      hexString += hex(int(decimal))
    return hexString

  @staticmethod
  def getFileName(name, repl=None):
    #type:(str, str) -> str
    fileName = name
    if (FS in name):
      if(repl):
        fileName = name.replace(FS, repl)
      else:
        index = name.rfind(FS)
        fileName = name[index + 1:]
    if (BS in name):
      if(repl):
        fileName = name.replace(BS, repl)
      else:
        index = name.rfind(BS)
        fileName = name[index + 1:]
    return fileName
