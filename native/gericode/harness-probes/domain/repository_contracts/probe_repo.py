from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO


class ProbeRepositoryContract(ABC):
    @abstractmethod
    def save(self, result: ProbeResultVO) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_recent(self, limit: int = 20) -> Iterable[ProbeResultVO]:
        raise NotImplementedError
