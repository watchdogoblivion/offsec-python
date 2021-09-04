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
  def _to(_type, obj):  #type: (Any, object) -> str
    if (_type == str):
      return json.dumps(obj, default=lambda obj: obj.__dict__)

  @staticmethod
  def _from(obj, clazz):  #type: (object, Type[T]) -> T
    _type = type(obj)
    newinstance = clazz()
    try:
      if (_type == str):
        jsonObj = json.loads(obj)  #type: dict
        objKeys = jsonObj.keys()
        for objKey in objKeys:
          setattr(newinstance, objKey, jsonObj[objKey])
      else:
        objKeys = obj.__dict__.keys()
        for objKey in objKeys:
          setattr(newinstance, objKey, getattr(obj, objKey))
      return newinstance
    except AttributeError as ae:
      print(traceback.format_exc())
