# author: WatchDogOblivion
# description: TODO

param (
    [string]$User = 'user',
    [string]$Pass = 'password'
)

$CurrentDomain = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDCName = ($CurrentDomain.PdcRoleOwner).Name
$SearchString = "LDAP://" + $PDCName + "/"
$DistinguishedName = "DC=$($CurrentDomain.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName
New-Object System.DirectoryServices.DirectoryEntry($SearchString, $User, $Pass)
