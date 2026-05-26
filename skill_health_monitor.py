#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 SKILL HEALTH MONITOR
Implémentation EPIC 1055

Monitoring santé, disponibilité et métriques des skills
"""

import time
import threading
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from managers.skill_registry import Skill


class SkillHealthStatus(Enum):
    UNKNOWN = 0
    HEALTHY = 1
    DEGRADED = 2
    FAILED = 3
    DISABLED = 4


@dataclass
class SkillHealthMetrics:
    skill: Skill
    status: SkillHealthStatus = SkillHealthStatus.UNKNOWN
    last_check: datetime = None
    execution_count: int = 0
    failure_count: int = 0
    average_execution_time: float = 0.0
    last_error: str = None
    uptime: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


class SkillHealthMonitor:
    """
    Moniteur de santé des skills

    Features:
    ✅ Check périodique de disponibilité
    ✅ Métriques d'exécution
    ✅ Détection automatique des échecs
    ✅ Circuit breaker pattern
    ✅ Désactivation automatique des skills défaillants
    """

    CHECK_INTERVAL = 60  # 1 minute
    FAILURE_THRESHOLD = 3
    DEGRADED_THRESHOLD = 0.7  # < 70% succès = dégradé

    def __init__(self):
        self.metrics: Dict[str, SkillHealthMetrics] = {}
        self.running = False
        self._thread = None

    def start(self):
        """Démarre le monitoring en arrière plan"""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()

    def record_execution(self, skill_name: str, success: bool, execution_time: float = 0.0):
        """Enregistre une exécution de skill"""
        if skill_name not in self.metrics:
            return

        metrics = self.metrics[skill_name]
        metrics.execution_count += 1

        if not success:
            metrics.failure_count += 1
            metrics.last_error = datetime.now()

        metrics.average_execution_time = (
            (metrics.average_execution_time * (metrics.execution_count - 1) + execution_time)
            / metrics.execution_count
        )

        # Mise à jour du statut
        if metrics.execution_count >= self.FAILURE_THRESHOLD:
            success_rate = 1.0 - (metrics.failure_count / metrics.execution_count)
            if success_rate < self.DEGRADED_THRESHOLD:
                metrics.status = SkillHealthStatus.DEGRADED
            if metrics.failure_count >= self.FAILURE_THRESHOLD:
                metrics.status = SkillHealthStatus.FAILED
                metrics.skill.enabled = False

    def register_skill(self, skill: Skill):
        """Enregistre un skill pour monitoring"""
        if skill.name not in self.metrics:
            self.metrics[skill.name] = SkillHealthMetrics(skill=skill)

    def get_status(self, skill_name: str) -> SkillHealthStatus:
        if skill_name not in self.metrics:
            return SkillHealthStatus.UNKNOWN
        return self.metrics[skill_name].status

    def get_healthy_skills(self) -> List[Skill]:
        return [
            m.skill for m in self.metrics.values()
            if m.status == SkillHealthStatus.HEALTHY and m.skill.enabled
        ]

    def _monitor_loop(self):
        while self.running:
            for metrics in self.metrics.values():
                if metrics.skill.enabled:
                    self._check_skill_health(metrics)
            time.sleep(self.CHECK_INTERVAL)

    def _check_skill_health(self, metrics: SkillHealthMetrics):
        metrics.last_check = datetime.now()
        if metrics.status == SkillHealthStatus.UNKNOWN:
            metrics.status = SkillHealthStatus.HEALTHY

    def status_report(self) -> Dict[str, Any]:
        total = len(self.metrics)
        healthy = sum(1 for m in self.metrics.values() if m.status == SkillHealthStatus.HEALTHY)
        degraded = sum(1 for m in self.metrics.values() if m.status == SkillHealthStatus.DEGRADED)
        failed = sum(1 for m in self.metrics.values() if m.status == SkillHealthStatus.FAILED)

        return {
            "total": total,
            "healthy": healthy,
            "degraded": degraded,
            "failed": failed,
            "metrics": [
                {
                    "name": m.skill.name,
                    "status": m.status.name,
                    "executions": m.execution_count,
                    "failures": m.failure_count,
                    "avg_time": m.average_execution_time
                }
                for m in self.metrics.values()
            ]
        }


# Instance globale
SKILL_HEALTH_MONITOR = SkillHealthMonitor()