Import-Module posh-git
$GitPromptSettings.DefaultPromptWriteStatusFirst = $true
$GitPromptSettings.EnableFileStatus = $false

If (Test-Path "~/local.profile.ps1") {
	. "~/local.profile.ps1"
}
