# m3-liaison-agent — tests unitaires de l'agent de liaison proactif
import threading
import time

from active_registry import ActiveConversationRegistry
from message_bus import MessageBus
from liaison_agent import LiaisonAgent, spawn_agent


def test_registry_register_and_expire():
    reg = ActiveConversationRegistry(default_ttl_seconds=1)
    reg.register("conv-1", "ws-A", ttl_seconds=1)
    assert reg.is_active("conv-1")
    time.sleep(1.2)
    assert not reg.is_active("conv-1")
    removed = reg.cleanup_expired()
    assert "conv-1" in removed
    print("OK test_registry_register_and_expire")


def test_registry_unregister():
    reg = ActiveConversationRegistry()
    reg.register("conv-2", "ws-B")
    assert reg.is_active("conv-2")
    assert reg.unregister("conv-2")
    assert not reg.is_active("conv-2")
    assert not reg.unregister("conv-2")  # déjà supprimé
    print("OK test_registry_unregister")


def test_registry_list_active():
    reg = ActiveConversationRegistry(default_ttl_seconds=60)
    reg.register("conv-a", "ws-1")
    reg.register("conv-b", "ws-2")
    active = reg.list_active()
    assert len(active) == 2
    ids = {e["conversation_id"] for e in active}
    assert ids == {"conv-a", "conv-b"}
    print("OK test_registry_list_active")


def test_bus_publish_subscribe():
    bus = MessageBus()
    received = []

    def cb(msg):
        received.append(msg)

    bus.subscribe("conv-x", cb)
    bus.publish("conv-x", {"event": "ping", "data": 1})
    assert len(received) == 1
    assert received[0]["event"] == "ping"
    assert bus.subscriber_count("conv-x") == 1

    bus.unsubscribe("conv-x")
    bus.publish("conv-x", {"event": "pong"})
    assert len(received) == 1  # aucun nouveau
    assert bus.subscriber_count("conv-x") == 0
    print("OK test_bus_publish_subscribe")


def test_bus_drain():
    bus = MessageBus()
    bus.subscribe("conv-d", lambda m: None)
    bus.publish("conv-d", {"msg": 1})
    bus.publish("conv-d", {"msg": 2})
    drained = bus.drain("conv-d")
    assert len(drained) == 2
    assert bus.drain("conv-d") == []  # file vidée
    print("OK test_bus_drain")


def test_agent_lifecycle():
    reg = ActiveConversationRegistry(default_ttl_seconds=60)
    bus = MessageBus()
    agent = LiaisonAgent(
        conversation_id="conv-agent",
        workspace_id="ws-agent",
        registry=reg,
        bus=bus,
        ttl_seconds=60,
    )
    info = agent.start()
    assert info["status"] == "active"
    assert info["conversation_id"] == "conv-agent"
    assert reg.is_active("conv-agent")
    assert bus.subscriber_count("conv-agent") == 1

    # message entrant via le bus
    received = []
    bus.subscribe("conv-agent", received.append)
    bus.publish("conv-agent", {"event": "test", "target_conversation_id": "conv-agent"})
    assert len(received) == 1
    assert received[0]["event"] == "test"

    death = agent.stop()
    assert death["event"] == "agent_death"
    assert not reg.is_active("conv-agent")
    assert bus.subscriber_count("conv-agent") == 0
    print("OK test_agent_lifecycle")


def test_spawn_agent():
    reg = ActiveConversationRegistry(default_ttl_seconds=60)
    bus = MessageBus()
    agent = spawn_agent(
        conversation_id="conv-spawn",
        workspace_id="ws-spawn",
        registry=reg,
        bus=bus,
        ttl_seconds=60,
    )
    assert isinstance(agent, LiaisonAgent)
    assert agent.conversation_id == "conv-spawn"
    assert reg.is_active("conv-spawn")
    agent.stop()
    print("OK test_spawn_agent")


def test_agent_expired():
    reg = ActiveConversationRegistry(default_ttl_seconds=60)
    bus = MessageBus()
    agent = LiaisonAgent(
        conversation_id="conv-exp",
        workspace_id="ws-exp",
        registry=reg,
        bus=bus,
        ttl_seconds=0,  # expiré immédiatement
    )
    time.sleep(0.01)  # laisser passer au moins une milliseconde
    assert agent.is_expired()
    print("OK test_agent_expired")


if __name__ == "__main__":
    test_registry_register_and_expire()
    test_registry_unregister()
    test_registry_list_active()
    test_bus_publish_subscribe()
    test_bus_drain()
    test_agent_lifecycle()
    test_spawn_agent()
    test_agent_expired()
    print("Tous les tests unitaires m3-liaison-agent passés.")
