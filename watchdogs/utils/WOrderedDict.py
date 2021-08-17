# author: WatchDogOblivion
# description: TODO
# WatchDogs Dict

from collections import OrderedDict;

class WOrderedDict(OrderedDict):
        
    def __init__(self, args):
        super(WOrderedDict, self).__init__(args);

    def wItems(self):
        if callable(getattr(self, "iteritems", None)):
            return super(WOrderedDict, self).iteritems();
        else:
            return super().items();