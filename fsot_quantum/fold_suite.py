"""
Fold-not-Hilbert competitor suite.

python -m fsot_quantum.fold_suite
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.fold_jobs import run_fold_jobs_panel
from fsot_quantum.fold_complexity import cost_contrast, nested_fold_scalars, fold_depth_ladder


def main() -> int:
    t0 = time.perf_counter()
    panel = run_fold_jobs_panel()
    folds = nested_fold_scalars()

    # Summarize by job family
    families: dict[str, list] = {}
    for r in panel["instances"]:
        j = r.get("job", "other")
        families.setdefault(j, []).append(r)

    family_sum = {}
    for j, items in families.items():
        oks = [bool(x.get("ok")) for x in items]
        family_sum[j] = {
            "pass": f"{sum(oks)}/{len(oks)}",
            "ok": all(oks),
            "n": len(oks),
        }

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_not_hilbert",
        "pin": "D1D38A",
        "thesis": panel["thesis"],
        "overall_ok": panel["overall_ok"],
        "pass": f"{panel['pass_count']}/{panel['total']}",
        "family_summary": family_sum,
        "fold_depth_ladder": fold_depth_ladder(),
        "complexity_weight": panel["complexity_weight"],
        "D_eff_routes": panel["D_eff_routes"],
        "nested_folds": folds,
        "scale_cost_ledger": panel["scale_cost_ledger"],
        "wall_seconds": time.perf_counter() - t0,
        "contrast": {
            "industry_bottleneck": (
                "Hilbert-space dimension / degrees of freedom — "
                "amplitudes in C^{2^n}; cost explodes with qubit count"
            ),
            "fsot_scaling": (
                "Complexity as domain folds (D_eff routes) + modular/algebraic "
                "structure + collapse/consensus — poly probes, not 2^n amplitudes"
            ),
            "example_n20": cost_contrast(20),
            "example_n32": cost_contrast(32),
        },
        "still_not_claimed": [
            "cryptographically large RSA factoring as a security break",
            "query-complexity asymptotic superiority proofs vs quantum in all models",
            "Hilbert-universal unitary simulation for arbitrary circuits",
        ],
        "now_implemented": [
            "fold_complexity: D_eff routes, φ-weight, cost contrast ledger",
            "fold jobs: DJ/BV/search/period/factor/Ising/phase-class",
            "honest: same QC questions, FSOT geometry of work",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "fold_jobs.json").write_text(json.dumps(panel, indent=2), encoding="utf-8")
    (out / "fold_suite.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold-not-Hilbert suite",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**pass:** `{report['pass']}`",
        f"**wall_s:** `{report['wall_seconds']:.3f}`",
        "",
        "## Thesis",
        "",
        report["thesis"],
        "",
        "## The bottleneck (correct term)",
        "",
        report["contrast"]["industry_bottleneck"],
        "",
        "## FSOT scaling",
        "",
        report["contrast"]["fsot_scaling"],
        "",
        "## Cost contrast examples",
        "",
        f"- n=20 Hilbert amps `{report['contrast']['example_n20']['hilbert_amplitudes']}` "
        f"vs fold budget `{report['contrast']['example_n20']['fold_probe_budget']}` "
        f"(ratio ~{report['contrast']['example_n20']['ratio_hilbert_over_fold']:.0f}×)",
        f"- n=32 Hilbert amps `{report['contrast']['example_n32']['hilbert_amplitudes']}` "
        f"vs fold budget `{report['contrast']['example_n32']['fold_probe_budget']}` "
        f"(ratio ~{report['contrast']['example_n32']['ratio_hilbert_over_fold']:.0f}×)",
        "",
        "## Job families",
        "",
        "| Job | Pass | OK |",
        "|-----|------|----|",
    ]
    for j, s in family_sum.items():
        md.append(f"| {j} | {s['pass']} | {s['ok']} |")
    md += [
        "",
        "## Nested D_eff folds",
        "",
    ]
    for f in folds:
        md.append(
            f"- fold {f['fold_index']}: **{f['domain']}** D_eff={f['D_eff']} "
            f"S={f['S']:.4f} ({f['class']}) — {f['role']}"
        )
    md += [
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.fold_suite",
        "```",
        "",
        "## Note",
        "",
        panel["note"],
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_NOT_HILBERT.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_NOT_HILBERT.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "pass": report["pass"],
        "family_summary": family_sum,
        "wall_seconds": report["wall_seconds"],
        "contrast_n32_ratio": report["contrast"]["example_n32"]["ratio_hilbert_over_fold"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
