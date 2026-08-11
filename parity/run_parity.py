#!/usr/bin/env python3
"""Parity: local seeds/scalar vs vendor/fsot_compute.py + pack codes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.scalar import domain_scalar
from fsot_quantum.seeds import COLLAPSE_THRESHOLD, SEEDS, authority_pin
from fsot_quantum.trinary import pack_u64, unpack_u64


def main() -> int:
    from vendor import fsot_compute as f

    report = {"pin": authority_pin(), "checks": []}

    def add(name, ok, **kw):
        report["checks"].append({"name": name, "ok": ok, **kw})

    add("pin_D1D38A", report["pin"] == "D1D38A", got=report["pin"])

    for name in ("Quantum_Mechanics", "Quantum_Computing"):
        o, v = float(domain_scalar(name)), float(f.domain_scalar(name))
        add(f"scalar_{name}", abs(o - v) < 1e-10, ours=o, vendor=v)

    thr_v = float(f.C_EFF * f.P_VAR)
    add("collapse_threshold", abs(COLLAPSE_THRESHOLD - thr_v) < 1e-12, ours=COLLAPSE_THRESHOLD, vendor=thr_v)

    # seed layer spots
    add("k", abs(SEEDS.k - float(f.K)) < 1e-12, ours=SEEDS.k, vendor=float(f.K))
    add("c_eff", abs(SEEDS.c_eff - float(f.C_EFF)) < 1e-12)
    add("p_var", abs(SEEDS.p_var - float(f.P_VAR)) < 1e-12)

    codes = [0, 1, 2, 0, 1, 2] * 5 + [0, 1]
    assert len(codes) == 32
    add("pack", unpack_u64(pack_u64(codes)) == codes)

    report["overall_ok"] = all(c["ok"] for c in report["checks"])
    out = ROOT / "results" / "parity.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
