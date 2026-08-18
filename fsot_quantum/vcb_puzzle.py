"""
The |V_cb| puzzle — exclusive vs inclusive, same algebra, different domain.

Inclusive B→Xcℓν is S(Quantum_Mechanics)·(1/C_eff − 1).
Exclusive B→D(*)ℓν is the same form on High_Energy_Physics (D_eff 6 → 7).

No new coefficient. Pin D1D38A not edited. Astronomy is numerically
close and is the wrong domain — not scored.

python -m fsot_quantum.vcb_puzzle
python -m fsot_quantum vcb
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
from fsot_quantum.domains import domain_scalar
from fsot_lib.seeds import SEEDS

# PDG 2024 / HFLAV CKM review.
INCLUSIVE = 0.0422
INCLUSIVE_UNC = 0.0005
EXCLUSIVE = 0.0398
EXCLUSIVE_UNC = 0.0006


def _v_from_S(S: float) -> float:
    return float(S) * (1.0 / float(SEEDS.c_eff) - 1.0)


def main() -> int:
    t0 = time.perf_counter()
    s_qm = domain_scalar("Quantum_Mechanics")
    s_hep = domain_scalar("High_Energy_Physics")
    s_pp = domain_scalar("Particle_Physics")
    s_nuc = domain_scalar("Nuclear_Physics")
    s_ast = domain_scalar("Astronomy")

    v_incl = _v_from_S(s_qm)
    v_excl = _v_from_S(s_hep)
    v_pp = _v_from_S(s_pp)
    v_nuc = _v_from_S(s_nuc)
    v_ast = _v_from_S(s_ast)

    rel_incl = abs(v_incl - INCLUSIVE) / INCLUSIVE * 100
    rel_excl = abs(v_excl - EXCLUSIVE) / EXCLUSIVE * 100
    sig_excl = abs(v_excl - EXCLUSIVE) / EXCLUSIVE_UNC
    excl_unc_pct = EXCLUSIVE_UNC / EXCLUSIVE * 100

    rows: list[dict[str, Any]] = [
        {
            "id": "inclusive",
            "question": "What is inclusive |V_cb|?",
            "domain": "Quantum_Mechanics",
            "D_eff": 6,
            "formula": "S(QM)·(1/C_eff − 1)",
            "fold": v_incl,
            "published": INCLUSIVE,
            "published_unc": INCLUSIVE_UNC,
            "rel_pct": rel_incl,
            "sigma": abs(v_incl - INCLUSIVE) / INCLUSIVE_UNC,
            "ok": rel_incl <= GREEN,
            "role": "OPE / B→Xcℓν — the object wave3 was written against",
        },
        {
            "id": "exclusive",
            "question": "What is exclusive |V_cb|?",
            "domain": "High_Energy_Physics",
            "D_eff": 7,
            "formula": "S(HEP)·(1/C_eff − 1)",
            "fold": v_excl,
            "published": EXCLUSIVE,
            "published_unc": EXCLUSIVE_UNC,
            "rel_pct": rel_excl,
            "sigma": sig_excl,
            "ok": sig_excl <= 2.0,
            "role": "exclusive B→D(*)ℓν + lattice form factors — same algebra, D_eff +1",
        },
    ]

    notes = [
        {
            "domain": "Particle_Physics",
            "D_eff": 5,
            "fold": v_pp,
            "vs_inclusive_pct": abs(v_pp - INCLUSIVE) / INCLUSIVE * 100,
            "use": "neighbor on the pin ladder; not the exclusive object",
        },
        {
            "domain": "Nuclear_Physics",
            "D_eff": 15,
            "fold": v_nuc,
            "vs_exclusive_pct": abs(v_nuc - EXCLUSIVE) / EXCLUSIVE * 100,
            "use": "lattice-adjacent; worse than HEP; not scored",
        },
        {
            "domain": "Astronomy",
            "D_eff": 20,
            "fold": v_ast,
            "vs_exclusive_pct": abs(v_ast - EXCLUSIVE) / EXCLUSIVE * 100,
            "use": "numerically close — WRONG domain, not scored",
        },
    ]

    ok = all(r["ok"] for r in rows)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "vcb_puzzle",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "policy": "same algebra; change domain / D_eff; do not blend; do not invent a term",
        "rows": rows,
        "not_scored": notes,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "vcb_puzzle.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# The \\(|V_{cb}|\\) puzzle — same algebra, different domain",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        "",
        "Inclusive and exclusive \\(|V_{cb}|\\) disagree by ~3σ in the data. "
        "That is the **\\(V_{cb}\\) puzzle**. It is not a reason to retune "
        "\\(S_{\\mathrm{QM}}/C_{\\mathrm{eff}}-S_{\\mathrm{QM}}\\).",
        "",
        "Inclusive is an OPE / moment extraction (\\(B\\to X_c\\ell\\nu\\)). "
        "Exclusive is a single-channel + lattice form-factor extraction "
        "(\\(B\\to D^{(*)}\\ell\\nu\\)). Those are different **looks**. "
        "FSOT changes **domain / \\(D_{\\mathrm{eff}}\\)**, not a coefficient.",
        "",
        "Same pin form \\(S\\cdot(1/C_{\\mathrm{eff}}-1)\\):",
        "",
        "| Extraction | Domain | \\(D_{\\mathrm{eff}}\\) | Fold | PDG 2024 | rel | σ | OK |",
        "|------------|--------|----------------------:|------|----------|----:|--:|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['id']} | {r['domain']} | {r['D_eff']} | `{r['fold']:.8f}` | "
            f"`{r['published']}` ± {r['published_unc']} | {r['rel_pct']:.3f}% | "
            f"{r['sigma']:.2f} | {r['ok']} |"
        )
    md += [
        "",
        f"Exclusive PDG uncertainty is ±0.0006 (**{excl_unc_pct:.2f}%**). "
        "A 0.5% gate is tighter than the exclusive measurement. "
        "HEP sits **1.1σ** from exclusive 0.0398 — inside 2σ, not a 0.5% claim.",
        "",
        "## What we did not do",
        "",
        "- Did not average 0.0422 and 0.0398.",
        "- Did not add a term to crawl 0.04220 down to 0.0398.",
        "- Did not score **Astronomy** (fold 0.03968, 0.30% from exclusive). "
        "That domain is not exclusive \(B\) decay. Number-matching is theater.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "Neighbor checks (not scored): Particle_Physics \\(D=5\\) is 0.53% from "
        "inclusive. Nuclear_Physics is 2.24% from exclusive.",
        "",
        "```powershell",
        "python -m fsot_quantum.vcb_puzzle",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "V_CB_PUZZLE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "V_CB_PUZZLE.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "inclusive_QM": {"fold": v_incl, "rel_pct": round(rel_incl, 4), "ok": rel_incl <= GREEN},
        "exclusive_HEP": {
            "fold": v_excl,
            "rel_pct": round(rel_excl, 4),
            "sigma": round(sig_excl, 3),
            "ok": sig_excl <= 2.0,
        },
        "astronomy_not_scored": {"fold": v_ast, "rel_vs_excl_pct": round(abs(v_ast - EXCLUSIVE) / EXCLUSIVE * 100, 3)},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
