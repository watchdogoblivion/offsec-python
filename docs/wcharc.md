#### Use case

    This module is mainly for manipulating characters in a file for
    payload generation and various testing.
    Like the woraclecc most these operations can be performed with
    a code editor like VSCode.
    This is simply for conveinence and speed.

#### Sample module wcharc - Convert characters

    Py.txt
        python -m pip install  type
        python -m pip install  request
        python -m pip install  beautifulsoup4
        python -m pip install  offsec-python

    wcharc -if i.txt -l -oc "python" -nc "python2.7"
        python2.7 -m pip install  type
        python2.7 -m pip install  request
        python2.7 -m pip install  beautifulsoup4
        python2.7 -m pip install  offsec-python2.7

    Test.txt
        *test
        *test
        *test test best
        *test test *best

    wcharc -if i.txt -l -oc "*" -nc ")" -iw
        1)test
        2)test
        3)test test best
        4)test test 5)best

##### _All modules have helper flags -h and --help for more assistance._
