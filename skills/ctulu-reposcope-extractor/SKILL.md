# Skill: ctulu-reposcope-extractor

## Contexte
Le stage EXTRACT du pipeline REPOSCOPE-COMPARE. Extrait les dimensions semantiques, techniques et architecturales d'un repo GitHub via l'API GitHub (gh CLI + httpx fallback).

## Outil CTULU
- **Package**: `reposcope_extractor` (PRD-081)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\reposcope-extractor\`
- **CLI**: `reposcope-extractor --target <owner/repo|yaml> --out data/ [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
reposcope-extractor --target gerivdb/ECOS-CLI --out data/ --output json
reposcope-extractor --target known_repositories.yaml --out data/ --dry-run --wal
```

```json
{
  "status": "ok|warn|error",
  "target": "<valeur --target>",
  "changes": ["extracted:1_repo", "output:data/reposcope_data_gerivdb-ECOS-CLI_20260616_023000.parquet"],
  "wal_entry": "2026-06-16T02:30:00 | reposcope-extract | gerivdb/ECOS-CLI | ok",
  "phi_cps_delta": 0.0
}
```

## Parametres
| Parametre | Defaut | Description |
|---|---|---|
| `--target` | requis | GitHub owner/repo ou path vers known_repositories.yaml |
| `--out` | `data/` | Repertoire de sortie pour Parquet |
| `--dry-run` | `false` | Simulation sans appel API |
| `--wal` | `false` | Ajout d'une entree WAL |
| `--output` | `json` | Format de sortie (json|text) |
| `--token` | `null` | GITHUB_TOKEN pour auth API |

## Dimensions extraites
- **Semantic**: description, topics, languages, readme_summary
- **Technical**: stars, forks, open_issues, commits_30d, language, license
- **Architectural**: is_template, is_fork, default_branch, created_at, updated_at
- **Derive**: strate_L (infere L0-L9), has_tests, deps_count

## Gestion rate-limit
- Backoff exponentiel (base=2.0, max_retries=3)
- Fallback gh CLI -> httpx direct
- Cache TTL 300s

## Anti-patterns
- Ne JAMAIS appeler l'API GitHub sans token sur ENV2 (rate-limit 60 req/h)
- Ne JAMAIS utiliser `reposcope-extractor` sans `--out` explicite
- Ne JAMAIS parser le README complet (limite a 500 chars)

## Tests
```bash
cd D:\DO\WEB\TOOLS\L4-TOOLS\CTULU
python scripts/run_unit_tests.py
# 56 tests, tous passing
```

## Dependances
- Python 3.11+, pandas, pyarrow, httpx, pyyaml, pydantic
- gh CLI (optionnel, fallback httpx)
