# author: WatchDogOblivion
# description: TODO
# WatchDogs Cast Utility

import json
import traceback
from typing import Type, Any

from watchdogs.utils.Constants import T


class Cast(object):

  def __init__(self):
    super(Cast, self).__init__()

  @staticmethod
  def _to(clazz, obj):  #type: (Any, object) -> str
    if (clazz == str):
      return json.dumps(obj, default=lambda obj: obj.__dict__)

  @staticmethod
  def _from(obj, clazz):  #type: (object, Type[T]) -> T
    newinstance = clazz()
    try:
      if (isinstance(obj, str)):
        jsonObj = json.loads(obj)  #type: dict
        objKeys = jsonObj.keys()
        for objKey in objKeys:
          setattr(newinstance, objKey, jsonObj[objKey])
      else:
        objKeys = obj.__dict__.keys()
        for objKey in objKeys:
          setattr(newinstance, objKey, getattr(obj, objKey))
    except AttributeError:
      print(traceback.format_exc())
    return newinstance
