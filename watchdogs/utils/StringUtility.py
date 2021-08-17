# author: WatchDogOblivion
# description: TODO
# WatchDogs String Utility

import re;

class StringUtility(object):

    @staticmethod
    def strTobool(s, customArray=None):
        if customArray:
            return s.lower() in customArray;
        return s.lower() in ("yes", "y", "true", "t");
    
    @staticmethod
    def handleType(convertTo, convertFrom, boolArray=None):
        typeTo = str(type(convertTo));
        typeFrom = type(convertFrom);

        if not typeTo == typeFrom:
            if typeTo.find("int") > -1:
                convertFrom = int(convertFrom);
            elif typeTo.find("str") > -1:
                convertFrom = str(convertFrom);
            elif typeTo.find("bool") > -1:
                convertFrom = StringUtility.strTobool(convertFrom, boolArray);
        return convertFrom;
    
    @staticmethod
    def toCamel(string,char="_"):
        camel = "";
        strings = string.split(char);
        length = len(strings);
        for i in range(length):
            s = strings[i];
            if(i == 0):
                camel += s.lower();
            else:
                camel += s[0].upper() + s[1:].lower();
        return camel;
    
    @staticmethod
    def sanitize(string, dic):
        cleansed = "";
        for k,v in dic.iteritems():
            cleansed = string.replace(k,v);
        return cleansed;
    
    @staticmethod
    def naturalOrdering(string):
        specArray = []
        stringArray = re.split(r'(\d+)', string);
        for s in stringArray:
            if(s.isdigit()):
                specArray.append(int(s));
            else:
                specArray.append(s);
        return specArray;