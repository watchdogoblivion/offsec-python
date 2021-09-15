#### Use case

    While penetration testing, I found certain capabilities split across
    different public python modules. So I wanted a central flow not only for
    all needed fuzzing but also with easy to follow documentation.

#### Sample module wrfuzzer - File upload

    The module wrfuzzer is used for fuzzing requests using a file that contains all the request
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

        Ensure that the file with the words to substitute in (-sf --substitutes-file), has the same number
        of words per line as the max FUZZ number -
        i.e 10 words per line if the max is FUZZ10 or 5 words per line if the max is FUZZ5.
        Each word in the fuzz file should be separated by a delimiter (the default is a colon but
        you can specify a delimiter).
        For example 3 above the fuzz file could contain:
            test:txt to replace FUZZ2.FUZZ1 as txt.test

        Run the script and use the flags to control filtering by length, status code, and/or text.
        Hide or display responses with a flag.
            wrfuzzer -if test_upload.txt -rh 10.10.10.93 -pf web.config -sf substitutesUpload.txt
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

            wrfuzzer -if test_upload.txt -rh 10.10.10.93 -pf web.config -sf substitutesUpload.txt -fl "1115" -ss -sr
                Fuzzing Request
                Response body:

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <body>
    <form
      action="upload.jsp"
      enctype="multipart/form-data"
      id="form1"
      method="post"
      name="form1"
    >
      <div>
        <span id="Label1" style="color:Green;"
          >File uploaded successfully.</span
        >
      </div>
    </form>
  </body>
</html>
```

                Response status: 200 - Response length: 1110 - Fuzz text: ['web', 'config']

        If any help is required, the standard --help and -h is available for all flags and descriptions.

#### Sample module wrfuzzer - Login

    Example:
        In the browser, go to a page that takes the credentials with which you will submit
        for logging in.
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

        Ensure that the file with the words to substitute in (-sf --substitutes-file), has the same number
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
            wfencoder -if substitutesCreds.txt -be -of substitutesECreds.txt

        Run the script and use the flags to control filtering by length, status code, and/or text.
        Hide or display responses with a flag.
            wrfuzzer -rh 10.10.10.95:8080 -if test_ECreds.txt -sf substitutesECreds.txt
                Fuzzing Request
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 403 - Response length: 3274
                Response status: 403 - Response length: 3274
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 200 - Response length: 0
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536
                Response status: 401 - Response length: 2536

            wrfuzzer -rh 10.10.10.95:8080 -if test_ECreds.txt -sf substitutesECreds.txt -fs "200" -ss -sr
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

                Response status: 200 - Response length: 0 - Fuzz text: dG9tY2F0OnMzY3JldA==

        If any help is required, the standard --help and -h is available for all flags and descriptions.

#### Sample module wrfuzzer - subdomain

    Example:
        In the browser, go to a page that you intended to fuzz.
            http://schooled.htb

        Launch burp suite and turn on proxy intercept.
        Go to browser and ensure that the browsers proxy is set for burp suite.

        (Be sure to watch out for headers: If-None-Match and If-Modified-Since if you are planing to
        filter by response length and not status)

        wrfuzzer -rh FUZZ.schooled.htb -if test_domains.txt -sf substitutesDomains.txt
            Fuzzing Request
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0
            Response status: 502 - Response length: 0

        Add filter on 200 status or filter out Response length 0 and show substitutes
        wrfuzzer -rh FUZZ.schooled.htb -if test_domains.txt -sf substitutesDomains.txt -fs "200" -fl 0 -ss
            Fuzzing Request
            Response status: 200 - Response length: 20750 - Fuzz text: ['moodle']

        You can also show the response with -sr
        wrfuzzer -rh FUZZ.schooled.htb -if test_domains.txt -sf substitutesDomains.txt -fs "200" -fl 0 -ss -sr
            Fuzzing Request
            Response body:

```html
<!DOCTYPE html>
<html lang="en">
  <title>Schooled - A new kind of educational institute</title>
</html>
<body class="host_version">
  <!-- Start header -->
  <header class="top-navbar">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="index.html">
          <img alt="" src="" />
        </a>
        <button
          aria-controls="navbars-rs-food"
          aria-expanded="false"
          aria-label="Toggle navigation"
          class="navbar-toggler"
          data-target="#navbars-host"
          data-toggle="collapse"
          type="button"
        >
          <span class="icon-bar"> </span>
          <span class="icon-bar"> </span>
          <span class="icon-bar"> </span>
        </button>
        <div class="collapse navbar-collapse" id="navbars-host">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
              <a class="nav-link" href="index.html"> Home </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="about.html"> About Us </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="teachers.html"> Teachers </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="contact.html"> Contact </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
  <!-- End header -->
</body>
```

            Response status: 200 - Response length: 20750 - Fuzz text: ['moodle']

#### Sample module wrfuzzer - ports

    Example:
        In the browser, go to a page that you intend to Fuzz, even if it returns
        no content.
            http://10.10.10.55

        Launch burp suite and turn on proxy intercept.
        Go to browser and ensure that the browsers proxy is set for burp suite.

        wrfuzzer -if test_ports.txt -rh 10.10.10.55:60000 -sf substitutesPorts.txt -rt 3 -fs "200" -fl "2" -ss
            Fuzzing Request
            Response status: 200 - Response length: 62 - Fuzz text: ['22']
            Response status: 200 - Response length: 137 - Fuzz text: ['90']
            Response status: 200 - Response length: 154 - Fuzz text: ['110']
            Response status: 200 - Response length: 22 - Fuzz text: ['200']
            Response status: 200 - Response length: 648 - Fuzz text: ['320']
            Response status: 200 - Response length: 838 - Fuzz text: ['888']
            Response status: 200 - Response length: 135 - Fuzz text: ['3306']
            Response status: 200 - Response length: 421 - Fuzz text: ['8080']
            Response status: 200 - Response length: 583 - Fuzz text: ['60000']

##### _All modules have helper flags -h and --help for more assistance._
