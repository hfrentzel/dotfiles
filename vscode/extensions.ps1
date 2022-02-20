function Install-VSCode-Extension{
    param (
        [string]$installedExtensions,
        [string]$extensionName,
        [string]$extensionId
    )
    
    if($installedExtensions | Select-String -Pattern $extensionId) {
        Echo "$extensionName already installed"
    } else {
        Echo "Installing $extensionName..."
        code --install-extension $extensionId
        Echo "$extensionName installed"
    }

}

function Install-Extension-List {
    param (
        $extensions
    )
    
    $currExtensions = code --list-extensions
    
    foreach ( $ext in $extensions) {
        Install-VSCode-Extension `
        -installedExtensions $currExtensions `
        -extensionName $ext['Name'] `
        -extensionId $ext['Id']
    }

}
