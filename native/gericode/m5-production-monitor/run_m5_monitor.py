"""M5 Production Monitor runner."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

repo_module = importlib.import_module("domain.repository_contracts.m5_production_monitor_repo")
M5MonitorRepositoryContract = repo_module.M5MonitorRepositoryContract

cli_module = importlib.import_module("infrastructure.adapters.in.m5_production_monitor_ports")
M5MonitorCLIAdapter = cli_module.M5MonitorCLIAdapter

fs_module = importlib.import_module("infrastructure.adapters.out.m5_production_monitor_ports")
M5MonitorFilesystemAdapter = fs_module.M5MonitorFilesystemAdapter

service_module = importlib.import_module("application.services.m5_monitor_service")
M5MonitorService = service_module.M5MonitorService

usecase_module = importlib.import_module("application.services.m5_monitor_usecase")
M5MonitorUseCase = usecase_module.M5MonitorUseCase


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="M5 Production Monitor")
    parser.add_argument("registry_path", type=Path, help="Path to concept registry")
    parser.add_argument("--threshold", type=float, default=0.7, help="Maturity threshold")
    parser.add_argument("--base-path", type=Path, default=Path(".m5"), help="Base path for persistence")
    args = parser.parse_args(argv)

    repo = M5MonitorFilesystemAdapter(args.base_path)
    service = M5MonitorService(None, repo)  # type: ignore[arg-type]
    usecase = M5MonitorUseCase(repo, service=service)

    result = usecase.execute(
        {
            "concept_registry_path": str(args.registry_path),
            "m5_threshold": args.threshold,
        }
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    print(f"Total concepts: {result['report']['total']}")
    print(f"Ready for integration: {result['ready_for_integration_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
