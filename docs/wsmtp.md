#### Use case

    This module is for sending smtp messages

    #### Sample module wsmtp
    wsmtp -rh 10.11.1.229 -n "sender" -p "spoiler" -se "sender@thinc.local" -re "reciever@thinc.local" -s "Updates" -b '
        Hey Reciever,

        I added the updates for your workstation in the .hta file in the link below.

        http://10.10.10.10:80/updates.hta

        Cheers!
    '
        send: 'ehlo WatchDogs.org\r\n'
        reply: '250-MAIL\r\n'
        reply: '250-SIZE 20480000\r\n'
        reply: '250-AUTH LOGIN\r\n'
        reply: '250 HELP\r\n'
        reply: retcode (250); Msg: MAIL
        SIZE 20480000
        AUTH LOGIN
        HELP
        send: 'AUTH LOGIN ZXJpYw==\r\n'
        reply: '334 UGFzc3dvcmQ6\r\n'
        reply: retcode (334); Msg: UGFzc3dvcmQ6
        send: 'c3VwM3JzM2NyM3Q=\r\n'
        reply: '235 authenticated.\r\n'
        reply: retcode (235); Msg: authenticated.
        send: 'mail FROM:<sender@thinc.local> size=314\r\n'
        reply: '250 OK\r\n'
        reply: retcode (250); Msg: OK
        send: 'rcpt TO:<reciever@thinc.local>\r\n'
        reply: '250 OK\r\n'
        reply: retcode (250); Msg: OK
        send: 'data\r\n'
        reply: '354 OK, send.\r\n'
        reply: retcode (354); Msg: OK, send.
        data: (354, 'OK, send.')
        send: 'Content-Type: text/html; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nMIME-Version: 1.0\r\nFrom: sender@thinc.local\r\nTo: reciever@thinc.local\r\nSubject: Updates\r\n\r\n\r\nHey Reciever, \r\n\r\nI added the updates for your workstation in the .hta file in the link below.\r\n\r\nhttp://192.168.119.144:80/updates.hta\r\n\r\nCheers!\r\n.\r\n'
        reply: '250 Queued (0.032 seconds)\r\n'
        reply: retcode (250); Msg: Queued (0.032 seconds)
        data: (250, 'Queued (0.032 seconds)')
        Successfully sent email
