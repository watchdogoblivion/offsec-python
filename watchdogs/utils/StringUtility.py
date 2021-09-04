# author: WatchDogOblivion
# description: TODO
# WatchDogs String Utility

import re;
from typing import Any;

class StringUtility(object):

    @staticmethod
    def strTobool(s, customArray=None):#type: (str, list[str]) -> bool
        if customArray:
            return s.lower() in customArray;
        return s.lower() in ("yes", "y", "true", "t");
    
    @staticmethod
    def handleType(convertTo, convertFrom, boolArray=None):#type: (Any, Any, list[bool]) -> Any
        typeTo = str(type(convertTo));
        typeFrom = type(convertFrom);
        converted = convertFrom;

        if not typeTo == typeFrom:
            if typeTo.find("int") > -1:
                converted = int(convertFrom);
            elif typeTo.find("str") > -1:
                converted = str(convertFrom);
            elif typeTo.find("bool") > -1:
                converted = StringUtility.strTobool(convertFrom, boolArray);
        return converted;
    
    @staticmethod
    def toCamel(string,char="_"):#type: (str, str) -> str
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
    def sanitize(string, dic):#type: (str, dict[str,str]) -> str
        cleansed = "";
        for k,v in dic.items():
            cleansed = string.replace(k,v);
        return cleansed;
    
    @staticmethod
    def naturalOrdering(string):#type: (str) -> list
        specArray = []
        stringArray = re.split(r'(\d+)', string);
        for s in stringArray:
            if(s.isdigit()):
                specArray.append(int(s));
            else:
                specArray.append(s);
        return specArray;