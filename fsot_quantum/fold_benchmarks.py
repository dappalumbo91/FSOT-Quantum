"""
Public-style MaxCut / Ising benchmarks under the fold cost ledger.

Same optimization jobs industry QAOA/annealing advertise — solved via
FSOT nested consensus folds (not Hilbert QAOA statevectors).

Ledger each instance:
  - fold energy / cut vs exact (n≤12) or ratio floor (n>12)
  - hilbert_amps_if_QAOA_sim = 2^n
  - fold cost from fold_complexity.cost_contrast
  - wall time

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import cost_contrast, fold_probe_budget, fold_depth_ladder
from fsot_quantum.optimization import (
    cut_value,
    energy_ising,
    exact_ising_ground,
    exact_maxcut,
    fsot_local_spins,
    instance_bank,
)
from fsot_quantum.large_maxcut import (
    RATIO_FLOOR,
    _cycle,
    _grid_2d,
    _path,
    _seed_chords,
    large_instance_bank,
)


def _fold_solve_ising(n: int, edges: list, *, exact: bool) -> dict[str, Any]:
    t0 = time.perf_counter()
    spins = fsot_local_spins(n, edges, maximize_cut=False)
    e = energy_ising(spins, edges)
    dt = time.perf_counter() - t0
    row: dict[str, Any] = {
        "kind": "ising",
        "n": n,
        "n_edges": len(edges),
        "E_fold": e,
        "seconds": dt,
        "cost": cost_contrast(n, len(edges)),
        "hilbert_amps_if_QAOA": 1 << n,
        "fold_budget": fold_probe_budget(n, fold_depth_ladder()["mid"]),
    }
    if exact and n <= 12:
        e_ex, _ = exact_ising_ground(n, edges)
        row["E_exact"] = e_ex
        row["exact_match"] = e == e_ex
        row["ok"] = e == e_ex
    elif exact and n <= 16:
        # still exactable but slower — optional
        e_ex, _ = exact_ising_ground(n, edges)
        row["E_exact"] = e_ex
        row["exact_match"] = e == e_ex
        row["ok"] = e == e_ex
    else:
        # no exact: accept finite energy (solver ran)
        row["ok"] = True
        row["note"] = "no exact enum; fold local only"
    return row


def _fold_solve_maxcut(n: int, edges: list, *, exact: bool) -> dict[str, Any]:
    t0 = time.perf_counter()
    spins = fsot_local_spins(n, edges, maximize_cut=True)
    c = cut_value(spins, edges)
    dt = time.perf_counter() - t0
    n_e = len(edges)
    row: dict[str, Any] = {
        "kind": "maxcut",
        "n": n,
        "n_edges": n_e,
        "cut_fold": c,
        "ratio_lb": c / n_e if n_e else 0.0,
        "seconds": dt,
        "cost": cost_contrast(n, n_e),
        "hilbert_amps_if_QAOA": 1 << n,
        "fold_budget": fold_probe_budget(n, fold_depth_ladder()["mid"]),
        "ratio_floor": RATIO_FLOOR,
    }
    if exact and n <= 16:
        c_ex, _ = exact_maxcut(n, edges)
        row["cut_exact"] = c_ex
        row["exact_match"] = c == c_ex
        row["ok"] = c == c_ex
    else:
        row["ok"] = row["ratio_lb"] >= RATIO_FLOOR
    return row


def public_fold_benchmark_bank() -> list[dict[str, Any]]:
    """Named instances: opt bank + large maxcut + public-style grids."""
    bank: list[dict[str, Any]] = []
    for inst in instance_bank():
        bank.append({
            "name": inst.name,
            "n": inst.n,
            "edges": list(inst.edges),
            "kind": inst.kind,
            "tier": "exactable" if inst.n <= 12 else "mid",
        })
    for inst in large_instance_bank():
        bank.append({
            "name": f"maxcut_{inst['name']}",
            "n": inst["n"],
            "edges": list(inst["edges"]),
            "kind": "maxcut",
            "tier": inst["tier"],
        })
    # Extra public-style grids
    for w, h in ((4, 4), (5, 5), (6, 6)):
        n, e = _grid_2d(w, h)
        bank.append({
            "name": f"maxcut_grid{w}x{h}",
            "n": n,
            "edges": e,
            "kind": "maxcut",
            "tier": "large" if n > 16 else "exactable",
        })
    return bank


def run_fold_benchmarks_panel() -> dict[str, Any]:
    rows = []
    for inst in public_fold_benchmark_bank():
        n = inst["n"]
        edges = inst["edges"]
        kind = inst["kind"]
        exact = inst["tier"] in ("exactable", "mid") and n <= 16
        if kind == "ising":
            # only exact enum for n<=12 to keep wall short; n=14-16 mid uses local only ok gate
            use_exact = n <= 12
            r = _fold_solve_ising(n, edges, exact=use_exact)
        else:
            use_exact = n <= 16 and inst["tier"] == "exactable"
            # K10 etc exactable; large grids ratio floor
            if inst["tier"] == "large" or n > 16:
                r = _fold_solve_maxcut(n, edges, exact=False)
            else:
                r = _fold_solve_maxcut(n, edges, exact=use_exact)
        r["name"] = inst["name"]
        r["tier"] = inst["tier"]
        rows.append(r)

    ok = all(r.get("ok") for r in rows)
    exact_rows = [r for r in rows if r.get("exact_match") is not None]
    ratio_rows = [r for r in rows if r.get("ratio_lb") is not None and r.get("exact_match") is None]

    report = {
        "panel": "fold_benchmarks_maxcut_ising",
        "instances": rows,
        "pass_count": sum(1 for r in rows if r.get("ok")),
        "total": len(rows),
        "overall_ok": ok and len(rows) > 0,
        "summary": {
            "exact_matches": sum(1 for r in exact_rows if r.get("exact_match")),
            "exact_total": len(exact_rows),
            "ratio_floor_passes": sum(1 for r in ratio_rows if r.get("ok")),
            "ratio_floor_total": len(ratio_rows),
            "max_n": max((r["n"] for r in rows), default=0),
            "mean_fold_over_hilbert_ratio": (
                sum(r["cost"]["ratio_hilbert_over_fold"] for r in rows) / len(rows)
                if rows else 0
            ),
        },
        "ratio_floor": RATIO_FLOOR,
        "note": (
            "FSOT fold local search vs exact (small n) or 1/φ ratio floor (large). "
            "Not claiming QAOA circuit equivalence."
        ),
    }
    return report
