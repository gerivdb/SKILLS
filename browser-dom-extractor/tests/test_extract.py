import pytest
from extract_keep_dom import extract_from_cdp

def test_cdp_not_running():
    # Doit quitter avec le code 1 si le port est fermé
    with pytest.raises(SystemExit) as exc:
        extract_from_cdp(9999, "https://keep.google.com", "body")
    assert exc.value.code == 1
