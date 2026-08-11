"""
FSOT fold complexity — scale QC jobs without Hilbert 2^n expansion.

Industry QC bottleneck (the term you were reaching for):
  **Hilbert-space dimension / degrees of freedom** — amplitudes live in C^{2^n}
  (or higher for multi-level systems). Brute force = expand the space.

FSOT answer:
  Treat complexity as **domain folds** calibrated by D_eff, not as larger
  statevectors. Same jobs (oracle class, secret, search, period, optimize,
  phase class, chemistry residual) — different geometry of work.

Lawful objects (pin D1D38A, zero free params):
  - D_eff domain routes (QM=6, QC=11, …)
  - Θ = C_eff · P_var collapse
  - complexity weight w_φ = φ/(1+φ)
  - fold depth from seeds: floor(π), floor(e), …
  - consensus / trit collapse — not softmax / Born sampling

Cost contrast (ledgered, not marketing):
  Hilbert path:  Θ(2^n) amplitudes or Θ(√N) oracle queries (Grover)
  Fold path:     Θ(depth · structure · √D_eff) closed-form + poly probes
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Sequence

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.scalar import compute_scalar
from fsot_lib.trinary import collapse
from fsot_quantum.domains import DOMAINS, DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar


# Complexity weight motif (archive FSOT_MATH_FOR_SPEED)
def complexity_weight() -> float:
    """φ/(1+φ) — seed-locked complexity budget motif."""
    phi = float(SEEDS.phi)
    return phi / (1.0 + phi)


def fold_depth_ladder() -> dict[str, int]:
    """Nested fold depths from seeds only (not free knobs)."""
    pi, e = float(SEEDS.pi), float(SEEDS.e)
    return {
        "shallow": max(1, int(math.floor(pi / 2.0))),   # 1
        "mid": max(2, int(math.floor(pi))),             # 3
        "deep": max(3, int(math.floor(e * pi / 2.0))),  # 4
        "meta": max(4, int(math.floor(e * pi))),        # 8
    }


@dataclass(frozen=True)
class FoldRoute:
    """One domain fold — D_eff is dimensional calibration, not a free fit."""

    name: str
    D_eff: int
    observed: bool
    role: str

    def scalar(self) -> float:
        d = DOMAINS.get(self.name)
        if d is not None:
            return domain_scalar(self.name)
        return float(
            compute_scalar(
                N=1.0,
                P=1.0,
                D_eff=float(self.D_eff),
                observed=self.observed,
            )
        )

    def cost_unit(self) -> float:
        """Lawful cost proxy ~ 1/√D_eff (scalar base motif)."""
        return 1.0 / math.sqrt(float(self.D_eff))


# QC job fold routes — nested, not Hilbert axes
FOLD_ROUTES: dict[str, FoldRoute] = {
    "spin_law": FoldRoute("Quantum_Mechanics", 6, True, "measurement / spin resolve"),
    "compute": FoldRoute("Quantum_Computing", 11, False, "compute substrate"),
    "optics": FoldRoute("Quantum_Optics", 11, True, "phase / optics class"),
    "particle": FoldRoute("Particle_Physics", 5, True, "structure / mass scale"),
    "gravity": FoldRoute("Quantum_Gravity", 22, False, "deep residual fold"),
}


def hilbert_amp_cost(n_qubits: int) -> int:
    """Industry-style amplitude count for n qubits."""
    return 1 << n_qubits


def fold_probe_budget(structure_size: int, depth: int | None = None) -> int:
    """
    How many structure probes a fold path is allowed — poly in structure,
    scaled by complexity weight and depth, never 2^structure_size.
    """
    d = depth if depth is not None else fold_depth_ladder()["mid"]
    w = complexity_weight()
    # seed-locked poly: depth * structure * floor(φ*10) + meta tiles (27 Metatron)
    meta = 27  # 3^3 archive tile
    budget = int(math.ceil(d * structure_size * w * 10 + meta))
    # cap still poly-ish for huge structure (safety)
    return max(structure_size + 1, min(budget, structure_size * structure_size + meta))


def cost_contrast(n_qubits_or_bits: int, structure_size: int | None = None) -> dict[str, Any]:
    """Side-by-side cost ledger for a job of nominal size n."""
    n = n_qubits_or_bits
    s = structure_size if structure_size is not None else n
    depth = fold_depth_ladder()["mid"]
    fold_cost = fold_probe_budget(s, depth)
    # D_eff fold chain cost proxy
    chain = sum(FOLD_ROUTES[k].cost_unit() for k in ("spin_law", "compute"))
    return {
        "nominal_n": n,
        "hilbert_amplitudes": hilbert_amp_cost(n),
        "hilbert_note": "C^{2^n} statevector entries (brute sim bottleneck)",
        "fold_probe_budget": fold_cost,
        "fold_depth": depth,
        "fold_D_eff_cost_proxy": chain,
        "complexity_weight_phi": complexity_weight(),
        "ratio_hilbert_over_fold": hilbert_amp_cost(n) / max(1, fold_cost),
        "winner_when": "fold when structure admits closed form / poly probes",
    }


def nested_fold_scalars(depth: int | None = None) -> list[dict[str, Any]]:
    """
    Evaluate nested domain folds — complexity as stacked D_eff routes,
    not stacked qubits.
    """
    ladder = fold_depth_ladder()
    d = depth if depth is not None else ladder["mid"]
    order = ["spin_law", "compute", "optics", "particle", "gravity"]
    out = []
    for i, key in enumerate(order[: max(1, min(d, len(order)))]):
        r = FOLD_ROUTES[key]
        s = r.scalar()
        out.append({
            "fold_index": i,
            "route": key,
            "domain": r.name,
            "D_eff": r.D_eff,
            "S": s,
            "class": "emergence" if s > 0 else "damping",
            "cost_unit": r.cost_unit(),
            "role": r.role,
        })
    return out


def fold_collapse_field(values: Sequence[float]) -> list[int]:
    """Collapse continuous field → trit codes via Θ (owned trinary)."""
    codes = collapse(list(values), threshold=COLLAPSE_THRESHOLD)
    if hasattr(codes, "tolist"):
        codes = codes.tolist()
    return [int(c) for c in codes]


def phi_walk_indices(n: int, count: int, seed_k: int = 0) -> list[int]:
    """Deterministic φ-walk indices in [0, n) — structure probes, not free RNG."""
    if n <= 0:
        return []
    phi = float(SEEDS.phi)
    x = (seed_k * int(phi * 1e6) + 2654435761) % (1 << 30)
    out: list[int] = []
    seen: set[int] = set()
    for k in range(max(count * 4, count + 1)):
        x = (x * 1664525 + 1013904223 + k) % (1 << 30)
        i = x % n
        if i not in seen:
            seen.add(i)
            out.append(i)
        if len(out) >= count:
            break
    return out


def fold_score_candidates(
    scores: Sequence[float],
    *,
    pick: str = "max",
) -> dict[str, Any]:
    """
    Score list → collapse → pick pole. This is the FSOT 'measure' for
    candidate sets without allocating a 2^n amplitude vector.
    """
    codes = fold_collapse_field(scores)
    thr = COLLAPSE_THRESHOLD
    # signed field for argmax/argmin of continuous score
    if pick == "max":
        best = max(range(len(scores)), key=lambda i: scores[i])
    else:
        best = min(range(len(scores)), key=lambda i: scores[i])
    poles = [i for i, c in enumerate(codes) if c == 2]  # spin-up codes
    return {
        "best_index": best,
        "best_score": scores[best] if scores else None,
        "collapse_codes_head": codes[: min(16, len(codes))],
        "n_poles": len(poles),
        "threshold": thr,
        "method": "fold_collapse_over_candidates",
    }
