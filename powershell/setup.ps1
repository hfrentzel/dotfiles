$dotfileDir = Split-Path $MyInvocation.MyCommand.Path -Parent

. "$dotfileDir/powershell/symlink.ps1"

If (-Not(Test-Path "~/Powershell")) {
	mkdir "~/Powershell"
}
AddSymLink -src "$dotfileDir/powershell/profile.ps1" -target "~/Powershell/profile.ps1"
AddSymLink -src "$dotfileDir/powershell/profile.ps1" -target "~/WindowsPowershell/profile.ps1"
AddSymLink -src "$dotfileDir/git/gitconfig" -target "~/.gitconfig"

