# Tests de fumée (smoke tests) pour browser-cdp-controller v2

"""Tests de base validant l'import et la disponibilité des primitives."""
import pytest

def test_import_module():
    """Vérifie que browser_controller s'importe sans erreur."""
    import browser_controller
    assert hasattr(browser_controller, "get_axtree")
    assert hasattr(browser_controller, "capture_storage_state")
    assert hasattr(browser_controller, "launch_chromium")

@pytest.mark.asyncio
async def test_get_axtree_returns_dict():
    """AXTree sur about:blank retourne un dict avec clé 'nodes'."""
    pytest.skip("requires CDP port 9222")

@pytest.mark.asyncio
async def test_capture_storage_state_creates_file(tmp_path):
    """capture_storage_state écrit un JSON avec 'version', 'cookies_meta', 'origins_meta'."""
    pytest.skip("requires CDP port 9222")