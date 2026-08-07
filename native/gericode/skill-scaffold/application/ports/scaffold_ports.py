"""
Hexagonal Ports — skill-scaffold
"""

from typing import Protocol


class IScaffoldBuilderPort(Protocol):
    """Inbound port: scaffold generation."""

    def generate(self, spec: dict) -> dict:
        ...


class ITemplateRepositoryPort(Protocol):
    """Outbound port: template access."""

    def get_template(self, template_name: str) -> str:
        ...
