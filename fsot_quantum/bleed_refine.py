"""
Bleed refine — apply Lean connective coupling to this QC fold.

python -m fsot_quantum.bleed_refine
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.quantum_bleed import coupled_equilibrium, qc_job_modulation
from fsot_quantum.lean_quantum_atlas import ingest_lean_quantum_atlas
from fsot_quantum.fsot_field_opt import run_fsot_field_opt_panel
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


def main() -> int:
    t0 = time.perf_counter()
    eq = coupled_equilibrium()
    mod = qc_job_modulation(eq)
    atlas = ingest_lean_quantum_atlas()
    opt = run_fsot_field_opt_panel()
    gset = run_gset_official_panel()
    chem = run_chemistry_fold_panel()
    qm = run_qm_wave_use_panel()

    g1 = None
    for r in gset.get("instances") or []:
        if str(r.get("name", "")).upper().startswith("G1"):
            g1 = r
            break

    # Diagnostic: seed modulation factor on the QC job (not a free LR)
    # If |mod-1| is tiny, bleed is a small wave — that is the physics, not a fail.
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "bleed_refine",
        "pin": "D1D38A",
        "thesis": (
            "Quantum jobs are not stuck at one D_eff. QM/QC/QO/particle/chem/CM "
            "bleed through A_bleed·POOF·|S_i||S_j| / (1+|ΔD|/25), then relax. "
            "Same connective law as FSOT-2.1-Lean complex-system derivation."
        ),
        "bleed": {
            "yin_yang": eq["yin_yang"],
            "steps": eq["steps"],
            "dt": eq["dt"],
            "qc_job_mod": mod,
            "QM_S_eq": eq["bare_S"]["QM"],
            "QC_S_eq": eq["bare_S"]["QC"],
            "QM_S_coupled": eq["coupled_S"]["QM"],
            "QC_S_coupled": eq["coupled_S"]["QC"],
            "dS_QM": eq["coupled_S"]["QM"] - eq["bare_S"]["QM"],
            "dS_QC": eq["coupled_S"]["QC"] - eq["bare_S"]["QC"],
            "n_edges": len(eq["interfaces"]),
            "note_I": (
                "I_ab=1 when signs oppose (emergence vs damping). "
                "The wave is ΔS after relaxation, not I+−I−."
            ),
        },
        "interfaces": eq["interfaces"],
        "nodes": eq["nodes"],
        "lean_atlas": {
            "ok": atlas["ok"],
            "status": atlas["status"],
            "n_files": atlas.get("n_files"),
            "total_records": atlas.get("total_records"),
            "panels": [
                {
                    "domain": r.get("domain"),
                    "D_eff": r.get("D_eff"),
                    "n": r.get("record_count"),
                    "median_pct": r.get("median_error_pct"),
                }
                for r in atlas.get("instances") or []
                if r.get("ok")
            ],
        },
        "job_ledgers_unchanged_default": {
            "field_opt_ok": opt["overall_ok"],
            "field_opt_exact": f"{opt['exact_hits']}/{opt['exact_total']}",
            "chem_0_5": f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
            "qm_0_5": f"{qm['n_green_0_5']}/{qm['n_observables']}",
            "g1_rel_pct": (g1 or {}).get("rel_err_vs_published_pct"),
        },
        "overall_ok": (
            atlas.get("ok", False)
            and opt["overall_ok"]
            and chem["overall_ok"]
            and qm["overall_ok"]
            and gset["overall_ok"]
            and math_ok(eq, mod)
        ),
        "wall_seconds": time.perf_counter() - t0,
        "plain_language": (
            "Think of D_eff like which part of the machine you're turning: "
            "measurement (QM, 6), compute (QC, 11), light (optics, 11 observed), "
            "atoms, bonds, packing. They share oil — A_bleed and POOF/SUCTION. "
            "The leak between gears is κ, smaller when the gears are farther "
            "apart in D. We let S wave until it settles. We do not add a new "
            "bolt (free parameter). LLM-style weights are that extra bolt; "
            "this fold stays mechanical."
        ),
        "note": (
            "Default job answers stay pin/field ledgers. Bleed is the connective "
            "picture for refinement — not a silent rescale of measured targets."
        ),
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "quantum_bleed.json").write_text(json.dumps(eq, indent=2), encoding="utf-8")
    (out / "lean_quantum_atlas.json").write_text(json.dumps(atlas, indent=2), encoding="utf-8")
    (out / "bleed_refine.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Quantum bleed refine — full Lean fabric, not just the 35-row core",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        report["thesis"],
        "",
        "## Plain language",
        "",
        report["plain_language"],
        "",
        "## Coupled S (this fold)",
        "",
        f"- yin–yang POOF/(POOF+SUCTION) = `{eq['yin_yang']:.4f}`",
        f"- relax steps = `{eq['steps']}` (round(1/POOF))",
        f"- S(QM) eq `{eq['bare_S']['QM']:.4f}` → coupled `{eq['coupled_S']['QM']:.4f}`",
        f"- S(QC) eq `{eq['bare_S']['QC']:.4f}` → coupled `{eq['coupled_S']['QC']:.4f}`",
        f"- QC job modulation (pack vs measure) = `{mod['mod']:.6f}` "
        f"(I_QC_CM={mod['I_QC_CM']:.4f}, I_QM_QC={mod['I_QM_QC']:.4f})",
        "",
        "A modulation near 1 means the wave is small — the medium is already "
        "close to equilibrium. That is information, not a miss.",
        "",
        "## FSOT-2.1-Lean quantum atlas (already solved there)",
        "",
        f"status=`{atlas['status']}` files=`{atlas.get('n_files')}` "
        f"records=`{atlas.get('total_records')}`",
        "",
        "| Domain | D_eff | n | median % |",
        "|--------|------:|--:|---------:|",
    ]
    for r in report["lean_atlas"]["panels"]:
        md.append(
            f"| {r['domain']} | {r['D_eff']} | {r['n']} | {r['median_pct']} |"
        )
    md += [
        "",
        "## Default job ledgers (unchanged claim)",
        "",
        f"- field opt exact {report['job_ledgers_unchanged_default']['field_opt_exact']}",
        f"- chemistry {report['job_ledgers_unchanged_default']['chem_0_5']} @0.5%",
        f"- QM waves {report['job_ledgers_unchanged_default']['qm_0_5']} @0.5%",
        f"- G1 vs BKS {report['job_ledgers_unchanged_default']['g1_rel_pct']}%",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.bleed_refine",
        "```",
        "",
        "Mother repo: https://github.com/dappalumbo91/FSOT-2.1-Lean",
        "",
    ]
    text = "\n".join(md)
    (out / "BLEED_REFINE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "BLEED_REFINE.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "bleed": report["bleed"],
        "lean_atlas": report["lean_atlas"],
        "jobs": report["job_ledgers_unchanged_default"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


def math_ok(eq: dict, mod: dict) -> bool:
    """Finite coupling, steps from seeds, modulation finite and positive."""
    if eq["steps"] < 1:
        return False
    if not (0 < eq["yin_yang"] < 1):
        return False
    m = mod.get("mod")
    return m is not None and m > 0 and abs(m) < 10


if __name__ == "__main__":
    raise SystemExit(main())
