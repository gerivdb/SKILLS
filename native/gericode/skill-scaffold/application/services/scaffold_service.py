"""
Hexagonal Adapters — skill-scaffold
"""

from typing import Protocol


class ScaffoldBuilderService:
    """Application service orchestrating scaffold generation."""

    def __init__(self) -> None:
        self._files: dict[str, str] = {}

    def add_file(self, path: str, content: str) -> None:
        self._files[path] = content

    def generate(self, spec: dict) -> dict:
        return {
            "skill": spec.get("name", "unknown"),
            "files": list(self._files.keys()),
        }


class CLIScaffoldAdapter:
    """CLI adapter for skill-scaffold."""

    def execute(self, command: str, payload: dict) -> dict:
        if command == "generate":
            service = ScaffoldBuilderService()
            for file_info in payload.get("files", []):
                service.add_file(file_info["path"], file_info["content"])
            return service.generate(payload)
        raise ValueError(f"Unknown command: {command}")
