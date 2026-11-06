"""
m3-liaison-agent — Bus de messages pub/sub inter-conversations.

Canal de diffusion des mises à jour entre les agents de liaison. Chaque
conversation dispose d'un file de messages ; les agents publient et
souscrivent pour relayer les changements de façon découplée.
"""

import queue
import threading
from typing import Any, Callable, Dict, List


class MessageBus:
    """Bus pub/sub thread-safe pour la diffusion inter-conversations."""

    def __init__(self):
        self._lock = threading.RLock()
        # conversation_id -> liste de callbacks abonnés
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        # conversation_id -> file de messages en attente
        self._queues: Dict[str, queue.Queue] = {}

    def subscribe(
        self, conversation_id: str, callback: Callable[[Dict[str, Any]], None]
    ) -> None:
        """Abonne un callback à une conversation."""
        with self._lock:
            self._subscribers.setdefault(conversation_id, []).append(callback)
            if conversation_id not in self._queues:
                self._queues[conversation_id] = queue.Queue()

    def unsubscribe(self, conversation_id: str) -> None:
        """Désabonne tous les callbacks d'une conversation."""
        with self._lock:
            self._subscribers.pop(conversation_id, None)
            self._queues.pop(conversation_id, None)

    def publish(self, conversation_id: str, message: Dict[str, Any]) -> None:
        """Publie un message destiné à une conversation."""
        with self._lock:
            callbacks = list(self._subscribers.get(conversation_id, []))
            q = self._queues.get(conversation_id)
        # Envoi hors verrou pour éviter les blocages longs
        for cb in callbacks:
            try:
                cb(message)
            except Exception:  # pragma: no cover - callback utilisateur
                pass
        if q is not None:
            q.put(message)

    def drain(self, conversation_id: str, timeout: float = 0.1) -> List[Dict[str, Any]]:
        """Vide la file de messages d'une conversation (non bloquant)."""
        messages: List[Dict[str, Any]] = []
        with self._lock:
            q = self._queues.get(conversation_id)
        if q is None:
            return messages
        while True:
            try:
                messages.append(q.get(timeout=timeout))
            except queue.Empty:
                break
        return messages

    def subscriber_count(self, conversation_id: str) -> int:
        """Nombre d'abonnés pour une conversation."""
        with self._lock:
            return len(self._subscribers.get(conversation_id, []))
