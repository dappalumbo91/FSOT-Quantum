"""
Next-track stress suite: large MaxCut · QAOA-FSOT · textbook sim compare.

Writes results/stress_next.json + STRESS_NEXT.md
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.large_maxcut import run_large_maxcut_panel
from fsot_quantum.qaoa_fsot import run_qaoa_panel
from fsot_quantum.textbook_sim_compare import run_textbook_compare
from fsot_quantum.gpu_parallel import prefer_device


def run_stress_next() -> dict:
    t0 = time.perf_counter()
    large = run_large_maxcut_panel()
    qaoa = run_qaoa_panel()
    text = run_textbook_compare()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device": prefer_device(),
        "panels": {
            "large_maxcut": {
                "overall_ok": large["overall_ok"],
                "exactable": f"{large['exactable_pass']}/{large['exactable_total']}",
                "large": f"{large['large_pass']}/{large['large_total']}",
                "summary": large.get("summary"),
            },
            "qaoa_fsot": {
                "overall_ok": qaoa["overall_ok"],
                "local_exact": f"{qaoa['local_exact_hits']}/{qaoa['total']}",
                "qaoa_exact": f"{qaoa['qaoa_exact_hits']}/{qaoa['total']}",
                "p_layers": qaoa["p_layers_seed"],
            },
            "textbook_sim_compare": {
                "overall_ok": text["overall_ok"],
                "pass": f"{text['pass_count']}/{text['total']}",
            },
        },
        "overall_ok": (
            large["overall_ok"] and qaoa["overall_ok"] and text["overall_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "stress_next.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# Next-track stress suite",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**device:** `{report['device']}`",
        f"**wall_s:** `{report['wall_seconds']:.3f}`",
        "",
        "## Panels",
        "",
        f"- **large_maxcut:** {report['panels']['large_maxcut']}",
        f"- **qaoa_fsot:** {report['panels']['qaoa_fsot']}",
        f"- **textbook_sim_compare:** {report['panels']['textbook_sim_compare']}",
        "",
        "Details: `LARGE_MAXCUT.md`, `QAOA_FSOT.md`, `TEXTBOOK_SIM_COMPARE.md`",
        "",
    ]
    (out / "STRESS_NEXT.md").write_text("\n".join(md), encoding="utf-8")
    return report


def main() -> int:
    r = run_stress_next()
    print(json.dumps(r, indent=2))
    return 0 if r["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
