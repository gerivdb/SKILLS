"""
m3-liaison-agent — Registre des conversations actives.

Suit quelles conversations NotebookLM sont actuellement ouvertes et en cours
d'utilisation. Associe un TTL à chaque entrée pour le nettoyage automatique
des conversations fermées ou abandonnées.
"""

import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional


class ActiveConversationRegistry:
    """Registre thread-safe des conversations actives avec TTL."""

    def __init__(self, default_ttl_seconds: int = 3600):
        self._lock = threading.RLock()
        self._default_ttl = default_ttl_seconds
        # conversation_id -> {workspace_id, registered_at, expires_at, metadata}
        self._entries: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        conversation_id: str,
        workspace_id: str,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Enregistre (ou réactive) une conversation comme active."""
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        now = datetime.now(timezone.utc)
        with self._lock:
            self._entries[conversation_id] = {
                "conversation_id": conversation_id,
                "workspace_id": workspace_id,
                "registered_at": now.isoformat(),
                "expires_at": (now + timedelta(seconds=ttl)).isoformat(),
                "ttl_seconds": ttl,
                "metadata": metadata or {},
            }

    def unregister(self, conversation_id: str) -> bool:
        """Supprime une conversation du registre (fermeture explicite)."""
        with self._lock:
            if conversation_id in self._entries:
                del self._entries[conversation_id]
                return True
            return False

    def is_active(self, conversation_id: str) -> bool:
        """Vérifie si une conversation est encore active (pas expirée)."""
        with self._lock:
            entry = self._entries.get(conversation_id)
            if entry is None:
                return False
            expires = datetime.fromisoformat(entry["expires_at"])
            return datetime.now(timezone.utc) < expires

    def list_active(self) -> List[Dict[str, Any]]:
        """Liste toutes les conversations actives non expirées."""
        with self._lock:
            now = datetime.now(timezone.utc)
            active = []
            for cid, entry in self._entries.items():
                expires = datetime.fromisoformat(entry["expires_at"])
                if now < expires:
                    active.append(
                        {
                            "conversation_id": cid,
                            "workspace_id": entry["workspace_id"],
                            "registered_at": entry["registered_at"],
                            "expires_at": entry["expires_at"],
                            "ttl_seconds": entry["ttl_seconds"],
                        }
                    )
            return sorted(active, key=lambda x: x["registered_at"])

    def cleanup_expired(self) -> List[str]:
        """Supprime les entrées expirées et retourne leurs IDs."""
        removed: List[str] = []
        with self._lock:
            now = datetime.now(timezone.utc)
            expired = [
                cid
                for cid, entry in self._entries.items()
                if now >= datetime.fromisoformat(entry["expires_at"])
            ]
            for cid in expired:
                del self._entries[cid]
                removed.append(cid)
            return removed

    def count(self) -> int:
        """Nombre de conversations actives."""
        with self._lock:
            return len(self._entries)
