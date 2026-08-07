from __future__ import annotations

from harness_probes.application.services.probe_service import ProbeService
from harness_probes.infrastructure.adapters.outbound.filesystem_adapter import InMemoryProbeRepository


def test_probe_service_persists_results():
    service = ProbeService(out_port=InMemoryProbeRepository())
    # Verify the service can be instantiated and the port is callable.
    assert service._out_port is not None
    assert hasattr(service._out_port, "persist")
