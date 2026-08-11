"""
Competitor climb v2 — surface-code stabilizers + larger Shor + mega GPU + chemistry.

python -m fsot_quantum.climb_v2
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.surface_code import run_surface_code_panel
from fsot_quantum.shor_gpu import run_shor_gpu_panel
from fsot_quantum.mega_gpu import run_mega_gpu_panel
from fsot_quantum.chemistry_strict import run_chemistry_strict_panel
from fsot_quantum.hilbert_batch import run_fused_climb_panel
from fsot_quantum.opt_gpu import run_opt_gpu_panel
from fsot_quantum.qaoa_fsot import run_qaoa_panel


def main() -> int:
    t0 = time.perf_counter()

    surface = run_surface_code_panel()
    shor = run_shor_gpu_panel()
    mega = run_mega_gpu_panel()
    chem = run_chemistry_strict_panel()
    fused = run_fused_climb_panel()
    opt = run_opt_gpu_panel()
    qaoa = run_qaoa_panel()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "climb_competitor_v2",
        "goal": (
            "FSOT-QC competitor climb: surface-code style stabilizers, "
            "larger modular Shor on GPU, mega-batch occupancy, chemistry ledger"
        ),
        "pin": "D1D38A",
        "surface_code": {
            "ok": surface["overall_ok"],
            "pass": f"{surface['pass_count']}/{surface['total']}",
            "ladder": surface["ladder"],
            "noise_gate": surface["noise_gate"],
            "note": surface["note"],
        },
        "shor_gpu": {
            "ok": shor["overall_ok"],
            "pass": f"{shor['pass_count']}/{shor['total']}",
            "cases": [
                {
                    "a": c["a"],
                    "N": c["N"],
                    "r": c["true_period"],
                    "hat": c["recovered_period"],
                    "ok": c["ok"],
                    "n_qubits": c["n_qubits"],
                    "s": c["seconds"],
                    "mem_mb": c.get("peak_mem_mb"),
                }
                for c in shor["cases"]
            ],
        },
        "mega_gpu": {
            "ok": mega["overall_ok"],
            "gpu": mega.get("gpu_name"),
            "highlights": mega.get("highlights"),
        },
        "chemistry_strict": {
            "ok": chem["overall_ok"],
            "frac_0_5": chem["frac_green_0_5"],
            "frac_5": chem["frac_band_5"],
            "median_pct": chem["median_rel_err_pct"],
            "aspiration_0_5_ok": chem["aspiration_0_5_ok"],
            "n_green": f"{chem['n_green_0_5']}/{chem['n_observables']}",
        },
        "fused_gpu": {
            "ok": fused["overall_ok"],
            "highlights": fused.get("highlights"),
        },
        "opt_gpu": {
            "ok": opt["overall_ok"],
            "highlights": opt.get("highlights"),
        },
        "qaoa_exact": qaoa.get("metrics_summary"),
        "qaoa_ok": qaoa["overall_ok"],
        "overall_ok": (
            surface["overall_ok"]
            and shor["overall_ok"]
            and mega["overall_ok"]
            and chem["overall_ok"]
            and fused["overall_ok"]
            and opt["overall_ok"]
            and qaoa["overall_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
        "still_not_claimed": [
            "cryptographically large Shor (RSA-scale)",
            "device-scale surface-code FTQC threshold proofs",
            "full molecular FCI / CASSCF",
            "100% chemistry observables @ 0.5% (aspiration)",
        ],
        "now_implemented_v2": [
            "planar surface-code Z-plaquette stabilizers d=3/5/7 + min-weight syndrome decoder",
            "GPU modular Shor ladder N∈{15,21,33,35,39,51}",
            "mega-batch GPU occupancy (pack + fused Hilbert + MaxCut + surface spins)",
            "chemistry strict 5% band + 0.5% green fraction ledger",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "surface_code.json").write_text(json.dumps(surface, indent=2), encoding="utf-8")
    (out / "shor_gpu.json").write_text(json.dumps(shor, indent=2), encoding="utf-8")
    (out / "mega_gpu.json").write_text(json.dumps(mega, indent=2), encoding="utf-8")
    (out / "climb_v2.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Competitor climb v2",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        f"**device/GPU:** `{report['mega_gpu'].get('gpu')}`",
        "",
        "## Panels",
        "",
        f"- **surface code:** {report['surface_code']['pass']} ok={report['surface_code']['ok']} "
        f"noise={report['surface_code']['noise_gate']}",
        f"- **Shor GPU:** {report['shor_gpu']['pass']} ok={report['shor_gpu']['ok']}",
        f"- **mega GPU:** ok={report['mega_gpu']['ok']} highlights={report['mega_gpu']['highlights']}",
        f"- **chemistry strict:** ok={report['chemistry_strict']['ok']} "
        f"0.5%={report['chemistry_strict']['n_green']} median={report['chemistry_strict']['median_pct']}",
        f"- **fused GPU:** ok={report['fused_gpu']['ok']}",
        f"- **opt GPU:** ok={report['opt_gpu']['ok']}",
        f"- **QAOA exact:** {report['qaoa_exact']}",
        "",
        "## Now implemented (v2)",
        "",
    ]
    for x in report["now_implemented_v2"]:
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
        "python -m fsot_quantum.climb_v2",
        "```",
        "",
        "Watch load: `nvidia-smi -l 1` while running.",
        "",
    ]
    md_text = "\n".join(md)
    (out / "CLIMB_V2.md").write_text(md_text, encoding="utf-8")
    (ROOT / "docs" / "CLIMB_V2.md").write_text(md_text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
