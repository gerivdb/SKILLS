#==============================================================================
# SKILL: agent-manager-ui-semantic-map
# Rôle: Empêcher les hallucinations d'interprétation des boutons graphiques Kilo.
# Dictionnaire sémantique : libellé UI → action Git réelle → effet sur worktree → effet sur agent-manager.json → nettoie ?
# Couche CRUD — Read (référence).
#==============================================================================

[CmdletBinding()]
param(
    [string]$UiLabel,       # Libellé du bouton/menu à interpréter (optionnel)
    [string]$ActionGit      # Action Git à vérifier (optionnel)
)

$timestamp = (Get-Date).ToUniversalTime().ToString("o")

# ── Dictionnaire sémantique complet ──
$dictionary = @(
    [PSCustomObject]@{
        UiLabel          = "Supprimer le Worktree"
        Icone            = "🗑️ Poubelle"
        ActionGitReelle  = "git worktree remove --force + git branch -D"
        EffetWorktree    = "Supprimé (dossier physique + référence Git)"
        EffetJson        = "Entrée retirée de worktrees et worktreeOrder"
        Nettoie          = "Oui"
        Avertissement    = "Irréversible — confirmer avant exécution"
    }
    [PSCustomObject]@{
        UiLabel          = "Mettre à jour depuis la base"
        Icone            = "🔀 Fusion Git"
        ActionGitReelle  = "git fetch + git merge origin/main"
        EffetWorktree    = "Mis à jour (commits de base intégrés)"
        EffetJson        = "Aucun changement"
        Nettoie          = "Non"
        Avertissement    = "NE NETTOIE RIEN — ne supprime pas de fichiers, ne retire pas d'entrées JSON"
    }
    [PSCustomObject]@{
        UiLabel          = "Nouvelle section"
        Icone            = "➕ Plus"
        ActionGitReelle  = "Crée clé 'sections' dans agent-manager.json (aucune action Git)"
        EffetWorktree    = "Aucun"
        EffetJson        = "Entrée déplacée vers une section thématique"
        Nettoie          = "Partiel"
        Avertissement    = "Réorganise l'affichage, ne modifie pas le dépôt Git"
    }
    [PSCustomObject]@{
        UiLabel          = "Épingler"
        Icone            = "📌 Épingle"
        ActionGitReelle  = "Modifie 'pinnedWorktrees' dans agent-manager.json (aucune action Git)"
        EffetWorktree    = "Aucun"
        EffetJson        = "Priorité d'affichage modifiée"
        Nettoie          = "Non"
        Avertissement    = "Affichage uniquement, pas d'impact sur le code"
    }
    [PSCustomObject]@{
        UiLabel          = "ungrouped"
        Icone            = "—"
        ActionGitReelle  = "Aucune (état d'affichage)"
        EffetWorktree    = "Aucun"
        EffetJson        = "Worktree sans section dédiée"
        Nettoie          = "Non"
        Avertissement    = "ungrouped n'est PAS un fantôme — ce n'est pas une entrée orpheline à supprimer"
    }
)

# ── Filtrage optionnel ──
$output = $dictionary
if ($UiLabel) {
    $output = $dictionary | Where-Object { $_.UiLabel -eq $UiLabel }
    if (-not $output) {
        Write-Output "[FAIL] Libellé UI '$UiLabel' introuvable dans le dictionnaire sémantique."
        exit 1
    }
}
if ($ActionGit) {
    $output = $output | Where-Object { $_.ActionGitReelle -like "*$ActionGit*" }
    if (-not $output) {
        Write-Output "[FAIL] Aucune entrée ne correspond à l'action Git '$ActionGit'."
        exit 1
    }
}

# ── Affichage ──
Write-Output "=== DICTIONNAIRE SÉMANTIQUE UI — Agent Manager ==="
Write-Output "Généré le : $timestamp"
Write-Output ""

foreach ($entry in $output) {
    Write-Output "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Output "Libellé UI : $($entry.UiLabel)"
    Write-Output "Icône      : $($entry.Icone)"
    Write-Output "Action Git : $($entry.ActionGitReelle)"
    Write-Output "Effet WT   : $($entry.EffetWorktree)"
    Write-Output "Effet JSON : $($entry.EffetJson)"
    Write-Output "Nettoie    : $($entry.Nettoie)"
    Write-Output "Avert.     : $($entry.Avertissement)"
}

Write-Output ""
Write-Output "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Output "RÈGLE D'OR : Jamais déduire la fonction d'un bouton à partir de son libellé seul."
Write-Output "             Toujours consulter ce dictionnaire avant d'agir."
Write-Output "             'ungrouped' = état d'affichage sans section, pas un fantôme."

exit 0