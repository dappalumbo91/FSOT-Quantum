"""
Fold path v6 — official G1 residual, wider arith, GPU occupancy.

python -m fsot_quantum.fold_v6
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
from fsot_quantum.fold_arith import run_fold_arith_panel
from fsot_quantum.fold_gpu_queue import (
    batch_domain_scalar_fold,
    batch_pack_fold,
    batch_search_fold,
)
from fsot_quantum.fold_multigpu import inventory
from fsot_quantum.fold_complexity import fold_budget_formal, cost_contrast
from fsot_quantum.gpu_parallel import prefer_device


def run_gpu_occupancy_v6() -> dict:
    dev = prefer_device()
    rows = []
    marked = [((i * 2654435761) + 11) % 8192 for i in range(2048 if dev == "cuda" else 64)]
    rows.append(batch_search_fold(8192, marked, device=dev))
    try:
        rows.append(batch_pack_fold(12_000_000 if dev == "cuda" else 50_000, device=dev))
    except RuntimeError as e:
        rows.append({"job": "pack", "ok": False, "error": str(e)[:200]})
    rows.append(batch_domain_scalar_fold(200_000 if dev == "cuda" else 5000, device=dev))
    ok = all(r.get("ok") for r in rows)
    return {
        "panel": "gpu_occupancy_v6",
        "device": dev,
        "inventory": inventory(),
        "instances": rows,
        "overall_ok": ok,
    }


def main() -> int:
    t0 = time.perf_counter()
    gset = run_gset_official_panel()
    arith = run_fold_arith_panel()
    gpu = run_gpu_occupancy_v6()

    official_ok = bool(gset.get("official_found")) and gset["overall_ok"]
    overall = official_ok and arith["overall_ok"] and gpu["overall_ok"]

    g1 = None
    for r in gset.get("instances") or []:
        if str(r.get("name", "")).upper().startswith("G1"):
            g1 = r
            break

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_v6_push",
        "pin": "D1D38A",
        "thesis": (
            "Official Gset G1 fold residual + 4-bit/modular-multiply folds "
            "+ GPU occupancy — still not Hilbert 2^n"
        ),
        "gset_official": {
            "ok": gset["overall_ok"],
            "status": gset["status"],
            "official_found": gset["official_found"],
            "pass": f"{gset['pass_count']}/{gset['total']}",
            "g1": g1,
        },
        "arith": {
            "ok": arith["overall_ok"],
            "pass": f"{arith['pass_count']}/{arith['total']}",
        },
        "gpu_occupancy": {
            "ok": gpu["overall_ok"],
            "device": gpu["device"],
            "n_gpu": gpu["inventory"]["n_gpu"],
        },
        "fold_budget_formal": {str(n): fold_budget_formal(n) for n in (8, 16, 32)},
        "cost_contrast_n32": cost_contrast(32),
        "overall_ok": overall,
        "wall_seconds": time.perf_counter() - t0,
        "now_implemented": [
            "official Stanford Gset G1 parse + incremental fold MaxCut residual",
            "4-bit ripple samples + modular multiply shift-add folds",
            "GPU occupancy climb (search 8k, pack 12M, D_eff scalars)",
        ],
        "still_not_claimed": [
            "full Gset G1–G54 published champion-cut table",
            "multi-GPU speedup (n_gpu still 1 here)",
            "Hilbert modular-multiply / QFT adder equivalence",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "gset_official.json").write_text(json.dumps(gset, indent=2), encoding="utf-8")
    (out / "fold_arith.json").write_text(json.dumps(arith, indent=2), encoding="utf-8")
    (out / "fold_v6.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold path v6",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        f"- **Gset official:** {report['gset_official']['status']} "
        f"found={report['gset_official']['official_found']} "
        f"pass={report['gset_official']['pass']}",
        f"- **G1:** {g1}",
        f"- **arith:** {report['arith']['pass']} ok={report['arith']['ok']}",
        f"- **GPU occupancy:** ok={report['gpu_occupancy']['ok']} "
        f"n_gpu={report['gpu_occupancy']['n_gpu']}",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.fold_v6",
        "```",
        "",
        "Gset G1 source: `https://web.stanford.edu/~yyye/yyye/Gset/G1` → `data/gset/G1.txt`",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_V6.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_V6.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2, default=str))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
