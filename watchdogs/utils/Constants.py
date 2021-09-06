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
