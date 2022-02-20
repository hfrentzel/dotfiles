If(-Not(Get-Command code))  {
    Echo "No VS Code command exists"
    Return
}
$PWD = pwd

. "$PWD/powershell/symlink.ps1"
AddSymLink -src "$PWD/vscode/settings.json" -target "~/AppData/Roaming/Code/User/settings.json"
AddSymLink -src "$PWD/vscode/keybindings.json" -target "~/AppData/Roaming/Code/User/keybindings.json"


. "$PWD/vscode/extensions.ps1"
$baseExtensions = @(
    @{Name="VS Code Vim";Id="vscodevim.vim"}
    @{Name="Live Server";Id="ritwickdey.LiveServer"}
    @{Name="GiLens";Id="eamodio.gitlens"}
    @{Name="VS Code Powershell";Id="ms-vscode.PowerShell"}
)

Install-Extension-List -extensions $baseExtensions

If(-Not(Get-Command python)) {
    Echo "No python command found. Skipping installation of python extensions"
    Return
}

$pythonExtensions = @(
    @{Name="VS Code Python";Id="ms-python.python"}
    @{Name="Pylance";Id="ms-python.vscode-pylance"}
)

Install-Extension-List -extensions $pythonExtensions
