# author: WatchDogOblivion
# description: TODO
# Active Directory - Request ticket

param (
    [string]$SPN='HTTP/server.core.com'
)

Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $SPN