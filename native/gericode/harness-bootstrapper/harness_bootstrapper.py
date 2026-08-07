"""
Harness Bootstrapper
Bootstrap le harness d'agent Hexagonal/DDD/DbC/ATDD/BDD.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


class HarnessBootstrapperError(Exception):
    """Erreur de bootstrap de harness."""


class HarnessBootstrapper:
    def __init__(self, agent_path: Path) -> None:
        self.agent_path = agent_path

    def bootstrap(self, agent_name: str, layer: str = "L4", domain: str = "ecosystem-tools") -> dict:
        """Bootstrap la structure complète de l'agent."""
        result: dict = {
            "agent_name": agent_name,
            "layer": layer,
            "domain": domain,
            "files_created": [],
            "errors": [],
        }

        if self.agent_path.exists():
            result["errors"].append(f"Agent path already exists: {self.agent_path}")
            result["status"] = "FAILED"
            return result

        try:
            # Create directory structure
            dirs = [
                "domain",
                "application/ports/in",
                "application/ports/out",
                "application/services",
                "infrastructure/adapters/in",
                "infrastructure/adapters/out",
                "infrastructure/config",
                "contracts",
                "tests/unit",
                "tests/integration",
                "tests/acceptance",
            ]
            for d in dirs:
                (self.agent_path / d).mkdir(parents=True, exist_ok=True)

            # Create core files
            self._create_file(self.agent_path / "domain" / "entities.py", self._get_entities_template(agent_name))
            self._create_file(self.agent_path / "domain" / "value_objects.py", self._get_value_objects_template())
            self._create_file(self.agent_path / "domain" / "events.py", self._get_events_template())
            self._create_file(self.agent_path / "application" / "ports" / "in" / "use_cases.py", self._get_in_ports_template(agent_name))
            self._create_file(self.agent_path / "application" / "ports" / "out" / "repository.py", self._get_out_ports_template())
            self._create_file(self.agent_path / "application" / "services" / "orchestrator.py", self._get_service_template(agent_name))
            self._create_file(self.agent_path / "infrastructure" / "adapters" / "in" / "cli.py", self._get_in_adapter_template())
            self._create_file(self.agent_path / "infrastructure" / "adapters" / "out" / "filesystem.py", self._get_out_adapter_template())
            self._create_file(self.agent_path / "contracts" / "contracts.py", self._get_contracts_template(agent_name))
            self._create_file(self.agent_path / "tests" / "acceptance" / "features" / f"{agent_name}.feature", self._get_bdd_feature_template(agent_name))

            result["files_created"] = [str(p.relative_to(self.agent_path)) for p in self.agent_path.rglob("*") if p.is_file()]
            result["status"] = "OK"
        except Exception as exc:
            result["errors"].append(str(exc))
            result["status"] = "FAILED"

        return result

    def _create_file(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        logger.info("Created: %s", path)

    def _get_entities_template(self, agent_name: str) -> str:
        return f'''"""
Domain entities for {agent_name}.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class AgentId:
    """Value object: unique agent identifier."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("AgentId cannot be empty")


@dataclass
class Agent:
    """Root entity: Agent."""
    id: AgentId
    name: str
    layer: Literal["L0", "L1", "L2", "L3", "L4", "L5"]
    domain: str
    created_at: datetime
    status: Literal["active", "inactive", "deprecated"] = "active"

    def deactivate(self) -> None:
        """Deactivate the agent."""
        object.__setattr__(self, "status", "inactive")

    def is_active(self) -> bool:
        """Check if agent is active."""
        return self.status == "active"
'''

    def _get_value_objects_template(self) -> str:
        return '''"""
Value objects for the domain.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    """Value object: logical layer."""
    value: str

    def __post_init__(self) -> None:
        valid = {"L0", "L1", "L2", "L3", "L4", "L5"}
        if self.value not in valid:
            raise ValueError(f"Invalid layer: {self.value}. Must be one of {valid}")
'''

    def _get_events_template(self) -> str:
        return '''"""
Domain events.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent:
    """Base domain event."""
    occurred_at: datetime
    aggregate_id: str
    metadata: dict[str, Any] | None = None


@dataclass
class AgentCreated(DomainEvent):
    """Event: agent created."""
    agent_name: str
    layer: str
    domain: str
'''

    def _get_in_ports_template(self, agent_name: str) -> str:
        return f'''"""
Inbound ports (use cases) for {agent_name}.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
from domain.entities import Agent, AgentId
from domain.value_objects import Layer


class IAgentUseCase(ABC):
    """Inbound port: agent use cases."""

    @abstractmethod
    def create_agent(self, name: str, layer: str, domain: str) -> Agent:
        """Create a new agent."""

    @abstractmethod
    def get_agent(self, agent_id: str) -> Agent | None:
        """Get agent by ID."""

    @abstractmethod
    def list_agents(self, layer: str | None = None) -> list[Agent]:
        """List all agents, optionally filtered by layer."""

    @abstractmethod
    def deactivate_agent(self, agent_id: str) -> None:
        """Deactivate an agent."""
'''

    def _get_out_ports_template(self) -> str:
        return '''"""
Outbound ports (repositories) for the domain.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from domain.entities import Agent, AgentId
from domain.value_objects import Layer


class IAgentRepository(ABC):
    """Outbound port: agent persistence."""

    @abstractmethod
    def save(self, agent: Agent) -> None:
        """Save agent."""

    @abstractmethod
    def get_by_id(self, agent_id: str) -> Agent | None:
        """Get agent by ID."""

    @abstractmethod
    def list_all(self, layer: str | None = None) -> list[Agent]:
        """List all agents."""

    @abstractmethod
    def delete(self, agent_id: str) -> None:
        """Delete agent."""
'''

    def _get_service_template(self, agent_name: str) -> str:
        return f'''"""
Application service: orchestrates use cases.
"""

from __future__ import annotations

from datetime import datetime
from domain.entities import Agent, AgentId
from domain.value_objects import Layer
from application.ports.in import IAgentUseCase
from application.ports.out import IAgentRepository


class AgentService(IAgentUseCase):
    """Service: implements agent use cases."""

    def __init__(self, repository: IAgentRepository) -> None:
        self._repository = repository

    def create_agent(self, name: str, layer: str, domain: str) -> Agent:
        """Create a new agent."""
        agent = Agent(
            id=AgentId(value=name.lower().replace(" ", "-")),
            name=name,
            layer=layer,
            domain=domain,
            created_at=datetime.utcnow(),
            status="active",
        )
        self._repository.save(agent)
        return agent

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get agent by ID."""
        return self._repository.get_by_id(agent_id)

    def list_agents(self, layer: str | None = None) -> list[Agent]:
        """List all agents."""
        return self._repository.list_all(layer)

    def deactivate_agent(self, agent_id: str) -> None:
        """Deactivate an agent."""
        agent = self._repository.get_by_id(agent_id)
        if agent:
            agent.deactivate()
            self._repository.save(agent)
'''

    def _get_in_adapter_template(self) -> str:
        return '''"""
Inbound adapter: CLI interface.
"""

from __future__ import annotations

import sys
from typing import Any
from application.services.orchestrator import AgentService
from application.ports.out import IAgentRepository


class CLIAdapter:
    """Inbound adapter: CLI interface."""

    def __init__(self, service: AgentService) -> None:
        self._service = service

    def handle_command(self, command: str, args: list[str]) -> int:
        """Handle CLI command."""
        if command == "create":
            if len(args) < 3:
                print("Usage: create <name> <layer> <domain>")
                return 1
            agent = self._service.create_agent(args[0], args[1], args[2])
            print(f"Created: {{agent.id.value}}")
            return 0
        elif command == "list":
            agents = self._service.list_agents()
            for a in agents:
                print(f"- {{a.id.value}} ({{a.layer}}) {{a.status}}")
            return 0
        else:
            print(f"Unknown command: {{command}}")
            return 1
'''

    def _get_out_adapter_template(self) -> str:
        return '''"""
Outbound adapter: filesystem persistence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from domain.entities import Agent, AgentId
from domain.value_objects import Layer
from application.ports.out import IAgentRepository


class FilesystemAgentRepository(IAgentRepository):
    """Outbound adapter: filesystem persistence."""

    def __init__(self, storage_path: Path) -> None:
        self._storage_path = storage_path
        self._storage_path.mkdir(parents=True, exist_ok=True)

    def save(self, agent: Agent) -> None:
        """Save agent to filesystem."""
        file_path = self._storage_path / f"{{agent.id.value}}.json"
        data = {{
            "id": agent.id.value,
            "name": agent.name,
            "layer": agent.layer,
            "domain": agent.domain,
            "created_at": agent.created_at.isoformat(),
            "status": agent.status,
        }}
        file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_by_id(self, agent_id: str) -> Agent | None:
        """Get agent by ID."""
        file_path = self._storage_path / f"{{agent_id}}.json"
        if not file_path.exists():
            return None
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return Agent(
            id=AgentId(value=data["id"]),
            name=data["name"],
            layer=data["layer"],
            domain=data["domain"],
            created_at=datetime.fromisoformat(data["created_at"]),
            status=data["status"],
        )

    def list_all(self, layer: str | None = None) -> list[Agent]:
        """List all agents."""
        agents = []
        for file_path in self._storage_path.glob("*.json"):
            agent = self.get_by_id(file_path.stem)
            if agent and (layer is None or agent.layer == layer):
                agents.append(agent)
        return agents

    def delete(self, agent_id: str) -> None:
        """Delete agent."""
        file_path = self._storage_path / f"{{agent_id}}.json"
        if file_path.exists():
            file_path.unlink()
'''

    def _get_contracts_template(self, agent_name: str) -> str:
        return f'''"""
Design by Contract contracts for {agent_name}.
"""

from __future__ import annotations

from typing import Any


def require(condition: bool, message: str) -> None:
    """Precondition: raise if condition is False."""
    if not condition:
        raise ValueError(f"Precondition failed: {{message}}")


def ensure(condition: bool, message: str) -> None:
    """Postcondition: raise if condition is False."""
    if not condition:
        raise ValueError(f"Postcondition failed: {{message}}")


def invariant(condition: bool, message: str) -> None:
    """Invariant: raise if condition is False."""
    if not condition:
        raise ValueError(f"Invariant failed: {{message}}")


# Example contracts
AGENT_NAME_CONTRACT = {{
    "min_length": 1,
    "max_length": 100,
    "pattern": r"^[a-zA-Z0-9_-]+$",
}}

LAYER_CONTRACT = {{
    "valid_values": {{"L0", "L1", "L2", "L3", "L4", "L5"}},
}}
'''

    def _get_bdd_feature_template(self, agent_name: str) -> str:
        return f'''Feature: {agent_name}
  As a user
  I want to interact with the agent
  So that I can manage agents

  Scenario: Create a new agent
    Given the agent service is available
    When I create an agent named "TestAgent" in layer "L4"
    Then the agent should be created successfully
    And the agent status should be "active"

  Scenario: List all agents
    Given there are 2 agents
    When I list all agents
    Then I should see 2 agents

  Scenario: Deactivate an agent
    Given an agent "TestAgent" exists
    When I deactivate the agent
    Then the agent status should be "inactive"
'''
