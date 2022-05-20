$filename = "~/variables"

If (-Not(Test-Path $filename)) {
    return
}

$local_useful_keys = @{}
foreach ($line in Get-Content $filename) {
    $array=$line -split " "
    # echo $array[0]
    # echo $array[1]
    $local_useful_keys[$array[0]] = $array[1]
}

function getVar {
    param (
        [string]$key
    )    
    Write-Output $local_useful_keys[$key]
}
