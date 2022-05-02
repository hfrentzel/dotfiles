Import-Module posh-git
$GitPromptSettings.DefaultPromptWriteStatusFirst = $true
$GitPromptSettings.EnableFileStatus = $false

If (Test-Path "~/local.profile.ps1") {
	. "~/local.profile.ps1"
}

If (Test-Path "~/dotfiles/python/python_helpers.ps1") {
	. "~/dotfiles/python/python_helpers.ps1"
}

If (Test-Path "~/dotfiles/git/git_stage.ps1") {
	. "~/dotfiles/git/git_stage.ps1"
}
