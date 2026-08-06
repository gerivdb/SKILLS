import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent
for pkg in ["n243-graph-builder", "n243-query-engine"]:
    p = SKILLS_ROOT / pkg
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
