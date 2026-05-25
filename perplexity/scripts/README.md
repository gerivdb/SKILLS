# README for scripts directory

This directory contains helper PowerShell scripts used to manage Perplexity skills.

Files:
- verify_pipe.ps1 : verifies that markdown skills at repository root contain the YAML literal `|` after frontmatter.
- generate-canonical-skill.ps1 : generates a canonical skill file with the `|` injected. Usage: powershell -File generate-canonical-skill.ps1 -Name my-skill -Description "desc" -Title "Title" -Body "Content..."
- batch-verify-and-report.ps1 : produces `scripts\skills_report.csv` listing each skill file, size, presence of `|`, title.
- upload-skills-to-perplexity.ps1 : template wrapper to upload skills via Perplexity API (requires API token and correct endpoint).

Usage recommendations:
1. Run verify_pipe.ps1 before attempting upload.
2. Use batch-verify-and-report.ps1 to get an inventory and CSV report.
3. Use generate-canonical-skill.ps1 to create new valid skills (always includes `|`).
4. Use upload-skills-to-perplexity.ps1 after filling the API token and endpoint.
