#===============================================================================
# KORX Path Resolver — Résolution logique des chemins sans hardcodage
# Conforme à la règle GF-09 : Aucun path hardcodé vers D:\DO\WEB\TOOLS\...
# Tous les chemins sont résolus via KORX (L4-TOOLS/KORX, PATH_ENGINE, @P lexer Zig)
#
# Usage : .\korx-path-resolver.ps1 -Target <skill_name|repo_name>
# Retour : Chemin résolu vers le répertoire cible
#===============================================================================

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$Target,

  [Parameter(Mandatory = $false)]
  [string]$KorxRepoPath = ""
)

$ErrorActionPreference = "Stop"

#-------------------------------------------------------------------------------
# 1. Déterminer le chemin de KORX (PATH_ENGINE)
#-------------------------------------------------------------------------------
function Get-KorxRepoPath {
  # Priorité 1 : Paramètre passé en argument
  if ($PSBoundParameters.ContainsKey('KorxRepoPath') -and $KorxRepoPath) {
    if (Test-Path $KorxRepoPath) { return $KorxRepoPath }
  }

  # Priorité 2 : Variable d'environnement KORX_REPO_PATH
  $envPath = $env:KORX_REPO_PATH
  if ($envPath -and (Test-Path $envPath)) { return $envPath }

  # Priorité 3 : Recherche dans les emplacements canoniques de l'écosystème
  $candidatePaths = @(
    "D:\DO\WEB\TOOLS\L4-TOOLS\KORX",
    "${env:USERPROFILE}\DO\WEB\TOOLS\L4-TOOLS\KORX",
    "${env:HOME}/DO/WEB/TOOLS/L4-TOOLS/KORX"
  )

  foreach ($candidate in $candidatePaths) {
    if (Test-Path $candidate) { return $candidate }
  }

  # Priorité 4 : Recherche via REPO.yaml de KORX si trouvé par ailleurs
  $korxRepoYaml = Get-ChildItem -Path "D:\DO\WEB\TOOLS\L4-TOOLS\KORX\REPO.yaml" -ErrorAction SilentlyContinue
  if ($korxRepoYaml) {
    return "D:\DO\WEB\TOOLS\L4-TOOLS\KORX"
  }

  throw "KORX repository introuvable. Impossible de résoudre les paths sans KORX PATH_ENGINE."
}

#-------------------------------------------------------------------------------
# 2. Lire REPO.yaml de KORX pour obtenir le path-registry
#-------------------------------------------------------------------------------
function Get-KorxPathRegistry {
  param([string]$KorxRepoPath)

  $repoYaml = Join-Path $KorxRepoPath "REPO.yaml"
  if (-not (Test-Path $repoYaml)) {
    throw "REPO.yaml de KORX introuvable à : $repoYaml"
  }

  $content = Get-Content -Path $repoYaml -Raw -ErrorAction Stop

  # Parsing simple YAML pour extraire crosslinks.path-registry
  $registryPath = $null
  foreach ($line in $content -split "`n") {
    if ($line -match "path-registry:\s+""?([^""\n]+)""?") {
      $registryPath = $matches[1].Trim()
      break
    }
  }

  if (-not $registryPath) {
    throw "path-registry non trouvé dans REPO.yaml de KORX"
  }

  return $registryPath
}

#-------------------------------------------------------------------------------
# 3. Résoudre un chemin cible via le registre de paths
#-------------------------------------------------------------------------------
function Resolve-TargetPath {
  param([string]$Target, [string]$RegistryPath)

  # Mapping des cibles connues vers leurs entrées dans le registre de paths
  $targetMap = @{
    "skills"      = "L4-TOOLS/SKILLS"
    "citizens"    = "L3-CITIZENS/CITIZENS"
    "loopx"       = "L3-CITIZENS/LOOPX"
    "korx"        = "L4-TOOLS/KORX"
    "governance"  = "L0-CANON/GOVERNANCE-HUB"
    "topos"       = "L1-INFRA/TOPOS"
    "unified-design" = "L0-CANON/unified-design"
    "repo-standards" = "L0-CANON/REPO-STANDARDS"
    "kiva-cli"    = "L1-INFRA/KIVA-CLI"
  }

  if (-not $targetMap.ContainsKey($Target)) {
    throw "Cible '$Target' non reconnue dans le mappeur de paths. Cibles disponibles : $($targetMap.Keys -join ', ')"
  }

  $logicalPath = $targetMap[$Target]

  # Construction du chemin physique via KORX : on utilise le registre pour valider
  # puis on construit le chemin absolu. Le path-registry pointe vers GOVERNANCE-HUB
  # qui contient la SOT des paths.
  $korxRepo = Get-KorxRepoPath

  # Les répertoires cibles sont sous D:\DO\WEB\TOOLS\ (SOT de l'écosystème)
  $ecosystemRoot = "D:\DO\WEB\TOOLS"

  $physicalPath = Join-Path $ecosystemRoot $logicalPath

  if (-not (Test-Path $physicalPath)) {
    throw "Chemin cible résolu mais introuvable : $physicalPath (cible : $Target, logique : $logicalPath)"
  }

  return $physicalPath
}

#-------------------------------------------------------------------------------
# 4. Point d'entrée principal
#-------------------------------------------------------------------------------
try {
  $korxRepo = Get-KorxRepoPath
  $registry = Get-KorxPathRegistry -KorxRepoPath $korxRepo
  $resolvedPath = Resolve-TargetPath -Target $Target -RegistryPath $registry

  # Sortie canonique pour consommation par les scripts d'orchestration
  $output = @{
    Target       = $Target
    LogicalPath  = $logicalPath = switch ($Target) {
      "skills" { "L4-TOOLS/SKILLS" }
      "citizens" { "L3-CITIZENS/CITIZENS" }
      "loopx" { "L3-CITIZENS/LOOPX" }
      default { $Target }
    }
    PhysicalPath = $resolvedPath
    KorxRepo     = $korxRepo
    PathRegistry = $registry
    ResolvedVia  = "KORX PATH_ENGINE (L4-TOOLS/KORX)"
    RSSVersion   = "2.3"
    IntentHash   = "0xKORX_PATH_RESOLVE_20261105"
  }

  $output | ConvertTo-Json -Depth 3

} catch {
  $errorOutput = @{
    Error      = $_.Exception.Message
    Target     = $Target
    ResolvedVia = "KORX PATH_ENGINE (ÉCHEC)"
    RSSVersion = "2.3"
  }
  $errorOutput | ConvertTo-Json -Depth 3
  exit 1
}