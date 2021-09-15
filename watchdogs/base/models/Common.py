# author: WatchDogOblivion
# description: TODO
# WatchDogs Common

import json
from typing import Any


class Common(object):

  def __init__(self):  #type: () -> None
    super(Common, self).__init__()

  def prepForDump(self, obj):  #type: (Any) -> Any

    if (hasattr(obj, "__dict__")):
      return obj.__dict__
    else:
      return str(obj)

  def __str__(self):  #type: () -> str
    return json.dumps(self, default=lambda obj: self.prepForDump(obj))

  def __repr__(self):  #type: () -> str
    return json.dumps(self, default=lambda obj: self.prepForDump(obj))