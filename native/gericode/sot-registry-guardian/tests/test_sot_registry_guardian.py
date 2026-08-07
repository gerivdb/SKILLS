"""Tests pour sot-registry-guardian."""

from __future__ import annotations

import pytest

from sot_registry_guardian import SOTGuardian, SOTGuardianError


def test_approved_channel_passes(tmp_path):
    guardian = SOTGuardian(tmp_path / "known_repositories.yaml")
    guardian.check_write("test-caller", "yaml-safe-injector")
    assert len(guardian.audit()) == 1
    assert guardian.audit()[0]["allowed"] is True


def test_unknown_channel_blocked(tmp_path):
    guardian = SOTGuardian(tmp_path / "known_repositories.yaml")
    with pytest.raises(SOTGuardianError):
        guardian.check_write("test-caller", "unknown-channel")


def test_audit_log(tmp_path):
    guardian = SOTGuardian(tmp_path / "known_repositories.yaml")
    guardian.check_write("caller-a", "yaml-safe-injector")
    guardian.check_write("caller-b", "verse_mapping")
    audit = guardian.audit()
    assert len(audit) == 2
    assert audit[0]["caller"] == "caller-a"
    assert audit[1]["channel"] == "verse_mapping"
