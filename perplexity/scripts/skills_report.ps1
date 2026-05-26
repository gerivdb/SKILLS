$perp = 'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity'
$files = Get-ChildItem -Path $perp -Filter '*.md' -File
$report = @()
foreach ($f in $files) {
    $lines = Get-Content $f.FullName -TotalCount 6
    $hasPipe = ($lines.Count -ge 5 -and $lines[4].Trim() -eq '|')
    $title = if ($lines.Count -ge 6) { $lines[5].TrimStart('#').Trim() } else { '' }
    $name = if (($lines -join "`n") -match '^name:\s+(\S+)') { $Matches[1] } else { $f.BaseName }
    $report += [PSCustomObject]@{ Name = $name; File = $f.Name; HasPipe = $hasPipe; SizeKB = [math]::Round($f.Length/1024,1); Title = $title }
}
$csvPath = Join-Path $perp 'scripts\skills_report.csv'
$report | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
Write-Output "Skills in /perplexity: $($files.Count)"
Write-Output "All have |: $($report.Where({$_.HasPipe}).Count) / $($files.Count)"
$report | Format-Table -AutoSize
