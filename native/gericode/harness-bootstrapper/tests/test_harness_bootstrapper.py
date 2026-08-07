"""Tests pour harness-bootstrapper."""

from __future__ import annotations

from pathlib import Path
import pytest

from harness_bootstrapper import HarnessBootstrapper, HarnessBootstrapperError


def test_bootstrap_agent(tmp_path):
    agent_path = tmp_path / "my-agent"
    bootstrapper = HarnessBootstrapper(agent_path=agent_path)
    result = bootstrapper.bootstrap(agent_name="my-agent", layer="L4", domain="ecosystem-tools")
    assert result["status"] == "OK"
    assert (agent_path / "domain" / "entities.py").exists()
    assert (agent_path / "application" / "ports" / "in" / "use_cases.py").exists()
    assert (agent_path / "infrastructure" / "adapters" / "out" / "filesystem.py").exists()
    assert (agent_path / "contracts" / "contracts.py").exists()
    assert (agent_path / "tests" / "acceptance" / "features" / "my-agent.feature").exists()


def test_bootstrap_existing_agent(tmp_path):
    agent_path = tmp_path / "my-agent"
    agent_path.mkdir()
    bootstrapper = HarnessBootstrapper(agent_path=agent_path)
    result = bootstrapper.bootstrap(agent_name="my-agent", layer="L4")
    assert result["status"] == "FAILED"
    assert len(result["errors"]) > 0


def test_bootstrap_with_domain(tmp_path):
    agent_path = tmp_path / "my-agent"
    bootstrapper = HarnessBootstrapper(agent_path=agent_path)
    result = bootstrapper.bootstrap(agent_name="my-agent", layer="L4", domain="custom-domain")
    assert result["status"] == "OK"
    assert result["domain"] == "custom-domain"
