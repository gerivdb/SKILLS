# upload-skills-to-perplexity.ps1 (template)
# Purpose: helper wrapper to upload a list of skills to Perplexity via API (user must fill token and endpoint)
param(
    [string]$ApiToken,
    [string]$ApiEndpoint = 'https://api.perplexity.ai/upload-skill',
    [string]$SkillsDir = 'C:\Users\GG\Desktop\skills essai1\B'
)

if (-not $ApiToken) { Write-Error 'ApiToken is required. Set it as parameter.'; exit 1 }

$files = Get-ChildItem -Path $SkillsDir -Filter '*.md' -File
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $body = @{ name = $f.BaseName; content = $content } | ConvertTo-Json -Depth 5
    try {
        $resp = Invoke-RestMethod -Uri $ApiEndpoint -Method Post -Headers @{ Authorization = "Bearer $ApiToken" } -Body $body -ContentType 'application/json' -ErrorAction Stop
        Write-Output "Uploaded $($f.Name) -> $($resp.status)"
    } catch {
        Write-Output "Failed upload $($f.Name): $($_.Exception.Message)"
    }
}
