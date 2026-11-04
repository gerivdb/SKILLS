"""
m3-bigquery-conversation-warehouse — Synchronisation periodique.

Synchronise toutes les conversations du graphe M3-Tree vers l'entrepot BigQuery.
Detecte les divergences et applique les upserts manquantes.

Ce script est appele periodiquement (cron / scheduler) pour maintenir la
coherence entre le graphe M3-Tree et l'entrepot BigQuery.

Dependances: upsert_conversation (meme package), google-cloud-bigquery.
"""

import argparse
import json
import sys
from datetime import timezone

try:
    from google.cloud import bigquery
except ImportError as exc:  # pragma: no cover
    print(f"ERREUR: google-cloud-bigquery introuvable: {exc}", file=sys.stderr)
    sys.exit(2)

from upsert_conversation import run_upsert, build_parameters  # noqa: E402


TABLE_FQN = "omni_m3.conversations"


def load_m3_tree_conversations(source_path: str):
    """
    Charge les conversations depuis une source M3-Tree.

    La source est un dump JSON du graphe M3-Tree contenant une cle "nodes".
    Retourne une liste de dictionnaires de conversations.
    """
    with open(source_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    conversations = []
    for node in data.get("nodes", []):
        if node.get("type") != "conversation":
            continue
        conversations.append({
            "conversationId": node["conversationId"],
            "title": node.get("title", ""),
            "createdAt": node.get("createdAt"),
            "updatedAt": node.get("updatedAt"),
            "author": node.get("author", ""),
            "tags": node.get("tags", []),
            "embeddingVector": node.get("embeddingVector", []),
            "linkedConversationIds": node.get("linkedConversationIds", []),
            "workspaceId": node.get("workspaceId", ""),
            "m3TreeNodeId": node.get("m3TreeNodeId", node["conversationId"]),
        })
    return conversations


def sync(project: str, source_path: str, dry_run: bool = False) -> int:
    conversations = load_m3_tree_conversations(source_path)
    client = bigquery.Client(project=project)

    inserted = 0
    updated = 0
    failed = 0

    for conv in conversations:
        cid = conv["conversationId"]
        # Verifier si la ligne existe deja (pour compter insert vs update)
        check_sql = f"""
        SELECT COUNT(1) AS cnt FROM `{TABLE_FQN}`
        WHERE conversationId = @cid
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("cid", "STRING", cid)
            ]
        )
        exists = False
        try:
            row = list(client.query(check_sql, job_config=job_config))[0]
            exists = row.cnt > 0
        except Exception as exc:  # pragma: no cover
            print(f"ERREUR: verification {cid}: {exc}", file=sys.stderr)
            failed += 1
            continue

        if dry_run:
            action = "UPDATE" if exists else "INSERT"
            print(f"[DRY RUN] {action} {cid}")
            inserted += 1
            continue

        try:
            run_upsert(client, conv)
            if exists:
                updated += 1
            else:
                inserted += 1
        except Exception as exc:  # pragma: no cover
            print(f"ERREUR: upsert {cid}: {exc}", file=sys.stderr)
            failed += 1

    print(
        f"SYNC TERMINE: {inserted} inseres, {updated} mises a jour, "
        f"{failed} echecs sur {len(conversations)} conversations."
    )
    return 1 if failed else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronise les conversations M3-Tree vers BigQuery"
    )
    parser.add_argument("--project", required=True, help="Projet GCP BigQuery")
    parser.add_argument("--source", required=True,
                        help="Chemin JSON du graphe M3-Tree source")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche les actions sans executer")
    args = parser.parse_args(argv)
    return sync(args.project, args.source, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
