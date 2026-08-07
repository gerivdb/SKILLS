"""
Hexagonal Ports — yaml-safe-injector
"""

from typing import Protocol


class IYamlInjectorPort(Protocol):
    """Inbound port: YAML injection use case."""

    def inject(
        self,
        target_path: str,
        updates: dict,
        repo_name: str,
        dry_run: bool = False,
    ) -> tuple[str, str]:
        ...


class IFileSystemPort(Protocol):
    """Outbound port: filesystem abstraction."""

    def read(self, path: str) -> str:
        ...

    def write(self, path: str, content: str) -> None:
        ...

    def exists(self, path: str) -> bool:
        ...
