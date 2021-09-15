# author: WatchDogOblivion
# description: TODO
# WatchDogs List Utility


class ListUtility(object):

  @staticmethod
  def group(lst, groupSize):
    #type: (list, int) -> list
    finalList = []
    groupSizeList = range(0, len(lst), groupSize)
    for groupSizeIndex in groupSizeList:
      finalList.append(lst[groupSizeIndex:groupSizeIndex + groupSize])
    return finalList