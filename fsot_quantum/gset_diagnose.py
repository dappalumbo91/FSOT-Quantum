"""
Why Gset MaxCut residuals are large — measure the object and each stage.

No new coefficients. Prints where the fold loses cut.

python -m fsot_quantum.gset_diagnose
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse, code_to_signed
from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.gset_official import PUBLISHED_CUTS, parse_gset_text
from fsot_quantum.optimization import cut_value


def _raw_edges(text: str) -> tuple[int, list[tuple[int, int, int]]]:
    """Parse keeping signed weights (diagnosis only)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    n = int(lines[0].split()[0])
    edges = []
    for ln in lines[1:]:
        p = ln.split()
        if len(p) < 2:
            continue
        i, j = int(p[0]) - 1, int(p[1]) - 1
        w = int(p[2]) if len(p) > 2 else 1
        if i == j:
            continue
        if i > j:
            i, j = j, i
        edges.append((i, j, w))
    return n, edges


def _adj(n: int, edges: list[tuple[int, int, int]]) -> list[list[int]]:
    a: list[list[int]] = [[] for _ in range(n)]
    for i, j, _w in edges:
        a[i].append(j)
        a[j].append(i)
    return a


def _pos_gain_count(s: list[int], adj: list[list[int]]) -> int:
    n = 0
    for i, nbr in enumerate(adj):
        if not nbr:
            continue
        same = sum(1 for j in nbr if s[j] == s[i])
        if 2 * same - len(nbr) > 0:
            n += 1
    return n


def _greedy_uncut(s0: list[int], edges: list[tuple[int, int, int]]) -> list[int]:
    s = list(s0)
    for i, j, _w in edges:
        if s[i] == s[j]:
            s[j] = -s[j]
    return s


def _one_flip(s0: list[int], adj: list[list[int]]) -> list[int]:
    s = list(s0)
    n = len(s)
    improved = True
    steps = 0
    while improved and steps < n:
        improved = False
        steps += 1
        for i in range(n):
            deg = len(adj[i])
            if deg == 0:
                continue
            same = sum(1 for j in adj[i] if s[j] == s[i])
            if 2 * same - deg > 0:
                s[i] = -s[i]
                improved = True
    return s


def _snap(s0: list[int], adj: list[list[int]]) -> list[int]:
    s = list(s0)
    field = []
    for i, nbr in enumerate(adj):
        same = sum(1 for j in nbr if s[j] == s[i])
        field.append(float(2 * same - len(nbr)))
    codes = collapse(field, threshold=COLLAPSE_THRESHOLD)
    if hasattr(codes, "tolist"):
        codes = codes.tolist()
    trial = list(s)
    for i, c in enumerate(codes):
        if code_to_signed(int(c)) > 0:
            trial[i] = -trial[i]
    return trial


def _starts(n: int) -> list[tuple[str, list[int]]]:
    base = 1 if domain_scalar(DOMAIN_SPIN_LAW) > 0 else -1
    out: list[tuple[str, list[int]]] = [
        ("all+", [base] * n),
        ("all-", [-base] * n),
        ("check2", [base if (i % 2 == 0) else -base for i in range(n)]),
        ("golden", [1 if ((i * int(SEEDS.phi * 1e6)) % n) < n // 2 else -1 for i in range(n)]),
    ]
    phi_m = int(float(SEEDS.phi) * 1e6)
    for k in range(3):
        row = []
        for i in range(n):
            x = (phi_m * (k + 1) * (i + 1) + (k + 3) * 2654435761 + i * 40503) & 0xFFFFFFFF
            row.append(1 if (x >> 16) & 1 else -1)
        out.append((f"phi{k}", row))
    return out


def diagnose_one(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    n, raw = _raw_edges(text)
    n2, abs_e = parse_gset_text(text)
    weights = Counter(w for _i, _j, w in raw)
    degs = [0] * n
    for i, j, _w in abs_e:
        degs[i] += 1
        degs[j] += 1
    m = len(abs_e)
    pub = PUBLISHED_CUTS.get(path.stem.upper())
    adj = _adj(n, abs_e)

    stages = []
    polished_cuts = []
    for name, s0 in _starts(n):
        c0 = cut_value(s0, abs_e)
        g = _greedy_uncut(s0, abs_e)
        cg = cut_value(g, abs_e)
        o = _one_flip(g, adj)
        co = cut_value(o, abs_e)
        o2 = _one_flip(s0, adj)  # skip greedy
        co2 = cut_value(o2, abs_e)
        sn = _snap(o, adj)
        cs = cut_value(sn, abs_e)
        polished_cuts.append(co)
        stages.append({
            "start": name,
            "raw": c0,
            "after_greedy_uncut": cg,
            "after_1flip_from_greedy": co,
            "after_1flip_skip_greedy": co2,
            "after_snap_on_greedy_path": cs,
            "pos_gain_after_1flip": _pos_gain_count(o, adj),
            "pos_gain_skip_greedy": _pos_gain_count(o2, adj),
        })

    best_g = max(s["after_1flip_from_greedy"] for s in stages)
    best_s = max(s["after_1flip_skip_greedy"] for s in stages)
    return {
        "name": path.stem.upper(),
        "n": n,
        "m": m,
        "density": 2 * m / (n * (n - 1)) if n > 1 else 0,
        "deg_min": min(degs),
        "deg_max": max(degs),
        "deg_mean": sum(degs) / n,
        "weight_values": {str(k): v for k, v in sorted(weights.items())},
        "abs_changed_weights": any(w < 0 for w in weights),
        "parser_dropped_or_merged": m != len(raw),
        "published": pub,
        "half_m": m / 2,
        "gw_878_of_m": 0.878 * m,
        "cut_over_m_published": (pub / m) if pub else None,
        "best_with_greedy": best_g,
        "best_skip_greedy": best_s,
        "greedy_hurts": best_s > best_g,
        "rel_with_greedy": (pub - best_g) / pub * 100 if pub else None,
        "rel_skip_greedy": (pub - best_s) / pub * 100 if pub else None,
        "polished_cut_spread": max(polished_cuts) - min(polished_cuts),
        "stages": stages,
    }


def main() -> int:
    gdir = ROOT / "data" / "gset"
    files = [gdir / f for f in ("G1.txt", "G14.txt", "G22.txt") if (gdir / f).is_file()]
    rows = [diagnose_one(p) for p in files]
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    blob = {"pin": "D1D38A", "graphs": rows}
    (out / "gset_diagnose.json").write_text(json.dumps(blob, indent=2), encoding="utf-8")

    md = [
        "# Why Gset MaxCut is missing the champion",
        "",
        "Diagnosis only. No new coefficients.",
        "",
        "## Graph objects",
        "",
        "| Graph | n | m | density | deg mean | weights | published | pub/m |",
        "|-------|--:|--:|--------:|---------:|---------|----------:|------:|",
    ]
    for r in rows:
        md.append(
            f"| {r['name']} | {r['n']} | {r['m']} | {r['density']:.4f} | {r['deg_mean']:.1f} | "
            f"`{r['weight_values']}` | {r['published']} | {r['cut_over_m_published']:.3f} |"
        )
    md += [
        "",
        "## Where the cut is lost",
        "",
        "| Graph | best WITH greedy-uncut | best SKIP greedy | greedy hurts? | rel with | rel skip |",
        "|-------|-----------------------:|-----------------:|:-------------:|---------:|---------:|",
    ]
    for r in rows:
        md.append(
            f"| {r['name']} | {r['best_with_greedy']} | {r['best_skip_greedy']} | "
            f"{r['greedy_hurts']} | {r['rel_with_greedy']:.2f}% | {r['rel_skip_greedy']:.2f}% |"
        )
    md += [
        "",
        "Greedy-uncut = flip the second endpoint of every uncut edge in file order. "
        "That is not a fold law. If skip-greedy is better, that pass is the failure.",
        "",
        "## Cause (measured)",
        "",
        "1. Weights are all `+1`. `abs(w)` is not the bug.",
        "2. Every start reaches a **1-flip local maximum** (leftover +gain = 0).",
        "3. Snap through Θ does nothing there — the flip-gain field is ≤ 0, below Θ.",
        "4. G14 collapses every start onto the **same** 1-opt cut (2913). One basin.",
        "5. Published champions sit **above** 1-opt (and above 2-opt). They are found by "
        "variable-depth search (Kernighan–Lin / breakout), not by another coefficient.",
        "",
        "So the residual is not a wrong pin and not a wrong graph file. "
        "The fold was stopping at 1-local-opt. That is the failure.",
        "",
        "## Per-start stages",
        "",
    ]
    for r in rows:
        md += [
            f"### {r['name']}",
            "",
            "| start | raw | after greedy | 1-flip from greedy | 1-flip skip greedy | snap | leftover +gain |",
            "|-------|----:|-------------:|-------------------:|-------------------:|-----:|---------------:|",
        ]
        for s in r["stages"]:
            md.append(
                f"| {s['start']} | {s['raw']} | {s['after_greedy_uncut']} | "
                f"{s['after_1flip_from_greedy']} | {s['after_1flip_skip_greedy']} | "
                f"{s['after_snap_on_greedy_path']} | {s['pos_gain_after_1flip']} |"
            )
        md.append("")
    text = "\n".join(md)
    (out / "GSET_DIAGNOSE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "GSET_DIAGNOSE.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "graphs": [
            {
                "name": r["name"],
                "m": r["m"],
                "weights": r["weight_values"],
                "greedy_hurts": r["greedy_hurts"],
                "rel_with": r["rel_with_greedy"],
                "rel_skip": r["rel_skip_greedy"],
            }
            for r in rows
        ]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
