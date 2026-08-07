import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from application.services.meta_coherence_service import MetaCoherenceService

__all__ = ["MetaCoherenceService"]
