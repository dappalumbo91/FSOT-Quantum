"""
Larger-n MaxCut without full enumeration (n > 12).

FSOT multi-start local search (zero free params) + certified bounds:
  cut_fsot  ≤ cut*  ≤ n_edges
  approx_ratio_lb = cut_fsot / n_edges   (vs trivial upper bound)
  when n ≤ 16: also exact residual vs full enum

Green for large-n panel (honest):
  - n ≤ 16: exact match (same as optimization panel)
  - n > 16: ratio_lb ≥ phi^{-1}  (seed golden lower envelope, no free fit)
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Sequence

from fsot_lib.seeds import SEEDS
from fsot_quantum.optimization import (
    cut_value,
    exact_maxcut,
    fsot_local_spins,
)

ROOT = Path(__file__).resolve().parents[1]
# Seed-locked acceptance floor for large-n (1/phi ≈ 0.618)
RATIO_FLOOR = 1.0 / float(SEEDS.phi)


def _cycle(n: int) -> list[tuple[int, int, int]]:
    return [(i, (i + 1) % n, 1) for i in range(n)]


def _path(n: int) -> list[tuple[int, int, int]]:
    return [(i, i + 1, 1) for i in range(n - 1)]


def _complete(n: int) -> list[tuple[int, int, int]]:
    e = []
    for i in range(n):
        for j in range(i + 1, n):
            e.append((i, j, 1))
    return e


def _grid_2d(w: int, h: int) -> tuple[int, list[tuple[int, int, int]]]:
    """w×h grid, row-major vertices."""
    n = w * h
    edges = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if x + 1 < w:
                edges.append((i, i + 1, 1))
            if y + 1 < h:
                edges.append((i, i + w, 1))
    return n, edges


def _seed_chords(n: int, k: int) -> list[tuple[int, int, int]]:
    """Deterministic extra edges from φ-walk (no free RNG)."""
    edges = []
    phi = float(SEEDS.phi)
    x = 1
    seen = set()
    for t in range(k * 4):
        x = (x * int(phi * 1e6) + t * 2654435761) % max(n * n, 1)
        a, b = x % n, (x // n) % n
        if a == b:
            continue
        if a > b:
            a, b = b, a
        if (a, b) in seen:
            continue
        seen.add((a, b))
        edges.append((a, b, 1))
        if len(edges) >= k:
            break
    return edges


def large_instance_bank() -> list[dict[str, Any]]:
    bank = []
    # Exactable mid size
    for n in (14, 16):
        bank.append({"name": f"cycle{n}", "n": n, "edges": _cycle(n), "tier": "exactable"})
        bank.append({"name": f"path{n}", "n": n, "edges": _path(n), "tier": "exactable"})
    bank.append({"name": "K8", "n": 8, "edges": _complete(8), "tier": "exactable"})
    bank.append({"name": "K10", "n": 10, "edges": _complete(10), "tier": "exactable"})

    # Large — no full enum for cut*
    for n in (18, 20, 24, 28, 32):
        e = _cycle(n) + _seed_chords(n, n // 2)
        bank.append({"name": f"cycle_chords{n}", "n": n, "edges": e, "tier": "large"})
    n, e = _grid_2d(5, 5)  # 25 verts
    bank.append({"name": "grid5x5", "n": n, "edges": e, "tier": "large"})
    n, e = _grid_2d(6, 6)  # 36
    bank.append({"name": "grid6x6", "n": n, "edges": e, "tier": "large"})
    bank.append({
        "name": "K12",
        "n": 12,
        "edges": _complete(12),
        "tier": "exactable",
    })
    return bank


def run_one(inst: dict[str, Any]) -> dict[str, Any]:
    n = inst["n"]
    edges = inst["edges"]
    n_edges = len(edges)
    t0 = time.perf_counter()
    spins = fsot_local_spins(n, edges, maximize_cut=True)
    cut = cut_value(spins, edges)
    dt = time.perf_counter() - t0

    row: dict[str, Any] = {
        "name": inst["name"],
        "n": n,
        "n_edges": n_edges,
        "tier": inst["tier"],
        "cut_fsot": cut,
        "upper_bound_edges": n_edges,
        "ratio_lb": cut / n_edges if n_edges else 0.0,
        "seconds": dt,
        "method": "fsot_multistart_local",
    }

    if n <= 16:
        exact_c, _ = exact_maxcut(n, edges)
        row["cut_exact"] = exact_c
        row["gap"] = exact_c - cut
        row["residual_pct"] = 100.0 * abs(exact_c - cut) / max(exact_c, 1)
        row["approx_vs_exact"] = cut / exact_c if exact_c else 1.0
        row["ok"] = cut == exact_c
        row["green"] = cut == exact_c
    else:
        # No exact: green if ratio vs edge upper bound clears seed floor
        row["cut_exact"] = None
        row["gap"] = None
        row["ratio_floor_seed"] = RATIO_FLOOR
        row["ok"] = row["ratio_lb"] + 1e-15 >= RATIO_FLOOR
        row["green"] = row["ok"]
        row["note"] = "large-n: no enum; ratio_lb = cut/|E| vs 1/phi floor"
    return row


def run_large_maxcut_panel() -> dict[str, Any]:
    rows = [run_one(i) for i in large_instance_bank()]
    exactable = [r for r in rows if r["tier"] == "exactable"]
    large = [r for r in rows if r["tier"] == "large"]
    report = {
        "panel": "large_maxcut",
        "ratio_floor_seed": RATIO_FLOOR,
        "instances": rows,
        "exactable_pass": sum(1 for r in exactable if r["ok"]),
        "exactable_total": len(exactable),
        "large_pass": sum(1 for r in large if r["ok"]),
        "large_total": len(large),
        "overall_ok": all(r["ok"] for r in rows),
        "summary": {
            "mean_ratio_lb_large": (
                sum(r["ratio_lb"] for r in large) / len(large) if large else None
            ),
            "mean_approx_exactable": (
                sum(r.get("approx_vs_exact", 0) for r in exactable) / len(exactable)
                if exactable
                else None
            ),
        },
    }
    out = ROOT / "results" / "large_maxcut.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Large-n MaxCut panel",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**exactable:** {report['exactable_pass']}/{report['exactable_total']}",
        f"**large (ratio ≥ 1/φ):** {report['large_pass']}/{report['large_total']}",
        f"**1/φ floor:** `{RATIO_FLOOR:.6f}`",
        "",
        "| name | n | |E| | cut_fsot | exact | ratio_lb | ok |",
        "|------|---|-----|----------|-------|----------|----|",
    ]
    for r in rows:
        md.append(
            f"| {r['name']} | {r['n']} | {r['n_edges']} | {r['cut_fsot']} | "
            f"{r.get('cut_exact')} | {r['ratio_lb']:.3f} | {r['ok']} |"
        )
    (ROOT / "results" / "LARGE_MAXCUT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report
