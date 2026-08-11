"""
Lattice-surgery style logical operations as pure FSOT folds.

Abstract planar patches (distance d) support:
  - encode logical |0>/|1>
  - merge two patches along a boundary (joint majority / consensus)
  - split a merged block back into two logicals
  - logical XX / ZZ measure via boundary product folds
  - logical CNOT skeleton: merge → measure → split (deterministic fold)

Not continuum lattice surgery FTQC thresholds — structure of the *job*
(logical multi-qubit ops) without Hilbert expansion.

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gates import consensus, neg
from fsot_quantum.surface_code import PlanarSurface, correct_once, surface_distances


@dataclass
class LogicalPatch:
    """One distance-d planar surface patch = one logical qubit (bit channel)."""

    d: int
    surf: PlanarSurface
    label: str = "L"

    @classmethod
    def zeros(cls, d: int, label: str = "L") -> "LogicalPatch":
        s = PlanarSurface(d)
        s.encode_logical_0()
        return cls(d=d, surf=s, label=label)

    def encode(self, bit: int) -> None:
        if bit:
            self.surf.encode_logical_1()
        else:
            self.surf.encode_logical_0()

    def logical_z(self) -> int:
        return self.surf.logical_z()

    def inject_and_correct(self, sites: list[int]) -> bool:
        self.surf.inject_bit_flips(sites)
        correct_once(self.surf)
        return all(x == 0 for x in self.surf.z_syndrome())


@dataclass
class MergedBlock:
    """Two patches merged along vertical boundary — joint physical array."""

    d: int
    # physical: d rows × (2d) cols layout (side by side)
    data: list[int]
    labels: tuple[str, str] = ("L0", "L1")

    @property
    def width(self) -> int:
        return 2 * self.d

    def idx(self, r: int, c: int) -> int:
        return r * self.width + c

    def logical_z_left(self) -> int:
        p = 1
        for r in range(self.d):
            p *= self.data[self.idx(r, 0)]
        return p

    def logical_z_right(self) -> int:
        p = 1
        for r in range(self.d):
            p *= self.data[self.idx(r, self.d)]  # left col of right patch
        return p

    def boundary_product(self) -> int:
        """Product along merge seam (between col d-1 and d)."""
        p = 1
        for r in range(self.d):
            # consensus of left-right boundary pair
            a = self.data[self.idx(r, self.d - 1)]
            b = self.data[self.idx(r, self.d)]
            c = consensus(a, b)
            p *= c if c != 0 else a * b
        return 1 if p >= 0 else -1


def merge_patches(a: LogicalPatch, b: LogicalPatch) -> MergedBlock:
    """Place patches side-by-side; apply boundary consensus fold."""
    assert a.d == b.d
    d = a.d
    w = 2 * d
    data = [1] * (d * w)
    for r in range(d):
        for c in range(d):
            data[r * w + c] = a.surf.data[r * d + c]
            data[r * w + (c + d)] = b.surf.data[r * d + c]
    # Boundary consensus fold: glue seam
    for r in range(d):
        i = r * w + (d - 1)
        j = r * w + d
        c = consensus(data[i], data[j])
        if c != 0:
            data[i] = c
            data[j] = c
    return MergedBlock(d=d, data=data, labels=(a.label, b.label))


def split_merged(block: MergedBlock) -> tuple[LogicalPatch, LogicalPatch]:
    """Split merged block into two patches; majority-decode each."""
    d = block.d
    w = block.width
    left = LogicalPatch.zeros(d, block.labels[0])
    right = LogicalPatch.zeros(d, block.labels[1])
    for r in range(d):
        for c in range(d):
            left.surf.data[r * d + c] = block.data[r * w + c]
            right.surf.data[r * d + c] = block.data[r * w + (c + d)]
    # Recover logical by majority on left column product already in logical_z
    # Clean residual with correct_once if needed
    if any(left.surf.z_syndrome()):
        correct_once(left.surf)
    if any(right.surf.z_syndrome()):
        correct_once(right.surf)
    return left, right


def logical_cnot_fold(control: LogicalPatch, target: LogicalPatch) -> dict[str, Any]:
    """
    Lattice-surgery CNOT skeleton (deterministic fold):
      1) merge control|target
      2) boundary product as joint measure class
      3) if boundary indicates anti-align for CNOT action, flip target logical
      4) split

    For CSS bit-channel abstract: CNOT(c,t): t ^= c in {0,1} with
      |0>_L → logical_z +1, |1>_L → logical_z -1
    """
    c_bit = 0 if control.logical_z() == 1 else 1
    t_bit = 0 if target.logical_z() == 1 else 1
    expect_t = t_bit ^ c_bit

    merged = merge_patches(control, target)
    seam = merged.boundary_product()
    # CNOT fold: if control is |1> (lz=-1), flip right patch columns
    if c_bit == 1:
        d, w = merged.d, merged.width
        for r in range(d):
            for c in range(d, w):
                merged.data[merged.idx(r, c)] = neg(merged.data[merged.idx(r, c)])

    left, right = split_merged(merged)
    got_c = 0 if left.logical_z() == 1 else 1
    got_t = 0 if right.logical_z() == 1 else 1
    ok = got_c == c_bit and got_t == expect_t
    return {
        "op": "logical_cnot_fold",
        "control_in": c_bit,
        "target_in": t_bit,
        "control_out": got_c,
        "target_out": got_t,
        "expect_target": expect_t,
        "seam": seam,
        "ok": ok,
        "d": control.d,
    }


def logical_zz_measure_fold(a: LogicalPatch, b: LogicalPatch) -> dict[str, Any]:
    """ZZ logical measure = product of logical Z after merge seam fold."""
    za = a.logical_z()
    zb = b.logical_z()
    merged = merge_patches(a, b)
    # ZZ = za * zb on independent patches
    zz = za * zb
    # Seam-based estimate after merge
    seam = merged.boundary_product()
    # After merge, product of left and right logical columns
    zz_merged = merged.logical_z_left() * merged.logical_z_right()
    ok = zz_merged == zz
    return {
        "op": "logical_zz_measure_fold",
        "zz": zz,
        "zz_merged": zz_merged,
        "seam": seam,
        "ok": ok,
        "d": a.d,
    }


def run_lattice_surgery_fold_panel() -> dict[str, Any]:
    ladder = surface_distances()
    rows = []

    for name, d in ladder.items():
        # Encode / measure identity
        p = LogicalPatch.zeros(d, "A")
        p.encode(0)
        rows.append({
            "job": f"encode0_{name}",
            "ok": p.logical_z() == 1,
            "d": d,
        })
        p.encode(1)
        rows.append({
            "job": f"encode1_{name}",
            "ok": p.logical_z() == -1,
            "d": d,
        })

        # Merge/split roundtrip preserves logicals
        a = LogicalPatch.zeros(d, "A")
        b = LogicalPatch.zeros(d, "B")
        a.encode(0)
        b.encode(1)
        m = merge_patches(a, b)
        a2, b2 = split_merged(m)
        rows.append({
            "job": f"merge_split_{name}",
            "ok": a2.logical_z() == 1 and b2.logical_z() == -1,
            "d": d,
            "lz": [a2.logical_z(), b2.logical_z()],
        })

        # ZZ measure all pairs of bits
        for ba, bb in ((0, 0), (0, 1), (1, 0), (1, 1)):
            a = LogicalPatch.zeros(d, "A")
            b = LogicalPatch.zeros(d, "B")
            a.encode(ba)
            b.encode(bb)
            r = logical_zz_measure_fold(a, b)
            r["job"] = f"zz_{name}_{ba}{bb}"
            rows.append(r)

        # CNOT all input pairs
        for bc, bt in ((0, 0), (0, 1), (1, 0), (1, 1)):
            c = LogicalPatch.zeros(d, "C")
            t = LogicalPatch.zeros(d, "T")
            c.encode(bc)
            t.encode(bt)
            r = logical_cnot_fold(c, t)
            r["job"] = f"cnot_{name}_{bc}{bt}"
            rows.append(r)

        # Error on control then CNOT still works if weight-1 correctable
        c = LogicalPatch.zeros(d, "C")
        t = LogicalPatch.zeros(d, "T")
        c.encode(1)
        t.encode(0)
        ok_err = c.inject_and_correct([0])
        r = logical_cnot_fold(c, t)
        rows.append({
            "job": f"cnot_after_w1_{name}",
            "ok": ok_err and r["ok"],
            "d": d,
            "correct_ok": ok_err,
            "cnot_ok": r["ok"],
        })

    ok_flags = [bool(r.get("ok")) for r in rows]
    report = {
        "panel": "lattice_surgery_fold",
        "ladder": ladder,
        "instances": rows,
        "pass_count": sum(ok_flags),
        "total": len(ok_flags),
        "overall_ok": all(ok_flags) and len(ok_flags) > 0,
        "note": (
            "Abstract merge/split/CNOT/ZZ folds on planar patches — "
            "logical multi-qubit jobs without Hilbert surgery sim. "
            "Not a continuum FTQC threshold claim."
        ),
    }
    return report
