"""
Cross-check this fold against the cloned FSOT-2.1-Lean engine.

Pin, seeds, overlapping D_eff, S(QM)/S(QC). Field usability = same math.

python -m fsot_quantum.crosscheck
"""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_quantum.domains import DOMAINS, domain_scalar

LEAN_VENDOR = ROOT / "_ref" / "FSOT-2.1-Lean" / "vendor" / "fsot_compute.py"
OURS_VENDOR = ROOT / "vendor" / "fsot_compute.py"
PIN = "D1D38A"


def _sha6(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:6].upper()


def run_crosscheck() -> dict[str, Any]:
    checks = []

    ours_pin = _sha6(OURS_VENDOR) if OURS_VENDOR.is_file() else None
    checks.append({"id": "pin_ours", "ok": ours_pin == PIN, "got": ours_pin, "want": PIN})

    lean_pin = _sha6(LEAN_VENDOR) if LEAN_VENDOR.is_file() else None
    checks.append({
        "id": "pin_lean",
        "ok": lean_pin == PIN if lean_pin else False,
        "got": lean_pin,
        "want": PIN,
        "skip": lean_pin is None,
    })
    checks.append({
        "id": "pin_match_each_other",
        "ok": ours_pin is not None and ours_pin == lean_pin,
        "ours": ours_pin,
        "lean": lean_pin,
    })

    # Seeds vs vendor (same pin file)
    from vendor import fsot_compute as f

    pairs = [
        ("pi", float(SEEDS.pi), float(f.PI)),
        ("e", float(SEEDS.e), float(f.E)),
        ("phi", float(SEEDS.phi), float(f.PHI)),
        ("gamma", float(SEEDS.gamma), float(f.GAMMA)),
        ("c_eff", float(SEEDS.c_eff), float(f.C_EFF)),
        ("p_var", float(SEEDS.p_var), float(f.P_VAR)),
        ("poof", float(SEEDS.poof), float(f.POOF)),
        ("suction", float(SEEDS.suction), float(f.SUCTION)),
        ("a_bleed", float(SEEDS.a_bleed), float(f.A_BLEED)),
        ("theta", float(COLLAPSE_THRESHOLD), float(f.C_EFF * f.P_VAR)),
    ]
    for name, a, b in pairs:
        checks.append({
            "id": f"seed_{name}",
            "ok": abs(a - b) < 1e-12,
            "ours": a,
            "vendor": b,
        })

    # Overlapping domain D_eff
    for name, d in DOMAINS.items():
        if name not in f.DOMAINS:
            checks.append({"id": f"dom_{name}", "ok": False, "reason": "missing in vendor"})
            continue
        vd = f.DOMAINS[name]
        checks.append({
            "id": f"dom_{name}_Deff",
            "ok": int(d.D_eff) == int(vd.D_eff),
            "ours": d.D_eff,
            "vendor": int(vd.D_eff),
        })
        checks.append({
            "id": f"dom_{name}_obs",
            "ok": bool(d.observed) == bool(vd.observed),
            "ours": d.observed,
            "vendor": bool(vd.observed),
        })

    s_qm = domain_scalar("Quantum_Mechanics")
    s_qc = domain_scalar("Quantum_Computing")
    s_qm_v = float(f.domain_scalar("Quantum_Mechanics"))
    s_qc_v = float(f.domain_scalar("Quantum_Computing"))
    checks.append({
        "id": "S_QM_match",
        "ok": abs(s_qm - s_qm_v) < 1e-9,
        "ours": s_qm,
        "vendor": s_qm_v,
    })
    checks.append({
        "id": "S_QC_match",
        "ok": abs(s_qc - s_qc_v) < 1e-9,
        "ours": s_qc,
        "vendor": s_qc_v,
    })
    checks.append({"id": "S_QM_emergence", "ok": s_qm > 0, "got": s_qm})
    checks.append({"id": "S_QC_damping", "ok": s_qc < 0, "got": s_qc})

    live = [c for c in checks if not c.get("skip")]
    n_ok = sum(1 for c in live if c.get("ok"))
    return {
        "panel": "crosscheck_lean",
        "pin": PIN,
        "n_checks": len(live),
        "n_pass": n_ok,
        "overall_ok": n_ok == len(live) and len(live) > 10,
        "checks": checks,
    }


def main() -> int:
    import json
    from datetime import datetime, timezone

    r = run_crosscheck()
    r["timestamp"] = datetime.now(timezone.utc).isoformat()
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "crosscheck.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
    md = [
        "# Cross-check vs FSOT-2.1-Lean",
        "",
        f"**overall_ok:** `{r['overall_ok']}`",
        f"**pass:** `{r['n_pass']}/{r['n_checks']}`",
        "",
        "Same pin, same seeds, same overlapping D_eff, same S(QM)/S(QC).",
        "",
        "```powershell",
        "python -m fsot_quantum.crosscheck",
        "```",
        "",
    ]
    (out / "CROSSCHECK.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "CROSSCHECK.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({
        "overall_ok": r["overall_ok"],
        "pass": f"{r['n_pass']}/{r['n_checks']}",
        "fails": [c["id"] for c in r["checks"] if not c.get("ok") and not c.get("skip")],
    }, indent=2))
    return 0 if r["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
