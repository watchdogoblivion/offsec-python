### **This project was created to aggregate the custom scripts I wrote during my trials through OSCP, HTB, and VHL.**

### _Either Installation approach below will work._

#### PYTHONPATH Install and Uninstall

    Add the project location your python path for the appropriate shell.
    ~./bashrc, ~./zshrc etc, session export, etc.

    Example:
        To InstallA
            code ~./bashrc
            -- Navigate to bottom and add below --
            export PYTHONPATH=${PYTHONPATH}:/path/to/project/watchdogs-offsec

            Then, ensure you install the needed dependencies:
                python -m pip install requests
                python -m pip install beautifulsoup4
                python -m pip install typing
                python -m pip install pathos

        To remove:
            Delete directory watchdogs-offsec and remove added export line from files above.

            Then run:
                    python -m pip uninstall requests
                    python -m pip uninstall beautifulsoup4
                    python -m pip uninstall typing
                    python -m pip uninstall pathos

#### PIP Install and Uninstall

    Navigate to project directory and excute the pip install command.

    Example:
        To Install
            python -m pip install -e watchdogs-offsec

        To Remove:
            python -m pip uninstall watchdogs-offsec

            Then run:
                    python -m pip uninstall requests
                    python -m pip uninstall beautifulsoup4
                    python -m pip uninstall typing
                    python -m pip uninstall pathos

#### Execute from anywhere

    Add bin to PATH variable
    For sudo modules, add bin to secure paths in sudoers file

    Example:
        code ~./bashrc
        -- Navigate to bottom and add below --
        export PATH=$PATH:/path/to/project/watchdogs-offsec/bin

        /etc/sudoers
        Defaults	secure_path="/usr/local/sbin:/path/to/project/watchdogs-offsec/bin"

#### Additional Info

    For installation options above, if running multiple python versions, simply specify the version in
    the shell command.
        python -m pip pipCommand package
        python2.7 -m pip pipCommand package
        python3 -m pip pipCommand package

## _The links below are to the docs for the modules_

These modules were built with Kali and python.

"wrfuzzer", the request fuzzer module, is the most used.

Mail modules:
> [TFTP module samples](docs/wtftp.md)\
> [SMTP module samples](docs/wsmtp.md)

Web modules:
> [Request Fuzzer module samples](docs/wrfuzzer.md)\
SQL web modules:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Blind SQL module samples](docs/wbsqli.md)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Error SQL module samples](docs/wesqli.md)\
The sql web modules above are by no means replacements for sqlmap. They do not cover all possible scenarios, only the ones I encountered.
They can still be used as templates for other manual scenarios since their injections follow a common structure. Using
-hp flag will allow for proxy interception and inspection, and the [web utils](watchdogs/web/webutils) package holds the queries used.

General modules:
> [Get SMB/Samba version samples](docs/wsmbv.md)\
[Set Java module samples](docs/wsetjava.md)\
[Reverse TCP Basic module samples](docs/wrtcpb.md)\
[Oracle Character Converter module samples](docs/woraclecc.md)\
[File encoder module samples](docs/wfencoder.md)\
[Encoding viewer module samples](docs/weviewer.md)\
[Character Converter module samples](docs/wcharc.md)

There are also the [other](other/) scripts that may hold interest. The libraries some of them leverage are quite useful.
