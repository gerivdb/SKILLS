$root = 'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS'
$perp = Join-Path $root 'perplexity'
$repoDocs = @('README.md','TAXONOMY.md','CONTRIBUTING.md','CITIZENS.md','CHANGELOG.md')
$perpNames = (Get-ChildItem $perp -Filter '*.md' -File).Name
Get-ChildItem $root -Filter '*.md' -File | Where-Object { $repoDocs -notcontains $_.Name -and $perpNames -contains $_.Name } | ForEach-Object { Remove-Item $_.FullName -Force; Write-Output "Removed: $($_.Name)" }
Write-Output 'Cleanup done'
