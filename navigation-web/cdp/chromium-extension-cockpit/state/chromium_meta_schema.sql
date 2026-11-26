-- =============================================================================
-- Chromium Control Plane (CCP) — Schéma relationnel unifié
-- Fichier : state/chromium_meta_schema.sql
--
-- Tables :
--   - extensions        : inventaire des extensions Chromium (slug, version, statut, commit git...)
--   - daemon_bridges    : dépendances vers des daemons locaux (ports 8810, 19988, 8244...)
--   - telemetry_events  : flux append-only d'événements CDP (console, network, runtime)
--   - snapshots         : instantanés d'état chrome.storage.local pour time-travel debug
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -------------------------------------------------------------
-- Table : extensions
-- Inventaire canonique des extensions Chromium du métacluster.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS extensions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT NOT NULL UNIQUE,            -- identifiant court (browse, sidekeep-x...)
    manifest_path   TEXT NOT NULL,                   -- chemin absolu vers manifest.json sur disque
    git_repo        TEXT NOT NULL,                   -- dépôt git propriétaire (ENV3-repo, DEEP-X...)
    git_commit      TEXT,                            -- dernier commit connu du manifest
    version         TEXT,                            -- version déclarée dans le manifest
    is_unpacked     INTEGER DEFAULT 1,               -- 1 = extension chargée en mode unpacké
    status          TEXT DEFAULT 'disabled',         -- active / disabled / unknown
    auto_reload     INTEGER DEFAULT 0,               -- 1 = rechargement HMR autorisé
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_extensions_slug ON extensions(slug);
CREATE INDEX IF NOT EXISTS idx_extensions_status ON extensions(status);

-- -------------------------------------------------------------
-- Table : daemon_bridges
-- Dépendances réseau locales par extension (pont 8810, relais 19988...)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daemon_bridges (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    extension_id    INTEGER NOT NULL,
    port            INTEGER NOT NULL,
    protocol        TEXT NOT NULL DEFAULT 'ws',      -- ws / http / tcp
    expected_status INTEGER DEFAULT 200,             -- code HTTP attendu en bonne santé
    fail_policy     TEXT NOT NULL DEFAULT 'fail-silent', -- fail-silent / mock / alert
    description     TEXT,
    FOREIGN KEY (extension_id) REFERENCES extensions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_daemon_bridges_ext ON daemon_bridges(extension_id);
CREATE INDEX IF NOT EXISTS idx_daemon_bridges_port ON daemon_bridges(port);

-- -------------------------------------------------------------
-- Table : telemetry_events
-- Flux append-only d'événements CDP (console.error, network, runtime).
-- Alimenté par un démon d'ingestion en flux continu (palier P2).
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS telemetry_events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    extension_id    INTEGER,
    source          TEXT NOT NULL,                   -- console / network / runtime / storage
    level           TEXT NOT NULL,                   -- error / warning / info / debug
    message         TEXT NOT NULL,
    stack_trace     TEXT,
    resolved        INTEGER DEFAULT 0,               -- 0 = ouvert / 1 = résolu
    FOREIGN KEY (extension_id) REFERENCES extensions(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_telemetry_ts ON telemetry_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_ext ON telemetry_events(extension_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_level ON telemetry_events(level);
CREATE INDEX IF NOT EXISTS idx_telemetry_resolved ON telemetry_events(resolved);

-- -------------------------------------------------------------
-- Table : snapshots
-- Instantanés d'état chrome.storage.local pour time-travel debug.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    extension_id    INTEGER NOT NULL,
    timestamp       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    label           TEXT,                              -- libellé optionnel (ex: "avant-reload-v1.0.2")
    storage_json    TEXT NOT NULL,                     -- dump JSON de chrome.storage.local
    FOREIGN KEY (extension_id) REFERENCES extensions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_snapshots_ext ON snapshots(extension_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_ts ON snapshots(timestamp);

-- -------------------------------------------------------------
-- Vue : santé synthétique par extension
-- -------------------------------------------------------------
CREATE VIEW IF NOT EXISTS extension_health AS
SELECT
    e.id,
    e.slug,
    e.version,
    e.status,
    e.auto_reload,
    COUNT(t.id) AS error_count,
    SUM(CASE WHEN t.level = 'error' AND t.resolved = 0 THEN 1 ELSE 0 END) AS unresolved_errors
FROM extensions e
LEFT JOIN telemetry_events t ON t.extension_id = e.id
GROUP BY e.id;
