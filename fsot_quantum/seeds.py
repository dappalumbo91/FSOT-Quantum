"""
Seed constants — Layer 0 / 1 / 2. Zero free parameters.

Authority: vendor/fsot_compute.py pin D1D38A (FSOT-2.1-Lean).
Numeric values match FSOT-GPU config/fsot_seeds.json triangulation.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

PIN_EXPECTED = "D1D38A"


def authority_pin(path: Path | None = None) -> str:
    """SHA-256 prefix of vendor/fsot_compute.py (first 6 hex upper)."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "vendor" / "fsot_compute.py"
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()[:6].upper()


def pin_matches() -> bool:
    try:
        return authority_pin() == PIN_EXPECTED
    except FileNotFoundError:
        return False


@dataclass(frozen=True)
class Seeds:
    # Layer 0 — foundational seeds
    pi: float = math.pi
    e: float = math.e
    phi: float = (1.0 + math.sqrt(5.0)) / 2.0
    gamma: float = 0.5772156649015329
    g_catalan: float = 0.9159655941772190

    # Layer 1 — primary derived (closed form from seeds; precomputed to pin precision)
    alpha: float = 8.082937414140405e-4
    psi_con: float = 0.6321205588285577  # 1 - exp(-1)
    eta_eff: float = 0.46694220692425986  # 1/(pi-1)
    beta: float = 2.620866911333223e-17
    chaos: float = -0.3310241826104818
    theta_s: float = 0.29089654054517305
    poof: float = 0.1534822148944508

    # Layer 2 — composite
    c_eff: float = 0.9577022026205613
    p_var: float = 0.9579871226722757
    b_in: float = 0.7879407922764435
    a_in: float = 1.6668538450045732
    a_bleed: float = 1.046973630587551
    suction: float = 0.14703398542810284
    p_new: float = 0.30030227667037146
    c_factor: float = 0.287600151819184
    k: float = 0.42022166416069665
    c_cosm: float = 1.0 / (1.618033988749895 * 10.0)  # 1/(phi*10)

    @property
    def collapse_threshold(self) -> float:
        """C_eff · P_var — trinary collapse gate (no free parameter)."""
        return self.c_eff * self.p_var


SEEDS = Seeds()
COLLAPSE_THRESHOLD = SEEDS.collapse_threshold

# Metatron trinary cube: 3³ = 27 opcode / word width preferred
MAX_TRITS_WORD = 27
STATES_PER_U64 = 32  # 2 bits/trit packing carrier (transport only)
