"""
Wider arithmetic as fold sequences — 4-bit add samples + modular multiply.

QC job analog: quantum adders / modular multiply in Shor.
FSOT: ripple-carry + shift-add multiply on logical bits (not 2^n QFT multiply).

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.logical_algo_fold import ripple_add
from fsot_quantum.surface_code import surface_distances


def _bits(x: int, n: int) -> list[int]:
    return [(int(x) >> i) & 1 for i in range(n)]


def _val(bits: list[int]) -> int:
    return sum(b << i for i, b in enumerate(bits))


def modular_multiply_fold(a: int, b: int, N: int, *, n_bits: int, d: int) -> dict[str, Any]:
    """
    Shift-add multiply then reduce mod N.
    Each add is a ripple-carry fold on n_bits+2 (room for carry).
    """
    # width must hold a*b (not just a,b)
    width = 2 * n_bits + 1
    acc = 0
    aa = a
    ok = True
    adds = 0
    for i in range(n_bits):
        if (b >> i) & 1:
            r = ripple_add(_bits(acc, width), _bits(aa, width), d)
            ok = ok and r["ok"]
            acc = int(r["got"])
            adds += 1
        r2 = ripple_add(_bits(aa, width), _bits(aa, width), d)
        ok = ok and r2["ok"]
        aa = int(r2["got"])
    expect_prod = a * b
    expect_mod = (a * b) % N
    prod_ok = acc == expect_prod
    got = acc % N
    return {
        "op": "modular_multiply_fold",
        "a": a,
        "b": b,
        "N": N,
        "product_fold": acc,
        "got": got,
        "expect_product": expect_prod,
        "expect": expect_mod,
        "fold_adds": adds,
        "ok": ok and prod_ok and got == expect_mod,
        "n_bits": n_bits,
        "d": d,
        "hilbert_amps_if_QFT_mul": 1 << (2 * n_bits + max(1, N.bit_length())),
    }


def run_fold_arith_panel() -> dict[str, Any]:
    d = surface_distances()["d3"]
    rows: list[dict[str, Any]] = []

    # 4-bit adder samples (seed-locked, not 16×16 exhaustive)
    phi = float(SEEDS.phi)
    x = 1
    for k in range(8):
        x = (x * int(phi * 1e6) + 31 * (k + 1)) % 256
        av, bv = (x >> 4) & 15, x & 15
        r = ripple_add(_bits(av, 4), _bits(bv, 4), d)
        r["job"] = f"add4_{av}_{bv}"
        rows.append(r)

    # Modular multiply: Shor-like (a*b mod N) small cases
    cases = [
        (3, 5, 7, 3),
        (2, 7, 15, 4),
        (4, 4, 15, 4),
        (5, 3, 21, 5),
        (6, 7, 15, 4),
        (8, 3, 21, 5),
    ]
    for a, b, N, nb in cases:
        r = modular_multiply_fold(a, b, N, n_bits=nb, d=d)
        r["job"] = f"mulmod_{a}_{b}_{N}"
        rows.append(r)

    ok_flags = [bool(r.get("ok")) for r in rows]
    return {
        "panel": "fold_arith_wider",
        "d": d,
        "instances": rows,
        "pass_count": sum(ok_flags),
        "total": len(ok_flags),
        "overall_ok": all(ok_flags) and len(ok_flags) > 0,
        "note": (
            "4-bit add samples + shift-add modular multiply via ripple folds. "
            "Not a Hilbert modular-mult circuit claim."
        ),
    }
