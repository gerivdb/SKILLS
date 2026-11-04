"""
m3-bigquery-conversation-warehouse — Script d'upsert des conversations.

Upsert une conversation NotebookLM dans la table BigQuery `conversations`.
Si le conversationId existe deja, les champs modifies sont mises a jour.
Sinon, une nouvelle ligne est inseree.

Codes retour:
  0 = insertion/mise a jour reussie
  1 = doublon (aucune modificationnee)
  2 = echec d'insertion
"""

import argparse
import json
import sys
from datetime import datetime, timezone

try:
    from google.cloud import bigquery
except ImportError as exc:  # pragma: no cover - dependance optionnelle
    print(f"ERREUR: google-cloud-bigquery introuvable: {exc}", file=sys.stderr)
    sys.exit(2)


TABLE_FQN = "omni_m3.conversations"

UPSERT_SQL = f"""
MERGE `{TABLE_FQN}` T
USING (
  SELECT
    @conversationId AS conversationId,
    @title AS title,
    @createdAt AS createdAt,
    @updatedAt AS updatedAt,
    @author AS author,
    @tags AS tags,
    @embeddingVector AS embeddingVector,
    @linkedConversationIds AS linkedConversationIds,
    @workspaceId AS workspaceId,
    @m3TreeNodeId AS m3TreeNodeId
) S
ON T.conversationId = S.conversationId
WHEN MATCHED THEN
  UPDATE SET
    title = S.title,
    updatedAt = S.updatedAt,
    author = S.author,
    tags = S.tags,
    embeddingVector = S.embeddingVector,
    linkedConversationIds = S.linkedConversationIds,
    workspaceId = S.workspaceId,
    m3TreeNodeId = S.m3TreeNodeId
WHEN NOT MATCHED THEN
  INSERT (conversationId, title, createdAt, updatedAt, author, tags,
          embeddingVector, linkedConversationIds, workspaceId, m3TreeNodeId)
  VALUES (S.conversationId, S.title, S.createdAt, S.updatedAt, S.author, S.tags,
          S.embeddingVector, S.linkedConversationIds, S.workspaceId, S.m3TreeNodeId)
"""


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Upsert une conversation NotebookLM dans BigQuery"
    )
    parser.add_argument("--conversation-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--created-at", required=True, help="ISO-8601 UTC")
    parser.add_argument("--updated-at", required=True, help="ISO-8601 UTC")
    parser.add_argument("--author", default="")
    parser.add_argument("--tags", default="", help="liste separée par des virgules ou JSON")
    parser.add_argument("--embedding-vector", default="", help="JSON tableau de float")
    parser.add_argument("--linked-conversation-ids", default="", help="liste separée par des virgules")
    parser.add_argument("--workspace-id", default="")
    parser.add_argument("--m3-tree-node-id", default="")
    parser.add_argument("--project", required=True, help="Projet GCP BigQuery")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche le SQL sans l'executer")
    return parser.parse_args(argv)


def to_timestamp(value: str):
    """Parse une chaine ISO-8601 en datetime aware UTC."""
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_array(value: str, item_type=str):
    if not value or not value.strip():
        return []
    raw = value.strip()
    if raw.startswith("["):
        try:
            return [item_type(x) for x in json.loads(raw)]
        except json.JSONDecodeError:
            return [item_type(x.strip()) for x in raw.strip("[]").split(",") if x.strip()]
    return [item_type(x.strip()) for x in raw.split(",") if x.strip()]


def build_parameters(conv: dict):
    """Construit la liste de paramètres BigQuery à partir d'un dict conversation."""
    return [
        bigquery.ScalarQueryParameter("conversationId", "STRING", conv["conversationId"]),
        bigquery.ScalarQueryParameter("title", "STRING", conv["title"]),
        bigquery.ScalarQueryParameter("createdAt", "TIMESTAMP", to_timestamp(conv["createdAt"])),
        bigquery.ScalarQueryParameter("updatedAt", "TIMESTAMP", to_timestamp(conv["updatedAt"])),
        bigquery.ScalarQueryParameter("author", "STRING", conv.get("author", "")),
        bigquery.ArrayQueryParameter("tags", "STRING", conv.get("tags", [])),
        bigquery.ArrayQueryParameter("embeddingVector", "FLOAT64", conv.get("embeddingVector", [])),
        bigquery.ArrayQueryParameter("linkedConversationIds", "STRING", conv.get("linkedConversationIds", [])),
        bigquery.ScalarQueryParameter("workspaceId", "STRING", conv.get("workspaceId", "")),
        bigquery.ScalarQueryParameter("m3TreeNodeId", "STRING", conv.get("m3TreeNodeId", conv["conversationId"])),
    ]


def run_upsert(client: bigquery.Client, conv: dict) -> bool:
    """Execute un MERGE upsert pour une conversation. Retourne True si reussi."""
    job_config = bigquery.QueryJobConfig(query_parameters=build_parameters(conv))
    query_job = client.query(UPSERT_SQL, job_config=job_config)
    query_job.result()  # bloque jusqu'a completion
    return True


def main(argv=None) -> int:
    args = parse_args(argv)

    try:
        created_at = to_timestamp(args.created_at)
        updated_at = to_timestamp(args.updated_at)
    except ValueError as exc:
        print(f"ERREUR: horodatage invalide: {exc}", file=sys.stderr)
        return 2

    conv = {
        "conversationId": args.conversation_id,
        "title": args.title,
        "createdAt": args.created_at,
        "updatedAt": args.updated_at,
        "author": args.author,
        "tags": to_array(args.tags),
        "embeddingVector": to_array(args.embedding_vector, item_type=float),
        "linkedConversationIds": to_array(args.linked_conversation_ids),
        "workspaceId": args.workspace_id,
        "m3TreeNodeId": args.m3_tree_node_id or args.conversation_id,
    }

    if args.dry_run:
        print("--- DRY RUN : SQL d'upsert ---")
        print(UPSERT_SQL)
        print("--- Parametres ---")
        for p in build_parameters(conv):
            print(f"  {p.name} = {p.value}")
        return 0

    client = bigquery.Client(project=args.project)
    try:
        run_upsert(client, conv)
    except Exception as exc:  # pragma: no cover - erreur runtime BigQuery
        print(f"ERREUR: echec de l'upsert BigQuery: {exc}", file=sys.stderr)
        return 2

    print(
        f"OK: conversation upserte {args.conversation_id} "
        f"(workspace={args.workspace_id or '-'})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
