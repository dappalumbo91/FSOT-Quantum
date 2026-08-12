"""
Longer lattice-surgery sequences — teleportation-style logical algorithms.

Uses existing merge/split/CNOT/ZZ folds as primitives:
  - logical SWAP = CNOT chain (3 CNOTs)
  - bit teleport: dest=0, CNOT(src, dest) copies bit (measure-and-copy fold)
  - 3-logical GHZ-class: CNOT(L0,L1), CNOT(L0,L2) from |x00> → |xxx>
  - teleportation circuit skeleton: copy then verify ZZ=+1

Not continuum FTQC teleportation thresholds.

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

from typing import Any

from fsot_quantum.lattice_surgery_fold import (
    LogicalPatch,
    logical_cnot_fold,
    logical_zz_measure_fold,
    merge_patches,
    split_merged,
)
from fsot_quantum.surface_code import surface_distances


def _encode(d: int, bit: int, label: str) -> LogicalPatch:
    p = LogicalPatch.zeros(d, label)
    p.encode(bit)
    return p


def apply_cnot(control: LogicalPatch, target: LogicalPatch) -> tuple[LogicalPatch, LogicalPatch, dict]:
    """CNOT fold that returns the output patches (re-encode from result bits)."""
    r = logical_cnot_fold(control, target)
    c = _encode(control.d, r["control_out"], control.label)
    t = _encode(target.d, r["target_out"], target.label)
    return c, t, r


def logical_swap_fold(a: LogicalPatch, b: LogicalPatch) -> dict[str, Any]:
    """SWAP = CNOT(a,b) CNOT(b,a) CNOT(a,b)."""
    a0 = 0 if a.logical_z() == 1 else 1
    b0 = 0 if b.logical_z() == 1 else 1
    a, b, r1 = apply_cnot(a, b)
    b, a, r2 = apply_cnot(b, a)
    a, b, r3 = apply_cnot(a, b)
    a1 = 0 if a.logical_z() == 1 else 1
    b1 = 0 if b.logical_z() == 1 else 1
    ok = a1 == b0 and b1 == a0 and r1["ok"] and r2["ok"] and r3["ok"]
    return {
        "op": "logical_swap_fold",
        "in": [a0, b0],
        "out": [a1, b1],
        "expect": [b0, a0],
        "ok": ok,
        "d": a.d,
    }


def logical_copy_fold(src: LogicalPatch) -> dict[str, Any]:
    """Teleport-style copy: dest|0>, CNOT(src, dest) → dest = src."""
    s = 0 if src.logical_z() == 1 else 1
    dest = _encode(src.d, 0, "D")
    src2, dest2, r = apply_cnot(src, dest)
    s2 = 0 if src2.logical_z() == 1 else 1
    d2 = 0 if dest2.logical_z() == 1 else 1
    zz = logical_zz_measure_fold(src2, dest2)
    ok = r["ok"] and s2 == s and d2 == s and zz["ok"] and zz["zz"] == 1
    return {
        "op": "logical_copy_teleport_fold",
        "src": s,
        "src_out": s2,
        "dest_out": d2,
        "zz": zz.get("zz"),
        "ok": ok,
        "d": src.d,
    }


def logical_ghz_class_fold(bit: int, d: int) -> dict[str, Any]:
    """
    Three-logical GHZ-class on bits: |x00> --CNOT01 CNOT02--> |xxx>.
    Same *job* as GHZ prepare, fold geometry.
    """
    a = _encode(d, bit, "A")
    b = _encode(d, 0, "B")
    c = _encode(d, 0, "C")
    a, b, r1 = apply_cnot(a, b)
    a, c, r2 = apply_cnot(a, c)
    bits = [
        0 if a.logical_z() == 1 else 1,
        0 if b.logical_z() == 1 else 1,
        0 if c.logical_z() == 1 else 1,
    ]
    ok = r1["ok"] and r2["ok"] and bits == [bit, bit, bit]
    return {
        "op": "logical_ghz_class_fold",
        "bit": bit,
        "out": bits,
        "ok": ok,
        "d": d,
    }


def logical_teleport_chain_fold(bit: int, d: int) -> dict[str, Any]:
    """
    A → B → C copy chain (two teleport-style copies).
    Final C equals original A.
    """
    a = _encode(d, bit, "A")
    c1 = logical_copy_fold(a)
    mid = _encode(d, c1["dest_out"], "B")
    c2 = logical_copy_fold(mid)
    ok = c1["ok"] and c2["ok"] and c2["dest_out"] == bit
    return {
        "op": "logical_teleport_chain_fold",
        "bit": bit,
        "mid": c1.get("dest_out"),
        "final": c2.get("dest_out"),
        "ok": ok,
        "d": d,
    }


def run_lattice_teleport_fold_panel() -> dict[str, Any]:
    ladder = surface_distances()
    rows: list[dict[str, Any]] = []
    for name, d in ladder.items():
        for ba, bb in ((0, 0), (0, 1), (1, 0), (1, 1)):
            r = logical_swap_fold(_encode(d, ba, "A"), _encode(d, bb, "B"))
            r["job"] = f"swap_{name}_{ba}{bb}"
            rows.append(r)
        for b in (0, 1):
            r = logical_copy_fold(_encode(d, b, "S"))
            r["job"] = f"copy_{name}_{b}"
            rows.append(r)
            r = logical_ghz_class_fold(b, d)
            r["job"] = f"ghz_{name}_{b}"
            rows.append(r)
            r = logical_teleport_chain_fold(b, d)
            r["job"] = f"teleport_chain_{name}_{b}"
            rows.append(r)

    ok_flags = [bool(r.get("ok")) for r in rows]
    return {
        "panel": "lattice_teleport_fold",
        "ladder": ladder,
        "instances": rows,
        "pass_count": sum(ok_flags),
        "total": len(ok_flags),
        "overall_ok": all(ok_flags) and len(ok_flags) > 0,
        "note": (
            "SWAP / copy / GHZ-class / A→B→C teleport chain as fold sequences. "
            "Not a device-scale FTQC teleportation threshold."
        ),
    }
