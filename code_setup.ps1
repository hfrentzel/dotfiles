If(-Not(Get-Command code))  {
	Echo "No VS Code command exists"
	Return
}
$PWD = pwd


$settingsJson = "~/AppData/Roaming/Code/User/settings.json"
If (Test-Path $settingsJson) {
	Echo "settings.json already exists"
} else {
	Echo "Creating settings.json symlink..."
	New-Item -ItemType SymbolicLink -Path $settingsJson -Target "$PWD/vscode/settings.json"
}

$keybindingsJson = "~/AppData/Roaming/Code/User/keybindings.json"
If (Test-Path $keybindingsJson) {
	Echo "keybindings.json already exists"
} else {
	Echo "Creating keybindings.json symlink..."
	New-Item -ItemType SymbolicLink -Path $keybindingsJson -Target "$PWD/vscode/keybindings.json"
}



$extensions = code --list-extensions
If($extensions | Select-String -Pattern "vscodevim.vim") {
	Echo "VS Code Vim already installed"
} else {
	Echo "Installing VS Code Vim..."
	code --install-extension vscodevim.vim
	Echo "VS Code Vim installed"
}

If($extensions | Select-String -Pattern "ritwickdey.LiveServer") {
	Echo "Live Server already installend"
} else {
	Echo "Installing Live Server..."
	code --install-extension ritwickdey.LiveServer
	Echo "Live Server installed"
}

If($extensions | Select-String -Pattern "eamodio.gitlens") {
	Echo "GitLens already installed"
} else {
	Echo "Installing GitLens..."
	code --install-extension eamodio.gitlens
	Echo "GitLens installed"
}

If(-Not(Get-Command python)) {
	Echo "No python command found. Skipping installation of python extensions"
	Return
}

If($extensions | Select-String -Pattern "ms-python.python") {
	Echo "VS Code Python already installend"
} else {
	Echo "Installing VS Code Python..."
	code --install-extension ms-python.python
	Echo "VS Code Python installed"
}

If($extensions | Select-String -Pattern "ms-python.vscode-pylance") {
	Echo "Pylance already installed"
} else {
	Echo "Installing Pylance..."
	code --install-extension ms-python.vscode-pylance
	Echo "Pylance installed"
}
