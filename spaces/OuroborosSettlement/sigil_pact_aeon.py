"""
SigilPact_Æon — Ouroboros Settlement Chamber (re-export shim).

The canonical implementation lives in sigils/sigil_pact_aeon.py (Ollama-integrated).
This module re-exports it so existing imports from spaces/OuroborosSettlement/
continue to work without maintaining a second copy.
"""

import sys
from pathlib import Path

# Ensure sigils/ is on the path regardless of cwd
_SIGILS_DIR = Path(__file__).resolve().parent.parent.parent / "sigils"
if str(_SIGILS_DIR) not in sys.path:
    sys.path.insert(0, str(_SIGILS_DIR))

from sigil_pact_aeon import (  # noqa: F401  (re-export)
    SigilPactAeon,
    aeon_agent,
    SIGIL_PROMPT_TEMPLATE,
    MANIFOLD_MEMORY_PATH,
    FRACTAL_MEMORY_PATH,
    MONOLITH_MEMORY_PATH,
    PRIORITY_ECHO_PATH,
)

__all__ = [
    "SigilPactAeon",
    "aeon_agent",
    "SIGIL_PROMPT_TEMPLATE",
    "MANIFOLD_MEMORY_PATH",
    "FRACTAL_MEMORY_PATH",
    "MONOLITH_MEMORY_PATH",
    "PRIORITY_ECHO_PATH",
]
