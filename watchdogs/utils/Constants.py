# author: WatchDogOblivion
# description: TODO
# WatchDogs Constants

from typing import TypeVar

########## General Constants ##########
FILE_NAME = 'filename'
NAME = 'name'
FUZZ = 'FUZZ'
REGEX_SUB = "\\1"
COLON = ':'
SEMI_COLON = ';'
EQUAL = '='
DOUBLE_QUOTE = '"'
DASH = '-'
LINE_FEED_N = '\n'
LINE_FEED_R = '\r'
LFN = '\n'
LFR = '\r'
LFRN = '\r\n'
LFRN_REGEX = r'[\r\n]'
SPACE = ' '
EMPTY = ''
RB = 'rb'
FS = '/'
BS = '\\'
COMMA = ','
HASH = '#'
T = TypeVar('T')
UTF8 = 'utf-8'
USC = "_"
V1 = "v1"
V2 = "v2"
V3 = "v3"

########## Delimiters ##########
D1 = ' : '
D2 = ' :: '
D3 = ' ::: '
D4 = '; '
D5 = ' - '
D6 = ', '
D7 = ' #'

########## HTTP(S) Request constants ##########
CONTENT_TYPE = 'Content-Type'
CONTENT_DISPOSITION = 'Content-Disposition'
CONTENT_LENGTH = 'Content-Length'
APPLICATION_JSON = 'application/json'
APPLICATION_ATOM_XML = 'application/atom+xml'
APPLICATION_FORM_URLENCODED = 'application/x-www-form-urlencoded'
APPLICATION_OCTET_STREAM = 'application/octet-stream'
APPLICATION_SVG_XML = 'application/svg+xml'
APPLICATION_XHTML_XML = 'application/xhtml+xml'
APPLICATION_XML = 'application/xml'
WILDCARD = '*'
MULTIPART_FORM_DATA = 'multipart/form-data'
TEXT_HTML = 'text/html'
TEXT_PLAIN = 'text/plain'
TEXT_XML = 'text/xml'
BEARER = 'Bearer '
BASIC = 'Basic '
ACCEPT = 'Accept'
ST = '*/*'
HTTP = 'http'
HTTP_PROTOCOL = 'http://'
HTTPS = 'https'
HTTPS_PROTOCOL = 'https://'
BOUNDARY = 'boundary'
METHOD = 'method'
ENDPOINT = 'endpoint'
HOST = 'host'
INFO = 'info'
HEADER = 'header'
BODY = 'body'
HTML_PARSER = 'html.parser'
HEAD = 'HEAD'
OPTIONS = 'OPTIONS'
TRACE = 'TRACE'
CONNECT = 'CONNECT'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
REQUEST_METHODS = [HEAD, OPTIONS, TRACE, CONNECT, GET, POST, PUT, PATCH, DELETE]

########## Lowercase Alphabet ##########
LA = 'a'
LB = 'b'
LC = 'c'
LD = 'd'
LE = 'e'
LF = 'f'
LG = 'g'
LH = 'h'
LI = 'i'
LJ = 'j'
LK = 'k'
LL = 'l'
LM = 'm'
LN = 'n'
LO = 'o'
LP = 'p'
LQ = 'q'
LR = 'r'
LS = 's'
LT = 't'
LU = 'u'
LV = 'v'
LW = 'w'
LX = 'x'
LY = 'y'
LZ = 'z'
LOWER_ALPHA = [
    LA, LB, LC, LD, LE, LF, LG, LH, LI, LJ, LK, LL, LM, LN, LO, LP, LQ, LR, LS, LT, LU, LV, LW, LX, LY, LZ
]

########## Uppercase alphabet ##########
UA = 'A'
UB = 'B'
UC = 'C'
UD = 'D'
UE = 'E'
UF = 'F'
UG = 'G'
UH = 'H'
UI = 'I'
UJ = 'J'
UK = 'K'
UL = 'L'
UM = 'M'
UN = 'N'
UO = 'O'
UP = 'P'
UQ = 'Q'
UR = 'R'
US = 'S'
UT = 'T'
UU = 'U'
UV = 'V'
UW = 'W'
UX = 'X'
UY = 'Y'
UZ = 'Z'
UPPER_ALPHA = [
    UA, UB, UC, UD, UE, UF, UG, UH, UI, UJ, UK, UL, UM, UN, UO, UP, UQ, UR, US, UT, UU, UV, UW, UX, UY, UZ
]

########## Numbers ##########
NUMS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

########## Number Strings ##########
SZERO = '0'
SONE = '1'
STWO = '2'
STHREE = '3'
SFOUR = '4'
SFIVE = '5'
SSIX = '6'
SSEVEN = '7'
SEIGHT = '8'
SNINE = '9'
NUM_STRINGS = [SZERO, SONE, STWO, STHREE, SFOUR, SFIVE, SSIX, SSEVEN, SEIGHT, SNINE]

########## Numbers words ##########
WZERO = 'ZERO'
WONE = 'ONE'
WTWO = 'TWO'
WTHREE = 'THREE'
WFOUR = 'FOUR'
WFIVE = 'FIVE'
WSIX = 'SIX'
WSEVEN = 'SEVEN'
WEIGHT = 'EIGHT'
WNINE = 'NINE'
WNUMS = [WZERO, WONE, WTWO, WTHREE, WFOUR, WFIVE, WSIX, WSEVEN, WEIGHT, WNINE]

########## Buffer Overflow ##########
ORIGINAL_BAD_CHARS = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
                      "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
                      "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
                      "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
                      "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
                      "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
                      "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
                      "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
                      "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
                      "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
                      "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
                      "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
                      "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
                      "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
                      "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
                      "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")