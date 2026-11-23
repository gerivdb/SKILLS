<#
.SYNOPSIS
    Skill spécialisé : Chromium Profil 2 durable avec CDP.
    Cible EXCLUSIVEMENT le profil : C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2
    Ne jamais utiliser ce skill pour un autre profil.

.DESCRIPTION
    Lance Chromium avec le user-data-dir parent + --profile-directory=Profile 2,
    et active le CDP sur 127.0.0.1:9222.
    Toutes les sorties filtrent Authorization/Cookie/Set-Cookie (BDCP).

.NOTES
    Version : 1.0.0
    Strate  : ENV2.env / L4-TOOLS/SKILLS
    Profil cible : Profile 2 (chemin durci, pas de profil temporaire)
#>

# ============================================================================
# CONFIGURATION DURCIE — PROFIL 2 UNIQUEMENT
# ============================================================================
$script:PROFILE_2_USER_DATA_DIR = "C:\Users\GG\AppData\Local\Chromium\User Data"
$script:PROFILE_2_DIRECTORY     = "Profile 2"
$script:PROFILE_2_CHROMIUM_EXE  = "C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe"
$script:PROFILE_2_CDP_PORT      = 9222
$script:PROFILE_2_CDP_ADDRESS   = "127.0.0.1"
$script:CDP_TIMEOUT_SEC         = 10

# --- Filtre de sécurité : masquer les en-têtes sensibles ---
function Filter-SensitiveHeaders-P2 {
    param([object]$InputObject)
    if ($null -eq $InputObject) { return $null }
    $type = $InputObject.GetType().Name
    if ($type -eq 'String') {
        $s = [string]$InputObject
        $s = $s -replace '(?i)authorization\s*:\s*[^,}\s]+', 'Authorization: [REDACTED]'
        $s = $s -replace '(?i)cookie\s*:\s*[^;,\s]+', 'Cookie: [REDACTED]'
        $s = $s -replace '(?i)set-cookie\s*:\s*[^;,\s]+', 'Set-Cookie: [REDACTED]'
        return $s
    }
    if ($type -eq 'PSCustomObject') {
        $clean = [PSCustomObject]@{}
        foreach ($prop in $InputObject.PSObject.Properties) {
            $name = $prop.Name
            if ($name -match '^(authorization|cookie|set-cookie)$') {
                $clean | Add-Member -MemberType NoteProperty -Name $name -Value '[REDACTED]' -Force
            } else {
                $clean | Add-Member -MemberType NoteProperty -Name $name -Value $prop.Value -Force
            }
        }
        return $clean
    }
    return $InputObject
}

# --- Test si CDP est déjà actif sur le port 9222 ---
function Test-ChromiumProfile2Cdp {
    <#
    .SYNOPSIS Vérifie que le CDP du Profil 2 répond sur 127.0.0.1:9222.
    #>
    try {
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:9222/json" -TimeoutSec 3 -ErrorAction Stop
        return @{ active = $true; port = 9222; address = '127.0.0.1'; targetCount = ($r | Measure-Object).Count }
    } catch {
        return @{ active = $false; port = 9222; address = '127.0.0.1'; error = $_.Exception.Message }
    }
}

# --- Lancement du Profil 2 avec CDP ---
function Start-ChromiumProfile2 {
    <#
    .SYNOPSIS
        Lance Chromium Profil 2 avec user-data-dir + --profile-directory=Profile 2 + CDP.
        C'est la SEULE façon correcte d'ouvrir le Profil 2.
    #>
    param(
        [switch]$NoFirstRun = $true,
        [switch]$NoDefaultBrowserCheck = $true
    )

    # Vérifier si déjà actif
    $status = Test-ChromiumProfile2Cdp
    if ($status.active) {
        Write-Output "CDP Profil 2 déjà actif sur 127.0.0.1:9222 (targetCount=$($status.targetCount))."
        return $status
    }

    # Vérifier l'exécutable
    if (-not (Test-Path -LiteralPath $script:PROFILE_2_CHROMIUM_EXE)) {
        throw "CHROMIUM_EXE_MISSING: $($script:PROFILE_2_CHROMIUM_EXE) introuvable."
    }

    # Argument --profile-directory est INDISPENSABLE pour cibler Profile 2
    $args = @(
        "--remote-debugging-port=$($script:PROFILE_2_CDP_PORT)",
        "--remote-debugging-address=$($script:PROFILE_2_CDP_ADDRESS)",
        "--user-data-dir=$($script:PROFILE_2_USER_DATA_DIR)",
        "--profile-directory=$($script:PROFILE_2_DIRECTORY)",
        "--no-first-run",
        "--no-default-browser-check"
    )

    Write-Output "Lancement Chromium Profil 2 :"
    Write-Output "  user-data-dir : $($script:PROFILE_2_USER_DATA_DIR)"
    Write-Output "  profile-dir   : $($script:PROFILE_2_DIRECTORY)"
    Write-Output "  CDP           : $($script:PROFILE_2_CDP_ADDRESS):$($script:PROFILE_2_CDP_PORT)"

    Start-Process -FilePath $script:PROFILE_2_CHROMIUM_EXE -ArgumentList $args -WindowStyle Hidden
    Write-Output "Chromium Profil 2 lancé."

    # Attendre que CDP réponde (max 30s)
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        $status = Test-ChromiumProfile2Cdp
        if ($status.active) {
            Write-Output "CDP Profil 2 accessible après $($i+1)s."
            return $status
        }
    }
    throw "CDP_TIMEOUT: Chromium Profil 2 n'a pas exposé le CDP sur 127.0.0.1:9222 après 30s."
}

# --- Garantie que le Profil 2 est actif ---
function Ensure-ChromiumProfile2 {
    <#
    .SYNOPSIS
        Garantit que le Profil 2 est lancé avec CDP. Lance si nécessaire.
    #>
    $status = Test-ChromiumProfile2Cdp
    if (-not $status.active) {
        $status = Start-ChromiumProfile2
    }
    return $status
}

# --- Liste des cibles CDP ---
function Get-ChromiumProfile2Targets {
    <#
    .SYNOPSIS Liste toutes les cibles CDP du Profil 2.
    #>
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:9222/json" -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
    return $r | Filter-SensitiveHeaders-P2
}

# --- Cible par pattern d'URL ---
function Get-ChromiumProfile2TargetByUrl {
    <#
    .SYNOPSIS Récupère la première cible CDP du Profil 2 dont l'URL match le pattern.
    .PARAMETER UrlPattern Pattern d'URL (ex: '*gemini*', '*deepseek*').
    #>
    param([string]$UrlPattern)
    $targets = Invoke-RestMethod -Uri "http://127.0.0.1:9222/json" -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
    $match = $targets | Where-Object { $_.type -eq 'page' -and $_.url -like $UrlPattern } | Select-Object -First 1
    if (-not $match) {
        return @{ found = $false; pattern = $UrlPattern }
    }
    return @{
        found = $true
        targetId = $match.id
        type = $match.type
        title = $match.title
        url = $match.url
        webSocketDebuggerUrl = $match.webSocketDebuggerUrl
    } | Filter-SensitiveHeaders-P2
}

# --- Ouvrir une nouvelle page dans le Profil 2 ---
function Open-ChromiumProfile2Page {
    <#
    .SYNOPSIS Ouvre une URL dans un nouvel onglet CDP du Profil 2.
    .PARAMETER Url URL à ouvrir.
    #>
    param([string]$Url)
    $encoded = [System.Web.HttpUtility]::UrlEncode($Url)
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/new?$encoded" -Method PUT -UseBasicParsing -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
    return $resp.Content | ConvertFrom-Json | Filter-SensitiveHeaders-P2
}

# --- Fermer une cible CDP ---
function Close-ChromiumProfile2Target {
    <#
    .SYNOPSIS Ferme une cible CDP du Profil 2 par targetId.
    .PARAMETER TargetId Identifiant de la cible.
    #>
    param([string]$TargetId)
    Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/close/$TargetId" -Method PUT -UseBasicParsing -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
}

# --- Export ---
Export-ModuleMember -Function Test-ChromiumProfile2Cdp, Start-ChromiumProfile2, Ensure-ChromiumProfile2, Get-ChromiumProfile2Targets, Get-ChromiumProfile2TargetByUrl, Open-ChromiumProfile2Page, Close-ChromiumProfile2Target
Export-ModuleMember -Variable PROFILE_2_USER_DATA_DIR, PROFILE_2_DIRECTORY, PROFILE_2_CHROMIUM_EXE, PROFILE_2_CDP_PORT, PROFILE_2_CDP_ADDRESS
