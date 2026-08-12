"""
Fold path v5 — leftovers: official Gset, multi-GPU honesty, adder/QFT-role, QEMU, note.

python -m fsot_quantum.fold_v5
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.fold_multigpu import run_fold_multigpu_panel
from fsot_quantum.logical_algo_fold import run_logical_algo_fold_panel
from fsot_quantum.qemu_fold_gate import run_qemu_fold_gate
from fsot_quantum.fold_complexity import fold_budget_formal, cost_contrast


def main() -> int:
    t0 = time.perf_counter()
    gset = run_gset_official_panel()
    gpu = run_fold_multigpu_panel()
    algo = run_logical_algo_fold_panel()
    qemu = run_qemu_fold_gate()

    note = ROOT / "papers" / "02-fold-not-hilbert" / "NOTE.md"
    note_ok = note.exists() and "foldBudget" in note.read_text(encoding="utf-8")

    qemu_ok = qemu["ok"] or qemu.get("status") == "skip"
    overall = (
        gset["overall_ok"]
        and gpu["overall_ok"]
        and algo["overall_ok"]
        and qemu_ok
        and note_ok
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_v5_leftovers",
        "pin": "D1D38A",
        "thesis": (
            "Hit leftover rungs honestly: official Gset if present, multi-GPU "
            "inventory+shards, adder/QFT-role folds, QEMU fold kernel, paper note"
        ),
        "gset_official": {
            "ok": gset["overall_ok"],
            "status": gset["status"],
            "parser_ok": gset["parser_ok"],
            "official_found": gset["official_found"],
            "n_official": gset["n_official"],
            "pass": f"{gset['pass_count']}/{gset['total']}",
        },
        "multigpu": {
            "ok": gpu["overall_ok"],
            "n_gpu": gpu["inventory"]["n_gpu"],
            "names": gpu["inventory"]["names"],
            "multi_gpu_available": gpu["inventory"]["multi_gpu_available"],
            "claimed_multi_gpu_speedup": gpu["claimed_multi_gpu_speedup"],
            "shards": f"{gpu['pass_count']}/{gpu['total']}",
        },
        "logical_algos": {
            "ok": algo["overall_ok"],
            "pass": f"{algo['pass_count']}/{algo['total']}",
        },
        "qemu_fold": {
            "ok": qemu["ok"],
            "status": qemu.get("status"),
            "fold_pass": qemu.get("fold_pass"),
            "cnotfold_pass": qemu.get("cnotfold_pass"),
            "kernel_pass": qemu.get("kernel_pass"),
            "reason": qemu.get("reason"),
        },
        "paper_note": {
            "ok": note_ok,
            "path": str(note.relative_to(ROOT)),
        },
        "fold_budget_formal": {str(n): fold_budget_formal(n) for n in (8, 16, 32)},
        "cost_contrast_n32": cost_contrast(32),
        "overall_ok": overall,
        "wall_seconds": time.perf_counter() - t0,
        "now_implemented": [
            "Gset official loader + parser fixture (skip if no archive)",
            "multi-GPU inventory + shard runner (honest n_gpu=1 on this host)",
            "ripple-carry adder + QFT-role bit-reversal/phase folds",
            "QEMU serial gate for fold + cnotfold kernel tests",
            "papers/02-fold-not-hilbert/NOTE.md",
        ],
        "still_not_claimed": [
            "G1–G54 published residual table without local/official files",
            "multi-GPU speedup on a 1-GPU machine",
            "Hilbert QFT/adder circuit equivalence",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "gset_official.json").write_text(json.dumps(gset, indent=2), encoding="utf-8")
    (out / "fold_multigpu.json").write_text(json.dumps(gpu, indent=2), encoding="utf-8")
    (out / "logical_algo_fold.json").write_text(json.dumps(algo, indent=2), encoding="utf-8")
    (out / "qemu_fold_gate.json").write_text(json.dumps(qemu, indent=2), encoding="utf-8")
    (out / "fold_v5.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold path v5 — leftovers",
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
        f"- **Gset official:** status={report['gset_official']['status']} "
        f"parser={report['gset_official']['parser_ok']} "
        f"found={report['gset_official']['official_found']} "
        f"pass={report['gset_official']['pass']}",
        f"- **multi-GPU:** n_gpu={report['multigpu']['n_gpu']} "
        f"{report['multigpu']['names']} shards={report['multigpu']['shards']} "
        f"claimed_speedup={report['multigpu']['claimed_multi_gpu_speedup']}",
        f"- **logical algos:** {report['logical_algos']['pass']} "
        f"ok={report['logical_algos']['ok']}",
        f"- **QEMU fold gate:** {report['qemu_fold']['status']} "
        f"fold={report['qemu_fold']['fold_pass']} "
        f"cnotfold={report['qemu_fold']['cnotfold_pass']} "
        f"kernel={report['qemu_fold']['kernel_pass']}",
        f"- **paper note:** ok={report['paper_note']['ok']} `{report['paper_note']['path']}`",
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
        "python -m fsot_quantum.fold_v5",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_V5.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_V5.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
