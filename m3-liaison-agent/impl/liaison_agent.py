"""
m3-liaison-agent — Agent de liaison temporaire et proactif.

Spawné à l'ouverture d'une conversation NotebookLM. Son rôle :
- Surveiller la conversation source (détection de modifications).
- Détecter les conversations liées via le graphe CASIS.
- Relayer les mises à jour de la conversation source vers les conversations liées.
- Relayer les mises à jour des conversations liées vers la source.
- S'auto-détruire à la fermeture de la conversation ou à l'expiration du TTL.

Cycle de vie : spawn (ouverture) → surveillance continue → destroy (fermeture/TTL).
"""

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Dict, List, Optional

from active_registry import ActiveConversationRegistry
from message_bus import MessageBus


class LiaisonAgent:
    """Agent de liaison éphémère pour une conversation NotebookLM."""

    def __init__(
        self,
        conversation_id: str,
        workspace_id: str,
        registry: ActiveConversationRegistry,
        bus: MessageBus,
        ttl_seconds: int = 3600,
        poll_interval: int = 30,
    ):
        self.agent_id = f"liaison-{uuid.uuid4().hex[:8]}"
        self.conversation_id = conversation_id
        self.workspace_id = workspace_id
        self.registry = registry
        self.bus = bus
        self.ttl_seconds = ttl_seconds
        self.poll_interval = poll_interval
        self.started_at = datetime.now(timezone.utc)
        self.last_activity_at = self.started_at
        self.running = False
        self._linked_conversations: List[str] = []

    # ------------------------------------------------------------------ #
    # Cycle de vie
    # ------------------------------------------------------------------ #

    def start(self) -> Dict[str, Any]:
        """Démarre l'agent : enregistrement, souscription, publication de naissance."""
        self.running = True
        self.registry.register(
            self.conversation_id, self.workspace_id, self.ttl_seconds
        )
        self.bus.subscribe(self.conversation_id, self._on_inbound_message)

        birth = {
            "agent_id": self.agent_id,
            "conversation_id": self.conversation_id,
            "workspace_id": self.workspace_id,
            "event": "agent_birth",
            "timestamp": self.started_at.isoformat(),
        }
        self.bus.publish(self.conversation_id, birth)

        self._refresh_links()
        return {
            "agent_id": self.agent_id,
            "conversation_id": self.conversation_id,
            "status": "active",
            "linked_conversations": self._linked_conversations,
        }

    def stop(self) -> Dict[str, Any]:
        """Arrêt propre : désenregistrement, désabonnement, publication de mort."""
        self.running = False
        death = {
            "agent_id": self.agent_id,
            "conversation_id": self.conversation_id,
            "event": "agent_death",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": (
                datetime.now(timezone.utc) - self.started_at
            ).total_seconds(),
        }
        self.bus.publish(self.conversation_id, death)
        self.bus.unsubscribe(self.conversation_id)
        self.registry.unregister(self.conversation_id)
        return death

    def is_expired(self) -> bool:
        """Vérifie si le TTL de l'agent est dépassé."""
        return (
            datetime.now(timezone.utc) - self.started_at
        ).total_seconds() > self.ttl_seconds

    # ------------------------------------------------------------------ #
    # Surveillance et détection de liens
    # ------------------------------------------------------------------ #

    def _refresh_links(self) -> None:
        """Détecte les conversations liées via le graphe CASIS (TQL)."""
        # TQL : trouver toutes les conversations ayant un edge avec self.conversation_id
        # Dans l'implémentation simplifiée, on interroge le registre/graph via le bus.
        query = {
            "op": "filter",
            "link_type": None,  # tous les types de lien
        }
        # Les liens réels sont résolus via le graphe CASIS (skill m3-casis-intercharts).
        # Ici on garde une liste vide à remplir par une intégration réelle.
        self._linked_conversations = []

    def detect_modification(self) -> Optional[Dict[str, Any]]:
        """
        Détecte une modification sur la conversation source.
        Retourne un payload de mise à jour ou None si rien de nouveau.
        À connecter à un webhook GAS ou un polling réel sur l'API NotebookLM.
        """
        # Stub : dans l'implémentation réelle, interroger l'API NotebookLM
        # pour vérifier si updatedAt a changé depuis last_activity_at.
        now = datetime.now(timezone.utc)
        self.last_activity_at = now
        return None

    # ------------------------------------------------------------------ #
    # Relai de messages
    # ------------------------------------------------------------------ #

    def _on_inbound_message(self, message: Dict[str, Any]) -> None:
        """Réception d'un message destiné à cette conversation depuis le bus."""
        if message.get("target_conversation_id") == self.conversation_id:
            # Relayer le contenu vers la conversation cible (stub : log + bus)
            print(
                f"[LIAISON {self.agent_id}] Message entrant pour "
                f"{self.conversation_id}: {message.get('event')}"
            )

    def relay_update(
        self, target_conversation_id: str, update: Dict[str, Any]
    ) -> None:
        """Pousse une mise à jour vers une conversation liée via le bus."""
        payload = {
            "agent_id": self.agent_id,
            "source_conversation_id": self.conversation_id,
            "target_conversation_id": target_conversation_id,
            "update": update,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.bus.publish(target_conversation_id, payload)

    # ------------------------------------------------------------------ #
    # Boucle principale (à exécuter dans un thread/process séparé)
    # ------------------------------------------------------------------ #

    def run_loop(self, max_iterations: Optional[int] = None) -> int:
        """
        Boucle de surveillance de l'agent.
        Retourne 0 si arrêt propre, 2 si erreur.
        """
        iteration = 0
        try:
            while self.running:
                if max_iterations is not None and iteration >= max_iterations:
                    break
                if self.is_expired():
                    print(
                        f"[LIAISON {self.agent_id}] TTL expiré, auto-destruction."
                    )
                    self.stop()
                    return 0

                update = self.detect_modification()
                if update:
                    for target in self._linked_conversations:
                        self.relay_update(target, update)

                time.sleep(self.poll_interval)
                iteration += 1
        except KeyboardInterrupt:
            self.stop()
            return 0
        except Exception as exc:  # pragma: no cover
            print(f"[LIAISON {self.agent_id}] ERREUR: {exc}", file=sys.stderr)
            return 2
        self.stop()
        return 0


def spawn_agent(
    conversation_id: str,
    workspace_id: str,
    registry: ActiveConversationRegistry,
    bus: MessageBus,
    ttl_seconds: int = 3600,
) -> LiaisonAgent:
    """Factory : crée et démarre un agent de liaison."""
    agent = LiaisonAgent(
        conversation_id=conversation_id,
        workspace_id=workspace_id,
        registry=registry,
        bus=bus,
        ttl_seconds=ttl_seconds,
    )
    agent.start()
    return agent


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Agent de liaison proactif pour conversation NotebookLM"
    )
    parser.add_argument("--conversation-id", required=True)
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--ttl", type=int, default=3600, help="TTL en secondes")
    parser.add_argument(
        "--poll-interval", type=int, default=30, help="Intervalle de polling en s"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=None, help="Itérations max (test)"
    )
    args = parser.parse_args(argv)

    registry = ActiveConversationRegistry()
    bus = MessageBus()

    agent = spawn_agent(
        conversation_id=args.conversation_id,
        workspace_id=args.workspace_id,
        registry=registry,
        bus=bus,
        ttl_seconds=args.ttl,
    )
    print(
        f"[LIAISON] Agent {agent.agent_id} spawné pour {args.conversation_id}"
    )
    return agent.run_loop(max_iterations=args.max_iterations)


if __name__ == "__main__":
    sys.exit(main())
