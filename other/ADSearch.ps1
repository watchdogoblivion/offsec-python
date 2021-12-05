# author: WatchDogOblivion
# description: TODO
# Active Directory - Search

param (
    [switch]$Services = $false,
    [switch]$Terminals = $false,
    [switch]$All = $false,
    [switch]$Groups = $false,
    [switch]$SPN = $false,
    [string]$SPNString = "*http*"
)

$CurrentDomain = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDCName = ($CurrentDomain.PdcRoleOwner).Name
$SearchString = "LDAP://" + $PDCName + "/"
$DistinguishedName = "DC=$($CurrentDomain.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName
$Searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]$SearchString)
$Entry = New-Object System.DirectoryServices.DirectoryEntry
$Searcher.SearchRoot = $Entry

if ($Services -or $Terminals -or $All) {
    if ($Services) {
        $Searcher.filter = "samAccountType=805306368"
    }
    elseif ($Terminals) {
        $Searcher.filter = "samAccountType=805306369"
    } 
    $Result = $Searcher.FindAll()
    Foreach ($obj in $Result) {
        Foreach ($prop in $obj.Properties) {
            $prop
        }
        Write-Output "------------------------"
    }
}
elseif ($Groups) {
    $Searcher.filter = "(objectClass=Group)"
    $Result = $Searcher.FindAll()
    Foreach ($obj in $Result) {
        $obj.Properties.name
    }
}
elseif ($SPN) {
    $Searcher.filter = "serviceprincipalname=$SPNString"
    $Result = $Searcher.FindAll()
    Foreach ($obj in $Result) {
        Foreach ($prop in $obj.Properties) {
            $prop
        }
    }
}
