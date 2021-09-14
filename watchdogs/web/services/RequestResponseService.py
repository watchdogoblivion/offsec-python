# author: WatchDogOblivion
# description: TODO
# WatchDogs Request Response Service

import io
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from watchdogs.utils import Cast
from watchdogs.base.models import AllArgs, Common
from watchdogs.web.models import Response, WebFile
from watchdogs.web.models.Requests import Request
from watchdogs.web.parsers import RequestArgs
from watchdogs.utils.Constants import (EMPTY, LFRN, HTTP, HTTP_PROTOCOL, HTTPS_PROTOCOL, HTTPS, HTML_PARSER,
                                       CONTENT_LENGTH, UTF8)


class RequestResponseService(Common):

  def __init__(self):  #type: () -> None
    super(RequestResponseService, self).__init__()

  def printRequest(self, request):  # type: (Request) -> None
    format = '{}: {}'

    info = []
    for infoKey, infoValue in request.getRequestInfo().__dict__:
      info.append(format.format(infoKey, infoValue))

    headers = []
    for headersKey, headersValue in request.getRequestHeaders().__dict__:
      headers.append(format.format(headersKey, headersValue))

    body = []
    if (request.getRequestBodyString()):
      body.append(request.getRequestBodyString())
    else:
      for k, v in request.getRequestBodyDict().items():
        body.append(format.format(k, v))

    print('{}{}{}{}{}{}{}{}{}{}{}'.format(LFRN, '-----------Request Start-----------',
                                          LFRN, LFRN.join(info), LFRN, LFRN.join(headers), LFRN,
                                          LFRN.join(body), LFRN, '----------- Request End ------------',
                                          LFRN))

  def getUrl(self, host, secure, endpoint=EMPTY):  #type: (str, bool, str) -> str
    standardProtocol = HTTP
    if (standardProtocol in host):
      return "{}{}".format(host, endpoint)
    else:
      protocol = HTTP_PROTOCOL
      if (secure):
        protocol = HTTPS_PROTOCOL
      return "{}{}{}".format(protocol, host, endpoint)

  def getRequestBody(self, request):  #type: (Request) -> OrderedDict | str
    if (request.getRequestBodyString()):
      return request.getRequestBodyString()
    elif (request.getRequestBodyDict()):
      requestBodyDict = request.getRequestBodyDict()
      for requestBodyKey in requestBodyDict:
        requestBodyValue = requestBodyDict[requestBodyKey]
        if (isinstance(requestBodyValue, WebFile)):
          webFile = Cast._to(WebFile, requestBodyValue)
          postFileIO = io.BytesIO(webFile.getContent())
          requestBodyDict[requestBodyKey] = (webFile.getFileName(), postFileIO, webFile.getContentType())
      return MultipartEncoder(fields=requestBodyDict, boundary=request.getRequestBoundary())

  def getProxies(self, requestArgs):  #type: (RequestArgs) -> dict
    proxies = {}
    if (requestArgs.httpProxy):
      proxies[HTTP] = self.getUrl(requestArgs.httpProxy, False)
    elif (requestArgs.httpsProxy):
      proxies[HTTPS] = self.getUrl(requestArgs.httpsProxy, True)
    return proxies

  def printResponse(self, allArgs, response):  #type: (AllArgs, Response) -> None
    requestArgs = allArgs.getArgs(RequestArgs)
    responseStatus = response.getResponseStatus()
    responseLength = response.getResponseLength()
    responseSoup = response.getResponseSoup()
    responseString = "Response status: {} - Response length: {}".format(responseStatus, responseLength)
    if (requestArgs.showResponse):
      responseString = "Response body: {}{}{}".format(LFRN, responseSoup.encode(UTF8), LFRN) + responseString
    print(responseString)

  def filterResponse(self, allArgs, response):  #type: (AllArgs, Response) -> None
    requestArgs = allArgs.getArgs(RequestArgs)
    responseSoup = response.getResponseSoup()
    responseStatus = response.getResponseStatus()
    responseLength = response.getResponseLength()
    shouldReturn = False
    if (requestArgs.filterLength and responseLength and responseLength in requestArgs.filterLength):
      shouldReturn = True
    if (requestArgs.filterStatus and responseStatus and not str(responseStatus) in requestArgs.filterStatus):
      shouldReturn = True
    if (requestArgs.filterIn and not requestArgs.filterIn.lower() in responseSoup.lower()):
      shouldReturn = True
    if (requestArgs.filterOut and requestArgs.filterOut.lower() in responseSoup.lower()):
      shouldReturn = True
    return shouldReturn

  def getFinalResponse(self, response):  #type: (requests.models.Response) -> Response
    responseSoup = BeautifulSoup(response.text, HTML_PARSER).prettify().rstrip()
    responseStatus = response.status_code
    responseLength = EMPTY
    try:
      responseLength = response.headers.get(CONTENT_LENGTH)
      if(responseLength == None):
        responseLength = 0
    except:
      print("An exception occurred trying to retrieve header {}".format(CONTENT_LENGTH))
      responseLength = 0

    return Response(response, responseSoup, responseStatus, responseLength)

  def handleResponse(self, allArgs, response):
    #type: (AllArgs, requests.models.Response) -> None
    finalResponse = self.getFinalResponse(response)

    if (self.filterResponse(allArgs, finalResponse)):
      return

    self.printResponse(allArgs, finalResponse)

  def sendRequest(self, allArgs, request):  #type: (AllArgs, Request) -> requests.models.Response
    requestArgs = allArgs.getArgs(RequestArgs)
    requestInfo = request.getRequestInfo()
    requestHeaders = request.getRequestHeaders()
    requestBody = self.getRequestBody(request)
    requestUrl = self.getUrl(requestInfo.getUrlHost(), requestArgs.secure, requestInfo.getEndpoint())
    request.setRequestUrl(requestUrl)

    req = requests.Request(requestInfo.getMethod(), requestUrl, headers=requestHeaders, data=requestBody)
    preparedRequest = req.prepare()
    session = requests.Session()
    session.proxies = self.getProxies(requestArgs)
    session.verify = not requestArgs.disableVerification
    response = requests.models.Response()
    try:
      return session.send(preparedRequest, timeout=requestArgs.readTimeout)
    except requests.exceptions.HTTPError:
      response.status_code = 500
      return response
    except requests.exceptions.ConnectionError:
      response.status_code = 502
      return response
    except requests.exceptions.Timeout:
      response.status_code = 504
      return response
    except requests.exceptions.RequestException:
      response.status_code = 500
      return response
    except Exception as e:
      print("An exception while retrieving the response:\n", e)
      return None