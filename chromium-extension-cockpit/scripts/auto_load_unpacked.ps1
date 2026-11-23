# auto_load_unpacked.ps1 — Hook autonome de dialogue Windows pour "Charger l'extension non empaquetée"
#
# Ce script est arme AVANT le clic CDP sur le bouton #loadUnpacked de chrome://extensions.
# Il guette l'apparition de la boite de dialogue IFileDialog Windows
# ("Sélectionner le répertoire de l'extension"), y injecte le chemin du dossier
# d'extension et valide par {ENTER}.
#
# Methode (deterministe, pas de reliance sur ValuePattern UIAutomation qui echoue
# sur le champ d'edition moderne de la boite IFileDialog) :
#   1. Detecter la fenetre par titre (UIAutomation TreeScope)
#   2. AppActivate pour donner le focus a la fenetre
#   3. Trouver le champ Edit "Dossier :", SetFocus dessus
#   4. SendKeys du chemin complet (caractère par caractère si besoin)
#   5. SendKeys {ENTER} pour valider et fermer le dialogue
#   6. Verifier que le dialogue a disparu (ferme) -> succès
#
# Usage :
#   powershell -WindowStyle Hidden -File auto_load_unpacked.ps1 -ExtensionPath "D:\...\GEM-X" -TimeoutSec 30
#
# Code de retour : 0 = dialogue rempli et valide (ferme), 1 = timeout/echec.

param(
    [Parameter(Mandatory = $true)]
    [string]$ExtensionPath,

    [int]$TimeoutSec = 30
)

$ErrorActionPreference = "Continue"
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

Add-Type -AssemblyName UIAutomationClient | Out-Null
Add-Type -AssemblyName UIAutomationTypes | Out-Null

function Find-ExtensionDialog {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $cond = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Window)
    $windows = $root.FindAll([System.Windows.Automation.TreeScope]::Children, $cond)
    $matches = New-Object System.Collections.Generic.List[System.Windows.Automation.AutomationElement]
    foreach ($win in $windows) {
        $name = try { $win.Current.Name } catch { $null }
        $class = try { $win.Current.ClassName } catch { $null }
        if ($null -eq $name -and $null -eq $class) { continue }
        $lname = ($name -or '').ToLower()
        $isDialog = ($class -eq '#32770') -or
                    ($lname -like '*extension*') -or ($lname -like '*dossier*') -or
                    ($lname -like '*folder*') -or ($lname -like '*sélectionner*') -or
                    ($lname -like '*select*')
        if ($isDialog) { $matches.Add($win) }
    }
    if ($matches.Count -eq 0) { return $null }
    return $matches[$matches.Count - 1]
}

function Find-EditControl {
    param([System.Windows.Automation.AutomationElement]$Root)
    $cond = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Edit)
    $edits = $Root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)
    if ($edits.Count -gt 0) { return $edits[0] }
    return $null
}

function Dialog-StillOpen {
    param([System.Windows.Automation.AutomationElement]$Dialog)
    if ($null -eq $Dialog) { return $false }
    try {
        # UIAutomation : si l'element n'est plus valide, acceder a Current jette une exception
        $null = $Dialog.Current.Name
        return $true
    } catch {
        return $false
    }
}

# ——————————————————————————————————————————————————————————————————————
# Boucle principale
# ——————————————————————————————————————————————————————————————————————

while ($stopwatch.Elapsed.TotalSeconds -lt $TimeoutSec) {
    $dialog = Find-ExtensionDialog
    if ($null -ne $dialog) {
        $title = try { $dialog.Current.Name } catch { '' }

        # 1. Focus fenetre
        try {
            $shell = New-Object -ComObject WScript.Shell
            $shell.AppActivate($title) | Out-Null
        } catch {}
        Start-Sleep -Milliseconds 400
        try { $dialog.SetFocus() } catch {}

        # 2. Focus champ Edit "Dossier :"
        $edit = Find-EditControl -Root $dialog
        if ($null -ne $edit) {
            try { $edit.SetFocus() } catch {}
            Start-Sleep -Milliseconds 300

            # 3. Ecrire le chemin dans le champ (SendKeys direct)
            try {
                # Tout selectionner d'abord pour eviter d'ajouter a un contenu existant
                $shell.SendKeys('^a')
                Start-Sleep -Milliseconds 100
                $shell.SendKeys($ExtensionPath)
                Start-Sleep -Milliseconds 500
            } catch {
                Write-Warning "[AUTO-LOAD] Echec SendKeys du chemin"
            }

            # 4. Valider par Entrée (ferme le dialogue et selectionne le dossier)
            try {
                $shell.SendKeys('{ENTER}')
            } catch {
                Write-Warning "[AUTO-LOAD] Echec SendKeys ENTER"
            }

            # 5. Attendre que le dialogue se ferme (verification)
            $closed = $false
            for ($i = 0; $i -lt 20; $i++) {
                Start-Sleep -Milliseconds 250
                if (-not (Dialog-StillOpen -Dialog $dialog)) {
                    $closed = $true
                    break
                }
                # Re-verifier si une nouvelle fenetre de dialogue est apparue
                $d2 = Find-ExtensionDialog
                if ($null -ne $d2 -and $d2.Current.RuntimeId -ne $dialog.Current.RuntimeId) {
                    $dialog = $d2
                }
            }

            if ($closed) {
                # Laisser Chromium enregistrer l'extension
                Start-Sleep -Milliseconds 1500
                exit 0
            }
            # Sinon le dialogue est encore ouvert : continuer la boucle pour reessayer
        }
    }
    Start-Sleep -Milliseconds 300
}

Write-Warning "[AUTO-LOAD] Dialogue IFileDialog non rempli/ferme dans le delai de ${TimeoutSec}s."
exit 1
