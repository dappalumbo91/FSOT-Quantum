"""
Verify: pin D1D38A + fsot_lib owned smoke + quantum domain fold + vendor parity.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.scalar import compute_scalar
from fsot_lib.trinary import pack_u64, unpack_u64
from fsot_quantum.domains import domain_scalar
from fsot_quantum.engine import QuantumEngine


PIN_EXPECTED = "D1D38A"


def authority_pin() -> str:
    p = ROOT / "vendor" / "fsot_compute.py"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:6].upper()


def _close(a: float, b: float, rel: float = 1e-9) -> bool:
    return abs(a - b) <= max(1e-12, rel * max(abs(a), abs(b)))


def run_all() -> dict:
    results = []

    pin = authority_pin()
    results.append({"name": "authority_pin", "ok": pin == PIN_EXPECTED, "got": pin})

    # vendor parity
    try:
        from vendor import fsot_compute as f

        checks = {}
        for name in ("Quantum_Mechanics", "Quantum_Computing"):
            o, v = float(domain_scalar(name)), float(f.domain_scalar(name))
            checks[name] = {"ours": o, "vendor": v, "ok": _close(o, v, 1e-10)}
        thr_v = float(f.C_EFF * f.P_VAR)
        checks["theta"] = {
            "ours": COLLAPSE_THRESHOLD,
            "vendor": thr_v,
            "ok": _close(COLLAPSE_THRESHOLD, thr_v, 1e-12),
        }
        results.append(
            {
                "name": "vendor_scalar_parity",
                "ok": all(c["ok"] for c in checks.values()),
                "checks": checks,
            }
        )
    except Exception as e:
        results.append({"name": "vendor_scalar_parity", "ok": False, "error": str(e)})

    codes = [i % 3 for i in range(32)]
    results.append(
        {"name": "fsot_lib_pack", "ok": unpack_u64(pack_u64(codes)) == codes}
    )

    eng = QuantumEngine()
    smoke = eng.smoke()
    results.append(
        {
            "name": "quantum_engine_fsot_lib",
            "ok": bool(smoke.get("ok")),
            "device": smoke.get("device"),
            "checks": {k: v.get("ok") for k, v in smoke.get("checks", {}).items()},
        }
    )

    # write engine smoke ledger too
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "quantum_engine_smoke.json").write_text(
        json.dumps(smoke, indent=2), encoding="utf-8"
    )

    overall = all(r.get("ok") for r in results)
    report = {
        "overall_ok": overall,
        "pin_expected": PIN_EXPECTED,
        "implementation": "fsot_lib from FSOT-GPU (vendored)",
        "collapse_threshold": COLLAPSE_THRESHOLD,
        "S_Quantum_Mechanics": domain_scalar("Quantum_Mechanics"),
        "S_Quantum_Computing": domain_scalar("Quantum_Computing"),
        "results": results,
    }
    (ROOT / "results" / "verify.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# FSOT-Quantum verify",
        "",
        f"**overall_ok:** `{overall}`",
        f"**implementation:** fsot_lib (FSOT-GPU owned)",
        f"**pin:** `{PIN_EXPECTED}`",
        f"**Θ:** `{COLLAPSE_THRESHOLD}`",
        "",
        "| Check | OK |",
        "|-------|----|",
    ]
    for r in results:
        md.append(f"| {r['name']} | {r.get('ok')} |")
    (ROOT / "results" / "VERIFY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def main() -> int:
    report = run_all()
    print(json.dumps(report, indent=2))
    print("overall_ok:", report["overall_ok"])
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
