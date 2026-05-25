# batch-verify-and-report.ps1
# Purpose: verify all skills, produce a CSV report with name, hasPipe, size, firstLineTitle
$root = 'C:\Users\GG\Desktop\skills essai1\B'
$files = Get-ChildItem -Path $root -Filter '*.md' -File
$report = @()
foreach ($f in $files) {
    $lines = Get-Content $f.FullName -TotalCount 6
    $hasPipe = ($lines.Count -ge 5 -and $lines[4].Trim() -eq '|')
    $title = if ($lines.Count -ge 6) { $lines[5].Trim() } else { '' }
    $report += [PSCustomObject]@{File=$f.Name; Path=$f.FullName; HasPipe=$hasPipe; SizeBytes=$f.Length; Title=$title}
}
$report | Export-Csv -Path (Join-Path $root 'scripts\skills_report.csv') -NoTypeInformation -Encoding UTF8
Write-Output "Report written to scripts\skills_report.csv"
