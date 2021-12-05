#### Use case

    This module is for getting SMB/Samba version when it is being hidden from popular
    enumeration tools such as nmap, smbclient, enum4linux etc.
    Determining the version can be a critical turning point when trying to obtain a
    foothold and it is the only exploitable service on the host.

#### Sample module wsmbv
    sudo wsmbv -i "tun0"
        The SMB/Samba version for host 10.11.1.x is: 1.1.7a

    You can enable debugging:
        wsmbv -i "tun0"
            Version could not be obtained. Try checking 'help' or enabling debugging. i.e 'wsmbv -h or wsmbv -dl 3'
        wsmbv -i "tun0" -dl 1
            An error occured - tcpdump: tun0: You don't have permission to capture on that device (socket: Operation not permitted)
        sudo wsmbv -dl 1
            An error occured - tcpdump: : No such device exists (SIOCGIFHWADDR: No such device)
    protocol negotiation failed: NT_STATUS_CONNECTION_DISCONNECTED
    address sudo issue


##### _All modules have helper flags -h and --help for more assistance._