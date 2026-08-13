"""
Next ladder rung: physics + quantum information.

Graph MaxCut is under 1% (aspiration met). This rung asks the QI and
condensed-matter / lepton numbers people wanted a QPU to reach —
plus the Lean QI fabric already solved on the same pin.

python -m fsot_quantum.physics_qi
python -m fsot_quantum qi
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

LEAN_QI = (
    "quantum_information_benchmark.json",
    "quantum_mechanics_entanglement_depth_panel_benchmark.json",
    "quantum_computing_math_depth_panel_benchmark.json",
    "quantum_computing_gap_fill_benchmark.json",
    "quantum_mechanics_gap_fill_benchmark.json",
    "quantum_optics_gap_fill_benchmark.json",
    "quantum_materials_benchmark.json",
    "founding_quantum_vacuum_panel_benchmark.json",
)

# Published pin-wave questions not yet on the harder-QC rung.
WANT = (
    ("Hashing_bound", "Quantum_Information", "wave6"),
    ("Nats_per_bit", "Quantum_Information", "wave6"),
    ("Ising3D_eta", "Condensed_Matter", "wave7"),
    ("Ising3D_alpha", "Condensed_Matter", "wave7"),
    ("Ising3D_delta", "Condensed_Matter", "wave7"),
    ("XY_nu", "Condensed_Matter", "wave7"),
    ("XY_eta", "Condensed_Matter", "wave7"),
    ("Heisenberg_nu", "Condensed_Matter", "wave7"),
    ("Heisenberg_eta", "Condensed_Matter", "wave7"),
    ("Lieb_square_ice", "Condensed_Matter", "wave7"),
    ("KT_T/J", "Condensed_Matter", "wave8"),
    ("(g-2)/2_electron", "Quantum_Mechanics", "wave10"),
    ("m_mu/m_e", "Particle_Physics", "wave10"),
    ("|V_ud|", "Particle_Physics", "wave8"),
    ("|V_cs|", "Particle_Physics", "wave8"),
    ("|V_tb|", "Particle_Physics", "wave9"),
)

QI_NAMES = {
    "surface_code_threshold",
    "toric_code_threshold",
    "fault_tolerant_threshold",
    "bell_state_entropy",
    "page_curve_ratio",
    "holevo_bound_ratio",
    "quantum_channel_capacity",
    "gate_fidelity_threshold",
    "coherence_time_ratio",
    "quantum_volume_log2",
}


def _wave_questions() -> list[dict[str, Any]]:
    from vendor import fsot_compute as f

    found: dict[str, Any] = {}
    for _name, _route, w in WANT:
        if w not in found:
            found[w] = {r.name: r for r in getattr(f, w)()}
    rows = []
    for name, route, w in WANT:
        r = found[w].get(name)
        if r is None or r.measured is None:
            rows.append({"id": f"Q-{name}", "ok": False, "reason": "missing"})
            continue
        c, m = float(r.computed), float(r.measured)
        rel = abs(c - m) / abs(m) * 100 if m else None
        rows.append({
            "id": f"Q-{name}",
            "question": f"What is {name}?",
            "route": [route],
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
    replay = replay_files(LEAN_QI, cap_per_file=80, return_all=True)
    live = [r for r in (replay.get("instances") or []) if not r.get("skip")]
    qi_named = [r for r in live if r.get("name") in QI_NAMES]
    n_w = sum(1 for r in waves if r.get("question"))
    n_w5 = sum(1 for r in waves if r.get("band_5"))
    n_w05 = sum(1 for r in waves if r.get("green_0_5"))
    n_live = len(live)
    n_g = sum(1 for r in live if r.get("green_0_5"))
    n_5 = sum(1 for r in live if r.get("band_5"))
    qi_ok = bool(qi_named) and all(r.get("green_0_5") for r in qi_named)
    wave_ok = n_w > 0 and n_w5 == n_w
    replay_ok = n_live > 0 and n_5 == n_live
    ok = wave_ok and replay_ok and qi_ok

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "physics_qi",
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
        "lean_replay": {
            "n_live": n_live,
            "n_green_0_5": n_g,
            "n_band_5": n_5,
            "n_qi_named": len(qi_named),
            "qi_named": qi_named,
        },
        "graph_rung": {
            "closed_aspiration": "<1% G1/G14/G22",
            "note": "Further graph chase is not this rung. Champions still unmatched.",
        },
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "physics_qi.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Physics + quantum information rung",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A",
        f"Pin-wave **{n_w5}/{n_w}** @5% · **{n_w05}/{n_w}** @0.5%",
        f"Lean QI/QM/QC fabric **{n_g}/{n_live}** @0.5% · named QI **{len(qi_named)}**",
        "",
        "Graph MaxCut is under 1% (G1/G14/G22). This rung is the next physics/QI "
        "questions: 3D Ising / XY / Heisenberg, hashing bound, g−2, lepton ratio, "
        "remaining CKM, and the Lean quantum-information fabric "
        "(surface/toric thresholds, Bell entropy, Holevo, channel capacity).",
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
        "## Named QI fabric (Lean material records)",
        "",
        "| Name | computed | measured | rel% | OK |",
        "|------|----------|----------|-----:|----|",
    ]
    for r in qi_named:
        md.append(
            f"| {r['name']} | `{r['computed']}` | `{r['measured']}` | "
            f"{r['rel_err_pct']:.4f} | {r.get('green_0_5')} |"
        )
    md += [
        "",
        f"Full Lean replay on this rung: **{n_g}/{n_live}** inside 0.5% "
        f"({n_5}/{n_live} inside 5%).",
        "",
        "```powershell",
        "python -m fsot_quantum.physics_qi",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "PHYSICS_QI.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "PHYSICS_QI.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "waves": f"{n_w5}/{n_w}",
        "green_0_5": f"{n_w05}/{n_w}",
        "lean_live": f"{n_g}/{n_live}",
        "qi_named": len(qi_named),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
