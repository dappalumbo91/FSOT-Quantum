"""
Coherence utilities for FSOT quantum registers.
Twin of FSOT-GPU coherence (threshold = C_eff·P_var).
"""

from __future__ import annotations

import math
from typing import Sequence

from fsot_quantum.seeds import COLLAPSE_THRESHOLD


def position_coherence(field: Sequence[float], threshold: float = COLLAPSE_THRESHOLD) -> float:
    if not field:
        return 0.0
    n = sum(1 for v in field if abs(float(v)) > threshold)
    return n / len(field)


def coherence_norm(field: Sequence[float], threshold: float = COLLAPSE_THRESHOLD) -> list[float]:
    n = len(field)
    if n == 0:
        return []
    coh = position_coherence(field, threshold)
    rms = math.sqrt(sum(float(v) * float(v) for v in field) / n)
    rms = max(rms, threshold)
    factor = coh + (1.0 - coh) * threshold
    scale = factor / rms
    return [float(v) * scale for v in field]
