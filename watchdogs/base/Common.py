# author: WatchDogOblivion
# description: TODO
# WatchDogs Common

import json;

class Common(object):

    def __init__(self):
        super(Common, self).__init__();

    def __str__(self):#type: (Common) -> str
        return json.dumps(self, default=lambda obj: obj.__dict__);

    def __repr__(self):#type: (Common) -> str
        return json.dumps(self, default=lambda obj: obj.__dict__);