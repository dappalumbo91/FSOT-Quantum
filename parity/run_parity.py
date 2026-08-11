#!/usr/bin/env python3
"""Parity: fsot_lib + quantum domain vs vendor/fsot_compute.py (pin D1D38A)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import pack_u64, unpack_u64
from fsot_quantum.domains import domain_scalar


def main() -> int:
    from vendor import fsot_compute as f

    pin = hashlib.sha256((ROOT / "vendor" / "fsot_compute.py").read_bytes()).hexdigest()[:6].upper()
    report = {"pin": pin, "checks": []}

    def add(name, ok, **kw):
        report["checks"].append({"name": name, "ok": ok, **kw})

    add("pin_D1D38A", pin == "D1D38A", got=pin)
    for name in ("Quantum_Mechanics", "Quantum_Computing"):
        o, v = float(domain_scalar(name)), float(f.domain_scalar(name))
        add(f"scalar_{name}", abs(o - v) < 1e-10, ours=o, vendor=v)
    thr_v = float(f.C_EFF * f.P_VAR)
    add("collapse_threshold", abs(COLLAPSE_THRESHOLD - thr_v) < 1e-12, ours=COLLAPSE_THRESHOLD, vendor=thr_v)
    add("k", abs(SEEDS.k - float(f.K)) < 1e-12, ours=SEEDS.k, vendor=float(f.K))
    codes = [0, 1, 2, 0, 1, 2] * 5 + [0, 1]
    add("pack", unpack_u64(pack_u64(codes)) == codes)

    # golden from FSOT-GPU if present
    golden = ROOT / "parity" / "golden.json"
    if golden.is_file():
        g = json.loads(golden.read_text(encoding="utf-8"))
        add("golden_present", True, keys=list(g.keys())[:8])

    report["overall_ok"] = all(c["ok"] for c in report["checks"])
    out = ROOT / "results" / "parity.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
