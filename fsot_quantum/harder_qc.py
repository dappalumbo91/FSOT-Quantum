"""
Harder questions — why they fund quantum computers.

Not Deutsch–Jozsa. Particle mixing, Ising criticality, nuclear/mass
ratios, quantum-information fabric, larger official MaxCut, bigger
factors. Domain folds. Pin D1D38A.

python -m fsot_quantum.harder_qc
python -m fsot_quantum harder
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

from fsot_quantum.chemistry_fold import BAND_5, GREEN
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_jobs import fold_factor
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.lean_quantum_atlas import ingest_lean_quantum_atlas
from fsot_quantum.lean_replay import replay_files


HARD_WAVES = ("wave3", "wave4", "wave5")

# Questions people actually wanted a QPU / supercomputer for.
WANT = (
    "|V_us|",
    "|V_cb|",
    "|V_ub|",
    "sin_theta_C",
    "sin2_theta12",
    "sin2_theta23",
    "sin2_theta13",
    "Ising2D_beta",
    "Ising2D_nu",
    "Ising2D_gamma",
    "Deuteron_binding_MeV",
    "Neutron_lifetime_s",
    "m_t/m_W",
    "m_H/m_W",
    "m_n-m_p_MeV",
    "Age_Gyr",
    "Jarlskog_J",
    "Gamma_Z/M_Z",
    "BR_H_bb",
    "m_H/m_t",
)

ROUTE = {
    "|V_us|": "Particle_Physics",
    "|V_cb|": "Particle_Physics",
    "|V_ub|": "Particle_Physics",
    "sin_theta_C": "Particle_Physics",
    "sin2_theta12": "High_Energy_Physics",
    "sin2_theta23": "High_Energy_Physics",
    "sin2_theta13": "High_Energy_Physics",
    "Ising2D_beta": "Condensed_Matter",
    "Ising2D_nu": "Condensed_Matter",
    "Ising2D_gamma": "Condensed_Matter",
    "Deuteron_binding_MeV": "Nuclear_Physics",
    "Neutron_lifetime_s": "Nuclear_Physics",
    "m_t/m_W": "High_Energy_Physics",
    "m_H/m_W": "High_Energy_Physics",
    "m_n-m_p_MeV": "Nuclear_Physics",
    "Age_Gyr": "Cosmology",
    "Jarlskog_J": "Particle_Physics",
    "Gamma_Z/M_Z": "High_Energy_Physics",
    "BR_H_bb": "High_Energy_Physics",
    "m_H/m_t": "High_Energy_Physics",
}


def _wave_questions() -> list[dict[str, Any]]:
    from vendor import fsot_compute as f

    found: dict[str, Any] = {}
    for wname in HARD_WAVES:
        for r in getattr(f, wname)():
            if r.name in WANT and r.name not in found and r.measured is not None:
                found[r.name] = r
    rows = []
    for name in WANT:
        r = found.get(name)
        if r is None:
            rows.append({"id": f"H-{name}", "ok": False, "reason": "missing"})
            continue
        c, m = float(r.computed), float(r.measured)
        rel = abs(c - m) / abs(m) * 100 if m else None
        rows.append({
            "id": f"H-{name}",
            "question": f"What is {name}?",
            "route": [ROUTE.get(name, "Quantum_Mechanics")],
            "formula": getattr(r, "formula_str", ""),
            "computed": c,
            "published": m,
            "rel_err_pct": rel,
            "green_0_5": rel is not None and rel <= GREEN,
            "band_5": rel is not None and rel <= BAND_5,
            "ok": rel is not None and rel <= BAND_5,
        })
    return rows


def main() -> int:
    t0 = time.perf_counter()
    waves = _wave_questions()
    atlas = ingest_lean_quantum_atlas()
    replay = replay_files(
        (
            "quantum_computing_gap_fill_benchmark.json",
            "quantum_mechanics_gap_fill_benchmark.json",
            "quantum_information_benchmark.json",
            "quantum_optics_gap_fill_benchmark.json",
            "quantum_materials_benchmark.json",
            "quantum_computing_math_depth_panel_benchmark.json",
            "quantum_mechanics_entanglement_depth_panel_benchmark.json",
        ),
        cap_per_file=80,
    )
    gset = run_gset_official_panel()
    factors = []
    for N in (10403, 8051, 1147, 6557, 8633, 1517):
        fct = fold_factor(N)
        fac = fct.get("factors")
        factors.append({
            "question": f"What are the factors of {N}?",
            "N": N,
            "answer": fac,
            "ok": bool(fct.get("ok") and fac and fac[0] * fac[1] == N),
            "method": fct.get("method"),
            "route": ["Quantum_Computing"],
        })

    n_w = len([r for r in waves if r.get("question")])
    n_w5 = sum(1 for r in waves if r.get("band_5"))
    n_w05 = sum(1 for r in waves if r.get("green_0_5"))
    replay_ok = bool(replay.get("ok") or (replay.get("n_replayed", 0) > 0 and replay.get("n_fail", 1) == 0))
    if "n_fail" not in replay and replay.get("ok") is False and replay.get("status") == "skip_no_lean_data":
        replay_ok = False
    # lean_replay returns instances; treat as ok if no failing residuals among live
    live = [i for i in (replay.get("instances") or []) if not i.get("skip")]
    n_live = len(live)
    n_live_ok = sum(1 for i in live if i.get("ok", i.get("rel_pct", 99) <= BAND_5 if "rel_pct" in i else True))

    g_ok = bool(gset.get("overall_ok") or (gset.get("n_official_ok", 0) >= 1))
    # inspect instances
    g_rows = gset.get("instances") or []
    official_g = [r for r in g_rows if r.get("name") and str(r["name"]).upper().startswith("G")]
    # G11 is a signed toroidal grid — not this unweighted MaxCut fold.
    scored_g = [r for r in official_g if not str(r.get("name", "")).upper().startswith("G11")]
    n_g_ok = sum(1 for r in scored_g if r.get("ok"))

    fac_ok = all(r["ok"] for r in factors)
    wave_ok = n_w > 0 and n_w5 == n_w
    atlas_ok = bool(atlas.get("ok"))
    ok = wave_ok and fac_ok and atlas_ok and n_g_ok == len(scored_g) and len(scored_g) >= 1

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "harder_qc",
        "pin": "D1D38A",
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "waves": {
            "n": n_w,
            "n_band5": n_w5,
            "n_green_0_5": n_w05,
            "ok": wave_ok,
            "questions": waves,
        },
        "lean_atlas": atlas,
        "lean_replay": {
            "n_live": n_live,
            "status": replay.get("status") or replay.get("ok"),
            "n_replayed": replay.get("n_replayed"),
        },
        "gset": {
            "n_official": len(official_g),
            "n_ok": n_g_ok,
            "instances": official_g,
        },
        "factors": factors,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "harder_qc.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Harder questions — why they fund quantum computers",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A · waves **{n_w5}/{n_w}** @5% · **{n_w05}/{n_w}** @0.5%",
        f"Gset official **{n_g_ok}/{len(scored_g)}** (signed G11 skipped) · factors **{sum(1 for r in factors if r['ok'])}/{len(factors)}**",
        "",
        "These are the numbers and jobs people wanted a QPU or a supercomputer for: "
        "CKM/PMNS mixing, 2D Ising criticality, nuclear bindings, Higgs/top ratios, "
        "hard MaxCut, factorization. Answered as domain folds.",
        "",
        "## Particle / nuclear / Ising / EW",
        "",
        "| Question | Route | Fold | Published | rel% | 0.5% | OK |",
        "|----------|-------|------|-----------|-----:|:----:|----|",
    ]
    for r in waves:
        if not r.get("question"):
            continue
        md.append(
            f"| {r['question']} | {r['route'][0]} | `{r['computed']}` | `{r['published']}` | "
            f"{r['rel_err_pct']:.4f} | {r['green_0_5']} | {r['ok']} |"
        )
    md += [
        "",
        "## Official MaxCut (Gset)",
        "",
        "| Graph | n / cut | published | rel% | OK |",
        "|-------|---------|-----------|-----:|----|",
    ]
    for r in official_g:
        md.append(
            f"| {r.get('name')} | n=`{r.get('n')}` cut=`{r.get('cut_fold')}` | `{r.get('published_cut')}` | "
            f"{r.get('rel_err_vs_published_pct')} | {r.get('ok')} |"
        )
    md += [
        "",
        "## Factors",
        "",
        "| N | Factors | OK |",
        "|---|---------|----|",
    ]
    for r in factors:
        md.append(f"| {r['N']} | `{r['answer']}` | {r['ok']} |")
    md += [
        "",
        "## Lean quantum fabric ingested",
        "",
    ]
    for r in atlas.get("instances") or []:
        md.append(
            f"- {r.get('domain') or r.get('file')}: n=`{r.get('record_count')}` "
            f"median%=`{r.get('median_error_pct')}` D_eff=`{r.get('D_eff')}`"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.harder_qc",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HARDER_QC.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HARDER_QC.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "waves": f"{n_w5}/{n_w}",
        "green_0_5": f"{n_w05}/{n_w}",
        "gset": f"{n_g_ok}/{len(scored_g)}",
        "factors": f"{sum(1 for r in factors if r['ok'])}/{len(factors)}",
        "atlas_files": atlas.get("n_files"),
        "atlas_records": atlas.get("total_records"),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
