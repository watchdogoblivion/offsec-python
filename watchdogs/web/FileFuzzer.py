# author: WatchDogOblivion
# description: TODO
# WatchDogs File Fuzzer

import re;
import argparse;
import requests;
from bs4 import BeautifulSoup;
from collections import OrderedDict;
from requests_toolbelt.multipart.encoder import MultipartEncoder;

from watchdogs.io import File;
from watchdogs.web.Locators import *;
from watchdogs.utils import Cast;
from watchdogs.utils.Constants import *;

class FileFuzzer(File, Common):

    VERSION = "1.0";
    BOUNDLESS_REGEX = r'(?:FUZZ)($|[^0-9])';
    BOUND_REGEX = r'FUZZ([0-9]+)';
    DUPLICATE_MESSAGE = "INFO: Duplicate FUZZ keys detected. Note: FUZZ is treated as FUZZ1";

    def __init__(self):
        super(FileFuzzer, self).__init__();
        self.requestFields = [] #type: list[str]
        self.secure = False #type: bool
        self.rhost = EMPTY #type: str
        self.raw_info = EMPTY #type: str
        self.raw_headers = EMPTY #type: str
        self.raw_body = EMPTY #type: str
        self.info = OrderedDict() #type: OrderedDict
        self.url = EMPTY #type: str
        self.headers = OrderedDict() #type: OrderedDict
        self.boundary = EMPTY #type: str
        self.body = OrderedDict() #type: OrderedDict
        self.postFile = EMPTY #type: str
        self.fuzzLocators = FuzzLocators() #type: FuzzLocators
        self.fuzzFile = EMPTY #type: str
        self.fuzzDelimiter = COLON #type: str
        self.httpProxy = EMPTY #type: str
        self.httpsProxy = EMPTY #type: str
        self.disableVerification = False #type: bool
        self.readTimeout = None #type: int
        self.filterLength = EMPTY #type: str
        self.filterStatus = EMPTY #type: str
        self.filterIn = EMPTY #type: str
        self.filterOut = EMPTY #type: str
        self.showResponse = False #type: bool
        self.showFuzz = False #type: bool
        self.FuzzText = EMPTY #type: str
        
    def __setattr__(self, name, value):#type: (FileFuzzer, str, T) -> T
        super(FileFuzzer, self).__setattr__(name, value);

        requestFields = self.requestFields if hasattr(self, "requestFields") else None;
        if (not requestFields == None) and (not name in requestFields):
            if name.find("raw_") > -1 or name.find("_raw") > -1:
                requestFields.append(name);

        return value;

    def parseArgs(self):#type: (FileFuzzer) -> None
        rhHelp = "Explictly specify the remote host.";
        ifHelp = ("Specify the input file to read from.\nWhen executing POST, always ensure there is a new line"
        "feed separating the body from the headers.\nIf fuzzing, the file must include exactly 1 'FUZZ' keyword.");
        sHelp = "Specifies https.";
        ofHelp = "Specify the output file to write to.";
        pfHelp = ("Specify a file to send in a POST request. This flag is for file uploads only and should not be"
        "used for other POST requests");
        ffHelp = "Specify a file to fuzz with. If this is not specified, no fuzzing will occur";
        hpHelp = "Specify a proxy.";
        spHelp = "Specify an ssl proxy";
        dvHelp = "For https proxies, this flag will disable cert verification.";
        rtHelp = "Specify the requests read time out.";
        flHelp = "Filter OUT fuzzed responses by coma separated lengths";
        fsHelp = "Filter IN fuzzed responses by coma separated status codes";
        fiHelp = "Filters in and keeps the responses with the specified text";
        foHelp = "Filters out and removes the responses with the specified text";
        srHelp = "Shows the response body";
        sfHelp = "Shows the fuzz text used in the request";
        vHelp = "Show version";
        hHelp = "Show this help message";
        VERSION = "File Fuzzer version: {}".format(FileFuzzer.VERSION);

        self.parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter);
        parser = self.parser;
        required = parser.add_argument_group("Required arguments");
        required.add_argument("-rh", "--rhost", required=True, help=rhHelp, type=str, metavar="127.0.0.1");
        required.add_argument("-if", "--input-file", required=True, help=ifHelp, type=str, metavar="request.txt");
        parser.add_argument("-s", "--secure", action="store_true", help=sHelp);
        parser.add_argument("-of", "--output-file", help=ofHelp, type=str, metavar=EMPTY);
        parser.add_argument("-pf", "--post-file", help=pfHelp, type=str, metavar=EMPTY);
        parser.add_argument("-ff", "--fuzz-file", help=ffHelp, type=str, metavar=EMPTY);
        parser.add_argument("-hp", "--http-proxy", help=hpHelp, type=str, metavar=EMPTY);
        parser.add_argument("-sp", "--https-proxy", help=spHelp, type=str, metavar=EMPTY);
        parser.add_argument("-dv", "--disable-verification", action="store_true", help=dvHelp, default=False);
        parser.add_argument("-rt", "--read-timeout", help=rtHelp, type=int, metavar=EMPTY, default=None);
        parser.add_argument("-fl", "--filter-length", help=flHelp, type=str, metavar=EMPTY, default=EMPTY);
        parser.add_argument("-fs", "--filter-status", help=fsHelp, type=str, metavar=EMPTY);
        parser.add_argument("-fi", "--filter-in", help=fiHelp, type=str, metavar=EMPTY);
        parser.add_argument("-fo", "--filter-out", help=foHelp, type=str, metavar=EMPTY);
        parser.add_argument("-sr", "--show-response", action="store_true", help=srHelp);
        parser.add_argument("-sf", "--show-fuzz", action="store_true", help=sfHelp);
        parser.add_argument("-v", "--version", action="version", help=vHelp, version=VERSION);
        parser.add_argument("-h", "--help", action="help", help=hHelp);
        self.args = parser.parse_args();
    
    def setBoundary(self,line,boundaryString):#type: (str,str) -> None
        eIndex = line.find(EQUAL, line.find(boundaryString));
        scIndex = line.find(SEMI_COLON, eIndex);
        nlIndex = line.find(LFN);
        if(scIndex > -1):
            self.boundary = line[eIndex+1:scIndex];
        elif(nlIndex > -1):
            self.boundary = line[eIndex+1:nlIndex];
        else:
            self.boundary = line[eIndex+1:];

    def setFields(self, lines):#type: (FileFuzzer,str) -> None
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
            elif((line == EMPTY and not isBody) or (index+1 == length and not isBody)):
                isBody = True;
                setattr(self, fields[1], value);
                value = "";
            elif(index+1 == length):
                value += line+LFN;
                setattr(self, fields[2], value);
                index+=1;
                break;

            value += line+LFN;
            index+=1;

    def parseInfo(self):#type: (FileFuzzer) -> None
        info = self.raw_info.rstrip().split(SPACE);
        self.info[METHOD] = info[0];
        self.info[ENDPOINT] = info[1];
    
    def parseHeaders(self):#type: (FileFuzzer) -> None
        headerArray = self.raw_headers.rstrip().split(LFN);
        for header in headerArray:
            index = header.find(COLON);
            self.headers[header[0:index]] = header[index+1:].strip();
        
    def parseBody(self):#type: (FileFuzzer) -> None
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
            if(not self.body):
                print("Could not parse thw post file specified. Please ensure that the -pf flag is being used with"
                " a proper file upload request. If the attempted request is not a file upload, then remove the -pf"
                " flag to send JSON or standard form data.");
                exit();
        else:
            self.body = self.raw_body;

    def getFuzzIndicies(self, *fuzzValues):# type: (FileFuzzer, str) -> list[int]
        boundRegex = FileFuzzer.BOUND_REGEX;
        fuzzIndicies = [];
        for fuzzValue in fuzzValues:
            if(fuzzValue):
                fuzzIndicies += re.findall(boundRegex,fuzzValue);
        return fuzzIndicies;

    def getBoundlessFuzz(self, *fuzzValues):# type: (FileFuzzer, str) -> str
        boundlessRegex = FileFuzzer.BOUNDLESS_REGEX;
        for fuzzValue in fuzzValues:
            boundlessArray = re.findall(boundlessRegex,fuzzValue);
            if(boundlessArray):
                if(len(boundlessArray) > 1):
                    print(FileFuzzer.DUPLICATE_MESSAGE);
                return fuzzValue;

    def handleBoundless(self, boundlessFuzz, fuzzIndicies, attrValue, attrKey, aVI=None):
        #type: (FileFuzzer, str, list[int], str | OrderedDict, str, AVI) -> None
        if(boundlessFuzz):
            boundlessRegex = FileFuzzer.BOUNDLESS_REGEX;
            newValue = re.sub(boundlessRegex, FUZZ+SONE+REGEX_SUB, boundlessFuzz);
            fuzzIndicies.append(SONE);
            if(type(attrValue) == str):
                setattr(self, attrKey, newValue);
            elif(aVI):
                aVIKey = aVI.getAVIKey();
                aVIValue = aVI.getAVIValue();
                fileName = aVI.getFileName();
                contentType = aVI.getContentType();
                if(type(aVIValue) == tuple):
                    newTuple = None;
                    if(fileName == boundlessFuzz):
                        newTuple = (newValue, aVIValue[1], contentType);
                    if(contentType == boundlessFuzz):
                        newTuple = (fileName, aVIValue[1], newValue);
                    if(newTuple):
                        attrValue[aVIKey] = newTuple;
                elif(type(aVIValue) == str):
                    attrValue[aVIKey] = newValue;

    def manageLocatorValues(self, fuzzIndicies, existingIndicies, locatorKey, locator):
        #type: (FileFuzzer, list[int], list[int], str, FuzzLocator) -> None
        if(len(fuzzIndicies) > 0):
            for index in fuzzIndicies:
                if(index in existingIndicies):
                    print(FileFuzzer.DUPLICATE_MESSAGE);
                container = LocatorContainer();
                container.setLocatorKey(locatorKey);
                container.setLocatorIndex(index);
                locator.getLocatorContainers().append(container);
                existingIndicies.append(container.getLocatorIndex());

    def updateFuzzLocator(self, *attrKeys):# type: (FileFuzzer, str) -> None
        locators = self.fuzzLocators;
        existingIndicies = [];
        for attrKey in attrKeys:
            attrValue = getattr(self, attrKey);
            locator = Cast._from(getattr(locators, attrKey), FuzzLocator);
            if(type(attrValue) == str):
                    fuzzIndicies = self.getFuzzIndicies(attrValue);
                    boundlessFuzz = self.getBoundlessFuzz(attrValue);
                    self.handleBoundless(boundlessFuzz, fuzzIndicies, attrValue, attrKey);
                    self.manageLocatorValues(fuzzIndicies, existingIndicies, attrKey, locator);
            elif(type(attrValue) == OrderedDict):
                aVI = OrderedDict(attrValue).items();
                for aVIKey,aVIValue in aVI:
                    fuzzValue = fileName = contentType = EMPTY;
                    if(type(aVIValue) == tuple):
                        fileName = aVIValue[0];
                        contentType = aVIValue[2];
                    elif(type(aVIValue) == str):
                        fuzzValue = aVIValue;
                    fuzzIndicies = self.getFuzzIndicies(fuzzValue, fileName, contentType);
                    boundlessFuzz = self.getBoundlessFuzz(fuzzValue, fileName, contentType);
                    aVI = AVI(aVIKey, aVIValue, fileName, contentType);
                    self.handleBoundless(boundlessFuzz, fuzzIndicies, attrValue, None, aVI);
                    self.manageLocatorValues(fuzzIndicies, existingIndicies, aVIKey, locator);

    def parseFile(self):# type: (FileFuzzer) -> None
        inputFile = open(self.inputFile, LR);
        lines = inputFile.readlines();

        self.setFields(lines);
        self.parseInfo();
        self.parseHeaders();
        self.parseBody();
        self.updateFuzzLocator(LR+HOST, INFO, HEADER+LS, BODY);
    
    def printRequest(self):# type: (FileFuzzer) -> None
        format = '{}: {}';

        info = [];
        for k, v in self.info.items():
            info.append(format.format(k, v));

        headers = [];
        for k, v in self.headers.items():
            headers.append(format.format(k, v));
        
        body = [];
        if(type(self.body) == str):
            body.append(self.body);
        else:
            for k, v in self.body.items():
                body.append(format.format(k, v));

        print('{}{}{}{}{}{}{}{}{}{}{}'.format(
            LFRN,
            '-----------Request Start-----------',
            LFRN,
            LFRN.join(info),
            LFRN,
            LFRN.join(headers),
            LFRN,
            LFRN.join(body),
            LFRN,
            '----------- Request End ------------',
            LFRN
        ));

    def getLocatorsTotalLength(self):# type: (FileFuzzer) -> int
        locators = self.fuzzLocators;
        rhostLength = len(locators.getRhost().getLocatorContainers());
        infoLength = len(locators.getInfo().getLocatorContainers());
        headersLength = len(locators.getHeaders().getLocatorContainers());
        bodyLength = len(locators.getBody().getLocatorContainers());
        return rhostLength + infoLength + headersLength + bodyLength;

    def getFuzzHelpers(self):# type: (FileFuzzer) -> list
        locators = vars(self.fuzzLocators);
        fuzzHelpers = [];
        for locatorField in locators:
            locator = Cast._from(locators[locatorField], FuzzLocator);
            containers = locator.getLocatorContainers();
            for container in containers:
                fuzzHelper = FuzzHelper();
                fuzzHelper.setLocatorIndex(int(container.getLocatorIndex()));
                fuzzHelper.setAttrKey(locatorField);
                fuzzHelper.setLocatorKey(container.getLocatorKey());
                attrValue = getattr(self, locatorField);
                if(type(attrValue) == str):
                    fuzzHelper.setOriginalFuzz(attrValue);
                else:
                    fuzzHelper.setOriginalFuzz(attrValue[fuzzHelper.getLocatorKey()])
                fuzzHelpers.append(fuzzHelper);
        return fuzzHelpers;

    def parseUrl(self, host, secure, endpoint=EMPTY):#type: (FileFuzzer, str, bool, str) -> str
        standardProtocol = HTTP;
        if(standardProtocol in host):
            return "{}{}".format(host, endpoint);
        else:
            protocol = HTTP_PROTOCOL;
            if(secure):
                protocol = HTTPS_PROTOCOL;
            return "{}{}{}".format(protocol, host, endpoint);

    def getBody(self):#type: (FileFuzzer) -> OrderedDict | str
        if(self.postFile):
            return MultipartEncoder(
                fields=self.body,
                boundary=self.boundary
            )
        return self.body;

    def getProxies(self):#type: (FileFuzzer) -> dict
        proxies = {};
        if(self.httpProxy):
            proxies[HTTP] = self.parseUrl(self.httpProxy, False);
        elif(self.httpsProxy):
            proxies[HTTPS] = self.parseUrl(self.httpsProxy, True);
        return proxies;
    
    def handleResponse(self, response):#type: (FileFuzzer, requests.models.Response) -> None
        responseSoup = BeautifulSoup(response.text, HTML_PARSER).prettify().rstrip();
        responseStatus = response.status_code;
        responseLength = EMPTY;
        try:
            responseLength = response.headers.get(CONTENT_LENGTH);
        except:
            print("An exception occurred trying to retrieve header {}".format(CONTENT_LENGTH));
        
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
            responseString = "Response body: {}{}".format(LFRN,responseSoup.encode(UTF8),LFRN) + responseString;
        print(responseString);

    def sendRequest(self):#type: (FileFuzzer) -> None
        self.url = self.parseUrl(self.rhost, self.secure, self.info[ENDPOINT]);

        req = requests.Request(self.info[METHOD],self.url,headers=self.headers,data=self.getBody());
        prepared = req.prepare();
        session = requests.Session();
        session.proxies = self.getProxies();
        session.verify = not self.disableVerification;
        response = session.send(prepared, timeout=self.readTimeout);
        self.handleResponse(response);

    def swapFuzz(self, substrings, fuzzHelpers):#type: (FileFuzzer, list[str], list[FuzzHelper]) -> None
        for fuzzHelper in fuzzHelpers:
            index = fuzzHelper.getLocatorIndex();
            arg1 = FUZZ + str(index);
            arg2 = substrings[index-1].rstrip();
            attrKey = fuzzHelper.getAttrKey();
            attrValue = getattr(self, attrKey);
            if(type(attrValue) == str):
                setattr(self, attrKey, str(attrValue).replace(arg1, arg2))
                continue;
            locatorKey = fuzzHelper.getLocatorKey();
            originalValue = attrValue[locatorKey];
            if(type(originalValue) == tuple):
                fileName = str(originalValue[0]);
                content = originalValue[1];
                contentType = str(originalValue[2]);
                if(arg1 in fileName):
                    newValue = fileName.replace(arg1, arg2);
                    attrValue[locatorKey] = (newValue, content, contentType);
                elif(arg1 in contentType):
                    newValue = contentType.replace(arg1, arg2);
                    attrValue[locatorKey] = (fileName, content, newValue);
            else:
                attrValue[locatorKey] = str(originalValue).replace(arg1, arg2);

    def swapBack(self, fuzzHelpers):#type: (FileFuzzer, list[FuzzHelper]) -> None
        for fuzzHelper in fuzzHelpers:
            originalValue = fuzzHelper.getOriginalFuzz();
            attrKey = fuzzHelper.getAttrKey();
            attrValue = getattr(self, attrKey);
            if(type(attrValue) == str):
                setattr(self, attrKey, originalValue)
                continue;
            locatorKey = fuzzHelper.getLocatorKey();
            attrValue[locatorKey] = originalValue;

    def fuzzRequest(self):#type: (FileFuzzer) -> None
        fuzzFile = open(self.fuzzFile, "r");
        lines = fuzzFile.readlines();
        fuzzHelpers = self.getFuzzHelpers();
        de = self.fuzzDelimiter;

        if(len(fuzzHelpers) <= 0):
            print("No FUZZ keyword located. Sending normal request.");
            self.sendRequest();
        else:
            for line in lines:
                self.FuzzText = line.rstrip();
                substrings = line.split(de);
                self.swapFuzz(substrings, fuzzHelpers);
                self.sendRequest();
                self.swapBack(fuzzHelpers);
    
    def processRequest(self):#type: (FileFuzzer) -> None
        if(self.getLocatorsTotalLength() > 0):
            print("Fuzzing Request");
            self.fuzzRequest();
        else:
            print("Sending Request");
            self.sendRequest();