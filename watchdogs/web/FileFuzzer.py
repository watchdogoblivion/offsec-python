# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import argparse;
import requests;
from bs4 import BeautifulSoup;
from requests_toolbelt.multipart.encoder import MultipartEncoder;

from watchdogs.io import File;
from collections import OrderedDict;
from watchdogs.utils.Constants import *;

class FileFuzzer(File):

    VERSION = "1.0";

    def __init__(self):
        self.requestFields = [];
        self.secure = False;
        self.rhost = "";
        self.raw_info = "";
        self.raw_headers = "";
        self.raw_body = "";
        self.info = OrderedDict();
        self.url = "";
        self.headers = OrderedDict();
        self.boundary = "";
        self.body = OrderedDict();
        self.postFile = "";
        self.httpProxy = "";
        self.httpsProxy = "";
        self.fuzzLocator = OrderedDict();
        self.fuzzFile = "";
        self.filterLength = "";
        self.filterStatus = "";
        self.filterIn = "";
        self.filterOut = "";
        self.showResponse = False;
        self.showFuzz = False;
        self.FuzzText = "";
        
    def __setattr__(self, name, value):
        super(FileFuzzer, self).__setattr__(name, value);
        if not name in self.requestFields:
            if name.find("raw_") > -1 or name.find("_raw") > -1:
                self.requestFields.append(name);

        return value;
        
    def parseArgs(self):
        self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        ifHelp = "Specify the input file to read from.\nWhen executing POST, always ensure there is a new line feed separating the body from the headers.\nIf fuzzing, the file must include exactly 1 'FUZZ' keyword.";
        required.add_argument("-if", "--input-file", required=True, help=ifHelp, type=str, metavar="request.txt");
        required.add_argument("-rh", "--rhost", required=True, help="Explictly specify the remote host.", type=str, metavar="127.0.0.1");
        parser.add_argument("-s", "--secure", action="store_true", help="Specifies https.");
        parser.add_argument("-of", "--output-file", help="Specify the output file to write to.", type=str, metavar="");
        parser.add_argument("-pf", "--post-file", help="Specify a file to send in a POST request. This flag is for file uploads only and should not be used for other POST requests", type=str, metavar="");
        parser.add_argument("-ff", "--fuzz-file", help="Specify a file to fuzz with. If this is not specified, no fuzzing will occur", type=str, metavar="");
        parser.add_argument("-fl", "--filter-length", help="Filter OUT fuzzed responses by coma separated lengths", type=str, metavar="", default="");
        parser.add_argument("-fs", "--filter-status", help="Filter IN fuzzed responses by coma separated status codes", type=str, metavar="");
        parser.add_argument("-fi", "--filter-in", help="Filters in and keeps the responses with the specified text", type=str, metavar="");
        parser.add_argument("-fo", "--filter-out", help="Filters out and removes the responses with the specified text", type=str, metavar="");
        parser.add_argument("-hp", "--http-proxy", help="Specify a proxy.", type=str, metavar="");
        parser.add_argument("-hs", "--https-proxy", help="Specify an ssl proxy", type=str, metavar="");
        parser.add_argument("-sr", "--show-response", action="store_true", help="Shows the response body");
        parser.add_argument("-sf", "--show-fuzz", action="store_true", help="Shows the fuzz text used in the request");
        parser.add_argument("-v", "--version", action="version", help="Show version", version="File Fuzzer version: {}".format(FileFuzzer.VERSION));
        parser.add_argument("-h", "--help", action="help", help="Show this help message");
        self.args = parser.parse_args();
    
    def setBoundary(self,line,boundaryString):
        eIndex = line.find(EQUAL, line.find(boundaryString));
        scIndex = line.find(SEMI_COLON, eIndex);
        nlIndex = line.find(LFN);
        if(scIndex > -1):
            self.boundary = line[eIndex+1:scIndex];
        elif(nlIndex > -1):
            self.boundary = line[eIndex+1:nlIndex];
        else:
            self.boundary = line[eIndex+1:];

    def setFields(self, lines):
        fields = self.requestFields;
        value = EMPTY;
        isBody = False;
        length = len(lines);
        index = 0;

        while(index < length):
            line = lines[index].rstrip();
            boundaryString = BOUNDARY+EQUAL+DASH+DASH;
            if(boundaryString in line):
                self.setBoundary(line,boundaryString);
            if(index == 0):
                setattr(self, fields[0], line);
                index+=1;
                continue;
            elif(line == EMPTY and not isBody):
                isBody = True;
                setattr(self, fields[1], value);
                index+=1;
                value = "";
            elif(index+1 == length):
                setattr(self, fields[2], value);
                index+=1;
                break;

            value += line+"\n";
            index+=1;

    def parseInfo(self):
        info = self.raw_info.rstrip().split(SPACE);
        self.info[METHOD] = info[0];
        self.info[ENDPOINT] = info[1];
    
    def parseHeaders(self):
        headerArray = self.raw_headers.rstrip().split(LFN);
        for header in headerArray:
            index = header.find(COLON);
            self.headers[header[0:index]] = header[index+1:].strip();
        
    def parseBody(self):
        if(self.postFile):
            filteredList = [(l) for l in self.raw_body.split(LFN) if l and not self.boundary in l];
            length = len(filteredList);

            for index in range(length):
                cd = CONTENT_DISPOSITION+COLON;
                ct = CONTENT_TYPE+COLON;
                fn = FILE_NAME+EQUAL+DOUBLE_QUOTE;
                n = NAME+EQUAL+DOUBLE_QUOTE;
                line = filteredList[index];
                startName = line.find(DOUBLE_QUOTE, line.find(n));
                endName = line.find(DOUBLE_QUOTE, startName+1);

                if(fn in line):
                    name = line[startName+1:endName];
                    startFileName = line.find(DOUBLE_QUOTE, line.find(fn));
                    endFileName = line.find(DOUBLE_QUOTE, startFileName+1);
                    fileName = line[startFileName+1:endFileName];
                    if(ct in filteredList[index+1]):
                        contentType = filteredList[index+1];
                        contentTypeValue = contentType[contentType.find(COLON)+1:];                    
                    self.body[name] = (fileName, open(self.postFile, RB), contentTypeValue);
                elif(cd in line):
                    name = line[startName+1:endName];
                    value = EMPTY;
                    i = index+1;
                    nextLine = filteredList[i];
                    while(True):
                        value += nextLine;
                        if(i+1 == length or cd in filteredList[i+1]):
                            self.body[name] = value;
                            break;
                        nextLine += filteredList[i+1];
        else:
            self.body = self.raw_body;

    def setFuzzLocator(self, *attrKeys):
        for attrKey in attrKeys:
            if(HOST in attrKey):
                value = getattr(self, attrKey);
                if(FUZZ in value):
                    self.fuzzLocator[attrKey]=attrKey;
            else:
                for k,v in getattr(self, attrKey).items():
                    if(type(v) == tuple and (FUZZ in v[0] or FUZZ in v[2])):
                        self.fuzzLocator[attrKey]=k;
                    elif(FUZZ in v):
                        self.fuzzLocator[attrKey]=k;

    def parseFile(self):
        inputFile = open(self.inputFile, "r");
        lines = inputFile.readlines();

        self.setFields(lines);
        self.parseInfo();
        self.parseHeaders();
        self.parseBody();
        self.setFuzzLocator(r+HOST, INFO, HEADER+s, BODY);
    
    def printRequest(self):
        format = '{}: {}';

        info = [];
        for k, v in self.info.items():
            info.append(format.format(k, v));

        headers = [];
        for k, v in self.headers.items():
            headers.append(format.format(k, v));
        
        body = [];
        for k, v in self.body.items():
            body.append(format.format(k, v));

        print('\r\n{}\n{}\r\n{}\r\n{}\r\n{}\r\n'.format(
            '-----------Request Start-----------',
            '\r\n'.join(info),
            '\r\n'.join(headers),
            '\r\n'.join(body),
            '----------- Request End ------------'
        ));
    
    def swapFuzz(self, arg1, arg2, attrKey, key):
        attrValue = getattr(self, attrKey);
        if(type(attrValue) == str):
            setattr(self, attrKey, attrValue.replace(arg1, arg2))
            return;

        value = attrValue[key];
        if(type(value) == tuple):
            if(arg1 in value[0]):
                attrValue[key] = (value[0].replace(arg1, arg2), value[1], value[2]);
            elif(arg1 in value[2]):
                attrValue[key] = (value[0], value[1], value[2].replace(arg1, arg2));
        else:
            attrValue[key] = value.replace(arg1, arg2);

    def parseUrl(self, host, secure, endpoint=""):
        standardProtocol = HTTP;
        if(standardProtocol in host):
            return "{}{}".format(host, endpoint);
        else:
            protocol = HTTP_PROTOCOL;
            if(secure):
                protocol = HTTPS_PROTOCOL;
            return "{}{}{}".format(protocol, host, endpoint);

    def getBody(self):
        if(self.postFile):
            return MultipartEncoder(
                fields=self.body,
                boundary=self.boundary
            )
        return self.body;

    def getProxies(self):
        proxies = {};
        if(self.httpProxy):
            proxies[HTTP] = self.parseUrl(self.httpProxy, False);
        if(self.httpsProxy):
            proxies[HTTPS] = self.parseUrl(self.httpProxy, True);
        return proxies;
    
    def handleResponse(self, response):
        responseSoup = BeautifulSoup(response.text, 'html.parser').prettify().rstrip();
        responseStatus = response.status_code;
        responseLength = response.headers[CONTENT_LENGTH];
        
        if(self.filterLength and responseLength in self.filterLength):
            return;
        if(self.filterStatus and not str(responseStatus) in self.filterStatus):
            return;
        if(self.filterIn and not self.filterIn.lower() in responseSoup.lower()):
            return;
        if(self.filterOut and self.filterOut.lower() in responseSoup.lower()):
            return;
        
        responseString = "Response status: {} - Response length: {}".format(responseStatus, responseLength);
        if(self.showFuzz):
            responseString += " - Fuzz text: {}".format(self.FuzzText);
        if(self.showResponse):
            responseString = "\r\nResponse body: {}\r\n".format(responseSoup) + responseString;
        
        print(responseString);

    def sendRequest(self):
        self.url = self.parseUrl(self.rhost, self.secure, self.info[ENDPOINT]);
        
        req = requests.Request(self.info[METHOD],self.url,headers=self.headers,data=self.getBody());
        prepared = req.prepare();
        s = requests.Session();
        s.proxies = self.getProxies();
        response = s.send(prepared);
        self.handleResponse(response);
   
    def fuzzRequest(self):
        fuzzFile = open(self.fuzzFile, "r");
        lines = fuzzFile.readlines();
        
        for line in lines:
            keys = self.fuzzLocator.keys();
            if(len(list(keys)) > 0):
                attrKey = list(keys)[0];
                key = self.fuzzLocator[list(keys)[0]];
                self.swapFuzz(FUZZ, line.rstrip(), attrKey, key);
                self.FuzzText = line.rstrip();
            self.sendRequest();
            self.swapFuzz(line.rstrip(), FUZZ, attrKey, key);
    
    def processRequest(self):
        if(len(self.fuzzLocator) > 0):
            print("Fuzzing Request");
            self.fuzzRequest();
        else:
            print("Sending Request");
            self.sendRequest();