function pinstall {
    param ($args)

    if (-Not($env:VIRTUAL_ENV)) {
        Write-Host "Not in virtual environment"
        return
    }
    pip install $args
}

function newenv {
    param (
        $version,
        $venvName
    )
    If (-Not($version) -or -Not(py "-$version" --version)) {
        Write-Host "Invalid Version"
        return
    }

    . ~/dotfiles/python/pyvenvs.ps1
    $venvs= Import-Csv -Path "~/dotfiles/python/.pyvenvs"

    $fixPwd = $pwd.Path.replace('\', '/')
    If ($venvs | Where-Object -Property Location -Like "$fixPwd/venv/Scripts/python") {
        Write-Host "Virtual Environment already exists in this directory"
        return
    }

    py "-$version" -m venv venv

    If ($lastExitCode -eq 0) {
        Write-Host "Venv created"
        $venvs += [PSCustomObject]@{Name=$venvName;Location="$fixPwd/venv/Scripts/python"}

        $venvs | Export-Csv -Path "~/dotfiles/python/.pyvenvs" 
    } else {
        Write-Host "Failed to create venv"
    }

    $venvs | Format-Table
}
