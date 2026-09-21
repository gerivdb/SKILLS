# intent-tools.ps1
# Wrapper PowerShell pour outils INTENT depuis n'importe quel workspace
# Conforme à la règle CMD wrapper (harmonisation-v8)
param(
    [Parameter(Mandatory=$false)]
    [string[]]$Args
)
$script = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\scripts\intent-tools\intent_tools_launcher.py"
& cmd /c python $script @Args
