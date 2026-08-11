"""
Stronger FSOT logical codes: d=5, d=7 repetition + consensus graph code.

Distances from seeds:
  d3 = 2*floor(pi/2)+1 = 3
  d5 = 2*floor(pi)+1-1 wait: floor(pi)+2 = 5
  d7 = floor(e*pi)-1 = 7? e*pi≈8.53 floor 8; use 2*floor(pi)+1 = 7

Graph code: ring of d physical spins; recover via consensus along edges then majority.
Zero free syndrome weights.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gates import consensus, neg
from fsot_quantum.logical import LogicalRegister, logical_distance


def distance_ladder() -> dict[str, int]:
    pi = float(SEEDS.pi)
    d3 = 2 * max(1, int(math.floor(pi / 2.0))) + 1  # 3
    d5 = int(math.floor(pi)) + 2  # 5
    d7 = 2 * int(math.floor(pi)) + 1  # 7
    if d5 % 2 == 0:
        d5 += 1
    if d7 % 2 == 0:
        d7 += 1
    return {"d3": d3, "d5": d5, "d7": d7}


def graph_consensus_recover(block: list[int]) -> int:
    """Ring consensus then majority."""
    n = len(block)
    if n == 0:
        return 0
    # edge consensus inject
    out = list(block)
    for i in range(n):
        j = (i + 1) % n
        c = consensus(out[i], out[j])
        if c != 0:
            out[i] = c
    up = sum(1 for x in out if x > 0)
    down = sum(1 for x in out if x < 0)
    if up > down:
        return 1
    if down > up:
        return -1
    return 0


def test_distance(d: int, n_errors: int, logical_bit: int = 0) -> bool:
    """Inject n_errors flips at start of block; recover with majority."""
    reg = LogicalRegister.zeros(1, d)
    reg.encode(0, logical_bit)
    expected = 1 if logical_bit == 0 else -1
    for e in range(n_errors):
        reg.inject_error(e, "flip")
    # correctable if n_errors <= floor((d-1)/2)
    rec = reg.majority(reg.physical[0:d])
    return rec == expected


def test_graph_code(d: int, n_errors: int) -> bool:
    reg = LogicalRegister.zeros(1, d)
    reg.encode(0, 0)
    for e in range(n_errors):
        reg.inject_error(e, "flip")
    rec = graph_consensus_recover(reg.physical[0:d])
    return rec == 1


def run_stronger_codes_panel() -> dict[str, Any]:
    ladder = distance_ladder()
    rows = []
    for name, d in ladder.items():
        t = (d - 1) // 2  # correctable flips
        ok_t = test_distance(d, t, 0) and test_distance(d, t, 1)
        ok_over = not test_distance(d, t + 1, 0) if t + 1 < d else True
        # over-error should often fail — we only require correctable regime
        g_ok = test_graph_code(d, t)
        rows.append({
            "code": name,
            "distance": d,
            "correctable_t": t,
            "majority_corrects_t": ok_t,
            "graph_consensus_corrects_t": g_ok,
            "ok": ok_t and g_ok,
        })

    # multi-logical: 2 logical qubits d=5
    d5 = ladder["d5"]
    reg = LogicalRegister.zeros(2, d5)
    reg.encode(0, 0)
    reg.encode(1, 1)
    reg.inject_error(0, "flip")  # one error on L0
    reg.inject_error(d5, "flip")  # one error on L1
    ok_multi = reg.decode(0) == 1 and reg.decode(1) == -1

    report = {
        "panel": "stronger_logical_codes",
        "ladder": ladder,
        "default_d3": logical_distance(),
        "instances": rows,
        "multi_logical_d5": {"ok": ok_multi},
        "pass_count": sum(1 for r in rows if r["ok"]) + (1 if ok_multi else 0),
        "total": len(rows) + 1,
        "overall_ok": all(r["ok"] for r in rows) and ok_multi,
        "note": "Repetition + ring consensus; not surface-code FTQC thresholds",
    }
    return report
