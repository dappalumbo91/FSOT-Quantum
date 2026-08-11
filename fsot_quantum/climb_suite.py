"""
Competitor climb suite — fused GPU Hilbert + modular Shor GPU + opt GPU.

python -m fsot_quantum.climb_suite
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.hilbert_batch import run_fused_climb_panel
from fsot_quantum.shor_gpu import run_shor_gpu_panel
from fsot_quantum.opt_gpu import run_opt_gpu_panel
from fsot_quantum.qaoa_fsot import run_qaoa_panel
from fsot_quantum.next_steps_suite import run_next_steps


def main() -> int:
    t0 = time.perf_counter()
    fused = run_fused_climb_panel()
    shor = run_shor_gpu_panel()
    opt = run_opt_gpu_panel()
    qaoa = run_qaoa_panel()
    # keep prior ladder green (lighter if already warm)
    nxt = run_next_steps()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "climb_competitor",
        "goal": "FSOT-QC as infrastructure-light competitor to QC job capabilities",
        "fused_gpu": {
            "ok": fused["overall_ok"],
            "gpu": fused.get("gpu_name"),
            "highlights": fused.get("highlights"),
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
                    "s": c["seconds"],
                    "mem_mb": c.get("peak_mem_mb"),
                }
                for c in shor["cases"]
            ],
        },
        "opt_gpu": {
            "ok": opt["overall_ok"],
            "highlights": opt.get("highlights"),
        },
        "qaoa_exact": qaoa.get("metrics_summary"),
        "qaoa_ok": qaoa["overall_ok"],
        "next_steps_ok": nxt["overall_ok"],
        "overall_ok": (
            fused["overall_ok"]
            and shor["overall_ok"]
            and opt["overall_ok"]
            and qaoa["overall_ok"]
            and nxt["overall_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "fused_gpu_climb.json").write_text(json.dumps(fused, indent=2), encoding="utf-8")
    (out / "shor_gpu.json").write_text(json.dumps(shor, indent=2), encoding="utf-8")
    (out / "opt_gpu.json").write_text(json.dumps(opt, indent=2), encoding="utf-8")
    (out / "climb_suite.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Competitor climb suite",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        f"- **fused GPU Hilbert:** {report['fused_gpu']}",
        f"- **Shor GPU:** {report['shor_gpu']['pass']} ok={report['shor_gpu']['ok']}",
        f"- **opt GPU:** {report['opt_gpu']}",
        f"- **QAOA exact:** {report['qaoa_exact']}",
        f"- **next_steps:** {report['next_steps_ok']}",
        "",
        "Watch load: `nvidia-smi -l 1` while running.",
        "",
    ]
    (out / "CLIMB.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "CLIMB.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
