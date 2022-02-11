. 'C:/Users/frentzeh/dotfiles/python/pyvenvs.ps1'

$lines = @()
$newLine = ''
for ($i = 0; $i -lt $envs.count; $i++ )
{
	$newLine += [String]::Format("{0,-20}", "$i) $($envs[$i]['Name'])")
	if (($i + 1) % 3 -eq 0) {
		$lines += "$newLine`n"
		$newLine = ''
	}
}
if ($newLine -ne '') {
	$lines += $newLine
}

function Start-Python {
	Write-Host $lines
	Write-Host ''

	$choice = Read-Host -Prompt "Select a python environment"
	if ($choice -eq 'q') {
		return 0
	}
	$env:PYPROMPT = $envs[$choice]['Name']
	$env:PYTHONSTARTUP = "C:/Users/frentzeh/dotfiles/python/startup.py"

	& $envs[$choice]['Location']
	return $LASTEXITCODE
}

Do {
	Start-Python 
} while ($LASTEXITCODE -eq 5)
