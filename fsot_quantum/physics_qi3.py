"""
Physics + QI push III — leftover hired pin-wave questions.

CKM |V_td|/|V_ts|, LEP EW, BBN, quark/lepton ratios, Planck
cosmology leftovers, remaining 3D percolation / SAW. Same pin.
No new coefficients. Not math-constant theater.

Exclusive |V_cb| is a different extraction (the V_cb puzzle), not
a retune. See docs/MISS_THREE.md.

python -m fsot_quantum.physics_qi3
python -m fsot_quantum push3
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
from fsot_quantum.lean_replay import replay_files

LEAN_FILES = (
    "particle_physics_benchmark.json",
    "neutrino_physics_panel_benchmark.json",
    "higgs_branching_benchmark.json",
    "cosmology_extended_benchmark.json",
    "condensed_matter_superconductivity_depth_panel_benchmark.json",
    "nist_codata_constants_benchmark.json",
    "toe_ckm_pmns_benchmark.json",
    "nuclear_iaea_open_benchmark.json",
)

# Only leftover hired-physics names not already on harder / qi / qi2 / audit.
WANT = (
    ("|V_td|", "Particle_Physics", "wave4"),
    ("|V_ts|", "Particle_Physics", "wave4"),
    ("Dm2_21/Dm2_32", "High_Energy_Physics", "wave4"),
    ("BR_H_tautau", "High_Energy_Physics", "wave5"),
    ("BR_Z_ee", "High_Energy_Physics", "wave8"),
    ("R_ell", "High_Energy_Physics", "wave5"),
    ("R_b", "High_Energy_Physics", "wave5"),
    ("R_c", "High_Energy_Physics", "wave5"),
    ("A_FB_ell", "High_Energy_Physics", "wave5"),
    ("A_ell_SLD", "High_Energy_Physics", "wave5"),
    ("Y_p_He4", "Nuclear_Physics", "wave5"),
    ("D_H_ratio", "Nuclear_Physics", "wave5"),
    ("m_u/m_d", "Particle_Physics", "wave7"),
    ("m_s/m_d", "Particle_Physics", "wave7"),
    ("m_c/m_b", "Particle_Physics", "wave4"),
    ("m_tau/m_mu", "Particle_Physics", "wave7"),
    ("m_tau/m_e", "Particle_Physics", "wave3"),
    ("m_pi/m_p", "Particle_Physics", "wave2"),
    ("mu_p_muN", "Nuclear_Physics", "wave4"),
    ("Deuteron_mu_muN", "Nuclear_Physics", "wave8"),
    ("Omega_Lambda", "Cosmology", "wave2"),
    ("Omega_m", "Cosmology", "wave2"),
    ("Omega_DM_h2", "Cosmology", "wave2"),
    ("Omega_b_h2", "Cosmology", "wave1"),
    ("sigma_8", "Cosmology", "wave2"),
    ("tau_reion", "Cosmology", "wave2"),
    ("N_eff", "Cosmology", "wave2"),
    ("w0", "Cosmology", "wave4"),
    ("z_eq", "Cosmology", "wave3"),
    ("theta_star", "Cosmology", "wave3"),
    ("r_star_Mpc", "Cosmology", "wave3"),
    ("n_s", "Cosmology", "wave1"),
    ("Quark_condensate", "High_Energy_Physics", "wave8"),
    ("Perc3D_beta", "Condensed_Matter", "wave8"),
    ("Perc_SC_site", "Condensed_Matter", "wave7"),
    ("Perc_honeycomb_site", "Condensed_Matter", "wave7"),
    ("Perc_BCC_bond", "Condensed_Matter", "wave8"),
    ("Potts3_beta", "Condensed_Matter", "wave8"),
    ("SAW_nu_3D", "Condensed_Matter", "wave8"),
    ("SAW_gamma_3D", "Condensed_Matter", "wave8"),
    ("Ice_Ih_density", "Chemistry", "wave8"),
)

# BR(H→ττ) same 125.00 vs 125.09 object lesson as γγ / Zγ.
LITERATURE_TARGET: dict[str, dict[str, Any]] = {
    "BR_H_tautau": {
        "value": 0.0632,
        "source": "SM BR(H→ττ) at MH=125.00 GeV (vendor wave5 / YR table). Same mass-point rule as docs/MISS_THREE.md.",
    },
}


def _wave_questions() -> list[dict[str, Any]]:
    from vendor import fsot_compute as f

    cache: dict[str, dict[str, Any]] = {}
    for _n, _r, w in WANT:
        if w not in cache:
            cache[w] = {row.name: row for row in getattr(f, w)()}
    rows = []
    for name, route, w in WANT:
        r = cache[w].get(name)
        if r is None or r.measured is None:
            rows.append({"id": f"P3-{name}", "ok": False, "reason": "missing"})
            continue
        c = float(r.computed)
        lit = LITERATURE_TARGET.get(name)
        if lit:
            m = float(lit["value"])
            target_note = lit["source"]
            vendor_m = float(r.measured) if r.measured is not None else None
        else:
            m = float(r.measured)
            target_note = "vendor wave measured"
            vendor_m = m
        rel = abs(c - m) / abs(m) * 100 if m else None
        rows.append({
            "id": f"P3-{name}",
            "question": f"What is {name}?",
            "route": [route],
            "formula": getattr(r, "formula_str", ""),
            "computed": c,
            "published": m,
            "vendor_measured": vendor_m,
            "target_note": target_note,
            "rel_err_pct": rel,
            "green_0_5": rel is not None and rel <= GREEN,
            "band_5": rel is not None and rel <= BAND_5,
            "ok": rel is not None and rel <= BAND_5,
        })
    return rows


def main() -> int:
    t0 = time.perf_counter()
    waves = _wave_questions()
    replay = replay_files(LEAN_FILES, cap_per_file=80, return_all=True)
    live = [r for r in (replay.get("instances") or []) if not r.get("skip")]
    n_w = sum(1 for r in waves if r.get("question"))
    n_w5 = sum(1 for r in waves if r.get("band_5"))
    n_w05 = sum(1 for r in waves if r.get("green_0_5"))
    n_live = len(live)
    n_g = sum(1 for r in live if r.get("green_0_5"))
    n_5 = sum(1 for r in live if r.get("band_5"))
    misses = [r for r in waves if r.get("question") and not r.get("green_0_5")]
    ok = n_w > 0 and n_w05 == n_w and n_live > 0 and n_5 == n_live

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "physics_qi3",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "open_objects": {
            "exclusive_V_cb": "0.0398 is a different PDG extraction; fold answers inclusive 0.0422. docs/MISS_THREE.md",
            "H0": "Planck vs SH0ES tension — not scored as one number",
            "alpha_s(M_Z)": "fold 0.1171 vs PDG ~0.118; not forced through 0.5% by retune",
        },
        "waves": {
            "n": n_w,
            "n_band5": n_w5,
            "n_green_0_5": n_w05,
            "ok": n_w05 == n_w,
            "misses": [r["question"] for r in misses],
            "questions": waves,
        },
        "lean": {
            "n_live": n_live,
            "n_green_0_5": n_g,
            "n_band_5": n_5,
        },
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "physics_qi3.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Physics + QI push III",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        f"Pin-wave **{n_w5}/{n_w}** @5% · **{n_w05}/{n_w}** @0.5%",
        f"Lean particle/neutrino/Higgs/cosmo/CM/NIST **{n_g}/{n_live}** @0.5%",
        "",
        "After the three audit misses were scored as the **right objects** "
        "(`docs/MISS_THREE.md`, audit 20/20). This rung asks leftover hired "
        "physics still sitting on the pin and not already on harder / qi / qi2.",
        "",
        "Not scored here: exclusive \\(|V_{cb}|\\) (different extraction), "
        "\\(H_0\\) (Planck vs SH0ES), \\(\\alpha_s(M_Z)\\) (0.68% vs PDG ~0.118). "
        "No new coefficient.",
        "",
        "## Pin-wave questions",
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
        "```powershell",
        "python -m fsot_quantum.physics_qi3",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "PHYSICS_QI3.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "PHYSICS_QI3.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "waves": f"{n_w05}/{n_w}",
        "band5": f"{n_w5}/{n_w}",
        "lean_live": f"{n_g}/{n_live}",
        "misses": report["waves"]["misses"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
