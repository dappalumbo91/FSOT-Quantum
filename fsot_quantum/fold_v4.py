"""
Fold path v4 — mp scheduler, teleport sequences, Gset-style, formal cost, Zig twin.

python -m fsot_quantum.fold_v4
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.fold_mp_scheduler import run_fold_mp_scheduler_panel
from fsot_quantum.lattice_teleport_fold import run_lattice_teleport_fold_panel
from fsot_quantum.gset_fold import run_gset_fold_panel
from fsot_quantum.fold_complexity import fold_budget_formal, cost_contrast


def _zig_fold_twin() -> dict:
    zig = shutil.which("zig")
    if not zig:
        return {"ok": False, "status": "skip", "reason": "zig not on PATH"}
    code = subprocess.run(
        [zig, "build", "run"],
        cwd=str(ROOT / "zig"),
        capture_output=True,
        text=True,
        timeout=180,
    )
    out = (code.stdout or "") + (code.stderr or "")
    ok = code.returncode == 0 and "PASS" in out
    return {
        "ok": ok,
        "status": "pass" if ok else "fail",
        "exit_code": code.returncode,
        "log_tail": out[-2000:],
    }


def _formal_python_fold() -> dict:
    """Runtime obligations for fold cost lemmas (always on)."""
    checks = {
        "fold8": fold_budget_formal(8) == 195 and fold_budget_formal(8) < 256,
        "fold16": fold_budget_formal(16) < (1 << 16),
        "fold20": fold_budget_formal(20) < (1 << 20),
        "fold32": fold_budget_formal(32) < (1 << 32),
        "runtime_le_formal8": True,
    }
    from fsot_quantum.fold_complexity import fold_probe_budget

    checks["runtime_le_formal8"] = fold_probe_budget(8) <= fold_budget_formal(8)
    ok = all(checks.values())
    return {"ok": ok, "checks": checks, "status": "pass" if ok else "fail"}


def main() -> int:
    t0 = time.perf_counter()
    mp = run_fold_mp_scheduler_panel()
    tele = run_lattice_teleport_fold_panel()
    gset = run_gset_fold_panel()
    formal_py = _formal_python_fold()
    zig = _zig_fold_twin()

    # Zig skip is allowed; formal python + other panels required
    overall = (
        mp["overall_ok"]
        and tele["overall_ok"]
        and gset["overall_ok"]
        and formal_py["ok"]
        and (zig["ok"] or zig.get("status") == "skip")
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_v4_natural_steps",
        "pin": "D1D38A",
        "thesis": (
            "Fold v4: multi-process scheduler, teleportation sequences, "
            "Gset-style MaxCut ledger, fold-vs-Hilbert formal cost, Zig twin"
        ),
        "mp_scheduler": {
            "ok": mp["overall_ok"],
            "workers": mp["workers"],
            "n_tasks": mp["n_tasks"],
            "serial_s": mp["serial"]["wall_seconds"],
            "pool_s": mp["pooled"].get("wall_seconds"),
            "speedup": mp["speedup_serial_over_pool"],
        },
        "lattice_teleport": {
            "ok": tele["overall_ok"],
            "pass": f"{tele['pass_count']}/{tele['total']}",
        },
        "gset_style": {
            "ok": gset["overall_ok"],
            "pass": f"{gset['pass_count']}/{gset['total']}",
            "instances": [
                {
                    "name": r["name"],
                    "n": r["n"],
                    "ratio": r["ratio_lb"],
                    "ok": r["ok"],
                    "s": r["seconds"],
                }
                for r in gset["instances"]
            ],
        },
        "formal_fold_cost": formal_py,
        "zig_fold_twin": {
            "ok": zig["ok"],
            "status": zig.get("status"),
            "reason": zig.get("reason"),
        },
        "cost_contrast_n32": cost_contrast(32),
        "fold_budget_formal": {str(n): fold_budget_formal(n) for n in (8, 16, 20, 32)},
        "overall_ok": overall,
        "wall_seconds": time.perf_counter() - t0,
        "now_implemented": [
            "multi-process fold scheduler (search/period/factor/Ising)",
            "lattice-surgery SWAP / copy / GHZ-class / A→B→C teleport chain",
            "Gset-style MaxCut n=40..100 under 1/φ floor + cost ledger",
            "foldBudget vs 2^n lemmas (Lean/Coq/Isabelle + Python + Zig)",
        ],
        "still_not_claimed": [
            "downloaded official Gset archive residuals",
            "continuum FTQC teleportation thresholds",
            "multi-GPU distributed fold (this is multi-process on one host)",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "fold_mp_scheduler.json").write_text(json.dumps(mp, indent=2), encoding="utf-8")
    (out / "lattice_teleport_fold.json").write_text(
        json.dumps(tele, indent=2), encoding="utf-8"
    )
    (out / "gset_fold.json").write_text(json.dumps(gset, indent=2), encoding="utf-8")
    (out / "fold_v4.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold path v4 — natural steps",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "## Thesis",
        "",
        report["thesis"],
        "",
        "## Panels",
        "",
        f"- **mp scheduler:** ok={report['mp_scheduler']['ok']} "
        f"workers={report['mp_scheduler']['workers']} "
        f"serial={report['mp_scheduler']['serial_s']:.3f}s "
        f"pool={report['mp_scheduler']['pool_s']} "
        f"speedup={report['mp_scheduler']['speedup']}",
        f"- **teleport sequences:** {report['lattice_teleport']['pass']} "
        f"ok={report['lattice_teleport']['ok']}",
        f"- **Gset-style MaxCut:** {report['gset_style']['pass']} "
        f"ok={report['gset_style']['ok']}",
        f"- **formal fold cost (Python):** {report['formal_fold_cost']['status']}",
        f"- **Zig fold twin:** {report['zig_fold_twin']['status']}",
        "",
        "## Fold vs Hilbert (formal integer proxy)",
        "",
        "| n | foldBudget | 2^n |",
        "|--:|-----------:|----:|",
    ]
    for n in (8, 16, 20, 32):
        md.append(f"| {n} | {fold_budget_formal(n)} | {1 << n} |")
    md += [
        "",
        "## Now implemented",
        "",
    ]
    for x in report["now_implemented"]:
        md.append(f"- {x}")
    md += ["", "## Still not claimed", ""]
    for x in report["still_not_claimed"]:
        md.append(f"- {x}")
    md += [
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.fold_v4",
        "python scripts\\run_multiprover_verification.py",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_V4.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_V4.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
