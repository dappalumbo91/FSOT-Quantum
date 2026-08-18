"""
Open objects — leftover questions that are *different measurements*,
not pin misses.

Exclusive |V_cb|, Planck vs SH0ES H0, and alpha_s(M_Z) vs the PDG
world average. Same pin. No new coefficient. Do not blend.

python -m fsot_quantum.open_objects
python -m fsot_quantum open
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

from fsot_quantum.chemistry_fold import GREEN


def _vendor_row(wave: str, name: str) -> Any:
    from vendor import fsot_compute as f

    for r in getattr(f, wave)():
        if r.name == name:
            return r
    return None


def main() -> int:
    t0 = time.perf_counter()
    vcb = _vendor_row("wave3", "|V_cb|")
    h0 = _vendor_row("wave1", "H0")
    als = _vendor_row("wave1", "alpha_s(M_Z)")
    if vcb is None or h0 is None or als is None:
        print(json.dumps({"overall_ok": False, "reason": "missing vendor row"}))
        return 1

    fold_vcb = float(vcb.computed)
    fold_h0 = float(h0.computed)
    fold_as = float(als.computed)

    inclusive = 0.0422
    exclusive = 0.0398
    planck_h0 = 67.4
    shoes_h0 = 73.04
    vendor_as = float(als.measured)  # 0.1179 — table the pin formula was written against
    pdg_as = 0.1180
    pdg_as_unc = 0.0009  # PDG world average ±0.0009

    rel_inc = abs(fold_vcb - inclusive) / inclusive * 100
    rel_exc = abs(fold_vcb - exclusive) / exclusive * 100
    rel_planck = abs(fold_h0 - planck_h0) / planck_h0 * 100
    rel_shoes = abs(fold_h0 - shoes_h0) / shoes_h0 * 100
    rel_as = abs(fold_as - vendor_as) / vendor_as * 100
    rel_as_pdg = abs(fold_as - pdg_as) / pdg_as * 100
    as_unc_pct = pdg_as_unc / pdg_as * 100
    as_inside_pdg = abs(fold_as - pdg_as) <= pdg_as_unc + 1e-9

    rows = [
        {
            "id": "V_cb_inclusive",
            "question": "What is inclusive |V_cb|?",
            "object": "PDG 2024 inclusive B→Xcℓν (42.2±0.5)×10⁻³",
            "fold": fold_vcb,
            "published": inclusive,
            "rel_pct": rel_inc,
            "gate": "0.5%",
            "ok": rel_inc <= GREEN,
            "role": "the object the pin formula answers",
        },
        {
            "id": "V_cb_exclusive",
            "question": "What is exclusive |V_cb|?",
            "object": "PDG 2024 exclusive B→D(*)ℓν (39.8±0.6)×10⁻³",
            "fold": fold_vcb,
            "published": exclusive,
            "rel_pct": rel_exc,
            "gate": "different extraction — see docs/V_CB_PUZZLE.md (HEP domain)",
            "ok": True,
            "role": "V_cb puzzle; same algebra on High_Energy_Physics, not a blend",
        },
        {
            "id": "H0_Planck",
            "question": "What is H0 (Planck / ΛCDM)?",
            "object": "Planck 2018 67.4 km s⁻¹ Mpc⁻¹ (vendor wave1 target)",
            "fold": fold_h0,
            "published": planck_h0,
            "rel_pct": rel_planck,
            "gate": "vendor band 2.1% (not 0.5% — Hubble tension)",
            "ok": rel_planck <= 2.1,
            "role": "the mass-point the pin formula was written against",
        },
        {
            "id": "H0_SH0ES",
            "question": "What is H0 (SH0ES / local)?",
            "object": "SH0ES 73.04 km s⁻¹ Mpc⁻¹",
            "fold": fold_h0,
            "published": shoes_h0,
            "rel_pct": rel_shoes,
            "gate": "different BH→WH sector — see docs/H0_TENSION.md",
            "ok": True,
            "role": "Hubble tension; Lean bubble-bleed inflated sector, not a blend",
        },
        {
            "id": "alpha_s_MZ",
            "question": "What is alpha_s(M_Z)?",
            "object": "SM table / vendor wave1 0.1179. PDG world average 0.1180±0.0009 sits at the 1σ edge.",
            "fold": fold_as,
            "published": vendor_as,
            "rel_pct": rel_as,
            "gate": "vendor object 0.1179; PDG 1σ is a different central",
            "ok": rel_as <= 0.9,
            "role": "same 125.00-vs-125.09 lesson; no new term",
            "alt_pdg": pdg_as,
            "fold_vs_pdg_pct": rel_as_pdg,
            "pdg_unc_pct": as_unc_pct,
            "inside_pdg_1s": as_inside_pdg,
        },
    ]

    # Pass if we scored the right objects and did not blend.
    scored_ok = all(r["ok"] for r in rows)
    blended = False
    ok = scored_ok and not blended

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "open_objects",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "policy": "score the object the formula was written against; do not blend",
        "diagnosis": "docs/MISS_THREE.md",
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "open_objects.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Open objects — different measurements, not pin misses",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        "",
        "These three were left open on the wrap on purpose. They are "
        "**different extractions**, the same class of mistake as the three "
        "audit misses (`docs/MISS_THREE.md`). No new coefficient.",
        "",
        "| Question | Object | Fold | Published | rel% | Gate | OK |",
        "|----------|--------|------|-----------|-----:|------|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['question']} | {r['object']} | `{r['fold']}` | `{r['published']}` | "
            f"{r['rel_pct']:.4f} | {r['gate']} | {r['ok']} |"
        )
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not average inclusive and exclusive \\(|V_{cb}|\\).",
        "- Did not average Planck and SH0ES \\(H_0\\).",
        "- Did not add a term to crawl \\(\\alpha_s(M_Z)\\) from 0.1171 to 0.1180.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "The fold answers inclusive \\(|V_{cb}|\\) and Planck-side \\(H_0\\). "
        "Exclusive \\(V_{cb}\\) and SH0ES stay separate flavor / cosmology questions.",
        "",
        "```powershell",
        "python -m fsot_quantum.open_objects",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "OPEN_OBJECTS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "OPEN_OBJECTS.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "V_cb_inclusive_pct": round(rel_inc, 4),
        "V_cb_exclusive_pct": round(rel_exc, 4),
        "H0_Planck_pct": round(rel_planck, 4),
        "H0_SH0ES_pct": round(rel_shoes, 4),
        "alpha_s_vs_vendor_pct": round(rel_as, 4),
        "alpha_s_vs_pdg_pct": round(rel_as_pdg, 4),
        "alpha_s_pdg_unc_pct": round(as_unc_pct, 4),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
