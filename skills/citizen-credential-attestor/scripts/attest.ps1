# scripts/attest.ps1
# citizen-credential-attestor : verifie les credentials cryptographiques d'un citizen
# Encodage CP1252 / ASCII

$ErrorActionPreference = "Stop"

param(
    [string]$CitizenId = "",
    [string]$ProofType = "both",
    [string]$CredStore = "D:\DO\WEB\TOOLS\L3-CITIZENS\LORX\credentials.yaml"
)

function Write-Log {
    param([string]$Message)
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Write-Output "[$ts] $Message"
}

if ([string]::IsNullOrWhiteSpace($CitizenId)) {
    Write-Log "ERREUR: citizen id vide"
    exit 1
}

Write-Log "Attestation credentials pour : $CitizenId"
$gpgOk = $false
$bdcpOk = $false

if ($ProofType -in @("gpg","both")) {
    $gpg = gpg --list-keys "$CitizenId" 2>$null
    if ($LASTEXITCODE -eq 0 -and $gpg) {
        $gpgOk = $true
        Write-Log "GPG: OK - cle trouvee pour $CitizenId"
    } else {
        Write-Log "GPG: ABSENT - aucune cle pour $CitizenId"
    }
}

if ($ProofType -in @("bdcp","both")) {
    $bdcpToken = $env:BDCP_TOKEN
    if (-not [string]::IsNullOrEmpty($bdcpToken)) {
        $bdcpOk = $true
        Write-Log "BDCP: OK - token present"
    } else {
        Write-Log "BDCP: ABSENT - variable BDCP_TOKEN non definie"
    }
}

if (($ProofType -eq "both" -and $gpgOk -and $bdcpOk) -or (($ProofType -eq "gpg" -and $gpgOk) -or ($ProofType -eq "bdcp" -and $bdcpOk))) {
    Write-Log "RESULTAT: ATTESTE - $CitizenId dispose des droits cryptographiques requis"
    exit 0
} else {
    Write-Log "RESULTAT: REVOKE - $CitizenId ne dispose pas des droits requis (gpg=$gpgOk bdcp=$bdcpOk)"
    exit 3
}
