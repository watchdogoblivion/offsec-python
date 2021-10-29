# author: WatchDogOblivion
# description: TODO
# WatchDogs General Utility
# pylint: disable=too-few-public-methods

import urllib

class GeneralUtility(object):

  @staticmethod
  def printTime(start, end):
    #type:(int,int)->None
    totalTime = end - start
    if (totalTime > 60):
      print("Total time: {} minutes".format(round(totalTime / 60, 2)))
    else:
      print("Total time: {} seconds".format(totalTime))

  @staticmethod
  def urlEncode(url):
    return urllib.quote(url)
