# author: WatchDogOblivion
# description: TODO
# WatchDogs String Utility

import re
from typing import Any

from watchdogs.utils.Constants import (EMPTY, USC)

class StringUtility(object):

  @staticmethod
  def strTobool(string, truthyArray=["yes", "y", "true", "t"]):  #type: (str, list[str]) -> bool
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
