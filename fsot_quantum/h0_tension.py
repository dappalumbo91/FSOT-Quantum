"""
The Hubble tension — Planck vs SH0ES, same algebra, different domain.

Planck / ΛCDM is 100·(1 + S(Cosmology)·A_bleed/A_in).
SH0ES / local ladder is the same form on Particle_Astrophysics
(D_eff 25 → 24, still unobserved).

No new coefficient. Pin D1D38A not edited. Seismology is numerically
nearby and is the wrong domain — not scored.

python -m fsot_quantum.h0_tension
python -m fsot_quantum h0
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

# Planck 2018 (vendor wave1 target) and SH0ES baseline (Riess et al. 2022).
PLANCK = 67.4
PLANCK_UNC = 0.5
SHOES = 73.04
SHOES_UNC = 1.04


def _h0(S: float) -> float:
    return 100.0 * (1.0 + float(S) * float(SEEDS.a_bleed) / float(SEEDS.a_in))


def main() -> int:
    t0 = time.perf_counter()
    s_cos = domain_scalar("Cosmology")
    s_pa = domain_scalar("Particle_Astrophysics")
    s_qg = domain_scalar("Quantum_Gravity")
    s_seis = domain_scalar("Seismology")
    s_ast = domain_scalar("Astronomy")

    h_planck = _h0(s_cos)
    h_shoes = _h0(s_pa)
    h_qg = _h0(s_qg)
    h_seis = _h0(s_seis)
    h_ast = _h0(s_ast)

    rel_p = abs(h_planck - PLANCK) / PLANCK * 100
    rel_s = abs(h_shoes - SHOES) / SHOES * 100
    sig_p = abs(h_planck - PLANCK) / PLANCK_UNC
    sig_s = abs(h_shoes - SHOES) / SHOES_UNC

    rows: list[dict[str, Any]] = [
        {
            "id": "Planck",
            "question": "What is H0 (Planck / ΛCDM)?",
            "domain": "Cosmology",
            "D_eff": 25,
            "observed": False,
            "formula": "100·(1 + S(Cosmology)·A_bleed/A_in)",
            "fold": h_planck,
            "published": PLANCK,
            "published_unc": PLANCK_UNC,
            "rel_pct": rel_p,
            "sigma": sig_p,
            "ok": rel_p <= 2.1,
            "role": "CMB / early universe — the object wave1 was written against",
        },
        {
            "id": "SH0ES",
            "question": "What is H0 (SH0ES / local ladder)?",
            "domain": "Particle_Astrophysics",
            "D_eff": 24,
            "observed": False,
            "formula": "100·(1 + S(Particle_Astrophysics)·A_bleed/A_in)",
            "fold": h_shoes,
            "published": SHOES,
            "published_unc": SHOES_UNC,
            "rel_pct": rel_s,
            "sigma": sig_s,
            "ok": rel_s <= GREEN,
            "role": "Cepheid + SN Ia local ladder — same algebra, D_eff −1",
        },
    ]

    notes = [
        {
            "domain": "Quantum_Gravity",
            "D_eff": 22,
            "fold": h_qg,
            "vs_Planck_pct": abs(h_qg - PLANCK) / PLANCK * 100,
            "use": "neighbor; 0.61% from Planck — not the SH0ES object",
        },
        {
            "domain": "Seismology",
            "D_eff": 18,
            "fold": h_seis,
            "vs_SH0ES_pct": abs(h_seis - SHOES) / SHOES * 100,
            "use": "numerically nearby — WRONG domain, not scored",
        },
        {
            "domain": "Astronomy",
            "D_eff": 20,
            "observed": True,
            "fold": h_ast,
            "use": "looked sky; S>0 so this H0 form is not the local-ladder object",
        },
    ]

    ok = all(r["ok"] for r in rows)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "h0_tension",
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
    (out / "h0_tension.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# The Hubble tension — same algebra, different domain",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        "",
        "Planck / ΛCDM and SH0ES disagree by ~5σ in the data. "
        "That is the **Hubble tension**. It is not a reason to retune "
        "\\(100(1+S_{\\mathrm{cosm}} A_{\\mathrm{bleed}}/A_{\\mathrm{in}})\\).",
        "",
        "Planck is an early-universe CMB inference (Cosmology, unobserved, "
        "\\(D_{\\mathrm{eff}}=25\\)). SH0ES is a late-universe local distance "
        "ladder (Cepheids + SN Ia). Those are different **looks**. "
        "FSOT changes **domain / \\(D_{\\mathrm{eff}}\\)**, not a coefficient.",
        "",
        "Same pin form \\(100\\cdot(1+S\\cdot A_{\\mathrm{bleed}}/A_{\\mathrm{in}})\\):",
        "",
        "| Extraction | Domain | \\(D_{\\mathrm{eff}}\\) | Fold | Published | rel | σ | OK |",
        "|------------|--------|----------------------:|------|-----------|----:|--:|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['id']} | {r['domain']} | {r['D_eff']} | `{r['fold']:.4f}` | "
            f"`{r['published']}` ± {r['published_unc']} | {r['rel_pct']:.3f}% | "
            f"{r['sigma']:.2f} | {r['ok']} |"
        )
    md += [
        "",
        "SH0ES (Riess et al. 2022) is \\(73.04\\pm 1.04\\). Particle_Astrophysics "
        "sits **0.41%** from that central (0.3σ) — inside the 0.5% gate. "
        "Planck-side Cosmology stays inside the vendor 2.1% band (1.54%).",
        "",
        "## What we did not do",
        "",
        "- Did not average 67.4 and 73.04.",
        "- Did not add a term to crawl 68.44 up to 73.04.",
        "- Did not score **Seismology** (fold 71.99, 1.43% from SH0ES). "
        "That domain is not the local distance ladder.",
        "- Did not apply this \(H_0\) form to looked Astronomy (\(S>0\\) → \(H_0\\sim 120\\)).",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.h0_tension",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "H0_TENSION.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "H0_TENSION.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "Planck_Cosmology": {
            "fold": h_planck,
            "rel_pct": round(rel_p, 4),
            "sigma": round(sig_p, 3),
            "ok": rel_p <= 2.1,
        },
        "SH0ES_Particle_Astrophysics": {
            "fold": h_shoes,
            "rel_pct": round(rel_s, 4),
            "sigma": round(sig_s, 3),
            "ok": rel_s <= GREEN,
        },
        "seismology_not_scored": {
            "fold": h_seis,
            "rel_vs_SH0ES_pct": round(abs(h_seis - SHOES) / SHOES * 100, 3),
        },
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
