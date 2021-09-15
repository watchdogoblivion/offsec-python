#### Use case

    Sometimes while enumerating, there may be files that are encoded in a
    way that obscures the actual content.
    This can be problematic if you obtained credentials.
    This module allows to view any text using the any of the encodings in
    the hard coded encodings list.
    This module actually uses iconv which is a Unix based cli program.

#### Sample module weviewer - Encode file contents

    Obtained.txt
        Admin password:
        �%G00dH@Ck1ng$

    weviewer -if fuzzFile.txt -ef 67
        Admin password:
        £%G00dH@Ck1ng$

##### _All modules have helper flags -h and --help for more assistance._
