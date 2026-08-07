from __future__ import annotations

from harness_probes.application.services.probe_service import ProbeService
from harness_probes.infrastructure.adapters.inbound.cli_adapter import CliAdapter
from harness_probes.infrastructure.adapters.outbound.filesystem_adapter import InMemoryProbeRepository


def build_service() -> ProbeService:
    return ProbeService(out_port=InMemoryProbeRepository())


def build_cli() -> CliAdapter:
    return CliAdapter(service=build_service())


if __name__ == "__main__":
    raise SystemExit(CliAdapter(service=build_service()).execute())

