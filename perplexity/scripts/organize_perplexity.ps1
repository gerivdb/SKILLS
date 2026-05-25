param()
$root = 'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS'
$perp = Join-Path $root 'perplexity'
$repoDocs = @('README.md','TAXONOMY.md','CONTRIBUTING.md','CITIZENS.md','CHANGELOG.md')

Write-Output "Organizing Perplexity skills: root=$root, dest=$perp"

$mdFiles = Get-ChildItem -Path $root -Filter '*.md' -File
foreach ($f in $mdFiles) {
    if ($repoDocs -contains $f.Name) { Write-Output "Skipping repo doc: $($f.Name)"; continue }
    if ($f.DirectoryName -eq $perp) { Write-Output "Already in perplexity: $($f.Name)"; continue }
    # read first 6 lines
    $lines = Get-Content -Path $f.FullName -TotalCount 6 -ErrorAction SilentlyContinue
    if ($lines -and $lines.Count -ge 2 -and $lines[0].Trim() -eq '---' -and ($lines -join "`n") -match "^name:\s+\S") {
        $dest = Join-Path $perp $f.Name
        Move-Item -Path $f.FullName -Destination $dest -Force
        Write-Output "Moved to perplexity: $($f.Name)"
    } else {
        Write-Output "Kept at root (not a Perplexity skill): $($f.Name)"
    }
}

Write-Output "Organize complete"
