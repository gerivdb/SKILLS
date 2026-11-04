-- ============================================================================
-- m3-bigquery-conversation-warehouse — Schéma BigQuery
-- Table: conversations
-- Skill: m3-bigquery-conversation-warehouse (IntentHash: 0xSKILL_M3_BCW_20261103)
-- Couche: L4-TOOLS | Depot: gerivdb/SKILLS | Branche: feat/omni-m3-bigquery-warehouse-skill4
-- ============================================================================
-- Cette table centralise les metadonnees de toutes les conversations NotebookLM
-- du maillage OMNI-INTER-NOTEBOOK-LM (~60 vaults) pour requetes analytiques
-- rapides et paralleles. Alimente egalement le moteur PGX d'analyse graphique.
-- ============================================================================

CREATE TABLE IF NOT EXISTS `omni_m3.conversations` (
  conversationId STRING NOT NULL,
  title STRING NOT NULL,
  createdAt TIMESTAMP NOT NULL,
  updatedAt TIMESTAMP NOT NULL,
  author STRING,
  tags ARRAY<STRING>,
  embeddingVector ARRAY<FLOAT64>,
  linkedConversationIds ARRAY<STRING>,
  workspaceId STRING,
  m3TreeNodeId STRING
);

-- Clustering recommande sur workspaceId pour optimiser les requetes
-- analytiques par workspace (ex: nombre de conversations par semaine par auteur).
-- BigQuery gere le stockage en colonnes ; cet ordre de colonnes est documentaire.

-- Exemple de requete analytique (a adapter au projet GCP cible) :
-- SELECT workspaceId, COUNT(*) AS nb_conversations
-- FROM `omni_m3.conversations`
-- WHERE createdAt >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
-- GROUP BY workspaceId;
