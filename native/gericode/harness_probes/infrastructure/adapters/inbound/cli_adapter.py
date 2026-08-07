from __future__ import annotations

from harness_probes.application.services.probe_service import ProbeService


class CliAdapter:
    def __init__(self, service: ProbeService) -> None:
        self._service = service

    def execute(self) -> int:
        results = self._service.run_all()
        for result in results:
            status = "PASS" if result.passed else "FAIL"
            print(f"[{result.probe_id}] {status}: {result.detail}")
        failed = [result for result in results if not result.passed]
        if failed:
            print(f"\nFAILED: {len(failed)} probe(s) failed")
            return 1
        print(f"\nOK: {len(results)} probe(s) passed")
        return 0



