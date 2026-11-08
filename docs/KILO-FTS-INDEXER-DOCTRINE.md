# METASKILL — Indexation FTS5 de l'historique KiloCode (ENV2)

## 1. Le Problème
L'historique natif de KiloCode est stocké dans une base SQLite (`kilo.db`, ~21 Go sur ENV2).
La recherche intégrée recharge et parcourt des volumes de texte importants à chaque requête,
ce qui devient très lent sur de longues sessions.

## 2. La Solution (Validée)
L'indexation plein-texte via une table virtuelle **SQLite FTS5** dans une base séparée
(`kilo_fts_index.db`), sans jamais modifier `kilo.db` source.

### Règle d'or
1. **Lire `kilo.db` en lecture seule** (mode `immutable`, URI `mode=ro`).
2. **Écrire l'index dans une base séparée** (`kilo_fts_index.db`).
3. **Ne jamais lancer d'indexation bloquante sur les 21 Go d'un coup** : utiliser `--limit` et `--offset` pour l'incrémental.

## 3. Commandes (HITL)

### Construire l'index (par lots de 1000)
```powershell
python kilo_fts_indexer.py build --limit 10000 --index "C:\Users\GG\.local\share\kilo\kilo_fts_index.db"
```

### Rechercher
```powershell
python kilo_fts_indexer.py search --index "C:\Users\GG\.local\share\kilo\kilo_fts_index.db" "navigateur Chromium Profile 2"
```

### Inspecter les tables de kilo.db
```powershell
python kilo_fts_indexer.py info
```

## 4. Pourquoi FTS5
- Même technologie que Navcom utilise en interne.
- Recherche BM25 (mots-clés) quasi instantanée après indexation.
- Pas de dépendance externe lourde (sqlite3 est dans la stdlib Python).
- Intégrable comme skill ENV2 (comme `browser-dom-extractor`).

## 5. Alternative clé en main
Pour un test immédiat sans écrire de code : **Navcom** (`pip install navcom`), qui lit `kilo.db` et crée un index FTS5 incrémental.
Si Navcom suffit, l'index FTS5 maison devient optionnel.
