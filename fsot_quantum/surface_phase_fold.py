"""
Surface + phase channel as FSOT folds — not larger Hilbert spaces.

Extends planar surface substrate with:
  1) Phase-flip (X-stabilizer dual) fold — same grid, dual incidence
  2) Nested decode: bit-flip fold then phase-flip fold
  3) Logical phase class from domain S (no QPE statevector)
  4) Multi-distance fold ladder d=3/5/7

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.fold_complexity import fold_depth_ladder, nested_fold_scalars
from fsot_quantum.gates import neg
from fsot_quantum.surface_code import (
    PlanarSurface,
    correct_once,
    decoder_table,
    surface_distances,
    test_correctable_weight,
)


class PhaseDualSurface:
    """
    Phase-flip channel on the dual of the planar grid.

    For vertex-data Z-plaquette codes, X-type errors are dual:
    we reuse the same incidence but interpret spins as phase trits
    and apply the same min-weight syndrome decoder (CSS duality fold).
    """

    def __init__(self, d: int):
        self.inner = PlanarSurface(d)
        self.d = d

    def encode_logical_plus(self) -> None:
        """|+>_L ~ logical 0 for phase channel bookkeeping."""
        self.inner.encode_logical_0()

    def encode_logical_minus(self) -> None:
        self.inner.encode_logical_1()

    def inject_phase_flips(self, sites: list[int]) -> None:
        # same spin flip algebra on dual channel
        self.inner.inject_bit_flips(sites)

    def correct_phase(self) -> list[int]:
        return correct_once(self.inner)

    def logical_phase(self) -> int:
        return self.inner.logical_z()

    def syndrome_clean(self) -> bool:
        return all(s == 0 for s in self.inner.z_syndrome())


def nested_bit_phase_correct(
    d: int,
    bit_sites: list[int],
    phase_sites: list[int],
    *,
    logical: int = 0,
) -> dict[str, Any]:
    """
    Nested fold: correct bit channel then phase channel on independent copies
    (CSS independent decoders). Combined logical OK if both channels recover.
    """
    # Bit channel
    bit = PlanarSurface(d)
    if logical == 0:
        bit.encode_logical_0()
        expect = 1
    else:
        bit.encode_logical_1()
        expect = -1
    bit.inject_bit_flips(bit_sites)
    correct_once(bit)
    bit_ok = all(s == 0 for s in bit.z_syndrome()) and bit.logical_z() == expect

    # Phase channel (dual fold)
    ph = PhaseDualSurface(d)
    if logical == 0:
        ph.encode_logical_plus()
    else:
        ph.encode_logical_minus()
    ph.inject_phase_flips(phase_sites)
    ph.correct_phase()
    phase_ok = ph.syndrome_clean() and ph.logical_phase() == expect

    return {
        "d": d,
        "bit_ok": bit_ok,
        "phase_ok": phase_ok,
        "ok": bit_ok and phase_ok,
        "method": "nested_css_bit_phase_folds",
    }


def phase_class_surface_fold() -> dict[str, Any]:
    """
    Logical phase class without QPE Hilbert register:
    domain S folds + surface distance ladder as structural depth.
    """
    s_qm = domain_scalar(DOMAIN_SPIN_LAW)
    s_qc = domain_scalar(DOMAIN_COMPUTE)
    ladder = surface_distances()
    folds = nested_fold_scalars(fold_depth_ladder()["mid"])
    # Phase depth index from distance
    depth = ladder["d5"]  # seed ladder mid
    ok = s_qm > 0 and s_qc < 0 and depth >= 5
    return {
        "job": "phase_class_surface_fold",
        "ok": ok,
        "S_QM": s_qm,
        "S_QC": s_qc,
        "class_QM": "emergence" if s_qm > 0 else "damping",
        "class_QC": "emergence" if s_qc > 0 else "damping",
        "surface_ladder": ladder,
        "phase_depth_d": depth,
        "nested_domain_folds": folds,
        "method": "D_eff_plus_surface_distance_fold",
        "hilbert_amps_avoided": "2^{t+n} QPE register",
    }


def run_surface_phase_fold_panel() -> dict[str, Any]:
    ladder = surface_distances()
    rows = []

    # Warm tables
    for d in ladder.values():
        decoder_table(d, (d - 1) // 2)

    # Bit channel w1 (reuse surface tests)
    for name, d in ladder.items():
        n = d * d
        w1 = sum(1 for i in range(n) if test_correctable_weight(d, [i], 0))
        rows.append({
            "job": f"bit_w1_{name}",
            "d": d,
            "ok": w1 == n,
            "w1_frac": w1 / n,
            "channel": "bit",
        })

    # Phase channel w1
    for name, d in ladder.items():
        n = d * d
        ok_c = 0
        for i in range(n):
            ph = PhaseDualSurface(d)
            ph.encode_logical_plus()
            ph.inject_phase_flips([i])
            ph.correct_phase()
            if ph.syndrome_clean() and ph.logical_phase() == 1:
                ok_c += 1
        rows.append({
            "job": f"phase_w1_{name}",
            "d": d,
            "ok": ok_c == n,
            "w1_frac": ok_c / n,
            "channel": "phase",
        })

    # Nested bit+phase simultaneous correctable weight-1 each
    for name, d in ladder.items():
        t = (d - 1) // 2
        n_ok = 0
        n_try = max(8, int(math.floor(float(SEEDS.e) * 4)))
        phi = float(SEEDS.phi)
        for k in range(n_try):
            # two independent sites via phi walk
            b = (k * int(phi * 1e6) + d * 17) % (d * d)
            p = (k * 1664525 + d * 31) % (d * d)
            r = nested_bit_phase_correct(d, [b], [p], logical=0)
            if r["ok"]:
                n_ok += 1
        rows.append({
            "job": f"nested_bit_phase_{name}",
            "d": d,
            "ok": n_ok == n_try,
            "pass": f"{n_ok}/{n_try}",
            "channel": "nested",
            "correctable_t": t,
        })

    # Logical |1> on both channels
    for name, d in ladder.items():
        r0 = nested_bit_phase_correct(d, [0], [1], logical=1)
        rows.append({
            "job": f"nested_logical1_{name}",
            "d": d,
            "ok": r0["ok"],
            "channel": "nested_L1",
        })

    phase_class = phase_class_surface_fold()
    rows.append(phase_class)

    ok_flags = [bool(r.get("ok")) for r in rows]
    report = {
        "panel": "surface_phase_fold",
        "ladder": ladder,
        "instances": rows,
        "pass_count": sum(ok_flags),
        "total": len(ok_flags),
        "overall_ok": all(ok_flags) and len(ok_flags) > 0,
        "note": (
            "Bit + phase CSS folds on planar surface geometry; "
            "phase class via D_eff — not QPE Hilbert expansion. "
            "Not a device-scale FTQC threshold certificate."
        ),
    }
    return report
