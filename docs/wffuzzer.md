#### Use case ####
    While penetration testing, I found certain capabilities split across
    different public python modules. So I wanted a central flow not only for
    all needed fuzzing but also with easy to follow documentation.

#### Sample module wffuzzer - File upload ####
    The module wffuzzer is used for fuzzing requests using a file that contains all the request
    information.

    All you need to do is intercept a request in burp suite, owasp zap, or any other interceptor
    application and copy & paste the contents to a file.
    Then specify the file, and a fuzz file (the file containing the list of words that will replace the
    text in the request) after replacing the value string with the keyword FUZZ.

    Example:
        In the browser, go to a page that allows a file upload.
            http://10.10.10.10/upload.jsp

        Launch burp suite and turn on proxy intercept.
        Go to browser and ensure that the browsers proxy is set for burp suite.

        On the previous browser page, select the file to upload and begin the upload.
        Go back to burp suite and copy and paste the intercepted request to a file; anyname.txt
        Ensure that there is a blank line separating the headers and the body (if there is a body).
        Place or Replace any value string that you want to fuzz with a FUZZ word -
        i.e FUZZ1,FUZZ2,FUZZ3. Note that FUZZ is treated as FUZZ1

            1. POST /upload.jsp HTTP/1.1 ->
               POST FUZZ/upload.jsp HTTP/1.1

            2. Content-Type: text/plain ->
               Content-Type: FUZZ1

            3. Content-Disposition: form-data; name="FileUpload1"; filename="postFile.txt" ->
               Content-Disposition: form-data; name="FileUpload"; filename="FUZZ2.FUZZ1"

        Ensure that the file with the words to substitute in (-ff --fuzz-file), has the same number
        of words per line as the max FUZZ number -
        i.e 10 words per line if the max is FUZZ10 or 5 words per line if the max is FUZZ5.
        Each word in the fuzz file should be separated by a delimiter (the default is a colon but
        you can specify a delimiter).
        For example 3 above the fuzz file could contain:
            test:txt to replace FUZZ2.FUZZ1 as txt.test

        Run the script and use the flags to control filtering by length, status code, and/or text.
        Hide or display responses with a flag.
            wffuzzer -if testrest -rh 10.10.10.10 -pf postFile.txt -ff fuzzFile.txt
                Fuzzing Request
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1115
                Response status: 200 - Response length: 1110

            wffuzzer -if testrest -rh 10.10.10.10 -pf postFile.txt -ff fuzzFile.txt -fl "1115" -sr
                Fuzzing Request
                Response body:
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <body>
        <form action="upload.jsp" enctype="multipart/form-data" id="form1" method="post" name="form1">
            <div>
                <span id="Label1" style="color:Green;">File uploaded successfully.</span>
            </div>
        </form>
    </body>
</html>
```
                Response status: 200 - Response length: 1110

        If any help is required, the standard --help and -h is available for all flags and descriptions.

#### Sample module wffuzzer - Login ####
    Example:
        In the browser, go to a page that allows a file upload.
            http://10.10.10.10/manager/html

        Launch burp suite and turn on proxy intercept.
        Go to browser and ensure that the browsers proxy is set for burp suite.

        On the previous browser page, enter the credentials and submit.
        Go back to burp suite and copy and paste the intercepted request to a file; anyname.txt
        Ensure that there is a blank line separating the headers and the body (if there is a body).
        Place or Replace any value string that you want to fuzz with a FUZZ word -
        i.e FUZZ1,FUZZ2,FUZZ3. Note that FUZZ is treated as FUZZ1

            1. username=admin&password=password ->
                username=FUZZ2&password=FUZZ

            2. {"username":"admin","password":"password"} ->
                {"username":"FUZZ1","password":"FUZZ2"}

            3. Authorization: Basic YWRtaW46cGFzc3dvcmQ= ->
                Authorization: Basic FUZZ1

        Ensure that the file with the words to substitute in (-ff --fuzz-file), has the same number
        of words per line as the max FUZZ number -
        i.e 10 words per line if the max is FUZZ10 or 5 words per line if the max is FUZZ5.
        Each word in the fuzz file should be separated by a delimiter (the default is a colon but
        you can specify a delimiter).
        For example 1 above the fuzz file could contain: pass:john to replace:
        username=FUZZ2&password=FUZZ as username=john&password=pass

        For the basic auth example above, if you have a file of creds that need to be encoded, you can
        use the module wfencoder.
        For example, copying tomcat default creds from a known repository and running below will create
        a file with the encoded creds:
            wfencoder -if fuzzFile.txt -be -of fuzzFileE.txt

        Run the script and use the flags to control filtering by length, status code, and/or text.
        Hide or display responses with a flag.
            wffuzzer -if testrest -rh 10.10.10.10:8080 -ff fuzzFileE.txt
                Fuzzing Request
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 403 - Response length: 3274
                Response status: 403 - Response length: 3274
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 200 - Response length: None
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536

            wffuzzer -if testrest -rh 10.10.10.10:8080 -ff fuzzFileE.txt -fs "200" -sf -sr
                Response body:
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <title>/manager</title>
    </head>
    <body bgcolor="#FFFFFF">
        <form action="/manager/html/upload;jsessionid=D87D42DF74671E9C074D5D6725C1F58C?org.apache.catalina.filters.CSRF_NONCE=9AA45FB11CE3D34D55AC7C3ABFF7F084" enctype="multipart/form-data" method="post">
            <table cellpadding="3" cellspacing="0">
                <tr>
                    <td class="row-right">
                        <small>Select WAR file to upload</small>
                    </td>
                    <td class="row-left">
                        <input name="deployWar" size="40" type="file"/>
                    </td>
                </tr>
                <tr>
                    <td class="row-right"></td>
                    <td class="row-left">
                        <input type="submit" value="Deploy"/>
                    </td>
                </tr>
            </table>
        </form>
    </body>
</html>
```
                Response status: 200 - Response length: None - Fuzz text: dG9tY2F0OnMzY3JldA==

        If any help is required, the standard --help and -h is available for all flags and descriptions.

##### _All modules have a -h and --help for more assistance._ #####