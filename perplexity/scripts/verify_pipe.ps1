param()
$root = 'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS'
$mdFiles = Get-ChildItem -Path $root -Filter '*.md' -Recurse -File | Where-Object { $_.DirectoryName -notlike '*\.git*' }
$ok = @(); $fail = @()
foreach ($f in $mdFiles) {
    $lines = Get-Content $f.FullName -TotalCount 6 -ErrorAction SilentlyContinue
    if ($lines.Count -ge 5 -and $lines[4].Trim() -eq '|') {
        $ok += $f.FullName
    } else {
        $fail += $f.FullName
    }
}
Write-Output "Checked: $($mdFiles.Count) | OK: $($ok.Count) | FAIL: $($fail.Count)"
if ($fail.Count -gt 0) { $fail | ForEach-Object { Write-Output "FAIL: $_" }; exit 2 }
Write-Output "All .md files have the '|' literal block indicator."
exit 0
