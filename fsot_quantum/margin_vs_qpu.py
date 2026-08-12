"""
Margin of error: FSOT field-of-use vs what QPUs have actually published.

This is a *job* comparison, not "our two-qubit gate vs IBM's".
A NISQ chip has a gate-error model. FSOT here answers the same hired
jobs with pin math (collapse, consensus, D_eff, seed formulas).

QPU numbers are literature-typical NISQ figures with citations in the
ledger — not scraped marketing. FSOT numbers are live from this repo.

Refinement doctrine (same as FSOT-Genetics domain interface):
  residual high → try adjacent *named* D_eff route, report, do not auto-fit.

python -m fsot_quantum.margin_vs_qpu
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.fsot_field_opt import run_fsot_field_opt_panel
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


# ---------------------------------------------------------------------------
# What QPUs have been *shown* to do in the field (typical NISQ, not ads)
# ---------------------------------------------------------------------------

QPU_FIELD = [
    {
        "job": "two_qubit_gate",
        "qpu_what": "Physical 2q gate fidelity on IBM/Google/IonQ NISQ",
        "qpu_error": "0.1–1% per gate (fidelity ~99.0–99.9%)",
        "qpu_cite": "device data sheets / IBM Quantum / Google Sycamore-class papers 2019–2025",
        "fsot_object": "no physical gate; collapse Θ is the analog of 'error floor' on a field",
        "fsot_margin": "Θ = C_eff·P_var ≈ 0.917 (not a % gate error)",
        "apples": False,
        "note": "Do not convert Θ into a fake IBM-style gate fidelity.",
    },
    {
        "job": "readout",
        "qpu_what": "Measurement assignment error",
        "qpu_error": "~0.5–5% typical superconducting; lower on some ions",
        "qpu_cite": "IBM Quantum backend properties (typical range)",
        "fsot_object": "superposed (0) resolves with sign(S(domain)) — deterministic",
        "fsot_margin": "0% RNG readout; wrong *domain* is the residual source",
        "apples": False,
        "note": "Different mechanism. Refinement = correct D_eff route, not a readout matrix.",
    },
    {
        "job": "VQE_small_molecule",
        "qpu_what": "Ground-state energy of H2/LiH/BeH2 on NISQ",
        "qpu_error": "Often misses chemical accuracy (1.6 mHa) without heavy mitigation; rare demos claim <1.6 mHa on toy geometries",
        "qpu_cite": "Kandala et al. Nature 2017; Qunova 2024 chemical-accuracy claims on commercial NISQ",
        "fsot_object": "pin chemistry observables (not the electronic Hamiltonian FCI)",
        "fsot_margin": None,  # filled live
        "apples": "partial — both hired as 'chemistry answers'; objects differ",
        "note": "Chemical accuracy ≈ 1.6 mHa. Our 0.5% band is relative error on pin formulas.",
    },
    {
        "job": "QAOA_MaxCut",
        "qpu_what": "Small MaxCut / Ising on 4–20 noisy qubits",
        "qpu_error": "Approximation ratio often ~0.7–0.9 of optimum; noise + shallow p",
        "qpu_cite": "Farhi et al.; IBM QAOA hardware papers (typical NISQ ratios)",
        "fsot_object": "collapse+consensus field on the graph (exact enum n≤12; G1 vs published BKS)",
        "fsot_margin": None,
        "apples": True,
        "note": "Same job class: cut / energy. We do not run a noisy p-layer QAOA circuit.",
    },
    {
        "job": "Shor_tiny",
        "qpu_what": "Factor 15 (and a few other tiny N) with compiled circuits",
        "qpu_error": "Demo success; not a scalable period-finding machine",
        "qpu_cite": "Vandersypen et al. Nature 2001; later photonic/ion compiled Shor-15",
        "fsot_object": "modular order fold + GPU statevector N≤51",
        "fsot_margin": None,
        "apples": True,
        "note": "Both are tiny-N. Neither is RSA. Exact recovery is the margin (0 or fail).",
    },
    {
        "job": "Bell_GHZ",
        "qpu_what": "Few-qubit Bell/GHZ on hardware after mitigation",
        "qpu_error": "Typically a few % below ideal fidelity",
        "qpu_cite": "standard device characterization",
        "fsot_object": "optional Hilbert bridge Bell F (sim) + consensus Bell analog",
        "fsot_margin": "sim F=1 is not a hardware fidelity — do not advertise as beating IBM Bell",
        "apples": False,
        "note": "Simulated unitaries have zero shot noise. That is not a QPU win.",
    },
    {
        "job": "surface_code",
        "qpu_what": "Below-threshold logical-qubit demos (small d)",
        "qpu_error": "Logical error still large at small distance; physical ~1e-3",
        "qpu_cite": "Google quantum error-correction papers (Sycamore / Willow class)",
        "fsot_object": "planar d=3/5/7 decode of injected t errors",
        "fsot_margin": "correctable-t exact on the abstract code; not a device threshold",
        "apples": False,
        "note": "We are not claiming a fridge-threshold experiment.",
    },
]


def _adjacent_routes(name: str) -> list[str]:
    """Lawful neighbors on the pin D_eff ladder — no continuous search."""
    if name not in DOMAINS:
        return []
    d0 = DOMAINS[name].D_eff
    out = []
    for k, v in DOMAINS.items():
        if k == name:
            continue
        if abs(v.D_eff - d0) <= 3:
            out.append(k)
    return out


def domain_refine_probe() -> dict[str, Any]:
    """
    Report S at QM and adjacent pin domains.
    Does **not** pick a winner to lower residual (that would be a fit).
    """
    core = [
        "Quantum_Mechanics",
        "Quantum_Computing",
        "Quantum_Optics",
        "Particle_Physics",
        "Atomic_Physics",
        "High_Energy_Physics",
        "Chemistry",
        "Molecular_Chemistry",
    ]
    rows = []
    for name in core:
        if name not in DOMAINS:
            continue
        s = domain_scalar(name)
        rows.append({
            "domain": name,
            "D_eff": DOMAINS[name].D_eff,
            "observed": DOMAINS[name].observed,
            "S": s,
            "class": "emergence" if s > 0 else "damping",
            "adjacent": _adjacent_routes(name),
        })
    return {
        "panel": "domain_refine_probe",
        "doctrine": "change named domain / D_eff; do not invent coefficients",
        "instances": rows,
        "overall_ok": len(rows) >= 6,
        "physics_reading": (
            "QM D=6 observed emergence (S>0) is the measurement / spin-law interface. "
            "QC D=11 unobserved damping (S<0) is the compute substrate before an observer "
            "hit. If that reading is wrong, the route table is what to correct — not a fit."
        ),
    }


def run_margin_panel() -> dict[str, Any]:
    chem = run_chemistry_fold_panel()
    qm = run_qm_wave_use_panel()
    opt = run_fsot_field_opt_panel()
    gset = run_gset_official_panel()
    probe = domain_refine_probe()

    g1 = None
    for r in gset.get("instances") or []:
        if str(r.get("name", "")).upper().startswith("G1"):
            g1 = r
            break

    # Fill live FSOT margins
    live = {row["job"]: row for row in QPU_FIELD}
    live["VQE_small_molecule"]["fsot_margin"] = (
        f"chemistry fold {chem['n_green_0_5_fold']}/{chem['n_observables']} "
        f"@0.5% (median {chem['median_rel_err_fold_pct']:.4f}%)"
    )
    live["QAOA_MaxCut"]["fsot_margin"] = (
        f"field opt exact {opt['exact_hits']}/{opt['exact_total']}; "
        f"G1 rel vs published BKS "
        f"{(g1 or {}).get('rel_err_vs_published_pct')}%"
    )
    live["Shor_tiny"]["fsot_margin"] = "period/factor exact on ledgered tiny N (not RSA)"

    # Refinement targets: anything not in 0.5% green, or G1 vs BKS
    refine = []
    if g1 and g1.get("rel_err_vs_published_pct") and g1["rel_err_vs_published_pct"] > 0.5:
        refine.append({
            "target": "Gset G1 MaxCut",
            "current_margin_pct": g1["rel_err_vs_published_pct"],
            "qpu_typical": "NISQ QAOA rarely reports 800-vertex hardware cuts",
            "fsot_next": (
                "Keep collapse+consensus field; more φ-starts from seeds only. "
                "Do not add a free temperature or learning rate."
            ),
            "domain_route": "Quantum_Computing (compute) + Condensed_Matter (graph pack)",
        })
    worst_qm = (qm.get("worst") or [None])[0]
    if worst_qm:
        refine.append({
            "target": f"QM pin {worst_qm['name']}",
            "current_margin_pct": worst_qm["rel_err_pct"],
            "qpu_typical": "QPUs do not compute α or M_Z/M_W; that is SM/data",
            "fsot_next": (
                "If residual grows, retune *route* (Particle / High_Energy / Atomic) "
                "not a coefficient. Default stays pin formula."
            ),
            "domain_route": "Particle_Physics D=5 / High_Energy D=7 / Atomic D=7",
        })
    refine.append({
        "target": "add field jobs QPUs are actually paid for",
        "current_margin_pct": None,
        "qpu_typical": "sampling, small VQE, small QAOA, characterization",
        "fsot_next": (
            "More pin-formula QM/QC atlas rows from FSOT-2.1-Lean "
            "(Quantum_Information 21 obs, QC gap-fill 177, QM gap-fill 50) "
            "ported as *formulas*, not as 2^n circuits."
        ),
        "domain_route": "import Lean gap-fill observables; still zero free params",
    })

    # Comparison rows for the markdown table
    compare = []
    for job in QPU_FIELD:
        compare.append({
            "job": job["job"],
            "qpu_error": job["qpu_error"],
            "fsot_margin": job["fsot_margin"],
            "same_object": job["apples"],
            "cite": job["qpu_cite"],
        })

    overall = (
        chem["overall_ok"]
        and chem["aspiration_0_5_ok"]
        and qm["overall_ok"]
        and opt["overall_ok"]
        and gset["overall_ok"]
        and probe["overall_ok"]
    )

    return {
        "panel": "margin_vs_qpu",
        "pin": "D1D38A",
        "qpu_field": QPU_FIELD,
        "live": {
            "chem_green": f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
            "chem_median_pct": chem["median_rel_err_fold_pct"],
            "qm_green": f"{qm['n_green_0_5']}/{qm['n_observables']}",
            "qm_median_pct": qm["median_rel_err_pct"],
            "qm_worst": worst_qm,
            "field_opt_exact": f"{opt['exact_hits']}/{opt['exact_total']}",
            "g1": g1,
            "S_QM": domain_scalar("Quantum_Mechanics"),
            "S_QC": domain_scalar("Quantum_Computing"),
        },
        "compare": compare,
        "refine": refine,
        "domain_probe": probe,
        "lean_atlas_ready_to_port": {
            "Quantum_Mechanics_gap_fill": "50 records, median% ~9.5e-5",
            "Quantum_Computing_gap_fill": "177 records, median% ~3.0e-4",
            "Quantum_Information": "21 records, median% 0",
            "Quantum_Optics_gap_fill": "50 records, median% ~9.5e-5",
            "source": "FSOT-2.1-Lean verified solves inventory",
        },
        "overall_ok": overall,
        "question_for_author": (
            "QC domain is pin-unobserved and S<0 (damping). "
            "Reading used here: compute substrate sits *before* observer collapse; "
            "QM D=6 observed S>0 is the measurement law. "
            "If the fluid picture is different (e.g. QC damping is decoherence-class "
            "on purpose), say how the system should interact and we will route that way."
        ),
    }


def main() -> int:
    t0 = time.perf_counter()
    panel = run_margin_panel()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "margin_vs_qpu",
        "pin": "D1D38A",
        "overall_ok": panel["overall_ok"],
        "wall_seconds": time.perf_counter() - t0,
        "live": panel["live"],
        "compare": panel["compare"],
        "refine": panel["refine"],
        "domain_probe": {
            "ok": panel["domain_probe"]["overall_ok"],
            "physics_reading": panel["domain_probe"]["physics_reading"],
            "n_domains": len(panel["domain_probe"]["instances"]),
        },
        "lean_atlas_ready_to_port": panel["lean_atlas_ready_to_port"],
        "question_for_author": panel["question_for_author"],
        "qpu_field": panel["qpu_field"],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "margin_vs_qpu.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Margin vs what quantum computers have actually done",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "This compares **jobs**, not fridge-gate fidelities. "
        "A QPU error bar is noise on a unitary. Our margin is residual of FSOT math "
        "against the same *hired answer*. Where the object differs, the table says so.",
        "",
        "## Live FSOT margins (this repo)",
        "",
        f"- chemistry fold: **{report['live']['chem_green']} @ 0.5%** "
        f"(median {report['live']['chem_median_pct']:.4f}%)",
        f"- QM pin waves: **{report['live']['qm_green']} @ 0.5%** "
        f"(median {report['live']['qm_median_pct']:.5f}%)",
        f"- field Ising/MaxCut exact: **{report['live']['field_opt_exact']}**",
        f"- G1 vs published BKS 11624: "
        f"**{(report['live']['g1'] or {}).get('rel_err_vs_published_pct')}%**",
        f"- S(QM)={report['live']['S_QM']:.4f} · S(QC)={report['live']['S_QC']:.4f}",
        "",
        "## Side-by-side",
        "",
        "| Job | Typical QPU field error | FSOT margin | Same object? |",
        "|-----|-------------------------|-------------|--------------|",
    ]
    for c in report["compare"]:
        md.append(
            f"| {c['job']} | {c['qpu_error']} | {c['fsot_margin']} | {c['same_object']} |"
        )
    md += [
        "",
        "## Where to refine (FSOT law, not a fudge)",
        "",
    ]
    for r in report["refine"]:
        md.append(f"### {r['target']}")
        md.append("")
        if r["current_margin_pct"] is not None:
            md.append(f"- current margin: **{r['current_margin_pct']:.4f}%**")
        md.append(f"- QPU typical: {r['qpu_typical']}")
        md.append(f"- next: {r['fsot_next']}")
        md.append(f"- route: `{r['domain_route']}`")
        md.append("")
    md += [
        "## Lean atlas sitting next door (FSOT-2.1-Lean)",
        "",
        "Not yet ported into this granular QC fold — next field-use add:",
        "",
    ]
    for k, v in report["lean_atlas_ready_to_port"].items():
        md.append(f"- **{k}:** {v}")
    md += [
        "",
        "## Physics reading (correct me if the fluid picture differs)",
        "",
        report["question_for_author"],
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.margin_vs_qpu",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "MARGIN_VS_QPU.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "MARGIN_VS_QPU.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "live": report["live"],
        "refine": report["refine"],
        "question_for_author": report["question_for_author"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2, default=str))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
