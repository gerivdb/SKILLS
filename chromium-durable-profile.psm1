<#
.SYNOPSIS Skill : Chromium durable avec user-data-dir + CDP (tout type de page).
.NOTES Aucun cookie, token ou Authorization n'est loggé. Persistance de session entre redémarrages via user-data-dir.
#>

# --- Configuration par défaut ---
$script:DEFAULT_PROFILE_DIR = "C:\Users\GG\AppData\Local\Chromium\PlaygroundProfile"
$script:DEFAULT_CDP_PORT = 9222
$script:DEFAULT_CHROMIUM_EXE = "C:\Program Files\Chromium\chrome.exe"
$script:CDP_TIMEOUT_SEC = 10

# --- Filtre de sécurité : masquer les en-têtes sensibles dans toute sortie ---
function Filter-SensitiveHeaders {
<#
.SYNOPSIS Supprime Authorization, Cookie, Set-Cookie d'un objet avant affichage/log.
.PARAMETER InputObject
#>
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

# --- Fonctions publiques ---

function Test-ChromiumCdp {
<#
.SYNOPSIS Vérifie que le port CDP répond (Chromium déjà lancé).
.PARAMETER Port
#>
  param([int]$Port = $script:DEFAULT_CDP_PORT)
  try {
    $r = Invoke-RestMethod -Uri "http://localhost:$Port/json" -TimeoutSec 3 -ErrorAction Stop
    return @{ active = $true; port = $Port; targetCount = ($r | Measure-Object).Count }
  } catch {
    return @{ active = $false; port = $Port; error = $_.Exception.Message }
  }
}

function Start-ChromiumProfile {
<#
.SYNOPSIS Lance Chromium avec user-data-dir dédié + CDP (profil durable).
.PARAMETER ProfileDir  Chemin du profil utilisateur (cookies, localStorage, session).
.PARAMETER ChromiumExe Chemin de l'exécutable Chromium/Chrome/Edge.
.PARAMETER Port        Port CDP (défaut 9222).
.PARAMETER NoFirstRun  Saute l'assistant première exécution.
.PARAMETER NoDefaultBrowserCheck Désactive les popups navigateur par défaut.
#>
  param(
    [string]$ProfileDir = $script:DEFAULT_PROFILE_DIR,
    [string]$ChromiumExe = $script:DEFAULT_CHROMIUM_EXE,
    [int]$Port = $script:DEFAULT_CDP_PORT,
    [switch]$NoFirstRun = $true,
    [switch]$NoDefaultBrowserCheck = $true
  )

  # Vérifier si déjà actif
  $status = Test-ChromiumCdp -Port $Port
  if ($status.active) {
    Write-Output "CDP déjà actif sur le port $Port (profil durable déjà lancé)."
    return $status
  }

  # Vérifier l'exécutable
  if (-not (Test-Path -LiteralPath $ChromiumExe)) {
    throw "CHROMIUM_EXE_MISSING: $ChromiumExe introuvable. Spécifiez -ChromiumExe."
  }

  # Construire les arguments
  $args = @(
    "--remote-debugging-port=$Port",
    "--remote-debugging-address=127.0.0.1",
    "--user-data-dir=$ProfileDir",
    "--no-first-run",
    "--no-default-browser-check"
  )

  # Lancer (fenêtre cachée si possible via style hidden sur le processus père)
  Start-Process -FilePath $ChromiumExe -ArgumentList $args -WindowStyle Hidden
  Write-Output "Chromium lancé avec profil $ProfileDir sur CDP port $Port."

  # Attendre que CDP réponde (max 30s)
  for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $status = Test-ChromiumCdp -Port $Port
    if ($status.active) {
      Write-Output "CDP accessible après $($i+1)s."
      return $status
    }
  }
  throw "CDP_TIMEOUT: Chromium n'a pas exposé le CDP sur le port $Port après 30s."
}

function Ensure-ChromiumProfile {
<#
.SYNOPSIS Garantit un profil Chromium durable + CDP actif. Lance si nécessaire.
.PARAMETER ProfileDir
.PARAMETER ChromiumExe
.PARAMETER Port
#>
  param(
    [string]$ProfileDir = $script:DEFAULT_PROFILE_DIR,
    [string]$ChromiumExe = $script:DEFAULT_CHROMIUM_EXE,
    [int]$Port = $script:DEFAULT_CDP_PORT
  )
  $status = Test-ChromiumCdp -Port $Port
  if (-not $status.active) {
    $status = Start-ChromiumProfile -ProfileDir $ProfileDir -ChromiumExe $ChromiumExe -Port $Port
  }
  return $status
}

function Get-ChromiumTargets {
<#
.SYNOPSIS Liste toutes les cibles CDP ouvertes.
.PARAMETER Port
#>
  param([int]$Port = $script:DEFAULT_CDP_PORT)
  $r = Invoke-RestMethod -Uri "http://localhost:$Port/json" -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
  return $r | Filter-SensitiveHeaders
}

function Get-ChromiumTargetByUrl {
<#
.SYNOPSIS Récupère le premier target CDP dont l'URL correspond à un pattern.
.PARAMETER UrlPattern  Pattern de l'URL (ex: '*deepseek*', '*script.google.com*').
.PARAMETER Port
#>
  param(
    [string]$UrlPattern,
    [int]$Port = $script:DEFAULT_CDP_PORT
  )
  $targets = Invoke-RestMethod -Uri "http://localhost:$Port/json" -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
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
  } | Filter-SensitiveHeaders
}

function Open-ChromiumPage {
<#
.SYNOPSIS Ouvre une URL dans un nouvel onglet CDP du profil durable.
.PARAMETER Url
.PARAMETER Port
#>
  param(
    [string]$Url,
    [int]$Port = $script:DEFAULT_CDP_PORT
  )
  $encoded = [System.Web.HttpUtility]::UrlEncode($Url)
  $resp = Invoke-WebRequest -Uri "http://localhost:$Port/json/new?$encoded" -Method PUT -UseBasicParsing -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
  return $resp.Content | ConvertFrom-Json | Filter-SensitiveHeaders
}

function Close-ChromiumTarget {
<#
.SYNOPSIS Ferme une cible CDP par targetId.
.PARAMETER TargetId
.PARAMETER Port
#>
  param(
    [string]$TargetId,
    [int]$Port = $script:DEFAULT_CDP_PORT
  )
  Invoke-WebRequest -Uri "http://localhost:$Port/json/close/$TargetId" -Method PUT -UseBasicParsing -TimeoutSec $script:CDP_TIMEOUT_SEC -ErrorAction Stop
}

# --- Export ---
Export-ModuleMember -Function Test-ChromiumCdp, Start-ChromiumProfile, Ensure-ChromiumProfile, Get-ChromiumTargets, Get-ChromiumTargetByUrl, Open-ChromiumPage, Close-ChromiumTarget
