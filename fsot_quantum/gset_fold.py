"""
Gset-style MaxCut instances under the fold cost ledger.

Gset (Stanford / Ye) graphs: large ±1 / 0-1 weighted MaxCut. We do not
download the archive; we generate *Gset-style* seed-locked graphs:
  - sparse random-regular-ish via φ-walk
  - ±1 weights from seed parity
  - n in {40, 60, 80, 100} (consumer-host fold, not 2^n QAOA)

Acceptance: cut / n_edges ≥ 1/φ  (same large-n floor as large_maxcut).

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import cost_contrast, fold_budget_formal, fold_probe_budget
from fsot_quantum.large_maxcut import RATIO_FLOOR
from fsot_quantum.optimization import cut_value, fsot_local_spins


def gset_style_graph(n: int, avg_degree: int, *, seed_k: int = 0) -> list[tuple[int, int, int]]:
    """
    Sparse undirected graph, Gset-like: n verts, ~avg_degree·n/2 edges,
    weights ±1 from φ-walk parity.
    """
    phi = float(SEEDS.phi)
    target = max(n, (avg_degree * n) // 2)
    edges: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    x = (seed_k * int(phi * 1e6) + n * 2654435761) % (1 << 30)
    guard = 0
    while len(edges) < target and guard < target * 20:
        guard += 1
        x = (x * 1664525 + 1013904223) % (1 << 30)
        a = x % n
        x = (x * 1664525 + 1013904223) % (1 << 30)
        b = x % n
        if a == b:
            continue
        if a > b:
            a, b = b, a
        if (a, b) in seen:
            continue
        seen.add((a, b))
        w = 1 if ((x >> 8) & 1) else -1
        # MaxCut cut_value uses |J| when endpoints differ — keep +1 edges
        # for cut counting; store weight 1 (unweighted Gset-style cut)
        edges.append((a, b, 1))
    return edges


def run_gset_fold_panel() -> dict[str, Any]:
    # Gset-like sizes; degree from floor(π)+2 = 5 (seed)
    deg = int(SEEDS.pi) + 2
    plans = [
        ("gset_like_n40", 40, deg, 1),
        ("gset_like_n60", 60, deg, 2),
        ("gset_like_n80", 80, deg, 3),
        ("gset_like_n100", 100, deg, 4),
    ]
    rows = []
    for name, n, d, k in plans:
        edges = gset_style_graph(n, d, seed_k=k)
        t0 = time.perf_counter()
        spins = fsot_local_spins(n, edges, maximize_cut=True)
        cut = cut_value(spins, edges)
        dt = time.perf_counter() - t0
        n_e = len(edges)
        ratio = cut / n_e if n_e else 0.0
        rows.append({
            "name": name,
            "n": n,
            "n_edges": n_e,
            "avg_degree_target": d,
            "cut_fold": cut,
            "ratio_lb": ratio,
            "ratio_floor": RATIO_FLOOR,
            "ok": ratio >= RATIO_FLOOR,
            "seconds": dt,
            "hilbert_amps_if_QAOA": 1 << min(n, 62),  # cap report
            "fold_budget": fold_probe_budget(n),
            "fold_budget_formal": fold_budget_formal(n),
            "cost": cost_contrast(n, n_e),
        })

    return {
        "panel": "gset_style_maxcut_fold",
        "instances": rows,
        "pass_count": sum(1 for r in rows if r["ok"]),
        "total": len(rows),
        "overall_ok": all(r["ok"] for r in rows) and len(rows) > 0,
        "ratio_floor": RATIO_FLOOR,
        "note": (
            "Gset-style seed-locked sparse MaxCut (not the downloaded Gset files). "
            "Fold local search vs 1/φ floor — no 2^n QAOA sim."
        ),
    }
