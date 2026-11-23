# Skill: skill-dependency-healer

## Description
Détecte et résout les dépendances manquantes ou circulaires entre skills. Lorsqu'un skill dépend d'un autre skill qui n'existe pas ou est déprécié, le healer propose soit la création du skill manquant, soit la suppression de la dépendance.

## Déclencheurs
- Mentions : "dépendances skills", "guérir dépendances", "skill manquant", "circulaire skills"

## Règles
- Si une dépendance pointe vers un skill absent : créer le skill squelette ou supprimer la dépendance
- Si une dépendance circulaire est détectée : proposer une résolution (fusion ou séparation)
- Si une dépendance pointe vers un skill déprécié : proposer une migration vers le skill successeur

## Invariants
- Aucun skill ne doit dépendre de lui-même
- Aucun cycle de dépendances n'est autorisé
- Toute dépendance doit pointer vers un skill actif (statut != deprecated)

## Statut
- Version : 1.0.0
- Statut : active
- Type : domain
- Dépendances : `skill-ecosystem-auditor`