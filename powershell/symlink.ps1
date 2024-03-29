function AddSymLink {
    param (
        [string]$src,
        [string]$target
    )
    
    if (Test-Path $target) {
        Write-Output "$target already exists"
    } else {
        Write-Output "Creating $target symlink..."
        New-Item -ItemType SymbolicLink -Path $target -Target $src
    }
}

function AddHardLink {
    param (
        [string]$src,
        [string]$target
    )
    
    if (Test-Path $target) {
        Write-Output "$target already exists"
    } else {
        Write-Output "Creating $target hard link..."
        New-Item -ItemType HardLink -Path $target -Target $src
    }
}
