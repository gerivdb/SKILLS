"""
Hexagonal Ports — sot-registry-guardian
"""

from typing import Protocol


class IRegistryValidatorPort(Protocol):
    """Inbound port: registry validation."""

    def validate_repo(self, full_name: str, local_path: str, layer: str) -> dict:
        ...


class ISOTRepositoryPort(Protocol):
    """Outbound port: SOT repository access."""

    def read(self) -> str:
        ...

    def write(self, content: str) -> None:
        ...
