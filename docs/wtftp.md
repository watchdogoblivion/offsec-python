#### Use case

    This module is for transferring files via tftp

#### Sample module wtftp
    wtftp -rh 10.11.1.111 -df '\Users\Administrator\Desktop\proof.txt' -ddf 'proof.txt' > check.txt
        ('\\Users\\Administrator\\Desktop\\proof.txt', 'proof.txt')

    wtftp -rh 10.11.1.111 -if 'traversal.txt'
        ('/Users/Administrator/NTUser.dat\n', '_Users_Administrator_NTUser.dat\n')
        ('/Documents and Settings/Administrator/NTUser.dat\n', '_Documents and Settings_Administrator_NTUser.dat\n')
        ...
        ('/Windows/System32/inetsrv/config/schema/ASPNET_schema.xml\n', '_Windows_System32_inetsrv_config_schema_ASPNET_schema.xml\n')
        ('/Windows/System32/inetsrv/config/applicationHost.config', '_Windows_System32_inetsrv_config_applicationHost.config')

    wtftp -rh 10.11.1.111 -uf 'test.txt' -udf '\Users\Administrator\Desktop\test.txt' -u
        ('test.txt', '\\Users\\Administrator\\Desktop\\test.txt')

    wtftp -rh 10.11.1.111 -if 'traversal.txt' -u > check.txt
        ('NTUser.dat\n', 'NTUser.dat\n')
        ('NTUser.dat\n', 'NTUser.dat\n')
        ...
        ('ASPNET_schema.xml\n', 'ASPNET_schema.xml\n')
        ('applicationHost.config', 'applicationHost.config')