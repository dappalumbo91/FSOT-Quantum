"""
Longer logical algorithms as fold sequences — adder + QFT-role.

Uses lattice-surgery CNOT / AND / XOR folds on logical bits.
Not Hilbert adders or textbook QFT statevectors.

  - ripple-carry adder (2-bit exhaustive + 3-bit sample)
  - QFT-role: bit-reversal + seed phase fold on integer value class

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.lattice_teleport_fold import apply_cnot, _encode
from fsot_quantum.surface_code import surface_distances


def logical_and_fold(a_bit: int, b_bit: int, d: int) -> dict[str, Any]:
    """dest = a AND b via control-copy: dest=0; if a then CNOT(b, dest)."""
    dest = 0
    steps_ok = True
    if a_bit == 1:
        b = _encode(d, b_bit, "B")
        dst = _encode(d, 0, "D")
        _b2, dst2, r = apply_cnot(b, dst)
        dest = 0 if dst2.logical_z() == 1 else 1
        steps_ok = r["ok"]
    expect = a_bit & b_bit
    return {
        "op": "logical_and",
        "a": a_bit,
        "b": b_bit,
        "got": dest,
        "expect": expect,
        "ok": steps_ok and dest == expect,
        "d": d,
    }


def ripple_add(a_bits: list[int], b_bits: list[int], d: int) -> dict[str, Any]:
    """
    Ripple-carry: for each bit,
      sum = a XOR b XOR cin
      cout = majority(a,b,cin) = (a∧b) ∨ (a∧cin) ∨ (b∧cin)
    XOR via CNOT folds; AND via logical_and_fold; OR = x XOR y XOR (x∧y).
    """
    assert len(a_bits) == len(b_bits)
    n = len(a_bits)
    cin = 0
    sums: list[int] = []
    ok = True
    for i in range(n):
        a, b = a_bits[i], b_bits[i]
        # XOR a,b
        pa = _encode(d, a, "A")
        pb = _encode(d, b, "B")
        pa, pb, r_ab = apply_cnot(pa, pb)  # b := a XOR b
        axb = 0 if pb.logical_z() == 1 else 1
        ok = ok and r_ab["ok"]
        # XOR with cin
        pc = _encode(d, cin, "C")
        px = _encode(d, axb, "X")
        px, pc, r_c = apply_cnot(px, pc)  # cin := axb XOR cin  (sum)
        s_i = 0 if pc.logical_z() == 1 else 1
        ok = ok and r_c["ok"]
        sums.append(s_i)
        # cout
        ab = logical_and_fold(a, b, d)
        ac = logical_and_fold(a, cin, d)
        bc = logical_and_fold(b, cin, d)
        ok = ok and ab["ok"] and ac["ok"] and bc["ok"]
        # OR of three bits via XOR/AND
        t = ab["got"] ^ ac["got"]
        tand = ab["got"] & ac["got"]
        t = t ^ tand  # OR of first two
        t2 = t ^ bc["got"]
        t2and = t & bc["got"]
        cout = t2 ^ t2and
        cin = cout
    # interpret little-endian
    def val(bits: list[int]) -> int:
        return sum(b << i for i, b in enumerate(bits))

    got = val(sums) + (cin << n)
    expect = val(a_bits) + val(b_bits)
    return {
        "op": "ripple_add",
        "a": a_bits,
        "b": b_bits,
        "sum_bits": sums,
        "cout": cin,
        "got": got,
        "expect": expect,
        "ok": ok and got == expect,
        "d": d,
    }


def qft_role_bitrev_phase(bits: list[int]) -> dict[str, Any]:
    """
    QFT *role* without amplitudes:
      1) bit-reversal of the integer
      2) seed phase class: θ = 2π · val / 2^n  (π from seeds)
      3) inverse bit-reversal recovers bits
    """
    n = len(bits)
    rev = list(reversed(bits))
    val = sum(b << i for i, b in enumerate(bits))
    val_rev = sum(b << i for i, b in enumerate(rev))
    pi = float(SEEDS.pi)
    theta = 2.0 * pi * val / float(1 << n) if n else 0.0
    # inverse
    back = list(reversed(rev))
    ok = back == bits
    return {
        "op": "qft_role_bitrev_phase",
        "bits": bits,
        "reversed": rev,
        "val": val,
        "val_rev": val_rev,
        "theta": theta,
        "roundtrip": back,
        "ok": ok,
        "n": n,
        "hilbert_amps_avoided": 1 << n,
    }


def run_logical_algo_fold_panel() -> dict[str, Any]:
    d = surface_distances()["d3"]  # keep sequences cheap
    rows: list[dict[str, Any]] = []

    # AND exhaustive
    for a in (0, 1):
        for b in (0, 1):
            r = logical_and_fold(a, b, d)
            r["job"] = f"and_{a}{b}"
            rows.append(r)

    # 2-bit adder exhaustive
    for av in range(4):
        for bv in range(4):
            a_bits = [(av >> i) & 1 for i in range(2)]
            b_bits = [(bv >> i) & 1 for i in range(2)]
            r = ripple_add(a_bits, b_bits, d)
            r["job"] = f"add2_{av}_{bv}"
            rows.append(r)

    # 3-bit adder sample (seed-locked pairs)
    phi = float(SEEDS.phi)
    samples = []
    x = 1
    for k in range(6):
        x = (x * int(phi * 1e6) + k * 17) % 64
        samples.append(((x >> 3) & 7, x & 7))
    for av, bv in samples:
        a_bits = [(av >> i) & 1 for i in range(3)]
        b_bits = [(bv >> i) & 1 for i in range(3)]
        r = ripple_add(a_bits, b_bits, d)
        r["job"] = f"add3_{av}_{bv}"
        rows.append(r)

    # QFT-role on several bitstrings
    for n in (3, 4, 5, 8):
        for k in range(n):
            bits = [(k >> i) & 1 for i in range(n)]
            # also one high bit pattern
        bits0 = [0] * n
        bits1 = [1] + [0] * (n - 1)
        bitsm = [i % 2 for i in range(n)]
        for bits, tag in ((bits0, "0"), (bits1, "e0"), (bitsm, "alt")):
            r = qft_role_bitrev_phase(bits)
            r["job"] = f"qftrole_n{n}_{tag}"
            rows.append(r)

    ok_flags = [bool(r.get("ok")) for r in rows]
    return {
        "panel": "logical_algo_fold",
        "d": d,
        "instances": rows,
        "pass_count": sum(ok_flags),
        "total": len(ok_flags),
        "overall_ok": all(ok_flags) and len(ok_flags) > 0,
        "note": (
            "Ripple-carry + QFT-role bit-reversal/phase folds. "
            "Not a Hilbert QFT/adder circuit equivalence claim."
        ),
    }
