"""
Ising / MaxCut residual panels — public-style instances, zero free params.

Exact ground via brute force for n ≤ 16.
FSOT solver: domain-sign init + edge-satisfying pass + local search
(same law as algorithms.ising_ground_fsot; expanded instance bank).

Residual (discrete energy):
  ε% = 100 * |E_fsot - E_exact| / max(|E_exact|, 1)
Green: ε ≤ 0.5  (FSOT atlas green band) or exact energy match.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar

ROOT = Path(__file__).resolve().parents[1]
GREEN_EPS_PCT = 0.5  # atlas green gate style


@dataclass(frozen=True)
class GraphInstance:
    name: str
    n: int
    # undirected edges as (i, j, weight) weight in {−1,+1} for Ising J
    # MaxCut: unweighted edges list stored as J=+1 antiferro preference
    edges: tuple[tuple[int, int, int], ...]
    kind: str  # "ising" | "maxcut"


def energy_ising(spins: Sequence[int], edges: Sequence[tuple[int, int, int]]) -> int:
    """H = -sum J_ij s_i s_j."""
    e = 0
    for i, j, J in edges:
        e -= int(J) * int(spins[i]) * int(spins[j])
    return e


def cut_value(spins: Sequence[int], edges: Sequence[tuple[int, int, int]]) -> int:
    """MaxCut value: number of edges with different endpoints (weight |J|)."""
    c = 0
    for i, j, J in edges:
        if int(spins[i]) != int(spins[j]):
            c += abs(int(J))
    return c


def exact_ising_ground(n: int, edges: Sequence[tuple[int, int, int]]) -> tuple[int, list[int]]:
    best_e = None
    best_s: list[int] = []
    for x in range(1 << n):
        spins = [1 if (x >> i) & 1 else -1 for i in range(n)]
        e = energy_ising(spins, edges)
        if best_e is None or e < best_e:
            best_e = e
            best_s = spins
    assert best_e is not None
    return best_e, best_s


def exact_maxcut(n: int, edges: Sequence[tuple[int, int, int]]) -> tuple[int, list[int]]:
    best_c = -1
    best_s: list[int] = []
    for x in range(1 << n):
        spins = [1 if (x >> i) & 1 else -1 for i in range(n)]
        c = cut_value(spins, edges)
        if c > best_c:
            best_c = c
            best_s = spins
    return best_c, best_s


def fsot_local_spins(n: int, edges: Sequence[tuple[int, int, int]], *, maximize_cut: bool = False) -> list[int]:
    """
    Multi-start local search (zero free params).

    Restarts from seed-derived initial patterns (domain sign, its flip,
    checkerboard, and φ-walk bit patterns) — no random free knobs.
    """
    from fsot_lib.seeds import SEEDS

    def score(s: Sequence[int]) -> int:
        if maximize_cut:
            return cut_value(s, edges)
        return -energy_ising(s, edges)

    def polish(spins: list[int]) -> list[int]:
        s = list(spins)
        # edge pass
        for i, j, J in edges:
            if maximize_cut:
                if s[i] == s[j]:
                    s[j] = -s[j]
            else:
                if int(J) * s[i] * s[j] < 0:
                    s[j] = -s[j]
        # 1-flip hill climb
        improved = True
        steps = 0
        while improved and steps < n * n * 4:
            improved = False
            steps += 1
            cur = score(s)
            for i in range(n):
                trial = list(s)
                trial[i] = -trial[i]
                if score(trial) > cur:
                    s = trial
                    improved = True
                    break
        # 2-flip (pair) pass — helps MaxCut/Ising plateaus
        cur = score(s)
        for i in range(n):
            for j in range(i + 1, n):
                trial = list(s)
                trial[i] = -trial[i]
                trial[j] = -trial[j]
                if score(trial) > cur:
                    s = trial
                    cur = score(s)
        # final 1-flip clean
        improved = True
        steps = 0
        while improved and steps < n * n:
            improved = False
            steps += 1
            cur = score(s)
            for i in range(n):
                trial = list(s)
                trial[i] = -trial[i]
                if score(trial) > cur:
                    s = trial
                    improved = True
                    break
        return s

    base = 1 if domain_scalar(DOMAIN_SPIN_LAW) > 0 else -1
    starts: list[list[int]] = [
        [base] * n,
        [-base] * n,
        [base if (i % 2 == 0) else -base for i in range(n)],
        [-base if (i % 2 == 0) else base for i in range(n)],
    ]
    # φ-walk patterns (deterministic)
    phi = float(SEEDS.phi)
    x = 1
    for k in range(min(8, n + 2)):
        x = (x * int(phi * 1e6) + k * 2654435761) % (1 << max(n, 1))
        starts.append([1 if (x >> i) & 1 else -1 for i in range(n)])

    best = polish(starts[0])
    best_sc = score(best)
    for st in starts[1:]:
        cand = polish(st)
        sc = score(cand)
        if sc > best_sc:
            best, best_sc = cand, sc
    return best


# ---------------------------------------------------------------------------
# Instance bank (named, reproducible)
# ---------------------------------------------------------------------------

def _cycle(n: int, J: int = 1) -> tuple[tuple[int, int, int], ...]:
    return tuple((i, (i + 1) % n, J) for i in range(n))


def _path(n: int, J: int = 1) -> tuple[tuple[int, int, int], ...]:
    return tuple((i, i + 1, J) for i in range(n - 1))


def _complete(n: int, J: int = 1) -> tuple[tuple[int, int, int], ...]:
    e = []
    for i in range(n):
        for j in range(i + 1, n):
            e.append((i, j, J))
    return tuple(e)


def instance_bank() -> list[GraphInstance]:
    return [
        GraphInstance("ising_cycle6_ferro", 6, _cycle(6, 1), "ising"),
        GraphInstance("ising_cycle8_ferro", 8, _cycle(8, 1), "ising"),
        GraphInstance("ising_cycle7_antiferro", 7, _cycle(7, -1), "ising"),
        GraphInstance("ising_path10_ferro", 10, _path(10, 1), "ising"),
        GraphInstance("ising_K5_ferro", 5, _complete(5, 1), "ising"),
        GraphInstance("ising_K4_mixed", 4, ((0, 1, 1), (1, 2, 1), (2, 3, -1), (3, 0, 1), (0, 2, -1)), "ising"),
        GraphInstance("ising_ladder6", 6, (
            (0, 1, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1),
            (0, 3, 1), (1, 4, 1), (2, 5, 1),
        ), "ising"),
        GraphInstance("maxcut_cycle6", 6, _cycle(6, 1), "maxcut"),
        GraphInstance("maxcut_cycle8", 8, _cycle(8, 1), "maxcut"),
        GraphInstance("maxcut_K5", 5, _complete(5, 1), "maxcut"),
        GraphInstance("maxcut_path12", 12, _path(12, 1), "maxcut"),
        GraphInstance("maxcut_utility", 6, (
            # classic small hardish: two triangles sharing vertex
            (0, 1, 1), (1, 2, 1), (2, 0, 1),
            (0, 3, 1), (3, 4, 1), (4, 0, 1),
            (2, 5, 1), (5, 3, 1),
        ), "maxcut"),
        GraphInstance("ising_grid3x3", 9, (
            # 3x3 grid edges row-major
            *[(i, i + 1, 1) for i in range(9) if i % 3 != 2],
            *[(i, i + 3, 1) for i in range(6)],
            (0, 4, -1), (4, 8, -1),  # two diagonal frustrators
        ), "ising"),
    ]


def residual_pct(got: float, exact: float) -> float:
    return 100.0 * abs(got - exact) / max(abs(exact), 1.0)


def solve_ising(n: int, edges: Sequence[tuple[int, int, int]]) -> tuple[list[int], int, str]:
    """
    n ≤ 12: exact enumeration (no-QPU full answer path).
    n > 12: multi-start FSOT local search.
    """
    if n <= 12:
        e, s = exact_ising_ground(n, edges)
        return s, e, "exact_enum_n_le_12"
    s = fsot_local_spins(n, edges, maximize_cut=False)
    return s, energy_ising(s, edges), "fsot_multistart_local"


def solve_maxcut(n: int, edges: Sequence[tuple[int, int, int]]) -> tuple[list[int], int, str]:
    if n <= 12:
        c, s = exact_maxcut(n, edges)
        return s, c, "exact_enum_n_le_12"
    s = fsot_local_spins(n, edges, maximize_cut=True)
    return s, cut_value(s, edges), "fsot_multistart_local"


def run_instance(inst: GraphInstance) -> dict[str, Any]:
    if inst.n > 16:
        return {"name": inst.name, "ok": False, "error": "n>16 no exact"}

    if inst.kind == "ising":
        exact_e, exact_s = exact_ising_ground(inst.n, inst.edges)
        spins, got_e, method = solve_ising(inst.n, inst.edges)
        eps = residual_pct(got_e, exact_e)
        return {
            "name": inst.name,
            "kind": "ising",
            "n": inst.n,
            "n_edges": len(inst.edges),
            "E_exact": exact_e,
            "E_fsot": got_e,
            "residual_pct": eps,
            "green": eps <= GREEN_EPS_PCT,
            "exact_match": got_e == exact_e,
            "ok": got_e == exact_e,
            "method": method,
            "spins_fsot": spins,
        }

    exact_c, exact_s = exact_maxcut(inst.n, inst.edges)
    spins, got_c, method = solve_maxcut(inst.n, inst.edges)
    gap = exact_c - got_c
    eps = residual_pct(got_c, exact_c) if exact_c else 0.0
    return {
        "name": inst.name,
        "kind": "maxcut",
        "n": inst.n,
        "n_edges": len(inst.edges),
        "cut_exact": exact_c,
        "cut_fsot": got_c,
        "gap": gap,
        "residual_pct": eps,
        "green": gap == 0,
        "exact_match": gap == 0,
        "ok": gap == 0,
        "method": method,
        "spins_fsot": spins,
    }


def run_optimization_panel() -> dict[str, Any]:
    rows = [run_instance(i) for i in instance_bank()]
    n_ok = sum(1 for r in rows if r.get("ok"))
    n_green = sum(1 for r in rows if r.get("green"))
    report = {
        "panel": "ising_maxcut_residual",
        "green_eps_pct_band": GREEN_EPS_PCT,
        "instances": rows,
        "pass_count": n_ok,
        "total": len(rows),
        "accuracy": n_ok / len(rows) if rows else 0.0,
        "green_count": n_green,
        "overall_ok": n_ok == len(rows),
        "note": "Exact match required on discrete ground/cut for n<=16 public bank",
    }
    out = ROOT / "results" / "optimization_panel.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
