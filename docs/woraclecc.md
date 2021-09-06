#### Use case

    Not a common module. This was created due to the fact that the base
    fuzz creds used for fuzzing Oracle logins, may not match the case
    sensitivity needed for a succesful login.
    For one machine, the default creds were upper cased, but the actual
    cred was both a mix of upper and lower and all lower.
    This module is mainly to quickly convert cred files for these cases.
    You could just as easily perform this with cerain code editors such
    as VSCode's command palette.

#### Sample module wfencoder - Encode file contents

    Cred.txt
        TEST/TEST
        okay/OKAY

    woraclecc -if oracle.txt -c ul
        TEST/test
        OKAY/okay

    woraclecc -if oracle.txt -c ll
        test/test
        okay/okay

##### _All modules have helper flags -h and --help for more assistance._
