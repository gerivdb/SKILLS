"""Tests du separateur de prefixes BRGS (Option B) - ADR-2026-10-12-001.

La politique SOT approuvee fournit `allowed_branch_prefixes` NUS (`feat` sans
slash) ; `pre-push` retirait en plus le slash (`${p%/}`). Resultat : `feat`
matchait `feature-x` - le garde laissait passer des branches hors routage.

Correctif minimal (hors SOT) :
  * `generate_rules.py` normalise tout prefixe non-trunk AVEC slash final ;
  * `pre-push` Guard 4 ne retire plus le slash.

Ces tests verrouillent la normalisation et la table de verite du separateur.
La logique de matching reproduit `pre-push` Guard 4 : `case branch in ${p}*)`
== `fnmatch(branch, p + "*")`.

IntentHash: 0xBRG_separator_lot2_20261012
"""

import fnmatch
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPO_ROOT / ".githooks" / "generate_rules.py"

# Manifeste dont la route expose des prefixes NUS (comme la politique approuvee).
MANIFEST_BARE = """\
branch_routing:
  repositories:
    main:
      role: critical
    "feat/*":
      role: development
      allowed_branch_prefixes: [chore, ci, docs, feat, fix]
    "fix/*":
      role: development
"""

# Manifeste sans allowed_branch_prefixes -> chemin de derivation (key[:-2]).
MANIFEST_DERIVED = """\
branch_routing:
  repositories:
    main:
      role: critical
    "feat/*":
      role: development
    "fix/*":
      role: development
    "ci/*":
      role: cicd
"""


def _load_generator():
    spec = importlib.util.spec_from_file_location("gen_under_test", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gen():
    return _load_generator()


def _vars(gen, tmp_path, repo_name, manifest):
    mf = tmp_path / "m.yaml"
    mf.write_text(manifest, encoding="utf-8")
    out = tmp_path / "r.sh"
    gen.generate_rules(str(mf), repo_name, str(out))
    data = {}
    for line in out.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        data[key.strip()] = val.strip().strip('"')
    return data


def _passes(branch, prefixes):
    """Miroir de Guard 4 (post-correctif): trunk skip + `case branch in ${p}*`."""
    if branch in ("main", "dev", "develop", "master"):
        return True
    return any(p and fnmatch.fnmatchcase(branch, p + "*") for p in prefixes)


# ---------------------------------------------------------------------------
# Normalisation du separateur
# ---------------------------------------------------------------------------

def test_bare_prefixes_become_slashed(gen, tmp_path):
    ps = _vars(gen, tmp_path, "feat/x", MANIFEST_BARE)["ALLOWED_PREFIXES"].split("|")
    for want in ("feat/", "fix/", "ci/", "chore/", "docs/"):
        assert want in ps, f"prefixe slashe manquant : {want}"
    for bare in ("feat", "fix", "ci", "chore", "docs"):
        assert bare not in ps, f"prefixe nu residuel : {bare}"


def test_derived_prefixes_become_slashed(gen, tmp_path):
    ps = _vars(gen, tmp_path, "GATEWAY-MANAGER", MANIFEST_DERIVED)["ALLOWED_PREFIXES"].split("|")
    for want in ("feat/", "fix/", "ci/"):
        assert want in ps
    assert "feat" not in ps and "fix" not in ps


def test_trunk_main_stays_exact(gen, tmp_path):
    ps = _vars(gen, tmp_path, "GATEWAY-MANAGER", MANIFEST_DERIVED)["ALLOWED_PREFIXES"].split("|")
    assert "main" in ps  # trunk : pas de slash, pas de glob


# ---------------------------------------------------------------------------
# Table de verite du separateur (famille de prefixes autorises du MANIFEST_BARE:
# chore/ ci/ docs/ feat/ fix/ + trunk main)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "branch,expected",
    [
        ("feat/new-thing", True),
        ("fix/x", True),
        ("ci/pipeline", True),
        ("chore/deps", True),
        ("docs/readme", True),
        ("main", True),
        ("feat/", True),
        ("feature-x", False),   # le faux positif elimine
        ("fixthing", False),
        ("cicd/x", False),      # ci/ != cicd (separateur strict)
        ("docsx/y", False),
        ("release/1.0", False), # hors famille autorisee du manifeste
        ("hotfix-urgent", False),
        ("random", False),
    ],
)
def test_truth_table_separator(gen, tmp_path, branch, expected):
    ps = _vars(gen, tmp_path, "feat/x", MANIFEST_BARE)["ALLOWED_PREFIXES"].split("|")
    assert _passes(branch, ps) is expected
