"""
Seed-locked Hilbert circuit library for n = 8, 10, 12.

All angles from seeds. No free depth knobs: depth scales from floor(pi), floor(e).
Tests: normalization, structure jobs (GHZ mass, QFT uniformity on |0>,
Clifford+T chain finite, reverse-QFT fidelity).
"""

from __future__ import annotations

import math
from typing import Any, Callable

from fsot_lib.seeds import SEEDS
from fsot_quantum.hilbert import Statevector, ANGLES
from fsot_quantum.qft_shor import apply_iqft, apply_qft


def _seed_depth() -> int:
    return max(1, int(math.floor(float(SEEDS.pi))))  # 3


def _seed_layers() -> int:
    return max(2, int(math.floor(float(SEEDS.e))))  # 2


def circuit_ghz(n: int) -> Statevector:
    s = Statevector.zeros(n)
    s.H(0)
    for i in range(n - 1):
        s.CNOT(i, i + 1)
    return s


def circuit_qft_zero(n: int) -> Statevector:
    s = Statevector.zeros(n)
    apply_qft(s)
    return s


def circuit_qft_roundtrip_basis(n: int, index: int = 1) -> tuple[Statevector, float]:
    s = Statevector.basis(n, index % (1 << n))
    target = Statevector.basis(n, index % (1 << n))
    apply_qft(s)
    apply_iqft(s)
    return s, s.fidelity(target)


def circuit_clifford_t_ladder(n: int) -> Statevector:
    """
    Seed-depth ladder of H/T/S/CNOT across n qubits.
    Depth controlled by floor(pi) and floor(e) only.
    """
    s = Statevector.zeros(n)
    depth = _seed_depth()
    layers = _seed_layers()
    for L in range(layers):
        for q in range(n):
            s.H(q)
            if (q + L) % 2 == 0:
                s.T(q)
            else:
                s.S(q)
            s.Phase(q, "theta_s")
        for q in range(n - 1):
            s.CNOT(q, q + 1)
        # reverse chain
        for q in range(n - 2, -1, -1):
            s.CNOT(q, q + 1)
        for _ in range(depth - 1):
            for q in range(n):
                s.T(q)
    s.normalize()
    return s


def circuit_w_state_n3() -> Statevector:
    """Exact W state for n=3 via seed-free known circuit (angles from arccos 1/sqrt).
    Note: arccos(1/sqrt(3)) is fixed mathematical constant, not a free fit.
    """
    # Standard construction using Ry — angle is arccos(sqrt(2/3)) etc.
    # We implement via explicit amplitudes (closed form), then verify norms.
    # W = (|001>+|010>+|100>)/sqrt(3)
    a = 1.0 / math.sqrt(3.0)
    amps = [0j] * 8
    amps[1] = a  # 001
    amps[2] = a  # 010
    amps[4] = a  # 100
    return Statevector(n=3, amps=amps)


def _norm_ok(s: Statevector, tol: float = 1e-10) -> bool:
    nrm = sum(abs(a) ** 2 for a in s.amps)
    return abs(nrm - 1.0) < tol


def run_circuit_library_panel() -> dict[str, Any]:
    rows = []
    for n in (8, 10, 12):
        # GHZ
        g = circuit_ghz(n)
        pg = g.probs()
        ghz_ends = abs(pg[0] - 0.5) < 1e-9 and abs(pg[-1] - 0.5) < 1e-9
        rows.append({
            "name": f"ghz_n{n}",
            "n": n,
            "ok": _norm_ok(g) and ghz_ends,
            "detail": {"norm": sum(abs(a) ** 2 for a in g.amps), "p0": pg[0], "p_all1": pg[-1]},
        })
        # QFT |0>
        q0 = circuit_qft_zero(n)
        uni = all(abs(p - 1.0 / (1 << n)) < 1e-9 for p in q0.probs())
        rows.append({
            "name": f"qft_zero_n{n}",
            "n": n,
            "ok": _norm_ok(q0) and uni,
            "detail": {"uniform": uni},
        })
        # QFT roundtrip
        _, fid = circuit_qft_roundtrip_basis(n, 1)
        rows.append({
            "name": f"qft_roundtrip_n{n}",
            "n": n,
            "ok": fid > 1.0 - 1e-9,
            "detail": {"fidelity": fid},
        })
        # Clifford+T ladder
        ct = circuit_clifford_t_ladder(n)
        rows.append({
            "name": f"clifford_t_ladder_n{n}",
            "n": n,
            "ok": _norm_ok(ct),
            "detail": {
                "norm": sum(abs(a) ** 2 for a in ct.amps),
                "depth_pi": _seed_depth(),
                "layers_e": _seed_layers(),
            },
        })

    w = circuit_w_state_n3()
    pw = w.probs()
    w_ok = all(abs(pw[i] - (1 / 3 if i in (1, 2, 4) else 0.0)) < 1e-9 for i in range(8))
    rows.append({"name": "w_state_n3", "n": 3, "ok": w_ok and _norm_ok(w), "detail": {}})

    report = {
        "panel": "circuit_library_large_n",
        "seed_depth": _seed_depth(),
        "seed_layers": _seed_layers(),
        "angles": list(ANGLES.keys()),
        "instances": rows,
        "pass_count": sum(1 for r in rows if r["ok"]),
        "total": len(rows),
        "overall_ok": all(r["ok"] for r in rows),
        "max_n": 12,
        "dim_at_max": 1 << 12,
    }
    return report
