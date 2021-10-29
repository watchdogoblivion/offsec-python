# author: WatchDogOblivion
# description: TODO

param (
    [string]$File = 'netUserDomain'
)


$IGNORED_REGEX = '((\bThe\b)|(\bUser\b)|([-]))'
$NAME_REGEX = '([a-zA-Z]+)'
$AllMatches = @()

foreach ($line in Get-Content $File) {
    $ShouldIgnore = $line -cmatch $IGNORED_REGEX
    if ($ShouldIgnore -or !($line.trim())) {
        continue
    }
    $Matched = $line | Select-String -Pattern $NAME_REGEX -AllMatches -CaseSensitive
    $AllMatches += $Matched.Matches.Value    
}

Write-Output $AllMatches