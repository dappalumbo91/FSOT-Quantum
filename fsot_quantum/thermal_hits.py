"""
Fridge thought as a seed-locked probe (concept C5).

Quiet water = field inside ±Θ → trit 0 (superposed).
Hits / heat = recent_hits in T1 plus a Chaos-signed kick on the field.
More hits → more |v| > Θ → fewer superposed sites.

No free temperature. Hit ladder from seeds only.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse
from fsot_quantum.domains import DOMAINS
from fsot_quantum.medium_strings import three_strings


def _hit_ladder() -> list[int]:
    s = SEEDS
    return [
        0,
        1,
        max(1, int(math.floor(s.pi / 2.0))),  # 1
        max(2, int(math.floor(s.pi))),        # 3
        max(3, int(math.floor(s.e * 2))),     # 5
        max(6, int(math.floor(s.e * s.pi))),  # 8
    ]


def _quiet_field(n: int) -> list[float]:
    """Quiet water: amplitude just inside Θ (superposed if left alone)."""
    thr = COLLAPSE_THRESHOLD
    phi = float(SEEDS.phi)
    field = []
    x = 1
    amp = thr * float(SEEDS.psi_con)  # < Θ
    for i in range(n):
        x = (x * int(phi * 1e6) + i * 17) % (1 << 30)
        sign = 1.0 if (x & 1) else -1.0
        field.append(sign * amp)
    return field


def _kick(field: list[float], hits: int) -> list[float]:
    """Chaos-signed jostle, strength = |Chaos| · hits · poof (all seeds)."""
    s = SEEDS
    kick = abs(float(s.chaos)) * float(hits) * float(s.poof)
    out = []
    x = hits * 2654435761 + 1
    for i, v in enumerate(field):
        x = (x * 1664525 + 1013904223) % (1 << 30)
        sign = 1.0 if (x & 1) else -1.0
        out.append(v + sign * kick)
    return out


def run_thermal_hits_panel() -> dict[str, Any]:
    n = max(32, int(math.floor(float(SEEDS.phi) * 40)))  # ~64
    base = _quiet_field(n)
    qc = DOMAINS["Quantum_Computing"]
    rows = []
    prev_super = None
    for h in _hit_ladder():
        kicked = _kick(base, h)
        codes = collapse(kicked)
        if hasattr(codes, "tolist"):
            codes = codes.tolist()
        codes = [int(c) for c in codes]
        n0 = sum(1 for c in codes if c == 1)
        frac_super = n0 / n
        br = three_strings(
            D_eff=qc.D_eff,
            observed=qc.observed,
            delta_psi=qc.delta_psi,
            delta_theta=qc.delta_theta,
            recent_hits=float(h),
        )
        rows.append({
            "hits": h,
            "frac_superposed": frac_super,
            "n_super": n0,
            "n": n,
            "S_QC_at_hits": br["S"],
            "T1": br["T1_observe_string"],
        })
        prev_super = frac_super

    # Pattern we asked for: cold (0 hits) wetter than hot (max hits)
    cold = rows[0]["frac_superposed"]
    hot = rows[-1]["frac_superposed"]
    fridge_pattern = cold > hot

    return {
        "panel": "thermal_hits_fridge",
        "concept": "C5",
        "instances": rows,
        "frac_super_cold": cold,
        "frac_super_hot": hot,
        "fridge_pattern_ok": fridge_pattern,
        "overall_ok": fridge_pattern and cold > 0.5,
        "note": (
            "Ultra-cold analog = hits 0 → stay in ±Θ (water usable). "
            "Heat analog = more hits → snap to poles. Not a millikelvin derivation."
        ),
    }
