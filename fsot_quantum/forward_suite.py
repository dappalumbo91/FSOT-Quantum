"""
Forward suite: next-steps + GPU headroom load.

python -m fsot_quantum.forward_suite
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.next_steps_suite import run_next_steps
from fsot_quantum.hilbert_gpu import run_gpu_headroom_panel
from fsot_quantum.qaoa_fsot import run_qaoa_panel


def main() -> int:
    t0 = time.perf_counter()
    next_s = run_next_steps()
    gpu = run_gpu_headroom_panel()
    qaoa = run_qaoa_panel()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "forward",
        "next_steps_ok": next_s["overall_ok"],
        "gpu_headroom_ok": gpu["overall_ok"],
        "qaoa_exact": qaoa.get("metrics_summary"),
        "qaoa_ok": qaoa["overall_ok"],
        "gpu_highlights": gpu.get("highlights"),
        "gpu_name": gpu.get("gpu_name"),
        "overall_ok": next_s["overall_ok"] and gpu["overall_ok"] and qaoa["overall_ok"],
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "gpu_headroom.json").write_text(json.dumps(gpu, indent=2), encoding="utf-8")
    (out / "forward_suite.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Forward suite",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**GPU:** `{report['gpu_name']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        f"- next_steps: {report['next_steps_ok']}",
        f"- gpu_headroom: {report['gpu_headroom_ok']} · {report['gpu_highlights']}",
        f"- qaoa: {report['qaoa_exact']}",
        "",
        "Run with `nvidia-smi -l 1` in another terminal to watch util%.",
        "",
    ]
    (out / "FORWARD.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "FORWARD.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
