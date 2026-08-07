from __future__ import annotations

from harness_probes.application.services.probe_service import ProbeService
from harness_probes.infrastructure.adapters.out.filesystem_adapter import InMemoryProbeRepository


def test_probe_service_returns_results():
    service = ProbeService(out_port=InMemoryProbeRepository())
    results = service.run_all()
    assert len(results) == 11
    assert all(result.probe_id.startswith("P-") for result in results)
